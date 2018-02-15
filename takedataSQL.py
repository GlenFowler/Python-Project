import pymysql

# MySQL server login credentials
host = 'sql11.freemysqlhosting.net'
username = 'sql11220934'
password = 'BV1N5fe9MQ'
database = 'sql11220934'


sql_connection = pymysql.connect(host, username, password, database)
shell = sql_connection.cursor()
shell.execute("use sql11220934")


def extract(table):
    query = "select * from " + table
    print(query)
    shell.execute(query)

    output = shell.fetchone()

    if table == 'Devices':
        print('{:^15}'.format('Hostname'), '{:^15}'.format('ManIPadd'), '{:^15}'.format('HWVer'),
              '{:^15}'.format('IOSVer'), '{:^15}'.format('Password'), '{:^15}'.format('Modules'))
        print('{:.^94}'.format(''))

        while output is not None:
            print('{:^15}'.format(output[0]), '{:^15}'.format(output[1]), '{:^15}'.format(output[2]),
                  '{:^15}'.format(output[3]), '{:^15}'.format(output[4]), '{:^15}'.format(output[5]))
            output = shell.fetchone()

    elif table == 'Topology':
        print('{:^15}'.format('Hostname'), '{:^75}'.format('Connected to'))
        print('{:.^94}'.format(''))

        while output is not None:
            print('{:^15}'.format(output[0]), '{:^75}'.format(output[1]))
            output = shell.fetchone()

    elif table == 'Interfaces':
        print('{:^15}'.format('Hostname'), '{:^75}'.format('Interfaces'))
        print('{:.^94}'.format(''))

        while output is not None:
            print('{:^15}'.format(output[0]), '{:^75}'.format(output[1]))
            output = shell.fetchone()

    sql_connection.commit()
    sql_connection.close()


if __name__ == '__main__':
    table = 'Topology'  # Testing variable
    extract(table)
