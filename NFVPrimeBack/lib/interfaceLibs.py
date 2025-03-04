import lib.handleLibs as hl
import os
import signal

def getInterfaceHostIpById(conn, data, userId):
    host = 0
    interfaceId = data["interface"]
    curs_obj = conn.cursor()

    curs_obj.execute("SELECT interface_host_ip as host FROM user_interfaces WHERE user_id = '{}' AND interface_id = '{}' LIMIT 1".format(userId, interfaceId))
    rows = curs_obj.fetchall()
    interfaceHost = rows[0][host]
    curs_obj.close()
    return interfaceHost

def getMaxInterfaceId(conn, userId):
    id = 0
    curs_obj = conn.cursor()

    curs_obj.execute("SELECT max(interface_id) as id FROM user_interfaces WHERE user_id = '{}'".format(userId))
    rows = curs_obj.fetchall()
    interfaceId = rows[0][id] if rows[0][id] != None else 0
    curs_obj.close()
    return interfaceId + 1

def getInterfaceMaxValues(conn):
    host = 0
    ethernet = 1
    curs_obj = conn.cursor()

    curs_obj.execute("SELECT max(interface_host_ip), max(interface_ns_ethernet) as host FROM user_interfaces where user_id != 0")
    rows = curs_obj.fetchall()
    interfaceHost = rows[0][host] if rows[0][host] else "10.0.0.100"
    interfaceHost = int(interfaceHost.split(".")[3])
    strInterfaceEthernet = rows[0][ethernet] if rows[0][host] else "16:1a:a7:f2:ac:38"
    intInterfaceEthernet = int(strInterfaceEthernet.replace(":", ""), 16)
    intInterfaceEthernet = intInterfaceEthernet + 1
    interfaceHostEthernet = ":".join([("%12x" % intInterfaceEthernet)[x:x+2] for x in range(0, 12, 2)])
    intInterfaceEthernet = intInterfaceEthernet + 2
    interfaceNsEthernet = ":".join([("%12x" % intInterfaceEthernet)[x:x+2] for x in range(0, 12, 2)])
    curs_obj.close()
    return interfaceHost + 1, interfaceHostEthernet, interfaceNsEthernet

def getInterfaceHostById(conn, userId, interfaceId):
    name = 0
    curs_obj = conn.cursor()

    curs_obj.execute("SELECT interface_host FROM user_interfaces WHERE user_id = {} AND interface_id = {}".format(userId, interfaceId))
    rows = curs_obj.fetchall()
    interfaceName = rows[0][name] if rows[0][name] != None else 0
    curs_obj.close()
    return interfaceName

def getInterfaceNameById(conn, userId, interfaceId):
    name = 0
    curs_obj = conn.cursor()

    curs_obj.execute("SELECT interface_name FROM user_interfaces WHERE user_id = {} AND interface_id = {}".format(userId, interfaceId))
    rows = curs_obj.fetchall()
    interfaceName = rows[0][name] if rows[0][name] != None else 0
    curs_obj.close()
    return interfaceName

