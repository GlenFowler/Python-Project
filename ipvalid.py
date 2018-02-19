import subprocess
import ipaddress
import re
import threading
import time
import platform
import queue  # import Queue

from colorama import init, deinit, Fore, Style


"""
Module for validation of the ip Addresses

This module do the validation of all of the ip addresses inside the range in the 
file **range.txt**, the different functions validate if the ip address has a 
correct format and if possible to ping that ip address. Pc Addresses are saved in
**pcs.txt**.

    Example:
    
            $ python3 ipvalid.py 
"""


init()


def ip_valid():

    """
    Main function for validation of IP addresses.

        Returns:
            list: ip_list, List of valid IP addresses.

    """

    ips = open('range.txt', 'r')
    ips.seek(0)
    ranges = ips.readlines()
    ips.close()
    range_list = []

    for ip in ranges:
        if re.match(r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9]?[0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9]?[0-9]?)/\d{1,2}$', ip):
            print('Network range: ', ip)
            network = ipaddress.ip_network(ip.rstrip('\n'))
            for host in network.hosts():
                range_list.append(str(host))
                # print(host)

    # print(range_list)
    # print(ranges)

    pcs = open('pcs.txt', 'r')
    pcs.seek(0)
    pc_list = pcs.readlines()
    pcs.close()

    for pc in pc_list:
        if pc.rstrip('\n') in range_list:
            range_list.remove(pc.rstrip('\n'))

    def threads():
        ip_list = []
        ip_queue = queue.Queue()
        threads = []

        print(Fore.YELLOW + Style.BRIGHT + 'Start validation')
        print(Style.RESET_ALL)

        for ip in range_list:

            th = threading.Thread(target=validformat, args=(ip, ip_queue))
            th.start()

            threads.append(th)

        for th in threads:
            th.join()

        # Waiting threads and queue
        time.sleep(3)
        
        # Extract Ip valid list
        # print ip_queue.qsize()
        for i in range(ip_queue.qsize()):
            ip_list.append(ip_queue.get())
            
        # print ip_list
        return ip_list
    
    ip_list = threads()
    # print ip_list

    ip_list = list(filter(lambda x: x is not None, ip_list))
    # print ip_list
    print(Fore.GREEN + Style.BRIGHT + 'There are', '{}'.format(len(ip_list)), 'valid devices')
    print(Style.RESET_ALL)
    return ip_list


def validformat(ip, ip_queue):

    """
    Function to validate the correct format of the IP addresses

        Args:
            ip (str): IP address.
            ip_queue (queue): Queue for save IP addresses.
    """
    
    ip = ip.rstrip('\n')
    # print ip
    regexip = re.compile(r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9]?[0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9]?[0-9]?)$')
    validip = regexip.match(ip)
    # print validip
    icmp = ping(ip)
    if validip is not None and icmp == 0:
        # print Fore.GREEN + 'Valid =', ip
        ip_queue.put(ip)


def ping(ip):

    """
    Function to pinging all the devices to know if there are reachable or not.

        Args:
            ip (str): IP address.

        Returns:
            ping: Value of the ping to the host. 0 for success.
    """
    if platform.system() is 'Windows':
        count = '-n'
    else:
        count = '-c'

    ping = subprocess.call(['ping', count, '2', ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE)  # subprocess.PIPE

    if ping == 0:
        print(Fore.GREEN + 'Ping ok to', ip.rstrip('\n'))
        print(Style.RESET_ALL)
    # elif ping == 2:
    #    print(Fore.RED + 'Invalid IP: ', ip.rstrip('\n'))
    #    print(Style.RESET_ALL)
    # else:
    #    print(Fore.RED + 'ping failed to', ip.rstrip('\n'))
    #    print(Style.RESET_ALL)

    return ping


deinit()

if __name__ == '__main__':
    ip_list = ip_valid()
    print('Valid IP addresses: ', ip_list)
