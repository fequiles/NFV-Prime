import threading #thread module imported
from socket import *
import struct
import binascii

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

def numberPacketsProcessed(n_transmitted, n_dropped, max_processed):
    total =  n_transmitted + n_dropped
    if total >= max_processed:
        return 1
    return 0

def saveInfos():
    """Funcao que salva as informacoes obtidas pelo algoritmo em um arquivo .csv de saida"""
    global n_dropped, n_transmitted, arquivoSaida

    saida = '{}__{}'.format(n_transmitted, n_dropped)
    arquivoSaida.write(saida)
    arquivoSaida.close()
    exit() 

def thread_Forwarder():
    """ Thread do Forwarder que ao receber um pacote envia para o destino"""
    global clientSocket, dropped, debug, n_transmitted, n_dropped
    while 1:
        contentReceived = clientSocket.recv(65535)
        mac_destino, mac_fonte, protocolo, carga_util = unpackFrameEthernet(contentReceived)
        ipOrigem, ipDestino, dados = ipPacketData(carga_util)
        if ipDestino == '10.0.1.101':
            print ("ipOrigem {} -> ipDestino {}".format(ipOrigem, ipDestino))
            senderSocket.send(contentReceived)
            if debug:
                n_transmitted += 1
                if numberPacketsProcessed(n_transmitted, n_dropped, 500): saveInfos()

dropped = []

debug = 0

if debug:
    n_transmitted = 0
    n_dropped = 0
    arquivoSaida = open('forwarder.csv', 'w')

clientSocket = socketStart('veth-ch0')
senderSocket = socketStart('veth-h1')

forwarder = threading.Thread(target=thread_Forwarder, args=())

forwarder.start()