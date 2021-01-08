#!/usr/bin/python3.7

import os
import sys
import argparse
import socket

p = argparse.ArgumentParser()
p = argparse.ArgumentParser(description='SSH auto create and deploy keys on host. Use host file to setup hostname, ip, username and password.')

p.version = '1.0'
p.add_argument('-g', '--generate', action='store_true', help='Generate new keys to host.')
p.add_argument('-d', '--deploy', action='store_true', help='Deploy keys to host.')
p.add_argument('-c', '--compress', action='store_true', help='Create archive keys to host.')
p.add_argument('-V', action='version')
args = p.parse_args()

def host_file():
  if not os.path.isfile('./host'):
    print ('Hosts file not found... create host firs.')
    sys.exit()

def keys_dir():
  if not os.path.exists('./keys'):
    os.system('mkdir -p ./keys')

def chek_vars():
  with open('./host', 'r') as f:
    for lines in f:
      if not lines.startswith('#') and not lines.startswith('\n'):
        vcount = len(lines.split())
        if vcount != 4:
          print ('Error hosts file syntax. Check hosts file.')
          sys.exit()
  f.close

def get_ip():
  with open('./host', 'r') as f:
    for lines in f:
      if not lines.startswith('#') and not lines.startswith('\n'):
        hostname, hostip, username, password = lines.split()
        try:
          ip = socket.gethostbyname(hostname)
        except:
          ip = '0.0.0.0'
        return ip
    f.close

def chek_args():
  if not args.generate and not args.deploy and not args.compress:
    print('You must set -g or -d keys... Please read help. --help')

def keys_gen():
  with open('./host', 'r') as f:
    for lines in f:
      if not lines.startswith('#') and not lines.startswith('\n'):
        hostname, hostip, username, password = lines.split()
        if os.path.isfile('keys/' + hostname + '/' + hostname + '.key'):
          print ('Keys for ' + hostname + ' alredy generated...')
        else:
          os.system('mkdir -p keys/' + hostname)
          os.system('ssh-keygen -N "" -b 4096 -t rsa -f keys/' + hostname + '/' + hostname + '.key >> /dev/null 2>&1')
          if os.path.isfile('keys/' + hostname + '/' + hostname + '.key'):
            print ('Keys for ' + hostname + ' generated successfully...')
          else:
            print ('Keys ' + hostname + ' generated failed...')
    f.close

def keys_dep():
  with open('./host', 'r') as f:
    for lines in f:
      if not lines.startswith('#') and not lines.startswith('\n'):
        hostname, hostip, username, password = lines.split()
        if not os.path.isfile('keys/' + hostname + '/' + hostname + '.key'):
          print ('No generate keys found for ' + hostname + ', generate key witch -g first' )
        else:
          os.system('sshpass -p ' + password + ' ssh-copy-id -o StrictHostKeyChecking=no -i keys/' + hostname + '/' + hostname + '.key.pub ' + username + '@' + hostip)
  f.close

def keys_compress():
  with open('./host', 'r') as f:
    for lines in f:
      if not lines.startswith('#') and not lines.startswith('\n'):
        hostname, hostip, username, password = lines.split()
        if os.path.isfile('archive/' + hostname + '.tar.bz2'):
          print ('Archive of ' + hostname + ' alredy exist...')
        else:
          if not os.path.exists('archive/'):
            os.system('mkdir -p archive/')
          if os.path.isfile('keys/' + hostname + '/' + hostname + '.key'):
            os.system('cd keys/' + hostname + ' && tar -cjpvf ' + hostname + '.tar.bz2 * >> /dev/null 2>&1')
            os.system('mv keys/' + hostname + '/' + hostname + '.tar.bz2 archive/')
            print ('Archive of keys for ' + hostname + ' create.')
          else:
            print ('No generate keys found... for host ' + hostname)

host_file()
keys_dir()
chek_vars()
chek_args()

if args.generate:
  keys_gen()

if args.deploy:
  keys_dep()

if args.compress:
  keys_compress()
