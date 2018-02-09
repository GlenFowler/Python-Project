import subprocess
import re
import threading
import time
import Queue

from colorama import init, deinit, Fore, Style

init()

def ip_valid():
    ips = open('range.txt', 'r')
    ips.seek(0)
    range_list = ips.readlines()
    ips.close()

    ip_list = []
    
    def threads ():
        ip_list = []
        ip_queue = Queue.Queue()
        threads = []
        
        print Fore.YELLOW + Style.BRIGHT + 'Start validation'
        print Style.RESET_ALL
        
        for ip in range_list:
            th = threading.Thread(target = ipvalid, args = (ip,ip_queue))
            th.start()
            threads.append(th)
            
        for th in threads:
            th.join()
        
        #Waiting threads and queue    
        time.sleep (3)
        
        #Extract Ip valid list
        #print ip_queue.qsize()
        for i in range(ip_queue.qsize()):
            ip_list.append(ip_queue.get())
            
        #print ip_list
        return ip_list
    
    ip_list = threads()
    #print ip_list
    
    
    ip_list = list(filter(lambda x: x!= None, ip_list))
    #print ip_list
    print Fore.GREEN + Style.BRIGHT + 'There are', '{}'.format(len(ip_list)), 'valid devices'
    print Style.RESET_ALL
    return ip_list


def ipvalid(ip, ip_queue):
    #time.sleep(2)
    
    ip_list = []
    ip = ip.rstrip('\n')
    #print ip
    regexIP = re.compile(r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9]?[0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9]?[0-9]?)$')
    validIP = regexIP.match(ip)
    #print validIP
    icmp = ping(ip)
    if validIP != None and icmp == 0:
        #print Fore.GREEN + 'Valid =', ip
        ip_queue.put(ip)


def ping(ip):
    #ip = '192.168.2.101'
    ping = subprocess.call(['ping', '-c', '2', ip], stdout = subprocess.PIPE, stderr = subprocess.PIPE) #subprocess.PIPE
    
    if ping == 0:
        print Fore.GREEN + 'Ping ok to', ip.rstrip('\n')
        print Style.RESET_ALL
    elif ping == 2:
        print Fore.RED + 'Invalid IP: ', ip.rstrip('\n')
        print Style.RESET_ALL
    else:
        print Fore.RED + 'ping failed to', ip.rstrip('\n')
        print Style.RESET_ALL

    return ping