#!/usr/bin/python3.7

import os
import sys
import argparse

def sdir():
  if not os.path.exists('source/'):
    os.system('mkdir source/')

def hdir(hostname):
  if os.path.exists(hostname + '/'):
    return True
  else:
    return False

def cnf(hostname):
  fin = open("openssl.tmpl", "rt")
  fout = open("openssl.cnf", "wt")
  for line in fin:
    fout.write(line.replace('host', hostname))
  fin.close()
  fout.close()

def wildhost(argshost):
  if '*' in argshost:
    hostname = argshost.replace('*.', '')
  else:
    hostname = argshost
  return hostname

def ca(ca_password):
  os.system('openssl genrsa -aes256 -passout pass:' + ca_password + ' -out source/ca-key.pem 4096 > /dev/null 2>&1')
  os.system('openssl req -batch -config openssl.cnf -passin pass:' + ca_password + ' -new -x509 -days 365 -key source/ca-key.pem -sha256 -out source/ca.pem > /dev/null 2>&1')

def server(hostname,password):
  os.system('echo "subjectAltName = DNS:' + hostname + ',IP:127.0.0.1" >> openssl.cnf')
  os.system('echo "extendedKeyUsage = serverAuth" >> openssl.cnf')
  os.system('openssl genrsa -out source/server-key.pem 4096 > /dev/null 2>&1')
  os.system('openssl req -batch -config openssl.cnf -sha256 -new -key source/server-key.pem -out source/server.csr > /dev/null 2>&1')
  os.system('openssl x509 -req  -passin pass:' + password + ' -extfile openssl.cnf -days 365 -sha256 -in source/server.csr -CA source/ca.pem -CAkey source/ca-key.pem -CAcreateserial -out source/server-cert.pem > /dev/null 2>&1')

def client(password):
  os.system('openssl genrsa -out source/client-key.pem 4096 > /dev/null 2>&1')
  os.system('openssl req -batch -config openssl.cnf -new -key source/client-key.pem -out source/client.csr > /dev/null 2>&1')
  os.system('echo extendedKeyUsage = clientAuth > openssl.cnf')
  os.system('openssl x509 -req -passin pass:' + password + '  -extfile openssl.cnf -days 365 -sha256 -in source/client.csr -CA source/ca.pem -CAkey source/ca-key.pem -CAcreateserial -out source/client-cert.pem > /dev/null 2>&1')

def make_chain(hostname):
  if not os.path.exists(hostname):
    os.system('mkdir ' + hostname)
    os.system('cp source/ca.pem ' + hostname)
    os.system('cp source/server-cert.pem ' + hostname + '/' + hostname + '-server-cert.pem')
    os.system('cp source/server-key.pem ' + hostname + '/' + hostname + '-server-key.pem')
    os.system('cp source/client-cert.pem ' + hostname + '/' + hostname + '-client-cert.pem')
    os.system('cp source/client-key.pem ' + hostname + '/' + hostname + '-client-key.pem')
    os.system('rm -rf ./source')

def clear():
  os.system('rm openssl.cnf')

def ca_check():
  if os.path.isfile('source/ca.pem'):
    return True
  else:
    return False

p = argparse.ArgumentParser()
p.add_argument('-p', '--password', action='store', required=True, help='Password for CA.')
p.add_argument('-H', '--hostname', action='store', required=True, help='Hostname')
args = p.parse_args()

if args.password and args.hostname:
  if hdir(wildhost(args.hostname)):
    print ('Ключевая пара уже создана для ' + wildhost(args.hostname))
  else:
    if not ca_check():
      sdir()
      cnf(args.hostname)
      ca(args.password)
      server(args.hostname, args.password)
      clear()
      cnf(args.hostname)
      client(args.password)
      clear()
      make_chain(wildhost(args.hostname))
    else:
      print ('Корневой сертификат или цепочка уже создан(ы).')
