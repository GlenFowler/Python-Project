import pymysql
import sys

from colorama import init, deinit, Fore, Style

"""
Module for saving data into a database

This module connect to a database and save data from devices.

    Example:

            $ python3 savedataSQL.py
"""

# MySQL server login credentials
host = ''
username = ''
password = ''
database = ''

init()


# table ---> Devices, Topology, Interfaces
def save(table, data):
    """
    Function to save data into a table of one SQL database.

        Args:
            table (str): SQL table where save data.
            data (str): data to save.

    """
    keys = []
    values = []
    j = ', '
    for key, value in data.items():
        # print(key, value)
        keys.append(key)
        value = '"' + value + '"'
        values.append(value)

    # print(values)
    sys.stdout.write(Fore.YELLOW + Style.BRIGHT + '\rconnecting to the DB and saving data')
    sys.stdout.flush()
    # print('\n')
    # print('connecting to the DB')
    sql_connection = pymysql.connect(host, username, password, database)
    # print(sql_connection)
    shell = sql_connection.cursor()
    shell.execute("use sql11222093")

    try:
        keys_i = j.join(keys)
        values_i = j.join(values)
        query = "insert into " + table + "(" + keys_i + ") values(" + values_i + ")"

        # print('Saving data')
        # print('lista: ', query)
        shell.execute(query)
        sql_connection.commit()
        sql_connection.close()
    except pymysql.err.IntegrityError:
        print(Fore.CYAN + Style.BRIGHT + '\nInput Already exists, need to update: ', values[0], 'in table: ', table,
              end='')
        print(Style.RESET_ALL)
        # print('updating')

        if table == 'Devices':

            query = "update " + table + " set " + keys[0] + "=" + values[0] + ", " + keys[2] + "=" + values[2] + ", " \
                    + keys[3] + "=" + values[3] + ", " + keys[4] + "=" + values[4] + ", " + keys[5] + "=" + values[5] + \
                    " where " + keys[1] + "=" + values[1]
        else:
            query = "update " + table + " set " + keys[1] + "=" + values[1] + " where " + keys[0] + "=" + values[0]

        # print('query: ', query)
        shell.execute(query)
        sql_connection.commit()
        sql_connection.close()


deinit()

if __name__ == '__main__':
    # Testing variables
    # device1 = {'Hostname': 'Router1', 'ManIPadd': '192.168.1.1', 'HWVer': 'asdfghjkl', 'IOSVer': '15.5',
    #            'Password': 'qwerty', 'Modules': 'SFW32'}
    device2 = {'Hostname': 'Router2', 'ManIPadd': '192.168.1.2', 'HWVer': 'asdfghjkl', 'IOSVer': '12.4',
               'Password': 'qwerty', 'Modules': 'SFW32'}
    topology1 = {'Hostname': 'Router2', 'Connected': '192.168.2.1, 192.168.5.4, 165.143.2.1'}
    interfaces1 = {'Hostname': 'Router2', 'Inter': 'Fa0/0', 'Description': 'asdfagasgasg', 'Status': 'UP',
                   'Protocol': 'UP', 'ip/mask': '192.168.4.1/24', 'MTU': '1500', 'BW': '1544 Kbit/sec'}

    tables = 'Interfaces'

    print('enviando datos')
    save(tables, interfaces1)
