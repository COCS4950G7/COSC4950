__author__ = 'chris hamm'
#NetworkServer_r11
#Created: 2/2/2015



#Designed to work with NetworkClient_r11


from socket import *
import socket
import thread
import platform

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

def sendDoneCommandToClient(self,networkSocket, clientIP, socketLock):
    print "Issuing Done Command to Client: " + str(clientIP) +"\n"
    networkSocket.settimeout(0.5)
    socketLock.acquire()
    while True:
        try:
            networkSocket.sendto("done",clientIP)
            print "sent Done command to client: " +str(clientIP) +"\n"
            self.incrementDoneCommandToClientCounter()
            break
        #except networkSocket.error as inst:
         #   print "Socket has timed out in sendDoneCommandToClient. Attempting to send again.\n"
        except Exception as inst:
            print "Exception in send Done command: " +str(inst) +"\n"
    socketLock.release()

def sendNextCommandToClient(self, networkSocket, clientIP, outboundMessage, socketLock):
    print "Sending Next Command to Client\n"
    networkSocket.settimeout(0.5)
    socketLock.acquire()
    while True:
        try:
            networkSocket.sendto(outboundMessage, clientIP)
            print "sent Next command to client "+str(clientIP)+"\n"
            self.incrementNextCommandToClientCounter()
            break
        except Exception as inst:
            print "Exception in send Next command: " +str(inst) +"\n"
    socketLock.release()


def checkForNextCommandFromClient(inboundData):
    print "Checking for the Next command from the client\n"
    if(compareString(inboundData,"NEXT",0,0,len("NEXT"),len("NEXT"))):
        print "NEXT command was received from the client\n"
        return True
    else:
        return False

def checkForFoundSolutionCommandFromClient(inboundData):
    print "Checking for the Found Solution Command from the client\n"
    if(compareString(inboundData,"FOUNDSOLUTION",0,0,len("FOUNDSOLUTION"),len("FOUNDSOLUTION"))):
        print "FOUNDSOLUTION Command was received from the client\n"
        return True
    else:
        return False

def checkForCrashedCommandFromClient(inboundData):
    print "Checking for the Crashed Command from the Client\n"
    if(compareString(inboundData,"CRASHED",0,0,len("CRASHED"),len("CRASHED"))):
        print "CRASHED Command was received from the client\n"
        return True
    else:
        return False


