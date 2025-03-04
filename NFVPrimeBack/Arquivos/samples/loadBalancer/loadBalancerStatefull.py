import threading #thread module imported
from socket import *
import struct
import binascii
import time

destinies = {}

def unpackFrameEthernet(frame):
    """Desempacota os dados Ethernet do frame"""
    destiny, origin, protocol = struct.unpack('! 6s 6s H', frame[:14])
    return bytesToHexa(destiny), bytesToHexa(origin), htons(protocol), frame[14:]

def bytesToHexa(bytes_address):
    """Transforma bytes to hexadecimal"""
    hex_list = []
    address = binascii.hexlify(bytes_address).decode("ascii")
    for i in range(0,12,2):
        hex_list.append(address[i:i+2])
    mac = ":".join(hex_list)
    return mac

def socketStart(net_interface):
    """Inicializa o socket de rede em modo RAW na interface desejada"""
    Socket = socket(AF_PACKET, SOCK_RAW, htons(3))
    Socket.bind((net_interface, 0))
    return Socket

def ipPacketData(data):
    """Desempacota os dados IP recebidos"""
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
    """Desempacota os dados UDP recebidos"""
    tupla_dados_udp = struct.unpack('! H H H H', carga[:8])
    porta_fonte = tupla_dados_udp[0]
    porta_destino = tupla_dados_udp[1]
    udp_len = tupla_dados_udp[2]
    udp_checksum = tupla_dados_udp[3]
    
    return porta_fonte, porta_destino, udp_len, udp_checksum, carga[8:]

def saveInfo():
    """Funcao que salva as informacoes obtidas pelo algoritmo em um arquivo .csv de saida"""
    global n_dropped, n_transmitted, outputFile, outputFileBucket, n_dummy1, n_dummy2, n_dummy3

    saida = '{};{};{};{};{}\n'.format(n_transmitted, n_dropped, n_dummy1, n_dummy2, n_dummy3)
    outputFile.write(saida)
    outputFileBucket.write('{};{};{};Finish;\n'.format(b_dummy1, b_dummy2, b_dummy3))
    outputFile.close()
    semaphore.release()
    outputFileBucket.close()
    exit()  

def thread_Time(thread_name, interval):
    """ Thread que analisa a quantidade de bytes recebidos pelas dummies 
    a cada intervalo de tempo"""
    global semaphore, b_dummy1, b_dummy2, b_dummy3, n_transmitted, n_dropped, outputFileBucket
    
    while 1: #Ver condicao do while
        # semaphore.acquire()
        saida = '{};{};{};\n'.format(b_dummy1, b_dummy2, b_dummy3)
        outputFileBucket.write(saida)
        b_dummy1 = 0
        b_dummy2 = 0
        b_dummy3 = 0
        # semaphore.release()
        time.sleep(interval)

def thread_LoadBalancer():
    """Thread do LoadBalancer que ao receber um pacote o desempacota, 
    verificando o destino e realizando posteriormente o envio para a melhor opcao de dummy"""
    global clientSocket, semaphore, debug, n_dropped, n_transmitted, n_dummy1, n_dummy2, n_dummy3, n_packet, b_dummy1, b_dummy2, b_dummy3

    n_traffics = 0
    while 1:
        contentReceived = clientSocket.recv(65535)
        mac_destino, mac_fonte, protocolo, carga_util = unpackFrameEthernet(contentReceived)
        ipOrigem, ipDestino, dados = ipPacketData(carga_util)
        porta_fonte, porta_destino, udp_len, udp_checksum, carga = dados_pacote_udp(dados)
        if debug: 
            total =  n_transmitted + n_dropped
            if total >= 3750:
                exit()
        if '10.0.1.' in ipDestino:
            semaphore.acquire()
            packetSize = len(carga)
            print ("ipOrigem {} -> ipDestino {}".format(ipOrigem, ipDestino))
            ip_destiny_port = '{}_{}_{}'.format(ipDestino, porta_destino, porta_fonte)
            if(destinies.get(ip_destiny_port)):
                destinies[ip_destiny_port]['socket'].send(contentReceived)
                if (destinies[ip_destiny_port]['socket'] == senderSocket_h1):
                    n_dummy1 += 1
                    b_dummy1 += packetSize
                elif (destinies[ip_destiny_port]['socket'] == senderSocket_h2):
                    n_dummy2 += 1
                    b_dummy2 += packetSize
                elif (destinies[ip_destiny_port]['socket'] == senderSocket_h3):
                    n_dummy3 += 1
                    b_dummy3 += packetSize
            else:
                if (n_traffics % 3 == 0):
                    senderSocket_h1.send(contentReceived)
                    destiny = {ip_destiny_port: {'socket': senderSocket_h1}}
                    destinies.update(destiny)
                    n_dummy1 += 1
                    b_dummy1 += packetSize
                elif (n_traffics % 3 == 1):
                    senderSocket_h2.send(contentReceived)
                    destiny = {ip_destiny_port: {'socket': senderSocket_h2 }}
                    destinies.update(destiny)
                    n_dummy2 += 1
                    b_dummy2 += packetSize
                elif (n_traffics % 3 == 2):
                    senderSocket_h3.send(contentReceived)
                    destiny = {ip_destiny_port: {'socket': senderSocket_h3}}
                    destinies.update(destiny)
                    n_dummy3 += 1
                    b_dummy3 += packetSize
                n_traffics += 1
            if debug:
                print("Transmitindo pacote")
                n_transmitted += 1
                total =  n_transmitted + n_dropped
                if total >= 3750:
                    saveInfo()
            n_packet += 1
        semaphore.release()

interval = 1
debug = 1
n_packet = 0

if debug:
    n_transmitted = 0
    n_dropped = 0
    n_dummy1= 0
    n_dummy2= 0
    n_dummy3 = 0
    b_dummy1= 0
    b_dummy2= 0
    b_dummy3 = 0
    outputFile = open('/home/felipe/Desktop/testesMestrado/loadBalancerStatefull.csv', 'a')
    outputFileBucket = open('/home/felipe/Desktop/testesMestrado/loadBalancerStatefullList.csv', 'a')
    timer = threading.Thread(target=thread_Time, args=('timer', interval))
    timer.start()

clientSocket = socketStart('veth-ch0')
senderSocket_h1 = socketStart('veth-h1')
senderSocket_h2 = socketStart('veth-h2')
senderSocket_h3 = socketStart('veth-h3')

semaphore = threading.Semaphore(1)
load_balancer = threading.Thread(target=thread_LoadBalancer, args=())

load_balancer.start()