def dummyInterface(interfaceNumber, interfaceHost, interfaceNamespace, interfaceEthernet, interfaceNsEthernet):
    # path = "sudo modprobe dummy \n"
    # path += "sudo ip link add " + str(interfaceName) + " type dummy \n"
    # path += "sudo ip link set " + str(interfaceName) + " multicast on\n"
    # path += "sudo ip link set dev " + str(interfaceName) + " address " + interfaceEthernet + "\n"
    # path += "sudo ip link set " + str(interfaceName) + " up \n"
    # path += "sudo ip addr add " + str(interfaceHost) + "/24 dev "+ str(interfaceName) + "\n"
    # path += "sudo ifconfig " + str(interfaceName) + " up\n"

    hostVethName = "veth-h{}".format(interfaceNumber)
    namespaceVethName = "veth-n{}".format(interfaceNumber)

    path =  "sudo ip link add {} type veth peer name {} \n".format(hostVethName, namespaceVethName)
    path += "sudo ip link set {} netns NFVPrime \n".format(namespaceVethName)
    path += "sudo ip netns exec NFVPrime ip link set dev {} up \n".format(namespaceVethName)
    path += "sudo ip netns exec NFVPrime ip link set {} promisc on \n".format(namespaceVethName)
    path += "sudo ip link set dev {} up \n".format(hostVethName)
    path += "sudo ip link set {} promisc on \n".format(hostVethName)
    path += "sudo ip link set dev {} address {} \n".format(hostVethName, interfaceEthernet)
    path += "sudo ip addr add {}/24 dev {} \n".format(interfaceHost, hostVethName)
    path += "sudo ip netns exec NFVPrime route add -host {} dev {} \n".format(interfaceHost, namespaceVethName)
    path += "sudo ip netns exec NFVPrime ip link set dev {} address {} \n".format(namespaceVethName, interfaceNsEthernet)
    path += "sudo ip netns exec NFVPrime ip addr add {}/24 dev {} \n".format(interfaceNamespace, namespaceVethName)
    path += "sudo route add -host {} dev {} \n".format(interfaceNamespace, hostVethName)

    print(path)
    return path

def getUserInterfaces(conn, userId):
    id = 0
    host = 1
    name = 2
    ether = 3
    hostip = 4
    ns_name = 5
    ns_ip = 6
    ns_ether = 7

    curs_obj = conn.cursor()
    curs_obj.execute("SELECT interface_id, interface_host, interface_name, interface_host_ethernet, interface_host_ip, interface_namespace_name, interface_namespace_ip, interface_ns_ethernet FROM user_interfaces WHERE user_id = {} or user_id = 0".format(userId))
    rows = curs_obj.fetchall()
    curs_obj.close()

    interfaces = {}
    i = 1
    for row in rows:
        interface = {
            "id": row[id],
            "name": row[name],
            "hostname": row[host],
            "hostip": row[hostip],
            "nsname": row[ns_name],
            "nsip": row[ns_ip],
            "hether": row[ether],
            "nsether": row[ns_ether]
        }
        interfaces["interface_"+ str(i)] = interface
        i += 1
    return interfaces

def insertUserInterface(conn, userId, interfaceId, interfaceName, interfaceHostName, interfaceHost, interfaceNamespaceName, interfaceNamespaceIp, hostEthernet, namespaceEthernet):
    curs_obj = conn.cursor()
    curs_obj.execute("INSERT INTO user_interfaces(user_id, interface_id, interface_name, interface_host, interface_host_ip, interface_namespace_name, interface_namespace_ip, interface_host_ethernet, interface_ns_ethernet) VALUES(%s, %s, %s, %s, %s, %s , %s, %s, %s)", (userId, interfaceId, interfaceName, interfaceHostName, interfaceHost, interfaceNamespaceName, interfaceNamespaceIp, hostEthernet, namespaceEthernet))
    conn.commit()
    curs_obj.close()

def deleteInterface(conn, userId, interfaceId):
    interfaceName = getInterfaceNameById(conn, userId, interfaceId)
    hostInterface = getInterfaceHostById(conn, userId, interfaceId)
    path = "sudo ip link delete " + hostInterface
    hl.executeProgram(path)

    pidns = hl.getPidByProcessName(conn, userId, "snif_{}_ns".format(interfaceName))
    try:
        os.killpg(os.getpgid(pidns), signal.SIGKILL)
    except:
        print('Interface: {} -> Sem PID'.format(interfaceId))
    hl.deletePid(conn, userId, pidns)
    curs_obj = conn.cursor()
    curs_obj.execute("DELETE FROM user_interfaces WHERE user_id = {} AND interface_id = {}".format(userId, interfaceId))
    conn.commit()
    curs_obj.close()

def deleteAllInterfaces(conn, userId):
    interfaces = getUserInterfaces(conn, userId)
    print(interfaces)
    for interface in interfaces:
        if interfaces[interface]['id'] != 0:
            deleteInterface(conn, userId, interfaces[interface]['id'])

