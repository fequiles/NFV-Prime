from socket import *
import struct
import binascii
import threading #thread module imported
import time #time module
import psycopg2

conn = psycopg2.connect(
    host="127.0.0.1",
    database="postgres",
    user="postgres",
    password="postgres",
    port="5433")

dummies = {}
user_id = ''
iRx=0
iTx=0

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
    return ip_origin, ip_destiny, data[header_size_bytes:]

def limpaRxTx():
    if (user_id != ''):
        cleanInterfacesRxTx() 

def thread_Time(thread_name, interval, ip):
    global user_id, iTx, iRx
    while 1:
        semaphore.acquire()
        try:
            uId, iId = getInterfaceIdsByHost(ip)
            user_id = uId
        except:
            print('Erro ao buscar interfaceId')
            break
        updateInterfaceRxTx(uId, iId, iRx, iTx)
        limpaRxTx()
        semaphore.release()  
        time.sleep(interval)

def getInterfaceIdsByHost(host):
    userId = 0
    interfaceId = 1
    curs_obj = conn.cursor()

    curs_obj.execute("SELECT user_id, interface_id as id FROM user_interfaces WHERE interface_host_ip = '{}'".format(host))
    rows = curs_obj.fetchall()
    uId = rows[0][userId] if rows[0][userId] != None else 0
    iId = rows[0][interfaceId] if rows[0][interfaceId] != None else 0
    curs_obj.close()

    return uId, iId

def updateInterfaceRxTx(uId, iId, rx, tx):
    print("UPDATE user_interfaces SET interface_tx = {}, interface_rx = {} WHERE user_id = {} AND interface_id = {}".format(tx, rx, uId, iId))
    curs_obj = conn.cursor()

    curs_obj.execute("UPDATE user_interfaces SET interface_tx = interface_tx + {}, interface_rx = interface_rx + {} WHERE user_id = {} AND interface_id = {}".format(tx, rx, uId, iId))
    conn.commit()
    curs_obj.close()

def cleanInterfacesRxTx():
    global iTx, iRx
    iRx = 0
    iTx = 0

def socketStart(net_interface):
    Socket = socket(AF_PACKET, SOCK_RAW, htons(3))
    Socket.bind((net_interface, 0))
    return Socket

def thread_ListenPort(thread_name, ip):
    clientSocket = socket(family=AF_INET, type=SOCK_DGRAM)
    clientSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    clientSocket.bind((ip, 9900))
    while 1:
        contentReceived, client = clientSocket.recvfrom(65535)

clientSocket = socketStart("veth-h1")
client_interface = "10.0.1.101"

semaphore = threading.Semaphore(1)
timer = threading.Thread(target=thread_Time, args=('timer', 1, client_interface))
timer.start()

listenport = threading.Thread(target=thread_ListenPort, args=('listenner', client_interface))
listenport.start()

while 1:
    contentReceived = clientSocket.recv(65535)
    mac_destino, mac_fonte, protocolo, carga_util = unpackFrameEthernet(contentReceived)
    ipOrigem, ipDestino, dados = ipPacketData(carga_util)
    size = len(contentReceived)
    semaphore.acquire()
    if ipDestino == "10.0.1.101":
        # print('{} -> {}, tam: {}'.format(ipOrigem, ipDestino, size))
        iRx = iRx + size
    # if ipOrigem == "10.0.1.102":
    #     iTx = iTx + size
    semaphore.release()
