import socket
import threading
import time

tLock = threading.Lock()
shutdown = False

def receiving(name, sock):
    while not shutdown:
        try:
            tLock.acquire()
            while True:
                data, addr = sock.recvfrom(1024)
                print str(data)
        except:
            pass
        finally:
            tLock.release()

host = '192.168.0.204'
port = 0

server = ('192.168.0.229', 5000)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))
s.setblocking(0)

rT = threading.Thread(target=receiving, args=('RecvThread', s))
rT.start()

alias = raw_input('Name: ')
message = raw_input(alias + '-> ')
while message != 'q':
    if message != '':
        s.sendto(alias + ': ' + message, server)
    tLock.acquire()
    message = raw_input(alias + ' -> ')
    tLock.release()
    time.sleep(0.2)

shutdown = True
rT.join()
s.close()
