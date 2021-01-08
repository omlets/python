#!/usr/bin/python3.7
import sys

if len(sys.argv) <= 1:
        print ('You must define username...')
        sys.exit()

sudo_file = '/etc/sudoers'
username = sys.argv[1]
sudo_string = sys.argv[1] + ' ALL=(ALL) NOPASSWD:ALL'

def check_sudo(fname, sl):
    with open(fname) as dataf:
        return any(sl in line for line in dataf)

def check_passwd(fname, sl):
    with open(fname) as dataf:
        return any(sl in line for line in dataf)

if not check_passwd('/etc/passwd', username):
	print ('User not found in system! Exit...')
else:
	if check_sudo(sudo_file, username):
	        print ('User alredy in sudoers file.')
	else:
	        with open(sudo_file, 'a') as myfile:
	                myfile.write(sudo_string + '\n')
	        print ('User added successfully.')
