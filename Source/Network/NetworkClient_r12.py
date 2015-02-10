__author__ = 'chris hamm'
#NetworkClient_r12
#Created: 2/8/2015

#Designed to work with NetworkServer_r12

#Must now be called by controller



from socket import *
import socket
from random import *
import platform
import sys
import Chunk

def compareString(inboundStringA, inboundStringB, startA, startB, endA, endB): #This function is now global
        try:
            posA = startA
            posB = startB
            #add check here (optional)
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
        except Exception as inst:
            print "ERROR in compareString: " + str(inst) +"\n"
            print "---- inboundStringA: '" + inboundStringA + "'\n"
            print "-------- startA: " + str(startA) + " endA: " + str(endA) +"\n"
            print "---- inboundStringB: '" + inboundStringB + "'\n"
            print "-------- startB: " + str(startB) + " endB: " + str(endB) +"\n"
            return False

def receiveData(self,networkSocket):
        print "Checking for inbound network data\n"
        networkSocket.settimeout(0.5)
        data = ""
        completeData = ""
        try: #receive data try block
            #while True:
            completeData = networkSocket.recv(2048)
                #if data:
                 #   completeData+= data
                  #  networkSocket.settimeout(0.5)
               # else:
                #    break
            if(len(completeData) < 1):
                print "received empty string\n"
            else: #not empty string
                #print "received data: " + str(data) +"\n" #something is logically wrong with the check for done command
                if(checkForDoneCommandFromServer(self,str(completeData))==True):
                    print "Server has issued the done command\n"
                    sendDoneCommandToController(self)
                    #break
                elif(checkForNextChunkParamsFromServer(self, str(completeData))==True):
                    print "Received Next Chunk Params From Server\n"
                    #insert chunk assembling process here
                    dataChunkFileSize = ""
                    closingParenthesisLocation = 0
                    #end of file size is marked by a closing parenthesis
                    #position [0:4] = 'NEXT'
                    #position [5:9] = 'SIZE('
                    for index in range(10,len(completeData)):
                        if(completeData[index] == ")"):
                            closingParenthesisLocation = index
                            break
                        else:
                            dataChunkFileSize+= str(completeData[index])
                    #removing keywords from the params
                    completeData= completeData[(closingParenthesisLocation+2):len(completeData)]
                    print "data after keywords where removed: "+str(completeData)+"\n"
                    inputData  = ""
                    recvData = ""
                    #receive the chunk data from the server
                    networkSocket.settimeout(0.5)
                    try:
                        import sys
                        print "dataChunkFileSize: " +str(dataChunkFileSize)+"\n"
                        while(sys.getsizeof(inputData) < dataChunkFileSize):
                            recvData = networkSocket.recv(4096)
                            #if(inputData >= dataChunkFileSize):
                             #   break
                            if recvData:
                                inputData+= recvData
                                networkSocket.settimeout(0.5) #reset the socket timeout
                            else:
                                break
                        self.incrementNextChunkDataFromServerCounter()
                    except Exception as inst:
                        if(compareString(str(inst),"timed out",0,0,len("timed out"),len("timed out"))==True):
                            print "ERROR in receiving chunk data from the server: timed out\n"
                            print "dataChunkFileSize: "+ str(dataChunkFileSize)+"\n"
                            print "Size of inputData: " + str(sys.getsizeof(inputData)) +"\n"
                            print "Size of recvData: " + str(sys.getsizeof(recvData))+"\n"
                        else:
                            print "Error in receiving chunk data from server: " +str(inst)+"\n"
                    #self.incrementNextChunkDataFromServerCounter() #Moved to above the except statement
                    #make a chunk object to send to the controller
                    tempChunk= Chunk.Chunk()
                    #set params
                    tempChunk.params = completeData
                    #set data
                    tempChunk.data = inputData
                    #send doignSTuff command to controller
                    sendDoingStuffCommandToController(self)
                    #send the chunk to the controller
                    sendNextChunkCommandToController(self,tempChunk)
                    #break #keep, this is part of the new code, NOT part of the old code moved from prev revision
                else: #then it is an unknown command
                    print "Unknown command received from the server: " + str(completeData) +"\n"
                    self.incrementUnknownCommandFromServerCounter()
                    #break
        except Exception as inst:
            if(compareString(str(inst),"timed out",0,0,len("timed out"), len("timed out"))==True):
                #dont display the timed out message
                fakeVar=True
            else:
                print "Exception in receive data: " + str(inst) +"\n"
                #break
        return completeData #if data is empty string, nothing was received

