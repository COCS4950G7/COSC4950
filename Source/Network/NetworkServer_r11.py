__author__ = 'chris hamm'
#NetworkServer_r11
#Created: 2/2/2015

#Now needs to be run through controller

#Designed to work with NetworkClient_r11

#NOTE FOR OPTIMIZATION, CALL THE THREAD LOCKS THROUGH SELF INSTEAD OF THROUGH AN ADDITIONAL PARAMETER

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
            self.doneCommandToClientCounterLock.acquire()
            self.incrementDoneCommandToClientCounter()
            self.doneCommandToClientCounterLock.release()
            break
        #except networkSocket.error as inst:
         #   print "Socket has timed out in sendDoneCommandToClient. Attempting to send again.\n"
        except Exception as inst:
            if(compareString(str(inst),"[Errno 32] Broken pipe",0,0,len("[Errno 32] Broken pipe"),len("[Errno 32] Broken pipe"))):
                print "Broken pipe error detected in sendData\n"
            else:
                print "Exception in send Done command: " +str(inst) +"\n"
    socketLock.release()

def sendNextCommandToClient(self, networkSocket, clientIP, outboundMessage, socketLock):
    print "Sending Next Command to Client\n"
    networkSocket.settimeout(0.5)
    socketLock.acquire()
    while True:
        try:
            networkSocket.sendto(outboundMessage, clientIP)
            print "sent Next command to client: "+str(clientIP)+"\n"
            self.nextCommandToClientCounterLock.acquire()
            self.incrementNextCommandToClientCounter()
            self.nextCommandToClientCounterLock.release()
            break
        except Exception as inst:
            print "Exception in send Next command: " +str(inst) +"\n"
    socketLock.release()

def sendNextDataCommandToClient(self, networkSocket, clientIP, outboundMessage, socketLock):
    print "Sending Next Data Command to Client\n"
    networkSocket.settimeout(0.5)
    socketLock.acquire()
    while True:
        try:
            networkSocket.sendto(outboundMessage,clientIP)
            print "sent next data command to client: "+str(clientIP)+"\n"
            self.nextDataCommandToClientCounter.acquire()
            self.incrementNextDataCommandToClientCounter()
            self.nextDataCommandToClientCounter.release()
            break
        except Exception as inst:
            print "Exception in send next Data Command to Client: " +str(inst)+"\n"
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

def sendNextChunkCommandToController(self):
    try:
        print "Sending nextChunk Command to the Controller\n"
        self.pipe.send("nextChunk")
        self.nextChunkCommandToControllerCounterLock.acquire()
        self.incrementNextChunkCommandToControllerCounter()
        self.nextChunkCommandToControllerCounterLock.release()
    except Exception as inst:
        print "Exception was thrown in sendNextChunkCommandToController: " +str(inst)+"\n"

def sendWaitingCommandToController(self):
    try:
        print "Sending waiting Command to the Controller\n"
        self.pipe.send("waiting")
        self.waitingCommandToControllerCounterLock.acquire()
        self.incrementWaitingCommandToControllerCounter()
        self.waitingCommandToControllerCounterLock.release()
    except Exception as inst:
        print "Exception was thrown in sendWaitingCommandToController: " +str(inst)+"\n"

def sendDoneCommandToController(self):
    try:
        print "Sending done Command to the Controller\n"
        self.pipe.send("done ")
        self.doneCommandToControllerCounterLock.acquire()
        self.incrementDoneCommandToControllerCounter()
        self.doneCommandToControllerCounterLock.release()
    except Exception as inst:
        print "Exception was thrown in sendDoneCommandToController: "+str(inst)+"\n"

def checkForNextChunkCommandFromController(self, inboundString):
    try:
        print "Checking for nextChunk Command from the Controller\n"
        if(compareString(inboundString, "nextChunk",0,0,len("nextChunk"),len("nextChunk"))==True):
            print "nextChunk Command was received from the Controller\n"
            self.nextChunkCommandFromControllerCounterLock.acquire()
            self.incrementNextChunkCommandFromControllerCounter()
            self.nextChunkCommandFromControllerCounterLock.release()
            return True
        else:
            return False
    except Exception as inst:
        print "Exception thrown in checkForNextChunkCommandFromController: " +str(inst)+"\n"
        return False

