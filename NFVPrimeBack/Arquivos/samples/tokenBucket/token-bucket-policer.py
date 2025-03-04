import threading #thread module imported
import time #time module
import socket

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
    semaphore.release()
    exit() 

def thread_Time(thread_name, interval):
    """ Thread que adiciona tokens aos buckets a cada intervalo de tempo
        interval -> intervalo de tempo para que sejam adicionados os tokens"""
    global semaphore, rate, bucket_size, bucket_max_size
    while 1:
        semaphore.acquire()
        bucket_size =  bucket_size + rate if bucket_size + rate <= bucket_max_size else bucket_max_size
        if debug:
            if numberPacketsProcessed(n_transmitted, n_dropped, 500): exit()
        semaphore.release()
        time.sleep(interval)

def thread_TokenBucket():
    """ Thread do TokenBucketPolicer que ao receber um pacote, decidindo se envia ou descarta o pacote de acordo com seus parametros"""
    global clientSocket, bucket_size, semaphore, bucket_max_size, dropped, debug, n_transmitted, n_dropped
    while 1:
        contentReceived, client = clientSocket.recvfrom(65535)
        packet_size = len(contentReceived) + header
        semaphore.acquire()
        if bucket_size < packet_size:
            dropped.append(contentReceived)
            if debug: 
                print("Mensagem dropada")
                n_dropped += 1
                if numberPacketsProcessed(n_transmitted, n_dropped, 500): saveInfos()
        else:
            if debug: 
                print("Transmitindo pacote")
                n_transmitted += 1
                if numberPacketsProcessed(n_transmitted, n_dropped, 500): saveInfos()
            clientSocket.sendto(contentReceived, (server_interface, 7000))
            bucket_size -= packet_size
        semaphore.release()

dropped = []
header = 42

rate = 174
bucket_size = 358
bucket_max_size = 400
interval = 1
client_interface = :dummy_2_1
server_interface = :dummy_2_2
debug = 1

if debug:
    n_transmitted = 0
    n_dropped = 0
    arquivoSaida = open('tokenBucketPolicer-{}-{}.csv'.format(rate, bucket_max_size), 'w')

clientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
clientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
clientSocket.bind((client_interface, 8001))

semaphore = threading.Semaphore(1)
timer = threading.Thread(target=thread_Time, args=('timer', interval))
token_bucket = threading.Thread(target=thread_TokenBucket, args=())

timer.start()
token_bucket.start()
