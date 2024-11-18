import threading #thread module imported
import time #time module
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

def analyzeBucket():
    """Funcao que analisa o bucket, obtendo a quantidade de pacotes de cada tipo presente"""
    global bucket, outputFileBucket
    
    b_guepard = 0
    b_elephant = 0
    b_middle = 0
    for packet in bucket:
        if packet[1] <= 100:
            b_guepard += 1
        elif packet[1] >= 1000:
            b_elephant += 1
        elif packet[1] > 100 and packet[1] < 1000:
            b_middle += 1
    saida = '{};{};{};\n'.format(b_guepard, b_elephant, b_middle)
    outputFileBucket.write(saida)

def consumeBucket():
    """Funcao que consome o bucket de acordo com a quantidade de pacotes que sao consumidos a cada intervao de tempo"""
    global bucket, packets_to_release, clientSocket, debug, n_transmitted, n_guepard, n_elephant, n_middle
    if (len(bucket) == 0):
        return
    while (len(bucket) > 0) and (packets_to_release > 0):
        semaphore.acquire()
        contentReceived = bucket.pop(0)
        senderSocket_h1.send(contentReceived[0])
        print(contentReceived)
        if debug: 
            print("Transmitindo pacote")
            if contentReceived[1] <= 100:
                n_guepard += 1
            elif contentReceived[1] >= 1000:
                n_elephant += 1
            elif contentReceived[1] > 100 and contentReceived[1] < 1000:
                n_middle += 1
            n_transmitted += 1
            total =  n_transmitted + n_dropped
            if total >= 3000:
                saveInfos()
        packets_to_release -= 1
        semaphore.release()
        

def thread_Time(thread_name, interval):
    """ Thread que reseta o consumo do bucket a cada intervalo de tempo
        interval -> intervalo de tempo para que sejam adicionados os tokens"""
    global semaphore, packets_to_release, packets_to_release_value
    while 1: #Ver condicao do while
        semaphore.acquire()
        packets_to_release = packets_to_release_value
        semaphore.release()
        analyzeBucket()
        consumeBucket()
        if debug: 
            total =  n_transmitted + n_dropped
            if total >= 3000:
                exit()
        
        time.sleep(interval)

def saveInfos():
    """Funcao que salva as informacoes obtidas pelo algoritmo em um arquivo .csv de saida"""
    global n_dropped, n_transmitted, outputFile, n_guepard, n_elephant, n_middle

    saida = '{};{};{};{};{};\n'.format(n_transmitted, n_dropped, n_guepard, n_elephant, n_middle)
    outputFile.write(saida)
    outputFile.close()
    outputFileBucket.close()
    semaphore.release()
    exit()  

def thread_LeakyBucket():
    """ Thread do LeakyBucket que ao receber um pacote enfileira, 
    transmite ou descarta o pacote, de acordo com seus parametros"""
    global clientSocket, packets_to_release, bucket, semaphore, bucket_max_size, debug, n_dropped, n_transmitted, n_guepard, n_elephant, n_middle

    while 1:
        contentReceived = clientSocket.recv(65535)
        mac_destino, mac_fonte, protocolo, carga_util = unpackFrameEthernet(contentReceived)
        ipOrigem, ipDestino, dados = ipPacketData(carga_util)
        if debug: 
            total =  n_transmitted + n_dropped
            if total >= 3000:
                exit()
        if len(bucket) > 0:
            semaphore.acquire()
            if len(bucket) < bucket_max_size:
                if ipDestino == '10.0.1.101':
                    if debug: 
                        print("Adicionou na fila e bucket nao vazio")
                    bucket.append([contentReceived, len(dados)])
            else:
                if debug: 
                    print("Mensagem dropada")
                    n_dropped += 1
                    total =  n_transmitted + n_dropped
                    if total >= 3000:
                        saveInfos()
        else:
            semaphore.acquire()
            if packets_to_release > 0:
                if ipDestino == '10.0.1.101':
                    print ("ipOrigem {} -> ipDestino {}".format(ipOrigem, ipDestino))
                    senderSocket_h1.send(contentReceived)
                    if debug: 
                        print("Transmitindo pacote")
                        if len(dados) <= 100:
                            n_guepard += 1
                        elif len(dados) >= 1000:
                            n_elephant += 1
                        elif len(dados) > 100 and len(dados) < 1000:
                            n_middle += 1
                        
                        n_transmitted += 1
                        total =  n_transmitted + n_dropped
                        if total >= 3000:
                            saveInfos()
                    packets_to_release -= 1
            else:
                if ipDestino == '10.0.1.101':
                    if debug: 
                        print("Adicionou na fila e bucket vazio")
                    bucket.append([contentReceived, len(dados)])
        semaphore.release()

bucket = []

packets_to_release = 50
bucket_max_size = 100
interval = 1
debug = 1

packets_to_release_value = packets_to_release

if debug:
    n_transmitted = 0
    n_dropped = 0
    n_guepard= 0
    n_elephant= 0
    n_middle = 0
    outputFile = open('/home/felipe/Desktop/testesMestrado/leakybucket-{}.csv'.format(packets_to_release_value), 'w')
    outputFileBucket = open('/home/felipe/Desktop/testesMestrado/leakybucket-{}-bucket.csv'.format(packets_to_release_value), 'w')

clientSocket = socketStart('veth-ch0')
senderSocket_h1 = socketStart('veth-h1')

semaphore = threading.Semaphore(1)
timer = threading.Thread(target=thread_Time, args=('timer', interval))
leaky_bucket = threading.Thread(target=thread_LeakyBucket, args=())

timer.start()
leaky_bucket.start()

