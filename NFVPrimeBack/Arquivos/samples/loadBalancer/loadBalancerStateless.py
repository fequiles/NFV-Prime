import threading #thread module imported
from socket import *
import struct
import binascii

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

def saveInfo():
    """Funcao que salva as informacoes obtidas pelo algoritmo em um arquivo .csv de saida"""
    global n_dropped, n_transmitted, outputFile, n_dummy1, n_dummy2, n_dummy3

    saida = '{};{};{};{};{}\n'.format(n_transmitted, n_dropped, n_dummy1, n_dummy2, n_dummy3)
    outputFile.write(saida)
    outputFile.close()
    semaphore.release()
    exit()  

def thread_LoadBalancer():
    """Thread do LoadBalancer que ao receber um pacote o desempacota, 
    verificando o destino e realizando posteriormente o envio para a melhor opcao de dummy"""
    global clientSocket, semaphore, debug, n_dropped, n_transmitted, n_dummy1, n_dummy2, n_dummy3, n_packet

    while 1:
        contentReceived = clientSocket.recv(65535)
        mac_destino, mac_fonte, protocolo, carga_util = unpackFrameEthernet(contentReceived)
        ipOrigem, ipDestino, dados = ipPacketData(carga_util)
        if debug: 
            total =  n_transmitted + n_dropped
            if total >= 1000:
                exit()
        if ipDestino == '10.0.1.101':
            print ("ipOrigem {} -> ipDestino {}".format(ipOrigem, ipDestino))
            if (n_packet % 3 == 0):
                senderSocket_h1.send(contentReceived)
                n_dummy1 += 1
            elif (n_packet % 3 == 1):
                senderSocket_h2.send(contentReceived)
                n_dummy2 += 1
            elif (n_packet % 3 == 2):
                senderSocket_h3.send(contentReceived)
                n_dummy3 += 1
            if debug: 
                print("Transmitindo pacote")
                n_transmitted += 1
                total =  n_transmitted + n_dropped
                if total >= 1000:
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
    outputFile = open('/home/felipe/Desktop/testesMestrado/loadBalancerStateless.csv', 'a')

clientSocket = socketStart('veth-ch0')
senderSocket_h1 = socketStart('veth-h1')
senderSocket_h2 = socketStart('veth-h2')
senderSocket_h3 = socketStart('veth-h3')

semaphore = threading.Semaphore(1)
load_balancer = threading.Thread(target=thread_LoadBalancer, args=())

load_balancer.start()