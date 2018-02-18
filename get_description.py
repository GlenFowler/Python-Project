"""He wants to see the interface description and interface status for each interface on each device."""
import re
import savedataSQL
import time

# Function device_info. Returns a dictionary with the device's information asked in point 3:
#  - Interface       		key of the dictionary, contain as value another dicitonary
#  - Description 			        'description'
#  - Physical status of the link    'status'
#  - Status of the link protocol    'prococol'
#  - IPv4 and mask of the interface 'ipmask'
#  - Bandwidth of the interface     'BW'
#  - MTU of the interface           'MTU'
# Receives the output of the commands 'show interface', and makes use of the
# functions show_interface to process those outputs.

"""(?P<INT>[A-Z][a-zA-Z]*(?!\d+(\/\d+){,2}).\d+(\/\d+){,2}) is (?P<STATUS>up|administratively down|down), line protocol is (?P<PROTO>up|down)"""


def show_interface(hostname, input_lines):
    """interfaces = {
        'interface': {
            'description': '',
            'status': '',
            'protocol': '',
            'ipmask':'',
            'BW': '',
            'MTU': ''
        }
    }"""

    # variable initialization

    interfaces = {}
    current_int = ''

    int_blocks = []
    block = []

    input_lines = input_lines.split('\n')

    # for each line in the input, find the patterns and separate into block
    # of data per interface
    for z in input_lines:
        # print(z)
        result = re.match(
            r"(?P<INT>[A-Z][a-zA-Z]*(?!\d+(\/\d+){,2}).\d+(\/\d+){,2}) is "
            r"(?P<STATUS>up|administratively down|down), line protocol is (?P<PROTO>up|down)",
            z)
        # get the lines than indicate the beginning of an interface block
        if result:
            int_blocks.append(block)
            block = []
            block.append(z.rstrip('\n'))
            line = z.rstrip('\n')
            current_int = result.group('INT')
            interfaces[result.group('INT')] = {
                'status': result.group('STATUS'),
                'protocol': result.group('PROTO')
            }

        # get the rest
        else:
            line = z.rstrip('\n')
            block.append(line)

            # extract the Description
            result2 = re.finditer(r"(?P<DESC>\s*(?<=Description:).*)", line.lstrip(' '))
            if result2:
                for i in result2:
                    interfaces[current_int]['description'] = i.group('DESC')

            # extract tho ip and the mask of the interface
            result2 = re.finditer(r"(?P<IP>\s*(?<=Internet address is).*)", line.lstrip(' '))
            if result2:
                for i in result2:
                    interfaces[current_int]['ipmask'] = i.group('IP')

            # extract the MTU and the BW of an interface
            result2 = re.finditer(r"(?P<MTU>\s*(?<=MTU )\d*) .*(?P<BW>(?<=BW )\d*.*) .*(?P<DLY>(?<=, DLY).*)", line)
            if result2:
                for i in result2:
                    interfaces[current_int]['MTU'] = i.group('MTU')
                    interfaces[current_int]['BW'] = i.group('BW').rstrip(',')

    # print the result
    # dumpclean(interfaces,0)
    # print(str({hostname:interfaces}))
    # return {hostname:interfaces}

    for key, value in interfaces.items():

        x = {'Hostname': hostname,
             'Inter': key,
             **value}
        savedataSQL.save('Interfaces', x)
        time.sleep(1)


        '''
        print('Interfaces', {
            'Hostname': hostname,
            'Inter': key,
            **value})
        '''


def dumpclean(obj, indentation):
    """
        Recursive function to print a dictionary
    """
    if type(obj) == dict:
        for k, v in obj.items():
            if hasattr(v, '__iter__'):
                print('\t' * indentation + k)
                dumpclean(v, indentation + 1)
            else:
                print('\t' * indentation + '%s : %s' % (k, v))
    elif type(obj) == list:
        for v in obj:
            if hasattr(v, '__iter__'):
                dumpclean(v, indentation + 1)
            else:
                print('\t' * indentation + v)
    else:
        print(obj)


# To test this file only
if __name__ == '__main__':
    # interf = open('../show_interface.txt', 'r')
    # interf.seek(0)
    out = "show interfaces" \
          "FastEthernet0/0 is up, line protocol is up "\
          "Hardware is Gt96k FE, address is c003.11c3.0000 (bia c003.11c3.0000)" \
          "Internet address is 192.168.7.1/24" \
          "MTU 1500 bytes, BW 10000 Kbit/sec, DLY 1000 usec,"\
          "reliability 255/255, txload 1/255, rxload 1/255" \


    show_interface('TunaRouter', out)  # interf.readlines()



