from socket import *
import time
import threading

def thread_Guepard(thread_name, interval):
    """Realiza o envio de 1000 pacotes do trafego guepardo"""
    global guepardMsg, clientSocket, addr_1
    n_packet = 0
    while n_packet < 1000: 
        clientSocket.sendto(guepardMsg, addr_1)
        n_packet += 1
        time.sleep(interval)

def thread_Elephant(thread_name, interval):
    """Realiza o envio de 1000 pacotes do trafego elefante"""
    global elephantMsg, clientSocket, addr_2
    n_packet = 0
    while n_packet < 1000: 
        clientSocket.sendto(elephantMsg, addr_2)
        n_packet += 1
        time.sleep(interval)

def thread_Middle(thread_name, interval, msg):
    """Realiza o envio de 1000 pacotes do trafego middle"""
    global middleMsg, clientSocket, addr_3
    n_packet = 0
    while n_packet < 1000: 
        clientSocket.sendto(msg, addr_3)
        n_packet += 1
        time.sleep(interval)

guepardMsg = b'Eu sou o guepardo'
guepardMsg += b"." * (16 - len(guepardMsg))
elephantMsg = b'Eu sou o elefante'
elephantMsg += b"." * (1024 - len(elephantMsg))
middleMsg = b'Eu sou o middle'
middleMsg += b"." * (256 - len(middleMsg))

addr_1 = ("10.0.1.104", 8001)
addr_2 = ("10.0.1.104", 8002)
addr_3 = ("10.0.1.104", 8003)

clientSocket = socket(family=AF_INET, type=SOCK_DGRAM)
clientSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
clientSocket.bind(('10.2.2.100', 8001))

threadGuepard = threading.Thread(target=thread_Guepard, args=('guepard', 0.01))
threadElephant = threading.Thread(target=thread_Elephant, args=('elephant', 0.04))
threadMiddle = threading.Thread(target=thread_Middle, args=('middle', 0.0166, middleMsg))

threadGuepard.start()
threadElephant.start()
threadMiddle.start()