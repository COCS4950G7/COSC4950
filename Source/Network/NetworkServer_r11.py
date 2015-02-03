__author__ = 'chris hamm'
#NetworkServer_r11
#Created: 2/2/2015

'''
import thread
import time
def func1():
    lock.acquire()
    try:
        for i in range(0,3):
            print "inside func1"
            time.sleep(2)
    finally:
        lock.release()
def func2():
    lock.acquire()
    try:
        for i in range(0,3):
            print "inside funct2"
            time.sleep(1)
    finally:
        lock.release()
lock = thread.allocate_lock()#lock mechanism to lock the print function
thread.start_new_thread(func1, ())
thread.start_new_thread(func2, ())
while True:
    testVar= True
'''
#Example 2
'''
import threading
import time
from socket import *

class ThreadingExample(threading.Thread):
    def __init__(self, Id, dt, lock, socket):
        super(ThreadingExample, self).__init__()
        self.id = Id
        self.dt= dt
        self.lock= lock
        self.socket= socket
        self.sentLock= False
    def run(self):
        while True:
            if(self.sentLock == False):
                self.lock.acquire()
                socket.send(self.lock)
                self.lock.release()
            self.lock.acquire()
            #for i in range(0,3):
             #   print ("Inside func %s" % self.id)
              #  time.sleep(self.dt)
            try:
                theInput = self.socket.recv(2048)
                for i in range(0,3):
                    print str(theInput)
            except Exception as inst:
                temp2 = True
                #print "ERROR: in recv " +str(theInput)
            finally:
                self.lock.release()
host= '' #Symbolic name, meaning all available interfaces
port= 49200
import socket
serverSocket = socket.socket(AF_INET,SOCK_STREAM)
serverSocket.bind((host, port))
serverSocket.listen(5)
lock = threading.Lock()
serverSocket.settimeout(1.0)
while True:
    try:
        lock.acquire()
        sock, addr = serverSocket.accept()
        ThreadingExample("1",1,lock, sock)
        print "A new thread was created"
    except Exception as inst:
        #print "ERROR: in accept new client try block " + str(inst)
        temp= True
    finally:
        lock.release()

#t1 = ThreadingExample("1",1,lock)
#t2 = ThreadingExample("2",2,lock)
#t1.start(); t2.start();
'''
from socket import *
import thread

def compareString(inboundStringA, inboundStringB, startA, startB, endA, endB): #This function is now global
        posA = startA
        posB = startB
        #add check here
        if((endA-startA) != (endB-startB)):
            return False
        for x in range(startA,endA):
            tempCharA= inboundStringA[posA]
            tempCharB= inboundStringB[posB]
            if(tempCharA != tempCharB):
                return False
            posA+= 1
            posB+= 1
        return True


class NetworkServer:


    def handler(clientsocket, clientaddr):
        print "Accepted connection from: ", clientaddr

        while 1:
            data = clientsocket.recv(1024)
            if not data:
                break
            else:
                if(compareString(data,"me 2",0,0,len("me 2"),len("me 2"))):
                    print "Received the me 2 command form server\n"
                else:
                    print "Did not receive the me2 command." + str(data)
                msg = "You sent me: %s" % data
                clientsocket.send(msg)
        clientsocket.close()

    if __name__ == "__main__":

        host = 'localhost'
        port = 55567
        buf = 1024

        addr = (host, port)

        serversocket = socket(AF_INET, SOCK_STREAM)

        serversocket.bind(addr)

        serversocket.listen(2)

        while 1:
            print "Server is listening for connections\n"

            clientsocket, clientaddr = serversocket.accept()
            thread.start_new_thread(handler, (clientsocket, clientaddr))
            print " A New thread was made\n"
        serversocket.close()


