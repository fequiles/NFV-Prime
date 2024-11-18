from socket import *
import time
import threading

def thread_Traffic(thread_name, interval, msg):
    """Realiza o envio de 1000 pacotes do trafego"""
    global clientSocket, addr_1
    n_packet = 0
    while n_packet < 1000: 
        clientSocket.sendto(msg, addr_1)
        n_packet += 1
        time.sleep(interval)

startMessage = b'Estou infectado'
startMessage += b"." * (1024 - len(startMessage))
middleMsg = b"." * 512
middleMsg += b"Estou infectado" + (b"." * (1024 - len('Estou infectado') - 512))
endMsg = b"." * 1009
endMsg += b"Estou infectado"

addr_1 = ("10.0.1.101", 8001)

clientSocket = socket(family=AF_INET, type=SOCK_DGRAM)
clientSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
clientSocket.bind(('10.2.2.100', 8001))

threadTraffic = threading.Thread(target=thread_Traffic, args=('traffic_sender', 0.04, middleMsg))

threadTraffic.start()
