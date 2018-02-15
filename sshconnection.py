import paramiko
import time
import threading
import socket
import re

from colorama import init, deinit, Fore, Style

"""
Module for SSH connection and data extraction

This module connects to devices with ssh and extract data to send it to a SQL database.
The file **password.txt** has all the possible passwords to connect with all the devices.

    Example:

            $ python sshconnection.py 
"""


init()


def connect_ssh(ip):

    """
    Function that makes the ssh connection to the devices

        Args:
            ip (str): IP address.
    """

    # Connection Boolean
    conn = False
    
    # Define User
    user_name = 'teopy'  # should be 'admin'
    
    # Define Password
    passwords = open('password.txt', 'r')
    password_list = passwords.readlines()
    passwords.close()
    # print password_list
    # password = 'python' #From 'password.txt'
          
    # Start SSH connection
    session = paramiko.SSHClient()
        
    # For testing purposes, this allows auto-accepting unknown host keys
    # Do not use in production! The default would be RejectPolicy
    session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    # Connection to the devices each one with his own password
    for password in password_list:
        
        # print password.rstrip('\n')
        try:    
            session.connect(ip, username=user_name, password=password.rstrip('\n'))
            # print session
            # print(Fore.GREEN + "Valid Password", password)
            # print(Style.RESET_ALL)
            conn = True
            break
        
        except paramiko.AuthenticationException or socket.error or paramiko.ssh_exception.SSHException:
            # print(Fore.RED + "Invalid Password or Socket Error", password)
            # print(Style.RESET_ALL)
            continue
          
    # print conn
    
    if conn:
        # time waiting
        period1 = 1
        period2 = 2

        # Start Shell
        shell = session.invoke_shell()
    
        # Send commands
        shell.send('terminal length 0\n')  # no pagination
        time.sleep(period1)
        # Sending commands for device information
        shell.send('show run\n')
        time.sleep(period1)
        # Command output
        output = shell.recv(65535)
        hostname = re.search(r'hostname (?P<hostname>\w+)', str(output)).group('hostname')
        print(hostname)
        print(password)
        print(output)
        time.sleep(period2)
        # Sending commands for topology
        shell.send('show ip route\n')
        time.sleep(period1)
        # Command output
        output = shell.recv(65535)
        print(str(output))
        time.sleep(period2)
        # Sending commands for interfaces
        shell.send('show ip int brief\n')
        time.sleep(period1)
        # Command output
        output = shell.recv(65535)
        print(output)
        time.sleep(period2)
        print(ip)
    else:
        print(Fore.RED + "Invalid Passwords, check configuration file password.txt!")
        print(Style.RESET_ALL)


def start_ssh(ip_list):
    """
    Main function to create threads to all IP address in the list

        Args:
            ip_list (list): IP addresses to connect.
    """
    
    def threads():
        threads = []
        
        print(Fore.YELLOW + Style.BRIGHT + 'Start data extraction')
        print(Style.RESET_ALL)
        
        for ip in ip_list:
            th = threading.Thread(target=connect_ssh, args=(ip,))
            th.start()
            threads.append(th)
            
        for th in threads:
            th.join()
        
        # Waiting threads and queue
        # time.sleep (3)
        
    threads()


deinit()

if __name__ == '__main__':

    ip_list = ['192.168.2.102', '192.168.2.103', '192.168.2.101', '192.168.2.105', '192.168.2.104']
    start_ssh(ip_list)
