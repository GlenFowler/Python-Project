import re
import savedataSQL
import pymysql
import networkx as nx
import matplotlib.pyplot as plt


# Function topology. This function insert into data base the name of the device and their subnettes directly connected
# Receives the output of the commands 'show ip route' and the name of the device

def topology(name="name", str_in="str"):
    regex = re.compile(r'(C\s+(?P<ip>(\d+.?)+\d).is directly connected, (?P<int>\w+(\/?\d){0,2}))')
    lista = []

    cad = regex.findall(str_in)

    for i in cad:
        x = i[1] + ' --> ' + i[3]
        lista.append(x)

    dic = {"Hostname": name, "Connected": ', '.join(lista)}
    savedataSQL.save("Topology", dic)


# Function query_topology. This function search which routers are connected between then

def query_topology():
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

    # Connection to the DB
    sql_connection = pymysql.connect(host, username, password, database)
    shell = sql_connection.cursor()
    query = "use " + database
    shell.execute(query)

    # Query
    query = "select * from Topology"
    # print(query)
    shell.execute(query)
    shell.close()

    # Output of the DB
    output = shell.fetchall()
    # print(output)

    # Regex for ip extraction
    regex = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')

    # Variables for draw
    routers = []
    routers_edges = []
    routers_conn = []

    # Prepare data to process then the data
    for row in output:
        cad = regex.findall(row[1])
        routers_conn.append((row[0], cad))
        if row[0] not in routers:
            routers.append(row[0])

    iprange = open('range.txt', 'r')
    ip_manager = regex.search(iprange.readline()).group()
    iprange.close()
    # print(ip_manager)

    # Determine the ip connections between routers
    for x in routers_conn:
        # print(x[1])
        if ip_manager in x[1]:
            x[1].remove(ip_manager)
        for i in routers_conn:
            if x[1] != i[1]:
                if set(x[1]).intersection(i[1]) != set():
                    # print(x[0], 'is connected with ', i[0])
                    routers_edges.append((x[0], i[0]))

    # print(routers)
    # print(routers_conn)
    # print(routers_edges)

    # Draw router topology
    G = nx.Graph()
    G.add_nodes_from(routers)
    G.add_edges_from(routers_edges)

    nx.draw(G, with_labels=True, pos=nx.spring_layout(G))

    plt.show()  # display


if __name__ == '__main__':
    query_topology()
