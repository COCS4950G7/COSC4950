__author__ = 'chris hamm'
#NetworkServer_r11
#Created: 2/2/2015

#NOTE,WHEN ISSUING THE DONE COMMAND,ONLY THE FIRST CLIENT RECV THE MESSAGE, SERVER DOES NOT SEEM TO SEND THE DONE COMMAND TO THE SECOND CLIENT

#CRITICAL ERROR, CANT PASS SELF TO THE HANDLER


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

def receiveData(networkSocket, socketLock):
        print "Checking for inbound network data\n"
        networkSocket.settimeout(0.5)
        data = ""
        socketLock.acquire()
        while True:
            try:
                data = networkSocket.recv(1024)
                if not data:
                    break
                else:
                    print "received data: " + str(data) +"\n"
            #except networkSocket.timeout as inst:
             #   print "Socket has timed out in receiveData.\n"
            except Exception as inst:
                print "Exception in receive data: " + str(inst) +"\n"
                break
        socketLock.release()
        return data #if data is empty string, nothing was received

def sendData(networkSocket, clientIP, outboundMessage, socketLock):
    print "Sending message to Client: " +str(clientIP) +"\n"
    networkSocket.settimeout(0.5)
    socketLock.acquire()
    while True:
        try:
            networkSocket.sendto(outboundMessage, clientIP)
            print "sent data: " +str(outboundMessage) + " to client: " +str(clientIP) +"\n"
            break
        #except networkSocket.timeout as inst:
         #   print "Socket has timed out in sendData. Attempting to send again.\n"
        except Exception as inst:
            print "Exception in send data: " +str(inst) +"\n"
    socketLock.release()

def sendDoneCommandToClient(networkSocket, clientIP, socketLock):
    print "Issuing Done Command to Client: " + str(clientIP) +"\n"
    networkSocket.settimeout(0.5)
    socketLock.acquire()
    while True:
        try:
            networkSocket.sendto("done",clientIP)
            print "sent Done command to client: " +str(clientIP) +"\n"
            break
        #except networkSocket.error as inst:
         #   print "Socket has timed out in sendDoneCommandToClient. Attempting to send again.\n"
        except Exception as inst:
            print "Exception in send Done command: " +str(inst) +"\n"
    socketLock.release()



def checkForNextCommandFromClient(inboundData):
    print "Checking for the Next command from the client\n"
    if(compareString(inboundData,"NEXT",0,0,len("NEXT"),len("NEXT"))):
        print "NEXT command was received from the client\n"
        return True
    else:
        return False





class NetworkServer():

    nextCommandFromClientCounter = 0

    def incrementNextCommandFromClientCounter(self):
        self.nextCommandFromClientCounter += 1

    def handler(self, clientsocket, clientaddr, socketLock, nextCommandFromClientCounterLock):
        print "Accepted connection from: " + str(clientaddr) + "\n"

        while 1:
            #data = clientsocket.recv(1024) #OLD RECV METHOD
            #if not data:
            #    break
            #else:
            #    if(compareString(data,"me 2",0,0,len("me 2"),len("me 2"))):
            #        print "Received the me 2 command form server\n"
            #    else:
            #        print "Did not receive the me2 command." + str(data)
            print "Checking for input from : " + str(clientaddr) + "\n"
            data = receiveData(clientsocket , socketLock)
            if(data != ""):
                msg = "You sent me: %s" % data + "\n"
                if(checkForNextCommandFromClient(data) == True):
                    nextCommandFromClientCounterLock.acquire()
                    self.incrementNextCommandFromClientCounter()
                    nextCommandFromClientCounterLock.release()
                sendData(clientsocket, clientaddr,msg,socketLock)
                #clientsocket.send(msg) #OLD SEND METHOD
        clientsocket.close()

    def __init__(self):

        if __name__ == "__main__": #Nick's thoughts, this is designed to access from outside the class ddefinition
                                   #move the vars below into a inititialization function

            host = 'localhost'
            port = 55568
            buf = 1024

            listOfClients = [] #list that holds the IPs of all the clients (in a tuple of socket, then ip)
            addr = (host, port)

            serversocket = socket(AF_INET, SOCK_STREAM)

            serversocket.bind(addr)

            serversocket.listen(2)
            socketLock = thread.allocate_lock()
            nextCommandFromClientCounterLock = thread.allocate_lock()
            try: #Main try block
                while 1:
                    print "Server is listening for connections\n"

                    clientsocket, clientaddr = serversocket.accept()
                    listOfClients.append((clientsocket, clientaddr))
                    thread.start_new_thread(self.handler, (clientsocket, clientaddr, socketLock,nextCommandFromClientCounterLock,)) #create a new thread
                    print " A New thread was made\n"
            except Exception as inst:
                print "ERROR IN MAIN THREAD: " +str(inst) + "\n"
            finally:
                #serversocket.close() #MOVED BELOW
                #print "Socket has been closed.\n"
                print "# of clients connected: " + str(len(listOfClients)) + "\n"
                print "Issuing Done Commands to clients...\n"
                for i in range(0, len(listOfClients)):
                    doneSock, doneAddr = listOfClients[i]
                    sendDoneCommandToClient(doneSock, doneAddr, socketLock)
                serversocket.close()
                print "Socket has been closed\n"
                nextCommandFromClientCounterLock.acquire()
                print "# of Next Commands received from the client: " + str(self.nextCommandFromClientCounter) + "\n"
                nextCommandFromClientCounterLock.release()

NetworkServer()
