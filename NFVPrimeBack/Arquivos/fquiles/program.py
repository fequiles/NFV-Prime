import sys
sys.path.insert(1,'./lib' )
import socket
import threading #thread module imported
from socket import *
import struct
import binascii
import re
import time

destinies = {}

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

def dados_pacote_udp(carga):
    tupla_dados_udp = struct.unpack('! H H H H', carga[:8])
    porta_fonte = tupla_dados_udp[0]
    porta_destino = tupla_dados_udp[1]
    udp_len = tupla_dados_udp[2]
    udp_checksum = tupla_dados_udp[3]
    
    return porta_fonte, porta_destino, udp_len, udp_checksum, carga[8:]

def saveInfos():
    """Funcao que salva as informacoes obtidas pelo algoritmo em um arquivo .csv de saida"""
    global n_dropped, n_transmitted, outputFile, outputFileTimes

    saida = '{};{};\n'.format(n_transmitted, n_dropped)
    outputFile.write(saida)
    outputFile.close()
    outputFileTimes.write('\n')
    outputFileTimes.close()
    semaphore.release()
    exit()  

def thread_DPI():
    """ Thread do LeakyBucket que ao receber um pacote enfileira, 
    transmite ou descarta o pacote, de acordo com seus parametros"""
    global clientSocket, semaphore, debug, n_dropped, n_transmitted, n_packet, outputFileTimes

    while 1:
        contentReceived = clientSocket.recv(65535)
        mac_destino, mac_fonte, protocolo, carga_util = unpackFrameEthernet(contentReceived)
        ipOrigem, ipDestino, dados = ipPacketData(carga_util)
        porta_fonte, porta_destino, udp_len, udp_checksum, carga = dados_pacote_udp(dados)
        if debug: 
            total =  n_transmitted + n_dropped
            if total >= 1000:
                exit()
        if '10.0.1.101' in ipDestino:
            stime = time.time()
            patternFind = re.search(".*Estou infectado.*", carga.decode("utf-8"))
            if (not patternFind):
                senderSocket_h1.send(contentReceived)
                if debug:
                    print("Transmitindo pacote")
                    n_transmitted += 1
                    etime = time.time()
                    saida = '{};'.format(etime - stime)
                    outputFileTimes.write(saida)
                    total =  n_transmitted + n_dropped
                    if total >= 1000:
                        saveInfos()
            else:
                if debug:
                    print("Pacote infectado, descartando")
                    etime = time.time()
                    saida = '{};'.format(etime - stime)
                    outputFileTimes.write(saida)
                    n_dropped += 1
                    total =  n_transmitted + n_dropped
                    if total >= 1000:
                        saveInfos()
            n_packet += 1
        semaphore.release()

interval = 1
debug = 1
n_packet = 0

if debug:
    n_transmitted = 0
    n_dropped = 0
    outputFile = open('./Arquivos/dpi.csv', 'a')
    outputFileTimes = open('./Arquivos/dpiTimes.csv', 'a')

clientSocket = socketStart('veth-ch0')
senderSocket_h1 = socketStart('veth-h1')

semaphore = threading.Semaphore(1)
dpi = threading.Thread(target=thread_DPI, args=())

dpi.start()

