__author__ = 'chris hamm'
#NetworkServer_r12
#Created: 2/8/2015

#NOTES: The layout of this revision is modelled after revXA. This revision has a layout difference from the rev11,
    #   the main server thread will not only check for inbound clients but it will also handle the inbound messages
    #   from the controller.
    #   This revision will be using RLocks instead of regular locks
    #   lock = threading.Lock()
    #   lock.acquire()
    #   lock.acquire() #this will block
    #
    #   lock = threading.RLock()
    #   lock.acquire()
    #   lock.acquire() #This wont block (this is nested)

import socket
from socket import *
import threading
import thread
import platform
import sys

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

def checkForNextCommandFromClient(self,inboundData):
    print "Checking for the Next command from the client\n"
    if(compareString(inboundData,"NEXT",0,0,len("NEXT"),len("NEXT"))):
        print "NEXT command was received from the client\n"
        self.nextCommandToClientCounterLock.acquire()
        self.incrementNextCommandFromClientCounter()
        self.nextCommandToClientCounterLock.release()
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

def checkForCrashedCommandFromClient(self,inboundData):
    print "Checking for the Crashed Command from the Client\n"
    if(compareString(inboundData,"CRASHED",0,0,len("CRASHED"),len("CRASHED"))):
        print "CRASHED Command was received from the client\n"
        crashedClientIP= ""
        for x in range(8, len(inboundData)):
            crashedClientIP += inboundData[x]
        print "Crashed Client IP: " + str(crashedClientIP) + "\n"
        self.listOfCrashedClientsLock.acquire()
        self.listOfCrashedClients.append(crashedClientIP)
        self.listOfCrashedClientsLock.release()
        print "Looking for a matching IP in the list of clients\n"
        foundMatch= False
        tempAddr2 = ""
        self.listOfClientsLock.acquire()
        for index in range(0, len(self.listOfClients)):
            tempSock, tempAddr= self.listOfClients[index]
            tempAddr2= str(tempAddr[0])
            if(crashedClientIP == tempAddr2):
                print "Matching IP Address was found\n"
                del self.listOfClients[index] #remove crashed client from listOfClients
                foundMatch= True
                self.stackOfChunksThatNeedToBeReassignedLock.acquire()
                self.dictionaryOfCurrentClientTasksLock.acquire()
                self.stackOfChunksThatNeedToBeReassigned.append(self.dictionaryOfCurrentClientTasks[tempAddr])
                self.dictionaryOfCurrentClientTasksLock.release()
                self.stackOfChunksThatNeedToBeReassignedLock.release()
                break
            else:
                print "No Matching IP found yet\n"
        self.listOfClientsLock.release()
        if(foundMatch==False):
            print "WARNING: No matching IP Address was found in the list of clients\n"
            self.incrementNumberOfIPAddressesNotFound()
        return True
    else:
        return False

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

def sendDoneCommandToClient(self,networkSocket, clientIP, socketLock):
    print "Issuing Done Command to Client: " + str(clientIP) +"\n"
    #networkSocket.settimeout(0.5)
    print "Acquiring socket lock\n"
    #self.socketLock.acquire()
    socketLock.acquire()
    networkSocket.settimeout(0.5)
    #self.serversocket.settimeout(0.5)
    print "socket lock acquired\n"
    while True:
        try:
            print "preparing to send done command to client\n"
            networkSocket.sendto("done",clientIP)
            #self.serversocket.sendto("done",clientIP)
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
                break
            elif(compareString(str(inst),"timed out",0,0,len("timed out"),len("timed out"))==True):
                #do not display the timeout error, but keep trying to send the done command
                fakeVar=True
                networkSocket.settimeout(0.5)#reset the socket timeout
                #DO NOT break
            else:
                print "Exception in send Done command: " +str(inst) +"\n"
                break
    #self.socketLock.release()
    socketLock.release()