def sendData(self,networkSocket, serverIP, outboundMessage): #return true if you need to break out of main client loop, else false
    print "Sending message to Server: " +str(serverIP) +"\n"
    #networkSocket.settimeout(0.5)
    while True:
        try:
            networkSocket.sendto(outboundMessage, serverIP)
            print "sent data: " +str(outboundMessage) + " to server: " +str(serverIP) +"\n"
            if(compareString(outboundMessage,"NEXT",0,0,len("NEXT"),len("NEXT"))==True):
                self.incrementNextCommandToServerCounter()
            elif(compareString(outboundMessage,"FOUNDSOLUTION",0,0,len("FOUNDSOLUTION"),len("FOUNDSOLUTION"))==True):
                self.incrementFoundSolutionCommandToServerCounter()
            elif(compareString(outboundMessage,"CRASHED",0,0,len("CRASHED"),len("CRASHED"))==True):
                self.incrementCrashedCommandToServerCounter()
            return False
            #break
        except Exception as inst:
            if(compareString(str(inst),"[Errno 32] Broken pipe",0,0,len("[Errno 32] Broken pipe"),len("[Errno 32] Broken pipe"))):
                print "Broken pipe error detected in sendData\n"
                return True
            else:
                print "Exception in send data: " +str(inst) +"\n"
                return False

def sendNextChunkCommandToServer(self, networkSocket):
    try:
        print "Sending nextChunk Command to Server\n"
        networkSocket.send("NEXT " + str(self.myIPAddress))
        self.incrementNextCommandToServerCounter()
    except Exception as inst:
        print "Exception thrown in sendNextChunkCommandToServer: " + str(inst)+"\n"

def sendFoundSolutionCommandToServer(self, networkSocket):
    try:
        print "Sending foundSolution Command to Server\n"
        networkSocket.send("FOUNDSOLUTION")
        self.incrementFoundSolutionCommandToServerCounter()
    except Exception as inst:
        print "Exception thrown in sendFoundSolutionCommandToServer: "+ str(inst)+"\n"

def sendCrashedCommandToServer(self, networkSocket):
    try:
        print "Sending Crashed Command to Server\n"
        networkSocket.send("CRASHED " + self.myIPAddress)
        self.incrementCrashedCommandToServerCounter()
    except Exception as inst:
        print "Exception thrown in the sendCrashedCommandToServer: "+str(inst)+"\n"

def checkForDoneCommandFromServer(self,inboundString):
    try:
        print "Checking for done command from server\n"
        if(compareString(inboundString,"done",0,0,len("done"),len("done"))==True):
            print "Done command was received from the server\n"
            self.incrementDoneCommandFromServerCounter()
            self.serverIssuedDoneCommand = True
            return True
        else:
            return False
    except Exception as inst:
        print "ERROR in checkForDoneCommandFromServer: " + str(inst) +"\n"
        return False

def checkForNextChunkParamsFromServer(self, inboundString):
    try:
        print "Checking for next chunk params from the server\n"
        if(compareString(inboundString,"NEXT",0,0,len("NEXT"),len("NEXT"))==True):
            print "Received the Next Chunk Params from Server\n"
            self.incrementNextChunkParamsFromServerCounter()
            return True
        else:
            return False
    except Exception as inst:
        print "ERROR in checkForNextChunkParamsFromServer: " +str(inst) +"\n"
        return False

def checkForNextChunkDataFromServer(self, inboundString):
    try:
        print "Checking for next chunk data from the server\n"
        if(compareString(inboundString,"nextChunkData",0,0,len("nextChunkData"),len("nextChunkData"))==True): #might omit this check
            print "Received the Next Chunk Data from Server\n"
            self.incrementNextChunkDataFromServerCounter()
            return  True
        else:
            return False
    except Exception as inst:
        print "ERROR in checkForNextChunkDataFromServer: " + str(inst) +"\n"
        return False

def sendNextChunkCommandToController(self, inboundChunk):
    try:
        print "Sending nextChunk Command to the Controller\n"
        self.pipe.send(inboundChunk)
        self.incrementNextChunkCommandToControllerCounter()
    except Exception as inst:
        print "ERROR in sendNextChunkCommandToController: " + str(inst)+"\n"

def sendDoneCommandToController(self):
    try:
        print "Sending done Command to the Controller\n"
        self.pipe.send("done")
        self.incrementDoneCommandToControllerCounter()
    except Exception as inst:
        print "ERROR in sendDoneCommandToController: " + str(inst)+"\n"

