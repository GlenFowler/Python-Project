import re
import savedataSQL

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