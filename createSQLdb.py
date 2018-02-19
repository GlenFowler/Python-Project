import pymysql  # import PyMySQL

# MySQL server login credentials
host = ''
username = ''
password = ''
database = ''

sql_connection = pymysql.connect(host, username, password, database)  #sql_connection = PyMySQL.connect(host, username, password, database)
# print(sql_connection)

# Creating DB
try:
    shell = sql_connection.cursor()
    shell.execute("use sql11222093")

    shell.execute("create table Devices(Hostname VARCHAR(30), ManIPadd VARCHAR(15) PRIMARY KEY, HWVer VARCHAR(30),"
                  "OSVer VARCHAR(20),Password VARCHAR(30), Modules TEXT)")

    shell.execute("create table Topology(Hostname VARCHAR(30) PRIMARY KEY, Connected TEXT)")

    shell.execute("create table Interfaces(Hostname VARCHAR(30) , Inter VARCHAR(20), Description TEXT, "
                  "Status VARCHAR(5), Protocol VARCHAR(5), ipmask VARCHAR(20) PRIMARY KEY, MTU VARCHAR(5),"
                  " BW VARCHAR(15))")
    print('Tables created')

except pymysql.err.InternalError:
    print('Tables already exists')


sql_connection.commit()
sql_connection.close()
