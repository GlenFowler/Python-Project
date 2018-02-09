#!/usr/bin/env python

#import modules
import threading
import re
import time
#import subprocess

#import my modules
import ipvalid
import sshconnection

#My variables
ip_list = []
ip = '192.168.2.101'

#Check and validation IP range
ip_list = ipvalid.ip_valid()
#print len(ip_list)
#print ip_list

#Connect to devices
sshconnection.start_ssh(ip_list)