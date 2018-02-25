import pymysql  # import PyMySQL
import re

# MySQL server login credentials
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

sql_connection = pymysql.connect(host, username, password, database)  #sql_connection = PyMySQL.connect(host, username, password, database)
# print(sql_connection)

# Creating DB
try:
    shell = sql_connection.cursor()
    query = "use " + database
    shell.execute(query)

    shell.execute("create table Devices(Hostname VARCHAR(30), ManIPadd VARCHAR(15) PRIMARY KEY, HWVer VARCHAR(30),"
                  "OSVer VARCHAR(20),Password VARCHAR(30), Modules TEXT)")

    shell.execute("create table Topology(Hostname VARCHAR(30) PRIMARY KEY, Connected TEXT)")

    shell.execute("create table Interfaces(Hostname VARCHAR(30) , Inter VARCHAR(20), Description TEXT, "
                  "Status VARCHAR(5), Protocol VARCHAR(5), ipmask VARCHAR(20), MTU VARCHAR(5),"
                  " BW VARCHAR(15), PRIMARY KEY (Hostname, Inter))")
    print('Tables created')

except pymysql.err.InternalError:
    print('Tables already exists')


sql_connection.commit()
sql_connection.close()