def sendNextCommandToClient(self, networkSocket, clientIP, outboundMessage, socketLock):
    print "Sending Next Command to Client\n"
    #networkSocket.settimeout(0.5)
    #self.socketLock.acquire()
    socketLock.acquire()
    networkSocket.settimeout(0.5)
    print "Acquired socket lock\n"
    #self.serversocket.settimeout(0.5)
    while True:
        try:
            print "preparing to send next command to client\n"
            networkSocket.sendto(outboundMessage, clientIP)
            #networkSocket.sendall(outboundMessage)
            #self.serversocket.sendto(outboundMessage, clientIP)
            print "sent Next command to client: "+str(clientIP)+"\n"
            self.nextCommandToClientCounterLock.acquire()
            self.incrementNextCommandToClientCounter()
            self.nextCommandToClientCounterLock.release()
            break
        except Exception as inst:
            if(compareString(str(inst),"timed out",0,0,len("timed out"), len("timed out"))==True):
                print "ERROR: timed out"
                print type(inst) #the exception instance
                print inst.args #srguments stored in .args
                print inst #_str_ allows args tto be printed directly
                fakeVar= True
               # networkSocket.settimeout(5.0) #reset the socket timeout
                #dont break
            else:
                print "Exception in send Next command: " +str(inst) +"\n"
                break
    #self.socketLock.release()
    socketLock.release()

def sendNextDataCommandToClient(self, networkSocket, clientIP, outboundMessage, socketLock):
    print "Sending Next Data Command to Client\n"
    #networkSocket.settimeout(0.5)
    #self.socketLock.acquire()
    socketLock.acquire()
    networkSocket.settimeout(0.5)
    print "Acquired socket lock\n"
    #self.serversocket.settimeout(0.5)
    while True:
        try:
            print "preparing to send next data to client\n"
            networkSocket.sendto(outboundMessage,clientIP)
            #self.serversocket.sendto(outboundMessage,clientIP)
            print "sent next data command to client: "+str(clientIP)+"\n"
            self.nextDataCommandToClientCounter.acquire()
            self.incrementNextDataCommandToClientCounter()
            self.nextDataCommandToClientCounter.release()
            break
        except Exception as inst:
            if(compareString(str(inst),"timed out",0,0,len("timed out"), len("timed out"))==True):
                #dont display the timeout message
                fakeVar= True
                networkSocket.settimeout(0.5) #reset the socket timeout
                #dont break
            else:
                print "Exception in send next Data Command to Client: " +str(inst)+"\n"
                break
    #self.socketLock.release()
    socketLock.release()