def sendConnectedCommandToController(self):
    try:
        print "Sending connected Command to the Controller\n"
        self.pipe.send("connected")
        self.incrementConnectedCommandToControllerCounter()
    except Exception as inst:
        print "ERROR in sendConnectedCommandToController: " + str(inst)+"\n"

def sendDoingStuffCommandToController(self):
    try:
        print "Sending doingStuff Command to the Controller\n"
        self.pipe.send("doingStuff")
        self.incrementDoingStuffCommandToControllerCounter()
    except Exception as inst:
        print "ERROR in sendDoingStuffCommandToController: " + str(inst)+ "\n"

def receiveServerIPFromController(self):
    try:
        print "Receiving the server IP from the Controller\n"
        self.serverIP= self.pipe.recv()
        self.incrementReceiveServerIPFromControllerCounter()
    except Exception as inst:
        print "ERROR in receiveServerIPFromController: " + str(inst) + "\n"

def checkForDoneCommandFromController(self, inboundString):
    try:
        print "Checking for done command from the Controller\n"
        if(compareString(inboundString, "done",0,0,len("done"), len("done"))==True):
            self.incrementDoneCommandFromControllerCounter()
            return True
        else:
            return False
    except Exception as inst:
        print "ERROR in checkingForDoneCommandFromController: " +str(inst)+"\n"
        return False

def checkForDoingStuffCommandFromController(self, inboundString):
    try:
        print "Checking for doingStuff Command from the Controller\n"
        if(compareString(inboundString,"doingStuff",0,0,len("doingStuff"),len("doingStuff"))==True):
            self.incrementDoingStuffCommandFromControllerCounter()
            return True
        else:
            return False
    except Exception as inst:
        print "ERROR in checkForDoingStuff Command from the Controller: " + str(inst) +"\n"
        return False

def checkForFoundSolutionCommandFromController(self, inboundString):
    try:
        print "Checking for foundSolution Command from the Controller\n"
        if(compareString(inboundString,"foundSolution",0,0,len("foundSolution"),len("foundSolution"))==True):
            self.incrementFoundSolutionCommandFromControllerCounter()
            return True
        else:
            return False
    except Exception as inst:
        print "ERROR in checkForFoundSolutionCommandFromController: " + str(inst) +"\n"
        return False

def checkForRequestNextChunkCommandFromController(self, inboundString):
    try:
        print "Checking for requestNextChunk Command from the Controller\n"
        if(compareString(inboundString,"requestNextChunk",0,0,len("requestNextChunk"),len("requestNextChunk"))==True):
            self.incrementRequestNextChunkCommandFromControllerCounter()
            return True
        else:
            return False
    except Exception as inst:
        print "ERROR in checkForRequestNextChunk Command from Controller: " + str(inst) +"\n"
        return False

