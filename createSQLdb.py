import pymysql  # import PyMySQL

# MySQL server login credentials
host = 'sql11.freemysqlhosting.net'
username = 'sql11220934'
password = 'BV1N5fe9MQ'
database = 'sql11220934'

sql_connection = pymysql.connect(host, username, password, database)  #sql_connection = PyMySQL.connect(host, username, password, database)
# print(sql_connection)

# Creating DB
try:
    shell = sql_connection.cursor()
    shell.execute("use sql11220934")
    shell.execute("create table Devices(Hostname VARCHAR(30), ManIPadd VARCHAR(15) PRIMARY KEY, HWVer VARCHAR(30),"
                  "IOSVer VARCHAR(20),Password VARCHAR(30), Modules VARCHAR(30))")
    shell.execute("create table Topology(Hostname VARCHAR(30) PRIMARY KEY, Connected VARCHAR(40))")
    shell.execute("create table Interfaces(Hostname VARCHAR(30) PRIMARY KEY, Inter VARCHAR(40))")
    print('Tables created')
#
except pymysql.err.InternalError:
    print('Tables already exists')


sql_connection.commit()
sql_connection.close()
