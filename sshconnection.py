import paramiko
import time
import threading

from colorama import init, deinit, Fore, Style

def connect_ssh(ip):
    try :
        #Define User
        user_name = 'teopy' #should be 'admin'
    
        #Define Password
        password = 'python' #From 'password.txt'
        
        #passwords = open('password.txt', 'r')
        #pass_list = passwords.readlines()
        #passwords.close()
        #print pass_list
    
        
    
        #Start SSH connection
        session = paramiko.SSHClient()
        
        #For testing purposes, this allows auto-accepting unknown host keys
        #Do not use in production! The default would be RejectPolicy
        session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        session.connect (ip, username = user_name, password = password)
    
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
    except paramiko.AuthenticationException:
        print Fore.RED + "Invalid Password, check configuration file password.txt!"
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