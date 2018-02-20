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
    host = 'sql11.freemysqlhosting.net'
    username = 'sql11222093'
    password = 'gcCS8F4Wku'
    database = 'sql11222093'

    sql_connection = pymysql.connect(host, username, password, database)
    shell = sql_connection.cursor()
    query = "use " + database
    shell.execute(query)

    # Query
    query = "select * from Topology"
    # print(query)
    shell.execute(query)
    shell.close()

    output = shell.fetchall()
    # print(output)

    regex = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')

    routers = []
    routers_edges = []
    routers_conn = []

    # Preper data to process then the data
    for row in output:
        cad = regex.findall(row[1])
        routers_conn.append((row[0], cad))
        if row[0] not in routers:
            routers.append(row[0])

    for x in routers_conn:
        # print(x[1])
        if '192.168.15.0' in x[1]:
            x[1].remove('192.168.15.0')
        for i in routers_conn:
            if x[1] != i[1]:
                if set(x[1]).intersection(i[1]) != set():
                    # print(x[0], 'is connected with ', i[0])
                    routers_edges.append((x[0], i[0]))

    print(routers)
    print(routers_conn)
    print(routers_edges)

    G = nx.Graph()
    G.add_nodes_from(routers)
    G.add_edges_from(routers_edges)

    nx.draw(G, with_labels=True)

    plt.show()  # display


if __name__ == '__main__':
    query_topology()
