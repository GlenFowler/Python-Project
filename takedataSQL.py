import pymysql
import re

"""
Module for extracting data from a database

This module connect to a database and extract data from devices stored in the database.

    Example:

            $ python3 takedataSQL.py
"""


# MySQL server login credentials
database_info = open('database.txt', 'r')
database_info.seek(0)
login_credentials = ' '.join(database_info.readlines())
database_info.close
# print(login_credentials)
host = re.search(r"host = '(?P<host>.*)'", login_credentials).group('host')
username = re.search(r"username = '(?P<username>.*)'", login_credentials).group('username')
password = re.search(r"password = '(?P<password>.*)'", login_credentials).group('password')
database = re.search(r"database = '(?P<database>.*)'", login_credentials).group('database')
# print(host, ' ', username, ' ', password, ' ', database)


def extract(table):
    """
    Function to save data into a table of one SQL database.

        Args:
            table (str): SQL table where extract data.

    """
    sql_connection = pymysql.connect(host, username, password, database)
    shell = sql_connection.cursor()
    query = "use " + database
    shell.execute(query)  # "use sql11222093"

    query = "select * from " + table + " ORDER BY Hostname"
    # print(query)
    shell.execute(query)
    shell.close()

    output = shell.fetchone()

    if table == 'Devices':
        x = len(output[1]) + 300
        print('{:^15}'.format('Hostname'), '{:^15}'.format('ManIPadd'), '{:^20}'.format('HWVer'),
              '{:^15}'.format('OSVer'), '{:^20}'.format('Password'), '{:^{}}'.format('Modules', x-80))
        print('{:.^{}}'.format('', x))

        while output is not None:
            print('{:^15}'.format(output[0]), '{:^15}'.format(output[1]), '{:^15}'.format(output[2]),
                  '{:^20}'.format(output[3]), '{:^15}'.format(output[4]), '{:^{}}'.format(output[5], x-80), '\n')
            output = shell.fetchone()

    elif table == 'Topology':
        x = len(output[1]) + 100
        print('{:^15}'.format('Hostname'), '{:^{}}'.format('Connected to', x-15))
        print('{:.^{}}'.format('', x))

        while output is not None:
            print('{:^15}'.format(output[0]), '{:^{}}'.format(output[1], x-15), '\n')
            output = shell.fetchone()

    elif table == 'Interfaces':
        # x = len(output[1]) + 100
        print('{:^15}'.format('Hostname'), '{:^20}'.format('Interfaces'), '{:^42}'.format('Description'),
              '{:^17}'.format('Status'), '{:^17}'.format('Protocol'),
              '{:^20}'.format('MTU'), '{:^15}'.format('BW'), '{:^30}'.format('IP/Mask'),)
        print('{:.^180}'.format(''))

        while output is not None:
            if output[2] is None:
                desc = 'None'
            else:
                desc = output[2]
            print('{:^15}'.format(output[0]), '{:^20}'.format(output[1]), '{:^40}'.format(desc),
                  '{:^20}'.format(output[3]), '{:^15}'.format(output[4]), '{:6}'.format(' '),
                  '{:^6}'.format(output[6]), '{:^30}'.format(output[7]), end='')

            if output[5] is None:
                ip = 'None'
            else:
                ip = output[5]

            print('{:^15}'.format(ip))
            output = shell.fetchone()
            print('\n', end='')

    sql_connection.commit()
    sql_connection.close()


if __name__ == '__main__':
    table = 'Topology'  # Testing variable # table ---> Devices, Topology, Interfaces
    # extract(table)
    # extract('Devices')
    extract('Interfaces')
