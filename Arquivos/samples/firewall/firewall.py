import threading #thread module imported
import socket
import struct
import binascii
import time

def bytesToHexa(bytes_address):
    hex_list = []
    address = binascii.hexlify(bytes_address).decode("ascii")
    for i in range(0,12,2):
        hex_list.append(address[i:i+2])
    mac = ":".join(hex_list)
    return mac  

def udp_unpack(data):
    s_port, d_port, length, checksum = struct.unpack('! H H H H', data[:8])
    return s_port, d_port, length, checksum, data[8:]

def unpackFrameEthernet(frame):
    destiny, origin, protocol = struct.unpack('! 6s 6s H', frame[:14])
    return bytesToHexa(destiny), bytesToHexa(origin), socket.htons(protocol), frame[14:]

def unpacketIpData(data):
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
    ip_origin = socket.inet_ntoa(ip_data_tuple[8])
    ip_destiny = socket.inet_ntoa(ip_data_tuple[9])
    header_size_bytes = (version & 15) * 4
   
    return ip_origin, ip_destiny, data[header_size_bytes:]

def unpackUdpData(data):
    tupla_dados_udp = struct.unpack('! H H H H', data[:8])
    origin_port = tupla_dados_udp[0]
    destiny_port = tupla_dados_udp[1]
    udp_len = tupla_dados_udp[2]
    udp_checksum = tupla_dados_udp[3]

    return destiny_port, data[8:]

def numberPacketsProcessed(n_transmitted, n_dropped, max_processed):
    total =  n_transmitted + n_dropped
    if total >= max_processed:
        return 1
    return 0

def saveInfos():
    """Funcao que salva as informacoes obtidas pelo algoritmo
     em um arquivo .csv de saida"""
    global n_dropped, n_transmitted, arquivoSaida

    saida = '{}__{}'.format(n_transmitted, n_dropped)
    arquivoSaida.write(saida)
    arquivoSaida.close()
    exit() 

def thread_Time(thread_name, interval):
    """ Thread que reseta o consumo do bucket a cada intervalo de tempo
        interval -> intervalo de tempo para que sejam adicionados os tokens"""
    global semaphore, turnedOff
    while 1: #Ver condicao do while
        semaphore.acquire()
        if turnedOff:
            turnedOff = False
        else:
            turnedOff = True
        semaphore.release()
        if debug: 
            total =  n_transmitted + n_dropped
            if total >= 500:
                exit()
        time.sleep(interval)

def thread_Firewall():
    """ Thread do Firewall que ao receber um pacote verifica  
    a origem do pacote e se necessario não o retransmite """
    global loopbackSocket, dropped, debug, n_transmitted, n_dropped, send
    while 1:
        contentReceived = loopbackSocket.recv(65535)
        mac_destino, mac_fonte, protocolo, carga_util = unpackFrameEthernet(contentReceived)
        ipOrigin, ipDestiny, data = unpacketIpData(carga_util)
        if ipDestiny == server_ip:
            destinyPort, udpData = unpackUdpData(data)
            if (destinyPort == 8001 and (turnedOff)):
                if (send):
                    print(time.time())
                    print(len(udpData))
                    clientSocket.sendto(udpData, (server_interface, 7000))
                    send = False
                else: 
                    send = True
                if debug:
                    n_transmitted += 1
                    if numberPacketsProcessed(n_transmitted, n_dropped, 500): saveInfos()

dropped = []

turnedOff = True
send = True

loopback = 'lo'
server_ip = :dummy_0
server_interface = :dummy_1
interval = 4
debug = 1

if debug:
    n_transmitted = 0
    n_dropped = 0
    arquivoSaida = open('forwarder.csv', 'w')

semaphore = threading.Semaphore(1)
loopbackSocket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(3))
loopbackSocket.bind((loopback, 0))

clientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
clientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
clientSocket.bind((server_ip, 8001))

timer = threading.Thread(target=thread_Time, args=('timer', interval))
firewall = threading.Thread(target=thread_Firewall, args=())

firewall.start()
timer.start()