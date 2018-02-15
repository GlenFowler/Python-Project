from ping3 import ping, verbose_ping
import subprocess
from colorama import init, deinit, Fore, Style
import platform

init()
'''
out = ping('google.com', timeout=2)

print('.........................')
print(out)
'''


def ping(ip):
    # ip = '192.168.2.101'
    if platform.system() is 'Windows':
        count = '-n'
    else:
        count = '-c'

    ping = subprocess.call(['ping', count, '2', ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE)  # subprocess.PIPE

    if ping == 0:
        print(Fore.GREEN + 'Ping ok to', ip.rstrip('\n'))
        print(Style.RESET_ALL)
    elif ping == 2:
        print(Fore.RED + 'Invalid IP: ', ip.rstrip('\n'))
        print(Style.RESET_ALL)
    else:
        print(Fore.RED + 'ping failed to', ip.rstrip('\n'))
        print(Style.RESET_ALL)

    return ping


ping('192.168.2.101')

print(platform.system())
deinit()