class NetworkClient():

    numOfParamsWithExtraData = 0

    #client records-------
    #outbound commands sent to server
    nextCommandToServerCounter = 0
    foundSolutionCommandToServerCounter = 0
    crashedCommandToServerCounter = 0

    #inbound commands from server
    doneCommandFromServerCounter = 0
    nextChunkParamsFromServerCounter = 0
    nextChunkDataFromServerCounter = 0
    unknownCommandFromServerCounter = 0

    #outbound commands sent to controller
    nextChunkCommandToControllerCounter = 0
    doneCommandToControllerCounter = 0
    connectedCommandToControllerCounter = 0
    doingStuffCommandToControllerCounter = 0

    #inbound commands from controller
    receiveServerIPFromControllerCounter = 0
    doneCommandFromControllerCounter = 0
    doingStuffCommandFromControllerCounter = 0
    foundSolutionCommandFromControllerCounter = 0
    requestNextChunkCommandFromControllerCounter = 0
    unknownCommandFromControllerCounter = 0

    #considering putting in a counter for number of exceptions thrown (for each exception type)
        #counter for how many times you have broken out of the main loop and not received the done command

    #increment counter functions
    def incrementNextCommandToServerCounter(self):
        self.nextCommandToServerCounter += 1

    def incrementFoundSolutionCommandToServerCounter(self):
        self.foundSolutionCommandToServerCounter+= 1

    def incrementCrashedCommandToServerCounter(self):
        self.crashedCommandToServerCounter+= 1

    def incrementDoneCommandFromServerCounter(self):
        self.doneCommandFromServerCounter+= 1

    def incrementNextChunkParamsFromServerCounter(self):
        self.nextChunkParamsFromServerCounter+= 1

    def incrementNextChunkDataFromServerCounter(self):
        self.nextChunkDataFromServerCounter+= 1

    def incrementUnknownCommandFromServerCounter(self):
        self.unknownCommandFromServerCounter+= 1

    def incrementNextChunkCommandToControllerCounter(self):
        self.nextChunkCommandToControllerCounter+= 1

    def incrementDoneCommandToControllerCounter(self):
        self.doneCommandToControllerCounter+= 1

    def incrementConnectedCommandToControllerCounter(self):
        self.connectedCommandToControllerCounter+= 1

    def incrementDoingStuffCommandToControllerCounter(self):
        self.doingStuffCommandToControllerCounter+= 1

    def incrementReceiveServerIPFromControllerCounter(self):
        self.receiveServerIPFromControllerCounter+= 1

    def incrementDoneCommandFromControllerCounter(self):
        self.doneCommandFromControllerCounter+= 1

    def incrementDoingStuffCommandFromControllerCounter(self):
        self.doingStuffCommandFromControllerCounter+= 1

    def incrementFoundSolutionCommandFromControllerCounter(self):
        self.foundSolutionCommandFromControllerCounter+= 1

    def incrementRequestNextChunkCommandFromControllerCounter(self):
        self.requestNextChunkCommandFromControllerCounter+= 1

    def incrementUnknownCommandFromControllerCounter(self):
        self.unknownCommandFromControllerCounter+= 1
    #end of increment counter functions

    def __init__(self, pipeendconnectedtocontroller):
        self.pipe = pipeendconnectedtocontroller #pipe to the controller
        try: #Main try block
            self.host = '' #new connection method
            self.port = 55568
            buf = 1024
            self.serverIP = '127.0.1.1'
            self.myIPAddress = ""
            self.listOfUnknownCommandsFromController = []
            self.serverIssuedDoneCommand= False

            #.........................................................................
            #Detect the Operating System
            #.........................................................................
            try: #getOS try block
                print "*************************************"
                print "    Network Client"
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
            #......................................
            #End of detect OS
            #......................................

            #.........................................................................
            #Retrieve the local network IP Address
            #.........................................................................
            try: #getIP tryblock
                print "STATUS: Getting your network IP adddress"
                if(platform.system()=="Windows"):
                    self.myIPAddress = socket.gethostbyname(socket.gethostname())
                    print self.myIPAddress
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
                    self.myIPAddress= get_lan_ip()
                    print self.myIPAddress
                elif(platform.system()=="Darwin"):
                    self.myIPAddress = socket.gethostbyname(socket.gethostname())
                    print self.myIPAddress
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

            clientsocket = socket.socket(AF_INET, SOCK_STREAM) #new create socket method
            try:
                receiveServerIPFromController(self) #NEW AUTOMATED METHOD
                print "Received IP Address from the Controller: '"+ str(self.serverIP)+"'\n"
            except Exception as inst:
                print "ERROR in get serverIP try block: " + str(inst) + "\n"
            try:
                clientsocket.connect((self.serverIP, self.port))
                print "Connected to server\n"
                sendConnectedCommandToController(self)
            except Exception as inst:
                print "ERROR in connect to server: " + str(inst) +"\n"
            data = "" #initialize data
            while True: #client main loop
                #receiveData(self, clientsocket) #old method of checking for server commands
                print "Checking for inbound network data\n"
                clientsocket.settimeout(0.5)
                data = ""
                completeData = ""
                try: #receive data try block
                    #while True:
                    try: #recv try block
                        while True:
                            data = clientsocket.recv(2048)
                            if data:
                                completeData+= data
                                clientsocket.settimeout(0.5)
                            else:
                                break
                    except Exception as inst:
                        if(compareString(str(inst),"timed out",0,0,len("timed out"),len("timed out"))==True):
                            #dont display the time out error
                            fakeVar=True
                        else:
                            print "Error in recv from clientsocket: " +str(inst)+"\n"
                        #if data:
                         #   completeData+= data
                          #  networkSocket.settimeout(0.5)
                       # else:
                        #    break
                    if(len(completeData) < 1):
                        #empty string, ignore it
                        fakeVar=True
                        #print "received empty string\n"
                    else: #not empty string
                        #print "received data: " + str(data) +"\n" #something is logically wrong with the check for done command
                        if(checkForDoneCommandFromServer(self,str(completeData))==True):
                            print "Server has issued the done command\n"
                            sendDoneCommandToController(self)
                            #break
                        elif(checkForNextChunkParamsFromServer(self, str(completeData))==True):
                            print "Received Next Chunk Params From Server\n"
                            #insert chunk assembling process here
                            dataChunkFileSize = ""
                            closingParenthesisLocation = 0
                            #end of file size is marked by a closing parenthesis
                            #position [0:4] = 'NEXT'
                            #position [5:9] = 'SIZE('
                            for index in range(10,len(completeData)):
                                if(completeData[index] == ")"):
                                    closingParenthesisLocation = index
                                    break
                                else:
                                    dataChunkFileSize+= str(completeData[index])
                            #removing keywords from the params
                            completeData= completeData[(closingParenthesisLocation+2):len(completeData)]
                            #print "data after keywords where removed from front: "+str(completeData)+"\n"
                            #remove extra code from after the params message and store it. So we can add it to the inbound data
                            #there are 9 legal spaces in the params
                            numOfSpaces = 0
                            overFlowParams = "" #stores the extra data at the end of the params that shouldnt be there
                            firstInvalidCharPosition = 0
                            print "checking for extra data in the params\n"
                            for x in range(0,len(completeData)):
                                if(numOfSpaces < 10):
                                    if(completeData[x].isspace()):
                                        numOfSpaces+= 1
                                    elif(x == len(completeData)):
                                        break
                                    else:
                                        firstInvalidCharPosition = x
                                        break
                            #copy the rest into overflowParams
                            if(firstInvalidCharPosition > 0):
                                self.numOfParamsWithExtraData+= 1
                                print "checking first char is a space\n"
                                if(completeData[x].isspace()):
                                    print"adding 1 to var to compensate for detected space\n"
                                    firstInvalidCharPosition+= 1
                                print "copying excess data from params into overflow\n"
                                overFlowParams= completeData[firstInvalidCharPosition:len(completeData)]
                                print "removing extra data from params\n"
                                completeData = completeData[0, firstInvalidCharPosition]
                                print "complete data after params cleanup: "+str(completeData)+"\n"
                            else:
                                print "no extra data was detected in the params\n"
                            inputData  = ""
                            recvData = ""
                            #receive the chunk data from the server
                            #clientsocket.settimeout(0.5)
                            try:
                                import sys
                                print "dataChunkFileSize: " +str(dataChunkFileSize)+"\n"
                                while(sys.getsizeof(inputData) < dataChunkFileSize):
                                    if(sys.getsizeof(inputData >= dataChunkFileSize)):
                                        break
                                    else:
                                        recvData = clientsocket.recv(4096)
                                        #if(inputData >= dataChunkFileSize):
                                         #   break
                                        if recvData:
                                            inputData+= recvData
                                            clientsocket.settimeout(0.5) #reset the socket timeout
                                        else:
                                            break
                                self.incrementNextChunkDataFromServerCounter()
                            except Exception as inst:
                                if(compareString(str(inst),"timed out",0,0,len("timed out"),len("timed out"))==True):
                                    print "ERROR in receiving chunk data from the server: timed out\n"
                                    print "dataChunkFileSize: "+ str(dataChunkFileSize)+"\n"
                                    print "Size of inputData: " + str(sys.getsizeof(inputData)) +"\n"
                                    print "Size of recvData: " + str(sys.getsizeof(recvData))+"\n"
                                else:
                                    print "Error in receiving chunk data from server: " +str(inst)+"\n"
                            if(len(overFlowParams) > 0):
                                print "adding overflow params to from of dataChunk\n"
                                inputData= str(overFlowParams) + str(inputData)
                                #print "inputData after adding overflowparams: "+str(inputData)+"\n"
                            #self.incrementNextChunkDataFromServerCounter() #Moved to above the except statement
                            #make a chunk object to send to the controller
                            tempChunk= Chunk.Chunk()
                            #set params
                            tempChunk.params = completeData
                            #set data
                            tempChunk.data = inputData
                            #send doignSTuff command to controller
                            sendDoingStuffCommandToController(self)
                            #send the chunk to the controller
                            sendNextChunkCommandToController(self,tempChunk)
                            #break #keep, this is part of the new code, NOT part of the old code moved from prev revision
                        else: #then it is an unknown command
                            print "Unknown command received from the server: " + str(completeData) +"\n"
                            self.incrementUnknownCommandFromServerCounter()
                            #break
                except Exception as inst:
                    if(compareString(str(inst),"timed out",0,0,len("timed out"), len("timed out"))==True):
                        #dont display the timed out message
                        fakeVar=True
                    else:
                        print "Exception in receive data: " + str(inst) +"\n"
                        #break
            #end communication with Network Server
            #communication with Controller
                print "Checking for controller commands...\n"
                if(self.pipe.poll()):
                    inboundControllerCommand= self.pipe.recv()
                    if(len(inboundControllerCommand) < 1):
                        print "received empty string, ignoring it\n"
                    else:
                        print "Received a Command from the Controller\n"
                        if(checkForFoundSolutionCommandFromController(self, inboundControllerCommand)==True):
                            print "foundSolution Command has been received from Controller\n"
                            sendFoundSolutionCommandToServer(self, clientsocket)
                        elif(checkForRequestNextChunkCommandFromController(self,inboundControllerCommand)==True):
                            print "requestNextChunk Command has been received from Controller\n"
                            sendNextChunkCommandToServer(self, clientsocket)
                        elif(checkForDoingStuffCommandFromController(self,inboundControllerCommand)==True):
                            print "doingStuff Command has been received from Controller\n"
                            #controller has parroted the command back, dont do anything
                        elif(checkForDoneCommandFromController(self, inboundControllerCommand)==True):
                            print "done command has been received from the Controller\n"
                            #just a confirmation message
                        else:
                            print "ERROR: unknown command received from Controller: " +str(inboundControllerCommand) +"\n"
                            self.incrementUnknownCommandFromControllerCounter()
                            self.listOfUnknownCommandsFromController.append(inboundControllerCommand)
            #end communication with controller
        except Exception as inst:
            print "ERROR in main try block: " + str(inst) +"\n"
        finally:
            if(self.serverIssuedDoneCommand==False):
                print "WARNING: Quitting before server has issued the Done Command! Sending Crash message to server\n"
                sendCrashedCommandToServer(self, clientsocket)
            clientsocket.close()
            print "Socket has been closed\n"
            print "----------------------numOfParamsWithExtraData--------------------\n"
            print "# of Chunk Params with Extra Data attached to the end (had to fix these): "+ str(self.numOfParamsWithExtraData)+"\n"
            print "----------------------Outbound Commands To Server-----------------\n"
            print "# of Next Commands Sent To Server: " + str(self.nextCommandToServerCounter) +"\n"
            print "# of Found Solution Commands Sent To Server: " +str(self.foundSolutionCommandToServerCounter) +"\n"
            print "# of Crashed  Commands Sent To Server: " + str(self.crashedCommandToServerCounter) +"\n"
            print "----------------------Inbound Commands From Server----------------\n"
            print "# of Done Commands Received From Server: " + str(self.doneCommandFromServerCounter) +"\n"
            print "# of next Chunk Params Received From Server: " + str(self.nextChunkParamsFromServerCounter) +"\n"
            print "# of next Chunk Data Received From Server: " + str(self.nextChunkDataFromServerCounter) + "\n"
            print "# of Unknown Commands Received From Server: " + str(self.unknownCommandFromServerCounter) +"\n"
            print "----------------------Outbound Commands To Controller---------------------\n"
            print "# of next Chunk Commands Sent to Controller: " + str(self.nextChunkCommandToControllerCounter) + "\n"
            print "# of Done Commands Sent To Controller: " + str(self.doneCommandToControllerCounter) + "\n"
            print "# of Connected Commands Sent to Controller: " + str(self.connectedCommandToControllerCounter) +"\n"
            print "# of doingStuff Commands Sent to Controller: " + str(self.doingStuffCommandToControllerCounter) +"\n"
            print "----------------------Inbound Commands From Controller-----------------------\n"
            print "# of Receive Server IP From Controller Commands: " + str(self.receiveServerIPFromControllerCounter) +"\n"
            print "# of done Commands Received from Controller: " +str(self.doneCommandFromControllerCounter)+"\n"
            print "# of doingStuff Commands Received From Controller: " + str(self.doingStuffCommandFromControllerCounter) +"\n"
            print "# of foundSolution Commands Received From Controller: " + str(self.foundSolutionCommandFromControllerCounter)+"\n"
            print "# of requestNextChunk Commands Received From Controller: " + str(self.requestNextChunkCommandFromControllerCounter)+"\n"
            print "# of unknown Commands Received From Controller: " + str(self.unknownCommandFromControllerCounter)+"\n"
            if(len(self.listOfUnknownCommandsFromController) > 0):
                for index in range(0, len(self.listOfUnknownCommandsFromController)):
                    print "     " + str(index) + ") " + str(self.listOfUnknownCommandsFromController[index]) +"\n"


