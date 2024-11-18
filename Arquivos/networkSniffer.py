from socket import *
import struct
import binascii
import threading #thread module imported
import time #time module
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="postgres",
    port="5432")

dummies = {}
user_id = ''

def unpackFrameEthernet(frame):
    destiny, origin, protocol = struct.unpack('! 6s 6s H', frame[:14])
    return bytesToHexa(destiny), bytesToHexa(origin), htons(protocol), frame[14:]

def bytesToHexa(bytes_address):
    hex_list = []
    address = binascii.hexlify(bytes_address).decode("ascii")
    for i in range(0,12,2):
        hex_list.append(address[i:i+2])
    mac = ":".join(hex_list)
    return mac

def socketStart(net_interface):
    Socket = socket(AF_PACKET, SOCK_RAW, htons(3))
    Socket.bind((net_interface, 0))
    return Socket

def ipPacketData(data):
    ip_data_tuple = struct.unpack("!BBHHHBBH4s4s", data[:20])
    version = ip_data_tuple[0]
    header_len = version >> 4
    service_type = ip_data_tuple[1]
    total_size = ip_data_tuple[2]
    identifier = ip_data_tuple[3]
    offset_fragment = ip_data_tuple[4]
    life_time_ttl = ip_data_tuple[5]
    protocols = ip_data_tuple[6]
    checksum_header = ip_data_tuple[7]
    ip_origin = inet_ntoa(ip_data_tuple[8])
    ip_destiny = inet_ntoa(ip_data_tuple[9])

    header_size_bytes = (version & 15) * 4
    return ip_origin, ip_destiny

def limpaRxTx():
    global dummiesRx, user_id
    if (user_id != ''):
        cleanInterfacesRxTx() 

def thread_Time(thread_name, interval):
    global dummiesRx, user_id
    while 1:
        semaphore.acquire()
        # if (user_id != ''):
        #     cleanDbInterfacesRxTx(user_id) 
        for dummy in dummies:
            try:
                uId, iId = getInterfaceIdsByHost(dummy)
                user_id = uId
            except:
                break
            updateInterfaceRxTx(uId, iId, dummies[dummy]['rx'], dummies[dummy]['tx'])
        limpaRxTx()
        semaphore.release()  
        time.sleep(interval)

def getInterfaceIdsByHost(host):
    userId = 0
    interfaceId = 1
    curs_obj = conn.cursor()

    curs_obj.execute("SELECT user_id, interface_id as id FROM user_interfaces WHERE interface_host = '{}'".format(host))
    rows = curs_obj.fetchall()
    uId = rows[0][userId] if rows[0][userId] != None else 0
    iId = rows[0][interfaceId] if rows[0][interfaceId] != None else 0
    curs_obj.close()

    return uId, iId

def updateInterfaceRxTx(uId, iId, rx, tx):
    print("UPDATE user_interfaces SET interface_tx = interface_tx + {}, interface_rx = interface_rx + {} WHERE user_id = {} AND interface_id = {}".format(tx, rx, uId, iId))
    curs_obj = conn.cursor()

    curs_obj.execute("UPDATE user_interfaces SET interface_tx = interface_tx + {}, interface_rx = interface_rx + {} WHERE user_id = {} AND interface_id = {}".format(tx, rx, uId, iId))
    conn.commit()
    curs_obj.close()

def cleanInterfacesRxTx():
    for dummy in dummies:
        dummies[dummy]['rx'] = 0
        dummies[dummy]['tx'] = 0

interval = 0.1

semaphore = threading.Semaphore(1)
timer = threading.Thread(target=thread_Time, args=('timer', interval))
timer.start()

sniffer = socketStart('veth4cb847d')
while True:
    contentReceived = sniffer.recv(65535)
    mac_destino, mac_fonte, protocolo, carga_util = unpackFrameEthernet(contentReceived)
    ipOrigem, ipDestino = ipPacketData(carga_util)
    size = len(contentReceived)
    if "10.0.0.1" in ipDestino:
        # print(ipDestino + " " + str(size) + " " + str(time.time()))
        semaphore.acquire()
        if (dummies.get(ipDestino)):
            dummies[ipDestino]['rx'] += size
        else:
            dummy = {ipDestino:{'rx': size, 'tx':0}}
            dummies.update(dummy)
            # dummies[ipDestino].rx = size
            # dummies[ipDestino].tx = 0
        semaphore.release()
    if "10.0.0.1" in ipOrigem:
        semaphore.acquire()
        if (dummies.get(ipOrigem)):
            dummies[ipOrigem]['tx'] += size
        else:
            dummy = {ipOrigem:{'rx': 0, 'tx':size}}
            dummies.update(dummy)
            # dummies[ipOrigem].tx = size
            # dummies[ipOrigem].rx = 0 
        semaphore.release()

# sudo docker run -d --name generator traffic /bin/bash -c "echo 'Hello World'; sleep infinity" --network="bridge"
