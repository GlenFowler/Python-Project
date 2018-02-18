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
    device['Password'] = password
    device['ManIPadd'] = IPmanagement
    device['HWVer'] = version['Hardware']
    device['OSVer'] = version['Type'] + ' ' + version['SoftwareVersion']
    device['Modules'] = modules['Description']  # De momento solo guardo la descripcion del primero para probar.

    print(modules['Description'])

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
    # savedataSQL.save('Devices', result)
    return result


# Function to process the output from command 'show inventory'
# Returns a dictionary with keys 1, 2, 3... for every module found in the device.
# The value of each module is another dictionary, with keys 'Name', 'Description', 'PID', 'VID', 'SN'

def show_inventory(stdout):
    module = r'(^NAME: "(?P<name>.*)", DESCR: "(?P<descr>.*)"\nPID: (?P<pid>.*), VID: (?P<vid>.*), SN: (?P<sn>.*))'
    # print(stdout)
    found_modules = re.finditer(module, stdout, re.MULTILINE)

    modules = {'Name': '', 'Description': '', 'PID': '', 'VID': '', 'SN': ''}

    i = 1
    for m in found_modules:
        module = {'Name': m.group('name'), 'Description': m.group('descr'), 'PID': m.group('pid'),
                  'VID': m.group('vid'), 'SN': m.group('sn')}
        modules[i] = module
        i = i + 1
    # print(modules)
    return modules


if __name__ == '__main__':
    hostname = 'ocsic'
    password = '1234'
    IPmanagement = '10.14.0.8'
    version_out = b'show version\r\nCisco IOS Software, 2600 Software (C2691-ADVENTERPRISEK9-M), Version 12.4(25c), RELEASE SOFTWARE (fc2)\r\nTechnical Support: http://www.cisco.com/techsupport\r\nCopyright (c) 1986-2010 by Cisco Systems, Inc.\r\nCompiled Thu 11-Feb-10 23:23 by prod_rel_team\r\n\r\nROM: ROMMON Emulation Microcode\r\nROM: 2600 Software (C2691-ADVENTERPRISEK9-M), Version 12.4(25c), RELEASE SOFTWARE (fc2)\r\n\r\nR4 uptime is 9 hours, 19 minutes\r\nSystem returned to ROM by unknown reload cause - suspect boot_data[BOOT_COUNT] 0x0, BOOT_COUNT 0, BOOTDATA 19\r\nSystem image file is "tftp://255.255.255.255/unknown"\r\n\r\n\r\nThis product contains cryptographic features and is subject to United\r\nStates and local country laws governing import, export, transfer and\r\nuse. Delivery of Cisco cryptographic products does not imply\r\nthird-party authority to import, export, distribute or use encryption.\r\nImporters, exporters, distributors and users are responsible for\r\ncompliance with U.S. and local country laws. By using this product you\r\nagree to comply with applicable laws and regulations. If you are unable\r\nto comply with U.S. and local laws, return this product immediately.\r\n\r\nA summary of U.S. laws governing Cisco cryptographic products may be found at:\r\nhttp://www.cisco.com/wwl/export/crypto/tool/stqrg.html\r\n\r\nIf you require further assistance please contact us by sending email to\r\nexport@cisco.com.\r\n\r\nCisco 2691 (R7000) processor (revision 0.1) with 187392K/9216K bytes of memory.\r\nProcessor board ID XXXXXXXXXXX\r\nR7000 CPU at 160MHz, Implementation 39, Rev 2.1, 256KB L2, 512KB L3 Cache\r\n2 FastEthernet interfaces\r\nDRAM configuration is 64 bits wide with parity enabled.\r\n55K bytes of NVRAM.\r\n\r\nConfiguration register is 0x2102\r\n\r\n'
    inventory_out = b'R4#show invent\r\nNAME: "2691 chassis", DESCR: "2691 chassis"\r\nPID:                   , VID: 0.1, SN: XXXXXXXXXXX\r\n\r\n\r\nR4#'
    # Llamada a la funcion
    device = device_info(hostname, password, IPmanagement, version_out.decode(), inventory_out.decode())
    print(device)
    print('Guardar en base de datos...')
    savedataSQL.save('Devices', device)