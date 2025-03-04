from socket import *
import time
import threading
import random
random.seed(10)

def thread_Traffic(thread_name, interval, msg, probability):
    """Realiza o envio de 1000 pacotes, podendo enviar pacotes infectados"""
    global clientSocket, addr_1, startMessage, middleMsg, endMsg
    n_packet = 0
    while n_packet < 1000:
        number = random.randint(0, 100)
        if number >= probability:
            clientSocket.sendto(msg, addr_1)
        else:
            if (number % 3) == 0:
                clientSocket.sendto(startMessage, addr_1)
            elif (number % 3) == 1:
                clientSocket.sendto(middleMsg, addr_1)
            elif (number % 3) == 2:
                clientSocket.sendto(endMsg, addr_1)
        n_packet += 1
        time.sleep(interval)

message = b'Estou limpo' + (b'.' * 1013)
startMessage = b'Estou infectado'
startMessage += b"." * (1024 - len(startMessage))
middleMsg = b"." * 512
middleMsg += b"Estou infectado" + b"." * (512 - len('Estou infectado'))
endMsg = b"." * (1024-len('Estou infectado'))
endMsg += b"Estou infectado"

addr_1 = ("10.0.1.101", 8001)

clientSocket = socket(family=AF_INET, type=SOCK_DGRAM)
clientSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
clientSocket.bind(('10.2.2.100', 8001))

threadTraffic = threading.Thread(target=thread_Traffic, args=('traffic_sender', 0.04, message, 10))

threadTraffic.start()
