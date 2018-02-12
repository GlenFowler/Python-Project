import paramiko
import time
import threading
import socket

from colorama import init, deinit, Fore, Style

def connect_ssh(ip):
    #Connection Boolean
    conn = False
    
    #Define User
    user_name = 'teopy' #should be 'admin'
    
    #Define Password
    passwords = open('password.txt', 'r')
    password_list = passwords.readlines()
    passwords.close()
    #print password_list
    #password = 'python' #From 'password.txt'
          
    #Start SSH connection
    session = paramiko.SSHClient()
        
    #For testing purposes, this allows auto-accepting unknown host keys
    #Do not use in production! The default would be RejectPolicy
    session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    #Connection to the devices each one with his own password
    for password in password_list:
        
        #print password.rstrip('\n')
        try:    
            session.connect (ip, username = user_name, password = password.rstrip('\n'))
            #print session
            print Fore.GREEN + "Valid Password", password
            print Style.RESET_ALL
            conn = True
            break
        
        except paramiko.AuthenticationException or socket.error:
            print Fore.RED + "Invalid Password or Socket Error", password
            print Style.RESET_ALL
            continue
          
    #print conn
    
    if conn == True:
        #Start Shell
        shell = session.invoke_shell()
    
        #Send commands
        shell.send('terminal length 0\n') #no pagination
        time.sleep(1)
        shell.send('show run\n')
        time.sleep(1)
        
        #Command output
        output = shell.recv(65535)
        #print output
        print ip
    else:
        print Fore.RED + "Invalid Passwords, check configuration file password.txt!"
        print Style.RESET_ALL
    
def start_ssh(ip_list):
    
    def threads (): 
        threads = []
        
        print Fore.YELLOW + Style.BRIGHT + 'Start data extraction'
        print Style.RESET_ALL
        
        for ip in ip_list:
            th = threading.Thread(target = connect_ssh, args = (ip,))
            th.start()
            threads.append(th)
            
        for th in threads:
            th.join()
        
        #Waiting threads and queue    
        #time.sleep (3)
        
    threads()