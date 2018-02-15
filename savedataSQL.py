import pymysql

# MySQL server login credentials
host = ''
username = ''
password = ''
database = ''


# table ---> Devices, Topology, Interfaces
def save(table, data):
    keys = []
    values = []
    j = ', '
    for key, value in data.items():
        print(key, value)
        keys.append(key)
        value = '"' + value + '"'
        values.append(value)

    print(keys[0])
    # print(values)
    print('connecting to the DB')
    sql_connection = pymysql.connect(host, username, password, database)
    # print(sql_connection)
    shell = sql_connection.cursor()
    shell.execute("use sql11220934")
    try:
        keys_i = j.join(keys)
        values_i = j.join(values)
        query = "insert into " + table + "(" + keys_i + ") values(" + values_i + ")"
        print('Saving data')
        # print('lista: ', query)
        shell.execute(query)
        sql_connection.commit()
        sql_connection.close()
    except pymysql.err.IntegrityError:
        print('Input Already exists, need to update')
        print('updating')

        if table == 'Devices':

            query = "update " + table + " set " + keys[0] + "=" + values[0] + ", " + keys[2] + "=" + values[2] + ", " \
                    + keys[3] + "=" + values[3] + ", " + keys[4] + "=" + values[4] + ", " + keys[5] + "=" + values[5] + \
                    " where " + keys[1] + "=" + values[1]
        else:
            query = "update " + table + " set " + keys[1] + "=" + values[1] + " where " + keys[0] + "=" + values[0]

        print('query: ', query)
        shell.execute(query)
        sql_connection.commit()
        sql_connection.close()


if __name__ == '__main__':
    # Testing variables
    # device1 = {'Hostname': 'Router1', 'ManIPadd': '192.168.1.1', 'HWVer': 'asdfghjkl', 'IOSVer': '15.5',
    #            'Password': 'qwerty', 'Modules': 'SFW32'}
    device2 = {'Hostname': 'Router2', 'ManIPadd': '192.168.1.2', 'HWVer': 'asdfghjkl', 'IOSVer': '12.4',
               'Password': 'qwerty', 'Modules': 'SFW32'}
    topology1 = {'Hostname': 'Router2', 'Connected': '192.168.2.1, 192.168.5.4, 165.143.2.1'}
    interfaces1 = {'Hostname': 'Router2', 'Inter': 'Fa0/0 Up Up, G0/1 Up Up'}
    tables = 'Topology'

    print('enviando datos')
    save(tables, topology1)