class NetworkServer():

    #Server command records
    #records of outbound commands to clients
    doneCommandToClientCounter = 0
    nextCommandToClientCounter = 0
    nextDataCommandToClientCounter = 0 #not yet implemented, only incrementor is implemented

    #records of inbound commands from clients
    nextCommandFromClientCounter = 0
    foundSolutionCommandFromClientCounter = 0
    crashedCommandFromClientCounter = 0
    unknownCommandFromClientCounter = 0

    #record of number of threads
    numberOfThreadsCreatedCounter = 0

    def incrementDoneCommandToClientCounter(self):
        self.doneCommandToClientCounter += 1

    def incrementNextCommandToClientCounter(self):
        self.nextCommandToClientCounter += 1

    def incrementNextDataCommandToClientCounter(self):
        self.nextDataCommandToClientCounter+= 1

    def incrementNextCommandFromClientCounter(self):
        self.nextCommandFromClientCounter += 1

    def incrementFoundSolutionCommandFromClientCounter(self):
        self.foundSolutionCommandFromClientCounter += 1

    def incrementUnknownCommandFromClientCounter(self):
        self.unknownCommandFromClientCounter += 1

    def incrementCrashedCommandFromClientCounter(self):
        self.crashedCommandFromClientCounter += 1

    def incrementNumberOfThreadsCreatedCounter(self):
        self.numberOfThreadsCreatedCounter+= 1

    def handler(self, clientsocket, clientaddr, socketLock, nextCommandFromClientCounterLock, foundSolutionCommandFromClientCounterLock, unknownCommandFromClientCounterLock, crashedCommandFromClientCounterLock):
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
                elif(checkForFoundSolutionCommandFromClient(data) == True):
                    foundSolutionCommandFromClientCounterLock.acquire()
                    self.incrementFoundSolutionCommandFromClientCounter()
                    foundSolutionCommandFromClientCounterLock.release()
                elif(checkForCrashedCommandFromClient(data)==True):
                    crashedCommandFromClientCounterLock.acquire()
                    self.incrementCrashedCommandFromClientCounter()
                    crashedCommandFromClientCounterLock.release()
                else:
                    unknownCommandFromClientCounterLock.acquire()
                    self.incrementUnknownCommandFromClientCounter()
                    unknownCommandFromClientCounterLock.release()
                sendData(clientsocket, clientaddr,msg,socketLock)
        clientsocket.close()

    def __init__(self):

        if __name__ == "__main__": #Nick's thoughts, this is designed to access from outside the class ddefinition
                                   #move the vars below into a inititialization function

            #host = 'localhost' #old connection method
            host = '' #New Connection method
            port = 55568
            buf = 1024

            listOfClients = [] #list that holds the IPs of all the clients (in a tuple of socket, then ip)

            #.........................................................................
            #Detect the Operating System
            #.........................................................................
            try: #getOS try block
                print "*************************************"
                print "    Network Server"
                print "*************************************"
                print "OS DETECTION:"
                if(platform.system()=="Windows"): #Detecting Windows
                    print platform.system()
                    print platform.win32_ver()
                elif(platform.system()=="Linux"): #Detecting Linux
                    print platform.system()
                    print platform.dist()
                elif(platform.system()=="Darwin"): #Detecting OSX
                    print platform.system()
                    print platform.mac_ver()
                else:                           #Detecting an OS that is not listed
                    print platform.system()
                    print platform.version()
                    print platform.release()
                print "*************************************"
            except Exception as inst:
                print "========================================================================================"
                print "ERROR: An exception was thrown in getOS try block"
                print type(inst) #the exception instance
                print inst.args #srguments stored in .args
                print inst #_str_ allows args tto be printed directly
                print "========================================================================================"
            #.........................................................................
            #End of Detect the Operating System
            #.........................................................................

            #.........................................................................
            #Retrieve the local network IP Address
            #.........................................................................
            try: #getIP tryblock
                print "STATUS: Getting your network IP adddress"
                if(platform.system()=="Windows"):
                    print socket.gethostbyname(socket.gethostname())
                elif(platform.system()=="Linux"):
                    #Source: http://stackoverflow.com/questions/11735821/python-get-localhost-ip
                    #Claims that this works on linux and windows machines
                    import fcntl
                    import struct
                    import os

                    def get_interface_ip(ifname):
                        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                        return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s',ifname[:15]))[20:24])
                    #end of def
                    def get_lan_ip():
                        ip = socket.gethostbyname(socket.gethostname())
                        if ip.startswith("127.") and os.name != "nt":
                            interfaces = ["eth0","eth1","eth2","wlan0","wlan1","wifi0","ath0","ath1","ppp0"]
                            for ifname in interfaces:
                                try:
                                    ip = get_interface_ip(ifname)
                                    print "IP address was retrieved from the " + str(ifname) + " interface."
                                    break
                                except IOError:
                                    pass
                        return ip
                    #end of def
                    print get_lan_ip()
                elif(platform.system()=="Darwin"):
                    print socket.gethostbyname(socket.gethostname())
                else:
                    #NOTE: MAY REMOVE THIS AND REPLACE WITH THE LINUX DETECTION METHOD
                    print "INFO: The system has detected that you are not running Windows, OS X, or Linux."
                    print "INFO: System is using a generic IP detection method"
                    print socket.gethostbyname(socket.gethostname())
            except Exception as inst:
                print "========================================================================================"
                print "ERROR: An exception was thrown in getIP try block"
                print type(inst) #the exception instance
                print inst.args #srguments stored in .args
                print inst #_str_ allows args tto be printed directly
                print "========================================================================================"
            #.........................................................................
            #End of Retrieve the local network IP Address
            #.........................................................................

            addr = (host, port)

            #serversocket = socket(AF_INET, SOCK_STREAM) #old create socket method
            serversocket = socket.socket(AF_INET, SOCK_STREAM) #new create socket method



            serversocket.bind(addr)

            serversocket.listen(2)
            #the thread locks
            socketLock = thread.allocate_lock()
            nextCommandFromClientCounterLock = thread.allocate_lock()
            foundSolutionCommandFromClientCounterLock = thread.allocate_lock()
            unknownCommandFromClientCounterLock = thread.allocate_lock()
            crashedCommandFromClientCounterLock = thread.allocate_lock()
            try: #Main try block
                while 1:
                    print "Server is listening for connections\n"

                    clientsocket, clientaddr = serversocket.accept()
                    listOfClients.append((clientsocket, clientaddr))
                    thread.start_new_thread(self.handler, (clientsocket, clientaddr, socketLock,nextCommandFromClientCounterLock, foundSolutionCommandFromClientCounterLock, unknownCommandFromClientCounterLock, crashedCommandFromClientCounterLock)) #create a new thread
                    print " A New thread was made\n"
                    self.incrementNumberOfThreadsCreatedCounter()
            except Exception as inst:
                print "ERROR IN MAIN THREAD: " +str(inst) + "\n"
            finally:
                print "# of clients connected: " + str(len(listOfClients)) + "\n"
                print "Issuing Done Commands to clients...\n"
                for i in range(0, len(listOfClients)):
                    doneSock, doneAddr = listOfClients[i]
                    sendDoneCommandToClient(self,doneSock, doneAddr, socketLock)
                serversocket.close()
                print "Socket has been closed\n"
                #printing out all of the records
                print "---------------Number of Threads Created-----------------------\n"
                print "# of Threads Created: " + str(self.numberOfThreadsCreatedCounter) +"\n"
                print "---------------Outbound Commands To Client(s)------------------\n"
                print "# of Done Commands sent to the clients: " + str(self.doneCommandToClientCounter) +"\n"
                print "# of Next Commands sent to the clients: " +str(self.nextCommandToClientCounter) +"\n"
                print "---------------Inbound Commands From Client(s)-----------------\n"
                nextCommandFromClientCounterLock.acquire()
                print "# of Next Commands received from the client: " + str(self.nextCommandFromClientCounter) + "\n"
                nextCommandFromClientCounterLock.release()
                foundSolutionCommandFromClientCounterLock.acquire()
                print "# of FOUNDSOLUTION Commands received from the client: " +str(self.foundSolutionCommandFromClientCounter) +"\n"
                foundSolutionCommandFromClientCounterLock.release()
                unknownCommandFromClientCounterLock.acquire()
                print "# of Unknown Commands received from Client: " + str(self.unknownCommandFromClientCounter) +"\n"
                unknownCommandFromClientCounterLock.release()
                crashedCommandFromClientCounterLock.acquire()
                print "# of Crashed Commands received from client: " + str(self.crashedCommandFromClientCounter) + "\n"
                crashedCommandFromClientCounterLock.release()

NetworkServer()