def checkForDoneCommandFromController(self, inboundString):
    try:
        print "Checking for done Command from the Controller\n"
        if(compareString(inboundString,"done",0,0,len("done"),len("done"))==True):
            print "done Command was received from the Controller\n"
            self.doneCommandFromControllerCounterLock.acquire()
            self.incrementDoneCommandFromControllerCounter()
            self.doneCommandFromControllerCounterLock.release()
            return True
        else:
            return False
    except Exception as inst:
        print "Exception thrown in checkForDoneCommandFromController: "+str(inst)+"\n"
        return False

class NetworkServer():

    #Server command records
    #records of outbound commands to clients
    doneCommandToClientCounter = 0
    nextCommandToClientCounter = 0
    nextDataCommandToClientCounter = 0 #needs the details of the chunk parsing to be added

    #records of inbound commands from clients
    nextCommandFromClientCounter = 0
    foundSolutionCommandFromClientCounter = 0
    crashedCommandFromClientCounter = 0
    unknownCommandFromClientCounter = 0

    #records of outbound commands to controller
    nextChunkCommandToControllerCounter = 0
    #ChunkAgain command is obsolete
    waitingCommandToControllerCounter = 0
    doneCommandToControllerCounter = 0

    #records of inbound commands from controller
    nextChunkCommandFromControllerCounter = 0
    #chunkAgain command is obsolete
    doneCommandFromControllerCounter = 0
    unknownCommandFromControllerCounter = 0

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

    def incrementNextChunkCommandToControllerCounter(self):
        self.nextChunkCommandToControllerCounter+= 1

    def incrementWaitingCommandToControllerCounter(self):
        self.waitingCommandToControllerCounter+= 1

    def incrementDoneCommandToControllerCounter(self):
        self.doneCommandToControllerCounter+= 1

    def incrementNextChunkCommandFromControllerCounter(self):
        self.nextChunkCommandFromControllerCounter+= 1

    def incrementDoneCommandFromControllerCounter(self):
        self.doneCommandFromControllerCounter+= 1

    def incrementUnknownCommandFromControllerCounter(self):
        self.unknownCommandFromControllerCounter+= 1

    def incrementNumberOfThreadsCreatedCounter(self):
        self.numberOfThreadsCreatedCounter+= 1

    def handler(self, clientsocket, clientaddr, socketLock, nextCommandFromClientCounterLock, foundSolutionCommandFromClientCounterLock, unknownCommandFromClientCounterLock, crashedCommandFromClientCounterLock):
        print "Accepted connection from: " + str(clientaddr) + "\n"

        while 1:
            #CHECKING FOR CLIENT INPUT
            print "Checking for input from : " + str(clientaddr) + "\n"
            data = receiveData(clientsocket , socketLock)
            if(data != ""):
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
                sendData(clientsocket, clientaddr, data, socketLock)
            #CHECKING FOR CONTROLLER INPUT
            print "Checking for input from the Controller\n"
            if(self.pipe.poll()):
                inboundControllerCommand= self.pipe.recv()
                print "Received a message from the Controller\n"
                if(checkForNextChunkCommandFromController(inboundControllerCommand)==True):
                    print "Waiting for corresponding chunk object...\n"
                    inboundControllerChunkObject = self.pipe.recv()
                    print "Received the chunk object\n"
                    #Insert chunk handling here
                elif(checkForDoneCommandFromController(inboundControllerCommand)==True):
                    print "check for done command from controller Function is Incomplete\n"
                else:
                    print "ERROR: Received unknown command from the Controller: '" +str(inboundControllerCommand)+"'\n"
                    self.unknownCommandFromControllerCounterLock.acquire()
                    self.incrementUnknownCommandFromControllerCounter()
                    self.unknownCommandFromControllerCounterLock.release()
        clientsocket.close()

    def __init__(self, pipeendconnectedtocontroller):
        self.pipe= pipeendconnectedtocontroller
        #print "Debugging line 1, before the if main\n"
        #if __name__ == "__main__": #Nick's thoughts, this is designed to access from outside the class ddefinition
                                   #move the vars below into a inititialization function
        #INDENT EVERYTHING AFTER THIS POINT IF YOU ARE GOING TO UNCOMMENT 'IF name == main
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
        #print "Creating the socket...\n"
        serversocket = socket.socket(AF_INET, SOCK_STREAM) #new create socket method
        #print "Successfully created the socket\n"

        #print "Binding the socket...\n"
        serversocket.bind(addr)
        #print "Successfully bound to the socket\n"

        serversocket.listen(2)
        #print "Initializing thread locks...\n"
        #the thread locks
        socketLock = thread.allocate_lock()
        #outbound to client command locks
        doneCommandToClientCounterLock = thread.allocate_lock()
        nextCommandToClientCounterLock = thread.allocate_lock()
        nextDataCommandToClientCounterLock = thread.allocate_lock()
        #inbound from client client command locks
        nextCommandFromClientCounterLock = thread.allocate_lock()
        foundSolutionCommandFromClientCounterLock = thread.allocate_lock()
        unknownCommandFromClientCounterLock = thread.allocate_lock()
        crashedCommandFromClientCounterLock = thread.allocate_lock()
        #outbound to controller command locks
        nextChunkCommandToControllerCounterLock = thread.allocate_lock()
        waitingCommandToControllerCounterLock = thread.allocate_lock()
        doneCommandToControllerCounterLock = thread.allocate_lock()
        #inbound from controller command locks
        nextChunkCommandFromControllerCounterLock = thread.allocate_lock()
        doneCommandFromControllerCounterLock = thread.allocate_lock()
        unknownCommandFromControllerCounterLock = thread.allocate_lock()
        #print "Successfully initialized the thread locks\n"
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
            doneCommandToClientCounterLock.acquire()
            print "# of Done Commands sent to the clients: " + str(self.doneCommandToClientCounter) +"\n"
            doneCommandToClientCounterLock.release()
            nextCommandToClientCounterLock.acquire()
            print "# of Next Commands sent to the clients: " +str(self.nextCommandToClientCounter) +"\n"
            nextCommandToClientCounterLock.release()
            nextDataCommandToClientCounterLock.acquire()
            print "# of Next Data Commands sent to the clients: " +str(self.nextDataCommandToClientCounter) + "\n"
            nextDataCommandToClientCounterLock.release()
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
            print "--------------Outbound Commands To Controller----------------\n"
            nextChunkCommandToControllerCounterLock.acquire()
            print "# of nextChunk Commands sent to the Controller: " +str(self.nextChunkCommandToControllerCounter)+"\n"
            nextChunkCommandToControllerCounterLock.release()
            waitingCommandToControllerCounterLock.acquire()
            print "# of waiting Commands sent to the Controller: " + str(self.waitingCommandToControllerCounter)+"\n"
            waitingCommandToControllerCounterLock.release()
            doneCommandToControllerCounterLock.acquire()
            print "# of done Commands sent to the Controller: " + str(self.doneCommandToControllerCounter)+"\n"
            doneCommandToControllerCounterLock.release()
            print "-------------Inbound Commands From Controller---------------\n"
            nextChunkCommandFromControllerCounterLock.acquire()
            print "# of nextChunk Commands received from the Controller: "+ str(self.nextChunkCommandFromControllerCounter)+"\n"
            nextChunkCommandFromControllerCounterLock.release()
            doneCommandFromControllerCounterLock.acquire()
            print "# of done Commands received from the Controller: " +str(self.doneCommandFromControllerCounter)+"\n"
            doneCommandFromControllerCounterLock.release()
            unknownCommandFromControllerCounterLock.acquire()
            print "# of unknown Commands received from the Controller: "+str(self.unknownCommandFromControllerCounter)+"\n"
            unknownCommandFromControllerCounterLock.release()


#NetworkServer() #No longer needed, controller calls NetworkServer now
