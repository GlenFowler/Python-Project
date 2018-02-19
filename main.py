#!/usr/bin/env python3

# import modules
# import time

# import my modules
import ipvalid
import sshconnection
import takedataSQL

# My variables
# ip_list = []
# ip = '192.168.2.101' # Testing variable
yes = ['YES', 'yes', 'Y', 'y']
no = ['NO', 'no', 'N', 'n']
no_yes = no + yes
answer = ''

while answer not in no_yes:
    answer = input('Do you want to search and save devices data? (YES/NO):')

if answer in yes:
    # Check and validation IP range
    ip_list = ipvalid.ip_valid()
    # print len(ip_list)
    # print(ip_list)

    # Connect to devices
    sshconnection.start_ssh(ip_list)
    answer = ''
answer = ''
while answer not in no_yes:
    answer = input('Do you want to look data already in DB? (YES/NO):')
if answer in yes:
    takedataSQL.extract('Devices')
    print('{:_^500}'.format(''))
    takedataSQL.extract('Topology')
    print('{:_^500}'.format(''))
    takedataSQL.extract('Interfaces')
    print('{:_^500}'.format(''))

print('\nGood bye!!')