class NetworkServer():
    #Declare class vars here
    host = ''
    port = 55568
    listOfClients = [] #list that holds the IPaddresses and ports of client that is connected to server
    listOfCrashedClients = [] #list of crashed clients
    stackOfClientsWaitingForNextChunk = []
    stackOfChunksThatNeedToBeReassigned = []
    dictionaryOfCurrentClientTasks = {}

    #Declare command record vars
    doneCommandToClientCounter = 0
    nextCommandToClientCounter = 0
    nextDataCommandToClientCounter = 0

    nextCommandFromClientCounter = 0
    foundSolutionCommandFromClientCounter = 0
    crashedCommandFromClientCounter = 0
    unknownCommandFromClientCounter = 0

    nextChunkCommandToControllerCounter = 0
    waitingCommandToControllerCounter = 0
    doneCommandToControllerCounter = 0

    nextChunkCommandFromControllerCounter = 0
    doneCommandFromControllerCounter = 0
    unknownCommandFromControllerCounter = 0

    numberOfThreadsCreatedCounter = 0

    #Define the locks here
    listOfClientsLock = threading.RLock()
    listOfCrashedClientsLock = threading.RLock()
    stackOfClientsWaitingForNextChunkLock = threading.RLock()
    stackOfChunksThatNeedToBeReassignedLock = threading.RLock()
    dictionaryOfCurrentClientTasksLock = threading.RLock()

    socketLock = threading.RLock()

    doneCommandToClientCounterLock = threading.RLock()
    nextCommandToClientCounterLock = threading.RLock()
    nextDataCommandToClientCounterLock = threading.RLock()

    nextCommandFromClientCounterLock = threading.RLock()
    foundSolutionCommandFromClientCounterLock = threading.RLock()
    crashedCommandFromClientCounterLock = threading.RLock()
    unknownCommandFromClientCounterLock = threading.RLock()

    nextChunkCommandToControllerCounterLock = threading.RLock()
    waitingCommandToControllerCounterLock = threading.RLock()
    doneCommandToControllerCounterLock = threading.RLock()

    nextChunkCommandFromControllerCounterLock = threading.RLock()
    doneCommandFromControllerCounterLock = threading.RLock()
    unknownCommandFromControllerCounterLock = threading.RLock()


    #Define incrementers here
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

    #Define the thread handler here
    def handler(self, clientSocket, clientAddr, socketLock):
        clientSocket.settimeout(0.5)
        while True:
            try: #handler main try block
                socketLock.acquire()
                inboundClientCommand = clientSocket.recv(2048)
                socketLock.release()
                if(checkForNextCommandFromClient(inboundClientCommand)==True):
                    #extract the clients IP from message
                    clientsIP = ""
                    for index in range(5, len(inboundClientCommand)):
                        clientsIP+= inboundClientCommand[index]
                    print "DEBUG: clientsIP: " +str(clientsIP)+"\n"
                    #determine if a chunk from stackofChunksThatMustBeReassigned can be used
                    self.stackOfChunksThatNeedToBeReassignedLock.acquire()
                    if(len(self.stackOfChunksThatNeedToBeReassigned) > 0):
                        self.dictionaryOfCurrentClientTasksLock.acquire()
                        self.dictionaryOfCurrentClientTasks[clientsIP] = self.stackOfChunksThatNeedToBeReassigned.pop()
                        self.dictionaryOfCurrentClientTasksLock.release()
                        dataFileSize = sys.getsizeof(self.dictionaryOfCurrentClientTasks[clientsIP].data)
                        tempKeywords= "NEXT " +"SIZE(" + str(dataFileSize) +") " + str(self.dictionaryOfCurrentClientTasks[clientsIP].params)
                        #send chhunk params to client
                        #socketLock.acquire() #functions already lock the socket
                        try:
                            print "clientIP: "+str(clientsIP)+"\n"
                            sendNextCommandToClient(self,clientSocket,clientsIP, tempKeywords, socketLock)
                        except Exception as inst:
                            print "ERROR in sending NextParams to the client: " +str(inst)+"\n"
                        #send the chunk data to the client
                        try:
                            sendNextDataCommandToClient(self,clientSocket,clientsIP, str(self.dictionaryOfCurrentClientTasks[clientsIP].data), socketLock)
                        except Exception as inst:
                            print "ERROR in sending NextData to the client: " +str(inst)+"\n"
                    else:
                        socketLock.acquire()
                        self.sendNextChunkCommandToController(self)
                        socketLock.release()
                        self.stackOfClientsWaitingForNextChunkLock.acquire()
                        self.stackOfClientsWaitingForNextChunk.append(clientsIP)
                        self.stackOfClientsWaitingForNextChunkLock.release()
                    self.stackOfChunksThatNeedToBeReassignedLock.release()
                elif(checkForFoundSolutionCommandFromClient(inboundClientCommand) == True):
                    self.foundSolutionCommandFromClientCounterLock.acquire()
                    self.incrementFoundSolutionCommandFromClientCounter()
                    self.foundSolutionCommandFromClientCounterLock.release()
                    self.listOfClientsLock.acquire()
                    socketLock.acquire()
                    for i in range(0, len(self.listOfClients)): #issueing done commands to all clients
                        (sock, addr) = self.listOfClients[i]
                        sock.sendall("done")
                    socketLock.release()
                    self.listOfClientsLock.release()
                elif(checkForCrashedCommandFromClient(self, inboundClientCommand)==True):
                    self.crashedCommandFromClientCounterLock.acquire()
                    self.incrementCrashedCommandFromClientCounter()
                    self.crashedCommandFromClientCounterLock.release()
                else:
                    self.unknownCommandFromClientCounterLock.acquire()
                    self.incrementUnknownCommandFromClientCounter()
                    self.unknownCommandFromClientCounterLock.release()
            except Exception as inst:
                print "Error in handler main try block: "+str(inst)+"\n"
        clientSocket.close()

    #Define the class constructor here
    def __init__(self, inboundpipefromcontroller):
        self.pipe= inboundpipefromcontroller

        #Create the serversocket
        serversocket= socket.socket(AF_INET, SOCK_STREAM)

        #bind the socket
        serversocket.bind(self.host, self.port)

        #detect the OS
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

        #get the IP address
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

        #start listening to the serversocket
        serversocket.listen(5)

        #Main thread server loop starts here
        try: #Main thread loop server try block
            serversocket.settimeout(0.5)
            while True:
                #check to see if a client is trying to connect
                try: #check for a client that wants to connect try block
                    clientSocket, clientAddr = serversocket.accept()
                    self.listOfClientsLock.acquire()
                    self.listOfClients.append((clientSocket, clientAddr))
                    self.listOfClientsLock.release()
                    thread.start_new_thread(self.handler, (clientSocket, clientAddr, self.socketLock))
                    print "A new thread has been made\n"
                    self.incrementNumberOfThreadsCreatedCounter()
                except Exception as inst:
                    print "Error in check for clients trying to connect try block: " +str(inst)+"\n"
                #check for input from the controller
                try: #check for controller input try block
                    if(self.pipe.poll()):
                        inboundControllerCommand = self.pipe.recv()
                        print "Received a command from the controller\n"
                        #check for the nextChunk command
                        if(checkForNextChunkCommandFromController(self, inboundControllerCommand)==True):
                            #wait for the chunk object from the controller
                            print "Waiting for the corresponding chunk object from controller\n"
                            inboundControllerObject= self.pipe.recv()
                            print "Received the chunk object from controller\n"
                            #check if clients are waiting for nextChunk
                            self.stackOfClientsWaitingForNextChunkLock.acquire()
                            if(len(self.stackOfClientsWaitingForNextChunk) > 0):
                                #add the keywords
                                storedClientIP = str(self.stackOfClientsWaitingForNextChunk.pop())
                                #find the first invalid char and mark its position, removing IP address from message
                                firstInvalidCharIndex = 5 #NEXT is first four positions
                                for x2 in range(5, len(storedClientIP)):
                                    if(storedClientIP[x2].isalpha()==True):
                                        firstInvalidCharIndex = x2
                                        break
                                    elif(storedClientIP[x2].isspace()==True):
                                        firstInvalidCharIndex = x2
                                        break
                                #if  invalidCharIndex still equal to 5, keep entire string
                                if(firstInvalidCharIndex == 5):
                                    print "inbound chunk object does not need to be cropped\n"
                                else:
                                    storedClientIP= storedClientIP[5:firstInvalidCharIndex] #crop the string
                                self.dictionaryOfCurrentClientTasksLock.acquire()
                                self.dictionaryOfCurrentClientTasks[storedClientIP] = inboundControllerObject
                                self.dictionaryOfCurrentClientTasksLock.release()
                                self.stackOfClientsWaitingForNextChunkLock.release()
                                chunkFileSize = sys.getsizeof(inboundControllerObject.data)
                                #adding keywords to the params
                                self.dictionaryOfCurrentClientTasksLock.acquire()
                                tempKeywords2= "NEXT " + "SIZE(" + str(chunkFileSize) +") " +str(self.dictionaryOfCurrentClientTasks[storedClientIP].params)
                                self.dictionaryOfCurrentClientTasksLock.release()
                                #retreiving client's port
                                clientPort= ""
                                self.listOfClientsLock.acquire()
                                for index in range(0, len(self.listOfClients)):
                                    tempSock, tempAddr = self.listOfClients[index]
                                    if(tempAddr[0] == storedClientIP):
                                        clientPort = tempAddr[1]
                                        break
                                self.listOfClientsLock.release()
                                if(clientPort == ""):
                                    raise Exception("ERROR: client IP did not find a match in the listOfClients")
                                sendNextCommandToClient(self,self.serversocket,(storedClientIP, clientPort), tempKeywords2, self.socketLock)
                                sendNextDataCommandToClient(self,self.serversocket, (storedClientIP, clientPort), str(inboundControllerObject.data), self.socketLock)
                            #otherwise no clients are waiting for nextChunk
                            else:
                                #store the chunk in the stack of chunksThatNeedToBeReassigned
                                self.stackOfChunksThatNeedToBeReassignedLock.acquire()
                                self.stackOfChunksThatNeedToBeReassigned.append(inboundControllerObject)
                                self.stackOfChunksThatNeedToBeReassignedLock.release()
                            self.stackOfClientsWaitingForNextChunkLock.release()
                        #check for the Done Command
                        elif(checkForDoneCommandFromController(self, inboundControllerCommand)==True):
                            print "Received the done command from the controller\n"
                        #else print the unknown command
                        print "ERROR unknown command received from controller: " + str(inboundControllerCommand)
                        self.unknownCommandFromControllerCounterLock.acquire()
                        self.incrementUnknownCommandFromControllerCounter()
                        self.unknownCommandFromControllerCounterLock.release()
                except Exception as inst:
                    print "Error in check for controller input try block: " +str(inst)+"\n"
        except Exception as inst:
            print "Error in the MAIN THREAD: " + str(inst)+"\n"
        #End of Main thread server loop

        #Finally block goes here