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
    #   lock = threading.Lock()
    #   lock.acquire()
    #   lock.acquire() #This wont block (this is nested)


import socket
from socket import *
import threading
from threading import RLock
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
        self.nextCommandFromClientCounterLock.acquire()
        print "Acquired nextCommandFromClient Lock\n"
        self.incrementNextCommandFromClientCounter()
        self.nextCommandFromClientCounterLock.release()
        print "Released nextCommandFromClient Lock\n"
        return True
    else:
        return False

def checkForFoundSolutionCommandFromClient(self,inboundData):
    print "Checking for the Found Solution Command from the client\n"
    if(compareString(inboundData,"FOUNDSOLUTION",0,0,len("FOUNDSOLUTION"),len("FOUNDSOLUTION"))):
        print "FOUNDSOLUTION Command was received from the client\n"
        self.foundSolutionCommandFromClientCounterLock.acquire()
        print "Acquired foundSolutionFromClient Lock\n"
        self.incrementFoundSolutionCommandFromClientCounter()
        self.foundSolutionCommandFromClientCounterLock.release()
        print "Released foundSolutionFromClient Lock\n"
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
        print "Acquired listOfCrashedClients Lock\n"
        self.listOfCrashedClients.append(crashedClientIP)
        self.listOfCrashedClientsLock.release()
        print "Released listOfCrashedClients Lock\n"
        print "Looking for a matching IP in the list of clients\n"
        foundMatch= False
        tempAddr2 = ""
        self.listOfClientsLock.acquire()
        print "Acquired listOfClients Lock\n"
        for index in range(0, len(self.listOfClients)):
            tempSock, tempAddr= self.listOfClients[index]
            tempAddr2= str(tempAddr[0])
            if(crashedClientIP == tempAddr2):
                print "Matching IP Address was found\n"
                del self.listOfClients[index] #remove crashed client from listOfClients
                foundMatch= True
                self.stackOfChunksThatNeedToBeReassignedLock.acquire()
                print "Acquired stackOfChunksThatNeedToBeReassigned Lock\n"
                self.dictionaryOfCurrentClientTasksLock.acquire()
                print "Acquired dictionaryOfCurrentClientTasks Lock\n"
                self.stackOfChunksThatNeedToBeReassigned.append(self.dictionaryOfCurrentClientTasks[tempAddr])
                self.dictionaryOfCurrentClientTasksLock.release()
                print "Released dictionaryOfCurrentClientTasks Lock\n"
                self.stackOfChunksThatNeedToBeReassignedLock.release()
                print "Released stackOfChunksThatNeedToBeReassigned Lock\n"
                break
            else:
                print "No Matching IP found yet\n"
        self.listOfClientsLock.release()
        print "Released listOfClients Lock\n"
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
            print "Acquired nextChunkCommandFromController Lock\n"
            self.incrementNextChunkCommandFromControllerCounter()
            self.nextChunkCommandFromControllerCounterLock.release()
            print "Released nextChunkCommandFromController Lock\n"
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
            print "Acquired doneCommandFromController Lock\n"
            self.incrementDoneCommandFromControllerCounter()
            self.doneCommandFromControllerCounterLock.release()
            print "Released doneCommandFromController Lock\n"
            return True
        else:
            return False
    except Exception as inst:
        print "Exception thrown in checkForDoneCommandFromController: "+str(inst)+"\n"
        return False







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
        #clientSocket.settimeout(0.5)
        inboundClientCommand= ""
        clientHasCrashed= False
        while True:
            try: #handler main try block
                socketLock.acquire()
                print "Handler Acquired socketLock\n"
                while True:
                    try: #recv inbound messages try block
                        inboundClientCommand = clientSocket.recv(2048)
                    #except socket.error as inst:
                       # if(compareString(str(inst),"[Errno 35] Resource temporarily unavailable",0,0,len("[Errno 35] Resource temporarily unavailable"),len("[Errno 35] Resource temporarily unavailable"))==True):
                        #    import time
                         #   time.sleep(0.25)
                          #  continue
                       # else:
                        #    print "Error in socket.error recv inbound messages try block: "+str(inst)+"\n"
                    except Exception as inst:
                        if(compareString(str(inst),"[Errno 35] Resource temporarily unavailable",0,0,len("[Errno 35] Resource temporarily unavailable"),len("[Errno 35] Resource temporarily unavailable"))==True):
                            import time
                            print "resource unavailable, sleeping then trying again\n"
                            time.sleep(0.25)
                            continue
                        elif(compareString(str(inst),"timed out",0,0,len("timed out"),len("timed out"))==True):
                            print "No input from the client detected\n"
                            break
                        else:
                            print "Error in recv command from the client: "+str(inst)+"\n"
                            break
                    #finally:
                socketLock.release()
                print "Handler Released socketLock\n"
                if(len(inboundClientCommand) < 1):
                    #empty string, no input from controller
                    fakeVar=True
                elif(checkForNextCommandFromClient(self,inboundClientCommand)==True):
                    #extract the clients IP from message
                    clientsIP = ""
                    for index in range(5, len(inboundClientCommand)):
                        clientsIP+= inboundClientCommand[index]
                    print "DEBUG: clientsIP: " +str(clientsIP)+"\n"
                    #determine if a chunk from stackofChunksThatMustBeReassigned can be used
                    self.stackOfChunksThatNeedToBeReassignedLock.acquire()
                    print "Acquired stackOfChunksThatNeedToBeReassigned Lock\n"
                    if(len(self.stackOfChunksThatNeedToBeReassigned) > 0):
                        self.dictionaryOfCurrentClientTasksLock.acquire()
                        print "Acquired dictionaryOfCurrentClientTasks Lock\n"
                        self.dictionaryOfCurrentClientTasks[clientsIP] = self.stackOfChunksThatNeedToBeReassigned.pop()
                        self.dictionaryOfCurrentClientTasksLock.release()
                        print "Released dictionaryOfCurrentClientTasks Lock\n"
                        dataFileSize = sys.getsizeof(self.dictionaryOfCurrentClientTasks[clientsIP].data)
                        tempKeywords= "NEXT " +"SIZE(" + str(dataFileSize) +") " + str(self.dictionaryOfCurrentClientTasks[clientsIP].params)
                        print "chunk params with keywords: " +str(tempKeywords) + "\n"
                        #send chhunk params to client
                        #socketLock.acquire() #functions already lock the socket
                        try:
                            print "clientIP: "+str(clientsIP)+"\n"
                            self.sendNextCommandToClient(clientSocket,clientsIP, tempKeywords, socketLock)
                        except Exception as inst:
                            print "ERROR in sending NextParams to the client: " +str(inst)+"\n"

                        try:
                            self.sendNextDataCommandToClient(clientSocket,clientsIP, str(self.dictionaryOfCurrentClientTasks[clientsIP].data), socketLock)
                        except Exception as inst:
                            print "ERROR in sending NextData to the client: " +str(inst)+"\n"
                    else:
                        #socketLock.acquire()
                        self.sendNextChunkCommandToController()
                        #socketLock.release()
                        self.stackOfClientsWaitingForNextChunkLock.acquire()
                        print "Acquired stackOfClientsWaitingForNextChunk Lock\n"
                        print "checking for duplicates in stack...\n"
                        foundDuplicate= False
                        for i in range(0, len(self.stackOfClientsWaitingForNextChunk)):
                            if(self.stackOfClientsWaitingForNextChunk[i] == clientsIP):
                                print "Duplicate value found, not adding to the stack\n"
                                foundDuplicate= True
                                break
                        if(foundDuplicate == False):
                            self.stackOfClientsWaitingForNextChunk.append(clientsIP)
                            print "added IP to the stack\n"
                        self.stackOfClientsWaitingForNextChunkLock.release()
                        print "Released stackOfClientsWaitingForNextChunk Lock\n"
                        print "Added client to the stack of clients waiting for next chunk\n"
                    self.stackOfChunksThatNeedToBeReassignedLock.release()
                    print "Released stackOfClientsWaitingForNextChunk Lock\n"
                elif(checkForFoundSolutionCommandFromClient(self,inboundClientCommand) == True):
                    self.listOfClientsLock.acquire()
                    print "Acquired listOfClients Lock\n"
                    socketLock.acquire()
                    print "Handler Acquired socketLock\n"
                    for i in range(0, len(self.listOfClients)): #issueing done commands to all clients
                        (sock, addr) = self.listOfClients[i]
                        sock.send("done")
                    socketLock.release()
                    print "Handler Released socketLock\n"
                    self.listOfClientsLock.release()
                    print "Released listOfClients Lock\n"
                elif(checkForCrashedCommandFromClient(self, inboundClientCommand)==True):
                    clientHasCrashed=True
                    self.crashedCommandFromClientCounterLock.acquire()
                    print "Acquired crashedCommandFromClient Lock\n"
                    self.incrementCrashedCommandFromClientCounter()
                    self.crashedCommandFromClientCounterLock.release()
                    print "Released crashedCommandFromClient Lock\n"
                else:
                    self.unknownCommandFromClientCounterLock.acquire()
                    print "Acquired unknownCommandFromClient Lock\n"
                    self.incrementUnknownCommandFromClientCounter()
                    self.unknownCommandFromClientCounterLock.release()
                    print "Released unknownCommandFromClient Lock\n"
            except Exception as inst:
                if(compareString(str(inst),"timed out",0,0,len("timed out"),len("timed out"))==True):
                    #dont display error message
                    fakeVar= True
                   # socketLock.release()
                else:
                    print "Error in handler main try block: "+str(inst)+"\n"
                    #socketLock.release()
            finally:
                print "Checking the 'clientHasCrashed' value\n"
                if(clientHasCrashed == True):
                    print "'clientHasCrashed' value is True, entering infinite while loop (with no print statements)\n"
                    while True:
                        #does not display any messages, just sits and waits
                        fakeVar=True
                    #end of While True
                else:
                    print "'clientHasCrashed' value not set, resuming handler loop\n"
        clientSocket.close()
        print "Handler's client socket has been closed\n"

    #Define the class constructor here
    def __init__(self, inboundpipefromcontroller):
        self.pipe= inboundpipefromcontroller

        #Create the serversocket
        import socket
        serversocket= socket.socket(AF_INET, SOCK_STREAM)

        #bind the socket
        serversocket.bind((self.host, self.port))

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
                    print "Acquiring listOfClients Lock\n"
                    self.listOfClientsLock.acquire()
                    print "Acquired listOfClients Lock\n"
                    self.listOfClients.append((clientSocket, clientAddr))
                    self.listOfClientsLock.release()
                    print "Released listOfClients Lock\n"
                    thread.start_new_thread(self.handler, (clientSocket, clientAddr, self.socketLock))
                    print "A new thread has been made\n"
                    self.incrementNumberOfThreadsCreatedCounter()
                except Exception as inst:
                    if(compareString(str(inst),"timed out",0,0,len("timed out"),len("timed out"))==True):
                        #dont print out the error
                        fakeVar= True
                    else:
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
                            try:
                                inboundControllerObject= self.pipe.recv()
                            except Exception as inst:
                                print "Error in trying to receive corresponding chunk object: " +str(inst)+"\n"
                            print "Received the chunk object from controller\n"
                            #check if clients are waiting for nextChunk
                            self.stackOfClientsWaitingForNextChunkLock.acquire()
                            print "Acquired stackOfClientsWaitingForNextChunk Lock\n"
                            if(len(self.stackOfClientsWaitingForNextChunk) > 0):
                                #add the keywords
                                storedClientIP = str(self.stackOfClientsWaitingForNextChunk.pop())
                                print "Popped client off the stackOfClientsForNextChunk\n"
                                #find the first invalid char and mark its position, removing IP address from message
                                firstInvalidCharIndex = 5 #NEXT is first four positions
                                for x2 in range(firstInvalidCharIndex, len(storedClientIP)):
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
                                print "Acquired dictionaryOfCurrentClientTasks Lock\n"
                                self.dictionaryOfCurrentClientTasks[storedClientIP] = inboundControllerObject
                                self.dictionaryOfCurrentClientTasksLock.release()
                                print "Released dictionaryOfCurrentClientTasks Lock\n"
                                #self.stackOfClientsWaitingForNextChunkLock.release()
                                chunkFileSize = sys.getsizeof(inboundControllerObject.data)
                                #adding keywords to the params
                                self.dictionaryOfCurrentClientTasksLock.acquire()
                                print "Acquired dictionaryOfCurrentClientTasks Lock\n"
                                tempKeywords2= "NEXT " + "SIZE(" + str(chunkFileSize) +") " +str(self.dictionaryOfCurrentClientTasks[storedClientIP].params)
                                self.dictionaryOfCurrentClientTasksLock.release()
                                print "Released dictionaryOfCurrentClientTasks Lock\n"
                                print "chunk params with keywords: " + str(tempKeywords2)+"\n"
                                #print "chunk data: " +str(inboundControllerObject.data)+"\n"
                                #retreiving client's port
                                clientPort= ""
                                tempSock= ""
                                self.listOfClientsLock.acquire()
                                print "Acquired listOfClients Lock\n"
                                for index in range(0, len(self.listOfClients)):
                                    tempSock, tempAddr = self.listOfClients[index]
                                    if(tempAddr[0] == storedClientIP):
                                        clientPort = tempAddr[1]
                                        break
                                self.listOfClientsLock.release()
                                print "Released listOfClients Lock\n"
                                if(clientPort == ""):
                                    print "ERROR unable to find a matching ip address\n"
                                    print "Trying to match this ip: " +str(storedClientIP)+"\n"
                                    raise Exception("ERROR: client IP did not find a match in the listOfClients")
                                self.sendNextCommandToClient(tempSock,(storedClientIP, clientPort), tempKeywords2, self.socketLock)
                                print "next Command was sent to the client, now preparing to send next data\n"
                                self.sendNextDataCommandToClient(tempSock, (storedClientIP, clientPort), str(inboundControllerObject.data), self.socketLock)
                                print "next Data Command was sent to the client\n"
                            #otherwise no clients are waiting for nextChunk
                            else:
                                #store the chunk in the stack of chunksThatNeedToBeReassigned
                                self.stackOfChunksThatNeedToBeReassignedLock.acquire()
                                print "Acquired stackOfChunksThatNeedToBeReassigned Lock\n"
                                self.stackOfChunksThatNeedToBeReassigned.append(inboundControllerObject)
                                self.stackOfChunksThatNeedToBeReassignedLock.release()
                                print "Released stackOfChunksThatNeedToBeReassigned Lock\n"
                            self.stackOfClientsWaitingForNextChunkLock.release()
                            print "Released stackOfClientsWaitingForNextChunk Lock\n"
                        #check for the Done Command
                        elif(checkForDoneCommandFromController(self, inboundControllerCommand)==True):
                            print "Received the done command from the controller\n"
                        #else print the unknown command
                        else:
                            print "ERROR unknown command received from controller: " + str(inboundControllerCommand)
                            self.unknownCommandFromControllerCounterLock.acquire()
                            print "Acquired unknownCommandFromController Lock\n"
                            self.incrementUnknownCommandFromControllerCounter()
                            self.unknownCommandFromControllerCounterLock.release()
                            print "Released unknownCommandFromController Lock\n"
                except Exception as inst:
                    print "Error in check for controller input try block: " +str(inst)+"\n"

        except Exception as inst:
            print "Error in the MAIN THREAD: " + str(inst)+"\n"
        #End of Main thread server loop

        #Finally block goes here
        finally:
            print "Acquiring lock for print command records\n"
            self.listOfClientsLock.acquire()
            print "Acquired listOfClients Lock\n"
            print "# of clients connected: " + str(len(self.listOfClients)) + "\n"
            self.listOfClientsLock.release()
            print "Released listOfClients Lock\n"
            print "Issuing Done Commands to clients...\n"
            self.listOfClientsLock.acquire()
            print "Acquired listOfClients Lock\n"
            for i in range(0, len(self.listOfClients)):
                doneSock, doneAddr = self.listOfClients[i]
                self.sendDoneCommandToClient(doneSock, doneAddr, self.socketLock)
            self.listOfClientsLock.release()
            print "Released listOfClients Lock\n"
            serversocket.close()
            print "Socket has been closed\n"
            #printing out all of the records
            print "---------------Number of Threads Created-----------------------\n"
            print "# of Threads Created: " + str(self.numberOfThreadsCreatedCounter) +"\n"
            print "---------------List of Crashed Clients-------------------------\n"
            self.listOfCrashedClientsLock.acquire()
            print "Acquired listOfCrashedClients Lock\n"
            print "# of Crashed Clients: " + str(len(self.listOfCrashedClients)) +"\n"
            if(len(self.listOfCrashedClients) > 0):
                for x in range(0, len(self.listOfCrashedClients)):
                    print str(x) + ")" + str(self.listOfCrashedClients[x]) +"\n"
            self.listOfCrashedClientsLock.release()
            print "Released listOfCrashedClients Lock\n"
            print "--------------Stack of Clients Waiting For Next Chunk---------------\n"
            self.stackOfClientsWaitingForNextChunkLock.acquire()
            print "Acquired stackOfClientsWaitingForNextChunk Lock\n"
            print "# of Clients Waiting For Next Chunk: " +str(len(self.stackOfClientsWaitingForNextChunk)) +"\n"
            if(len(self.stackOfClientsWaitingForNextChunk) > 0):
                while(len(self.stackOfClientsWaitingForNextChunk) > 0):
                    print str(self.stackOfClientsWaitingForNextChunk.pop()) + "\n"
            self.stackOfClientsWaitingForNextChunkLock.release()
            print "Released stackOfClientsWaitingForNextChunk Lock\n"
            print "--------------Stack of Chunks That Need To Be Reassigned----------------\n"
            self.stackOfChunksThatNeedToBeReassignedLock.acquire()
            print "Acquired stackOfChunksThatNeedToBeReassigned Lock\n"
            print "# of Chunks That Need To Be Reassigned: " + str(len(self.stackOfChunksThatNeedToBeReassigned)) +"\n"
            self.stackOfChunksThatNeedToBeReassignedLock.release()
            print "Released stackOfChunksThatNeedToBeReassigned Lock\n"
            print "--------------Dictionary of Current Client Tasks---------------------\n"
            self.dictionaryOfCurrentClientTasksLock.acquire()
            print "Acquired dictionaryOfCurrentClientTasks Lock\n"
            print "[key]         [value]"  +"\n"
            for key, value in self.dictionaryOfCurrentClientTasks.iteritems():
                print str(key), str(value)
            self.dictionaryOfCurrentClientTasksLock.release()
            print "Released dictionaryOfCurrentClientTasks Lock\n"
            print "---------------Outbound Commands To Client(s)------------------\n"
            self.doneCommandToClientCounterLock.acquire()
            print "Acquired doneCommandToClient Lock\n"
            print "# of Done Commands sent to the clients: " + str(self.doneCommandToClientCounter) +"\n"
            self.doneCommandToClientCounterLock.release()
            print "Released doneCommandToClient Lock\n"
            self.nextCommandToClientCounterLock.acquire()
            print "Acquired nextCommandToClient Lock\n"
            print "# of Next Commands sent to the clients: " +str(self.nextCommandToClientCounter) +"\n"
            self.nextCommandToClientCounterLock.release()
            print "Released nextCommandToClient Lock\n"
            self.nextDataCommandToClientCounterLock.acquire()
            print "Acquired nextDataCommandToClient Lock\n"
            print "# of Next Data Commands sent to the clients: " +str(self.nextDataCommandToClientCounter) + "\n"
            self.nextDataCommandToClientCounterLock.release()
            print "Released nextDataCommandToClient Lock\n"
            print "---------------Inbound Commands From Client(s)-----------------\n"
            self.nextCommandFromClientCounterLock.acquire()
            print "Acquired nextCommandFromClient Lock\n"
            print "# of Next Commands received from the client: " + str(self.nextCommandFromClientCounter) + "\n"
            self.nextCommandFromClientCounterLock.release()
            print "Released nextCommandFromClient Lock\n"
            self.foundSolutionCommandFromClientCounterLock.acquire()
            print "Acquired foundSolutionFromClient Lock\n"
            print "# of FOUNDSOLUTION Commands received from the client: " +str(self.foundSolutionCommandFromClientCounter) +"\n"
            self.foundSolutionCommandFromClientCounterLock.release()
            print "Released foundSolutionFromClient Lock\n"
            self.unknownCommandFromClientCounterLock.acquire()
            print "Acquired unknownCommandFromClient Lock\n"
            print "# of Unknown Commands received from Client: " + str(self.unknownCommandFromClientCounter) +"\n"
            self.unknownCommandFromClientCounterLock.release()
            print "Released unknownCommandFromClient Lock\n"
            self.crashedCommandFromClientCounterLock.acquire()
            print "Acquired crashedCommandFromClient Lock\n"
            print "# of Crashed Commands received from client: " + str(self.crashedCommandFromClientCounter) + "\n"
            self.crashedCommandFromClientCounterLock.release()
            print "Released crashedCommandFromClient Lock\n"
            print "--------------Outbound Commands To Controller----------------\n"
            self.nextChunkCommandToControllerCounterLock.acquire()
            print "Acquired nextChunkCommandToController Lock\n"
            print "# of nextChunk Commands sent to the Controller: " +str(self.nextChunkCommandToControllerCounter)+"\n"
            self.nextChunkCommandToControllerCounterLock.release()
            print "Released nextChunkCommandToController Lock\n"
            self.waitingCommandToControllerCounterLock.acquire()
            print "Acquire waitingCommandToController Lock\n"
            print "# of waiting Commands sent to the Controller: " + str(self.waitingCommandToControllerCounter)+"\n"
            self.waitingCommandToControllerCounterLock.release()
            print "Released waitingCommandToController Lock\n"
            self.doneCommandToControllerCounterLock.acquire()
            print "Acquired doneCommandToController Lock\n"
            print "# of done Commands sent to the Controller: " + str(self.doneCommandToControllerCounter)+"\n"
            self.doneCommandToControllerCounterLock.release()
            print "Released doneCommandToController Lock\n"
            print "-------------Inbound Commands From Controller---------------\n"
            self.nextChunkCommandFromControllerCounterLock.acquire()
            print "Acquired nextChunkCommandFromController Lock\n"
            print "# of nextChunk Commands received from the Controller: "+ str(self.nextChunkCommandFromControllerCounter)+"\n"
            self.nextChunkCommandFromControllerCounterLock.release()
            print "Released nextChunkCommandFromController Lock\n"
            self.doneCommandFromControllerCounterLock.acquire()
            print "Acquired doneCommandFromController Lock\n"
            print "# of done Commands received from the Controller: " +str(self.doneCommandFromControllerCounter)+"\n"
            self.doneCommandFromControllerCounterLock.release()
            print "Released doneCommandFromController Lock\n"
            self.unknownCommandFromControllerCounterLock.acquire()
            print "Acquired unknownCommandFromController Lock\n"
            print "# of unknown Commands received from the Controller: "+str(self.unknownCommandFromControllerCounter)+"\n"
            self.unknownCommandFromControllerCounterLock.release()
            print "Released unknownCommandFromController Lock\n"

    def sendNextChunkCommandToController(self):
        try:
            print "Sending nextChunk Command to the Controller\n"
            self.pipe.send("nextChunk")
            print "Sent the nextChunk Command to the Controller\n"
            self.nextChunkCommandToControllerCounterLock.acquire()
            print "Acquired nextChunkCommandToController Lock\n"
            self.incrementNextChunkCommandToControllerCounter()
            self.nextChunkCommandToControllerCounterLock.release()
            print "Released nextChunkCommandToController Lock\n"
            print "Incremented the nextChunkToCOntrollerCounter\n"
        except Exception as inst:
            print "Exception was thrown in sendNextChunkCommandToController: " +str(inst)+"\n"

    def sendDoneCommandToClient(self,networkSocket, clientIP, socketLock):
        print "Issuing Done Command to Client: " + str(clientIP) +"\n"
        print "Acquiring socket lock\n"
        socketLock.acquire()
        print "Acquired socketLock\n"
        networkSocket.settimeout(0.5)
        #self.serversocket.settimeout(0.5)
        print "socket lock acquired\n"
        try:
            print "preparing to send done command to client\n"
            networkSocket.send("done")
            print "sent Done command to client: " +str(clientIP) +"\n"
            self.doneCommandToClientCounterLock.acquire()
            print "Acquired doneCommandToClient Lock\n"
            self.incrementDoneCommandToClientCounter()
            self.doneCommandToClientCounterLock.release()
            print "Released doneCOmmandToClient Lock\n"
        except Exception as inst:
            if(compareString(str(inst),"[Errno 32] Broken pipe",0,0,len("[Errno 32] Broken pipe"),len("[Errno 32] Broken pipe"))):
                print "Broken pipe error detected in sendData\n"
                self.doneCommandToClientCounterLock.release()
                print "Released doneCommandToClient Lock\n"
            elif(compareString(str(inst),"timed out",0,0,len("timed out"),len("timed out"))==True):
                #do not display the timeout error, but keep trying to send the done command
                fakeVar=True
            else:
                print "Exception in send Done command: " +str(inst) +"\n"
                self.doneCommandToClientCounterLock.release()
                print "Released doneCommandToClient Lock\n"
        socketLock.release()
        print "Released socketLock\n"

    def sendNextCommandToClient(self, networkSocket, clientIP, outboundMessage, socketLock):
        print "Sending Next Command to Client\n"
        socketLock.acquire()
        print "Acquired socketLock\n"
        #networkSocket.settimeout(0.5)
        #print "Acquired socket lock\n"
        try:
            networkSocket.send(outboundMessage)
            print "sent Next command to client: "+str(clientIP)+"\n"
            self.nextCommandToClientCounterLock.acquire()
            print "Acquired nextCommandToClient Lock\n"
            self.incrementNextCommandToClientCounter()
            self.nextCommandToClientCounterLock.release()
            print "Released nextCommandToClient Lock\n"
        except Exception as inst:
            if(compareString(str(inst),"timed out",0,0,len("timed out"), len("timed out"))==True):
                print "ERROR: timed out"
                print type(inst) #the exception instance
                print inst.args #srguments stored in .args
                print inst #_str_ allows args tto be printed directly
                fakeVar= True
                #self.nextCommandToClientCounterLock.release()
            else:
                print "Exception in send Next command: " +str(inst) +"\n"
                #self.nextCommandToClientCounterLock.release()
        finally:
            socketLock.release()
            print "Released socketLock\n"

    def sendNextDataCommandToClient(self, networkSocket, clientIP, outboundMessage, socketLock):
        print "Sending Next Data Command to Client\n"
        socketLock.acquire()
        print "Acquired socket lock\n"
        try:
            print "preparing to send next data to client\n"
            networkSocket.send(outboundMessage)
            print "sent next data command to client: "+str(clientIP)+"\n"
            self.nextDataCommandToClientCounterLock.acquire()
            print "Acquired nextDataCommandToClient Lock\n"
            self.incrementNextDataCommandToClientCounter()
            self.nextDataCommandToClientCounterLock.release()
            print "Released nextDataCommandToClient Lock\n"
        except Exception as inst:
            if(compareString(str(inst),"timed out",0,0,len("timed out"), len("timed out"))==True):
                #dont display the timeout message
                fakeVar= True
                #networkSocket.settimeout(0.5) #reset the socket timeout
                #dont break
                #self.nextDataCommandToClientCounterLock()
            else:
                print "Exception in send next Data Command to Client: " +str(inst)+"\n"
                #self.nextDataCommandToClientCounterLock()
        finally:
            socketLock.release()
            print "Released socketLock\n"

