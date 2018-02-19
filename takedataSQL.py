import pymysql

"""
Module for extracting data from a database

This module connect to a database and extract data from devices stored in the database.

    Example:

            $ python3 takedataSQL.py
"""

# MySQL server login credentials
host = ''
username = ''
password = ''
database = ''


# sql_connection = pymysql.connect(host, username, password, database)
# shell = sql_connection.cursor()
# shell.execute("use sql11220934")



def extract(table):
    """
    Function to save data into a table of one SQL database.

        Args:
            table (str): SQL table where extract data.

    """
    sql_connection = pymysql.connect(host, username, password, database)
    shell = sql_connection.cursor()
    shell.execute("use sql11222093")

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
              '{:^10}'.format('Status'), '{:^17}'.format('Protocol'),
              '{:^20}'.format('MTU'), '{:^15}'.format('BW'), '{:^30}'.format('IP/Mask'),)
        print('{:.^180}'.format(''))

        while output is not None:
            if output[2] is None:
                desc = 'None'

            print('{:^15}'.format(output[0]), '{:^20}'.format(output[1]), '{:^40}'.format(desc),
                  '{:^13}'.format(output[3]), '{:^15}'.format(output[4]), '{:6}'.format(' '),
                  '{:^6}'.format(output[6]), '{:^30}'.format(output[7]), end='')

            print('{:15}'.format(output[5]))
            output = shell.fetchone()
            print('\n', end='')

    sql_connection.commit()
    sql_connection.close()


if __name__ == '__main__':
    table = 'Topology'  # Testing variable # table ---> Devices, Topology, Interfaces
    extract(table)
    extract('Devices')
    extract('Interfaces')
