__author__ = 'chris hamm'
#NetworkServer_r11
#Created: 2/2/2015

#NOTE,WHEN ISSUING THE DONE COMMAND,ONLY THE FIRST CLIENT RECV THE MESSAGE, SERVER DOES NOT SEEM TO SEND THE DONE COMMAND TO THE SECOND CLIENT

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
        except Exception as inst:
            print "Exception in send Done command: " +str(inst) +"\n"
    socketLock.release()


class NetworkServer:

    def handler(clientsocket, clientaddr, socketLock):
        print "Accepted connection from: "+ str(clientaddr) +"\n"

        while 1:
            #data = clientsocket.recv(1024) #OLD RECV METHOD
            #if not data:
            #    break
            #else:
            #    if(compareString(data,"me 2",0,0,len("me 2"),len("me 2"))):
            #        print "Received the me 2 command form server\n"
            #    else:
            #        print "Did not receive the me2 command." + str(data)
            print "Checking for input from : " +str(clientaddr) +"\n"
            data = receiveData(clientsocket,socketLock)
            if(data != ""):
                msg = "You sent me: %s" % data + "\n"
                sendData(clientsocket, clientaddr,msg,socketLock)
                #clientsocket.send(msg) #OLD SEND METHOD
        clientsocket.close()



    if __name__ == "__main__":

        host = 'localhost'
        port = 55567
        buf = 1024
        listOfClients = [] #list that holds the IPs of all the clients (in a tuple of socket, then ip)
        addr = (host, port)

        serversocket = socket(AF_INET, SOCK_STREAM)

        serversocket.bind(addr)

        serversocket.listen(2)
        socketLock = thread.allocate_lock()
        try: #Main try block
            while 1:
                print "Server is listening for connections\n"

                clientsocket, clientaddr = serversocket.accept()
                listOfClients.append((clientsocket, clientaddr))
                thread.start_new_thread(handler, (clientsocket, clientaddr, socketLock)) #create a new thread
                print " A New thread was made\n"
        except Exception as inst:
            print "ERROR IN MAIN THREAD: " +str(inst) +"\n"
        finally:
            serversocket.close()
            print "Socket has been closed.\n"
            print "# of clients connected: " + str(len(listOfClients)) +"\n"
            print "Issuing Done Commands to clients..."
            for i in range(0,len(listOfClients)):
                doneSock, doneAddr = listOfClients[i]
                sendDoneCommandToClient(doneSock,doneAddr,socketLock)


