import MySQLdb

routers = ['Router 1','Router 2','Router 3','Router 4','Router 5']

host = 'sql11.freemysqlhosting.net'
username =  'sql11220934'
password = 'BV1N5fe9MQ'
database =  'sql11220934'

sql_connection = MySQLdb.connect(host , username, password, database)

print sql_connection

shell = sql_connection.cursor()
shell.execute("use sql11220934")
shell.execute("grant all on sql11220934.* to 'sql11220934'@'sql11.freemysqlhosting.net")
shell.execute("create table Routers(Device VARCHAR(30))")
shell.execute("insert into Routers (Device) values('RouterX')")

sql_connection.commit()
sql_connection.close()