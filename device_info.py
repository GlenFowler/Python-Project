import re
import savedataSQL


# Function device_info. Returns a dictionary with the device's information asked in point 1:
#  - Hardware version 		'HWVer'
#  - OS version 			'OSVer'
#  - Management IP address  'ManIPadd'
#  - Password 				'Password'
#  - Modules 				'Modules'
# Receives the output of the commands 'show version' and 'show inventory', and makes use of the
# functions show_version and show_inventory to process those outputs.

def device_info(hostname, password, IPmanagement, version_out, inventory_out):
    device = {'Hostname': '', 'ManIPadd': '', 'HWVer': '', 'OSVer': '', 'Password': '', 'Modules': ''}

    version = show_version(version_out)

    modules = show_inventory(inventory_out)

    device['Hostname'] = hostname
    device['Password'] = password.rstrip('\n')
    device['ManIPadd'] = IPmanagement
    device['HWVer'] = version['Hardware']
    device['OSVer'] = version['Type'] + ' ' + version['SoftwareVersion']
    device['Modules'] = modules  # De momento solo guardo la descripcion del primero para probar.

    # print(device)

    savedataSQL.save('Devices', device)
    return device


# Function to process the output from command 'show version'
# Returns a dictionary with keys 'Type', 'SoftwareVersion' and 'Hardware'
# The value of the key 'Type' (IOS, Nexus) will indicate if it is a Cisco IOS device or a Nexus device.

def show_version(stdout):
    result = {'Type': '', 'SoftwareVersion': '', 'Hardware': ''}

    # IOS patterns
    IOS_version = r'(?<=Cisco IOS Software, ).*, Version (?P<version>.*)'
    IOS_hardware = r'(?P<hardware>Cisco (.*) \(.*\))(?= processor)'

    # NXOS patterns
    NXOS_check = r'(^Cisco Nexus Operating System \(NX-OS\) Software)'
    NXOS_version = r'(?<=system: version )(?P<version>.*)(?= \[)'
    NXOS_hardware = r'(?<=Hardware\n)(?P<hardware>.*)'

    # Test if it is a Cisco IOS device

    IOS_match = re.search(IOS_version, stdout, flags=0)

    if IOS_match:

        result['Type'] = 'IOS'

        IOS_version = IOS_match.group('version').split(',')[0]
        result['SoftwareVersion'] = IOS_version

        IOS_hardware = re.search(IOS_hardware, stdout, flags=0).group('hardware')
        result['Hardware'] = IOS_hardware


    # Test if it is a Nexus device

    else:

        NXOS_match = re.search(NXOS_check, stdout, flags=0)
        if NXOS_match:
            result['Type'] = 'Nexus'

            NXOS_version = re.search(NXOS_version, stdout, flags=0).group('version')
            result['SoftwareVersion'] = NXOS_version

            NXOS_hardware = re.search(NXOS_hardware, stdout, flags=0).group('hardware')
            result['Hardware'] = NXOS_hardware

    # In case it is not an IOS device either a Nexus device, result will be empty
    return result


# Function to process the output from command 'show inventory'
# Returns a dictionary with keys 1, 2, 3... for every module found in the device.
# The value of each module is another dictionary, with keys 'Name', 'Description', 'PID', 'VID', 'SN'

def show_inventory(stdout):
    # print(stdout)
    modules = []
    data = re.findall(r'(NAME: "(?P<name>.*)", .*\n.* SN: (?P<sn>\w+))', stdout)  # r'(NAME: "(?P<name>.*)", )'
    # print('x :', x)

    for i in data:
        s = 'Module: ' + i[1] + ' SN: ' + i[2]
        # print(s)
        modules.append(s)

    modules = ', '.join(modules)
    # print('return: ', modules)

    return modules
