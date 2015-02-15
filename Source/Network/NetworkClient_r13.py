__author__ = 'chris hamm'
#NetworkClient_r13
#created: 2/10/2015

#Designed to work with NetworkServer_r13

#REVISION NOTES:
    #Moving to a more modular style, no master receive or send function.
    #

#By recommendation, implement without the command logs

def receiveCommandFromServer(self, clientSocket): #NOTE used for normal recv
    try:
        receivedCommand= ""
        #print "Checking for command from the server\n"
        serverInput= clientSocket.recv(4096)
        if(len(serverInput) > 0):
            receivedCommand= serverInput
        return receivedCommand
    except Exception as inst:
        if(compareString(str(inst),"timed out",0,0,len("timed out"),len("timed out"))==True):
            #Do not display the error message
            fakeVar=True
            return ""
        else:
            print "===================================================================\n"
            print "ERROR in receiveCommandFromServer: "+str(inst)+"\n"
            print "===================================================================\n"
            return "" #the empty string

#FUNCTIONS=========================================================================================
#CompareString function-----------------------------------------
def compareString(inboundStringA, inboundStringB, startA, startB, endA, endB):
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

#Inbound commands from controller functions-----------------------------------------
def receiveServerIPFromController(self):
    try:
        print "Receiving the server IP from the Controller\n"
        tempServerIP= self.pipe.recv()
        print "Received the server IP from the controller\n"
        return tempServerIP
    except Exception as inst:
        print "===================================================================\n"
        print "ERROR in receiveServerIPFromController: " + str(inst) + "\n"
        print "===================================================================\n"
        return ""

def checkForDoneCommandFromController(self, inboundString):
    try:
        print "Checking for done command from the Controller\n"
        if(compareString(inboundString, "done",0,0,len("done"), len("done"))==True):
            print "Received the done command from the controller\n"
            return True
        else:
            return False
    except Exception as inst:
        print "===================================================================\n"
        print "ERROR in checkingForDoneCommandFromController: " +str(inst)+"\n"
        print "===================================================================\n"
        return False

def checkForDoingStuffCommandFromController(self, inboundString):
    try:
        print "Checking for doingStuff Command from the Controller\n"
        if(compareString(inboundString,"doingStuff",0,0,len("doingStuff"),len("doingStuff"))==True):
            print "Received doingSTuff COmmand from the COntroller\n"
            return True
        else:
            return False
    except Exception as inst:
        print "===================================================================\n"
        print "ERROR in checkForDoingStuff Command from the Controller: " + str(inst) +"\n"
        print "===================================================================\n"
        return False

def checkForFoundSolutionCommandFromController(self, inboundString):
    try:
        print "Checking for foundSolution Command from the Controller\n"
        if(compareString(inboundString,"foundSolution",0,0,len("foundSolution"),len("foundSolution"))==True):
            print "Received foundSolution command from the controller\n"
            return True
        else:
            return False
    except Exception as inst:
        print "===================================================================\n"
        print "ERROR in checkForFoundSolutionCommandFromController: " + str(inst) +"\n"
        print "===================================================================\n"
        return False

def checkForRequestNextChunkCommandFromController(self, inboundString):
    try:
        print "Checking for requestNextChunk Command from the Controller\n"
        if(compareString(inboundString,"requestNextChunk",0,0,len("requestNextChunk"),len("requestNextChunk"))==True):
            print "Received requestNextChunk Command from the controller\n"
            return True
        else:
            return False
    except Exception as inst:
        print "===================================================================\n"
        print "ERROR in checkForRequestNextChunk Command from Controller: " + str(inst) +"\n"
        print "===================================================================\n"
        return False

#Outbound commands to controller functions----------------------------------------
def sendNextChunkCommandToController(self, inboundChunk):
    try:
        print "Sending nextChunk Command to the Controller\n"
        self.pipe.send(inboundChunk)
        print "Sent nextChunk Command to the controller\n"
    except Exception as inst:
        print "===================================================================\n"
        print "ERROR in sendNextChunkCommandToController: " + str(inst)+"\n"
        print "===================================================================\n"

def sendDoneCommandToController(self):
    try:
        print "Sending done Command to the Controller\n"
        self.pipe.send("done")
        print "Sent done Command to the controller\n"
    except Exception as inst:
        print "===================================================================\n"
        print "ERROR in sendDoneCommandToController: " + str(inst)+"\n"
        print "===================================================================\n"

def sendConnectedCommandToController(self):
    try:
        print "Sending connected Command to the Controller\n"
        self.pipe.send("connected")
        print "Sent connected command to the controller\n"
    except Exception as inst:
        print "===================================================================\n"
        print "ERROR in sendConnectedCommandToController: " + str(inst)+"\n"
        print "===================================================================\n"

def sendDoingStuffCommandToController(self):
    try:
        print "Sending doingStuff Command to the Controller\n"
        self.pipe.send("doingStuff")
        print "Sent doingSTuff Command to the Controller\n"
    except Exception as inst:
        print "===================================================================\n"
        print "ERROR in sendDoingStuffCommandToController: " + str(inst)+ "\n"
        print "===================================================================\n"

#Inbound commands from server functions----------------------------------------
def checkForDoneCommandFromServer(self,inboundString):
    try:
        print "Checking for done command from server\n"
        if(compareString(inboundString,"done",0,0,len("done"),len("done"))==True):
            print "Done command was received from the server\n"
            self.serverIssuedDoneCommand = True
            return True
        else:
            return False
    except Exception as inst:
        print "===================================================================\n"
        print "ERROR in checkForDoneCommandFromServer: " + str(inst) +"\n"
        print "===================================================================\n"
        return False

def checkForNextCommandFromServer(self, inboundString): #NOTE: Different than previous revisions, this only checks for the NEXT keyword
    try:
        print "Checking for nextCommand from server\n"
        if(compareString(inboundString,"NEXT",0,0,len("NEXT"),len("NEXT"))==True):
            print "Next Command was received from the server\n"
            return True
        else:
            return False
    except Exception as inst:
        print "===================================================================\n"
        print "ERROR in checking for nextCommand from the server: " +str(inst)+"\n"
        print "===================================================================\n"
        return False

def extractSizeOfParamFromNextCommand(self, inboundString): #NOTE: New component to extract the file size of the params from the next command
    try: #THIS can also extract the length of params from the next command
        print "Extracting size of Params from the next Command\n"
        firstOpenParenthesisPos= 0
        firstClosingParenthesisPos= 0
        sizeOfChunkParams = ""
        #Command layout: "NEXT PSIZE() DSIZE()"
        #Step 1: find the first Open Parenthesis, which immeadiately follows the PSIZE
        try: #step 1 try block
            print "Finding the first Open Parenthesis\n"
            for index in range(0,len(inboundString)):
                if(inboundString[index] == "("):
                    firstOpenParenthesisPos= index
                    break
            if(firstOpenParenthesisPos == 0):
                raise Exception("No open parenthesis was found")
        except Exception as inst:
            print "===================================================================\n"
            print "Exception thrown in Step 1: find first Open parenthesis: " +str(inst)+"\n"
            print "===================================================================\n"
            raise Exception ("Exception thrown in step 1 of extractSizeOfParamsFromNextCommand")
        #Step 2: find the corresponding closing parenthesis
        try: #Step 2 try block
            print "Finding the corresponding closing parenthesis\n"
            for index in range(firstOpenParenthesisPos, len(inboundString)):
                if(inboundString[index] == ")"):
                    firstClosingParenthesisPos= index
                    break
            if(firstClosingParenthesisPos == 0):
                raise Exception ("No closing parenthesis was found")
        except Exception as inst:
            print "===================================================================\n"
            print "Exception thrown in Step 2: find corresponding closing parenthesis: " +str(inst)+"\n"
            print "===================================================================\n"
            raise Exception ("Exception thrown in Step 2 of extractSizeOfParamsFromNextCommand")
        #Step 3: retreive the params file size
        try: #step 3 try block
            print "Retreiving the params file size\n"
            for index in range(firstOpenParenthesisPos+1,firstClosingParenthesisPos):
                sizeOfChunkParams+= str(inboundString[index])
            return sizeOfChunkParams
        except Exception as inst:
            print "===================================================================\n"
            print "Exception thrown in Step 3: retreive the params file size: "+str(inst)+"\n"
            print "===================================================================\n"
            raise Exception ("Exception thrown in Step 3 of extractSizeOfParamsFromNextCommand")
    except Exception as inst:
        print "===================================================================\n"
        print "ERROR in extractSizeOfParamsFromNextCommand: " +str(inst)+"\n"
        print "===================================================================\n"
        return 0 #return filesize of zero if there was an error

def extractSizeOfDataFromNextCommand(self, inboundString): #NOTE: this is a new component. This can also extract the length of Data from the next command
    try:
        print "Extracting size of data from next Command\n"
        firstOpenParenthesisPos = 0
        firstClosingParenthesisPos = 0
        sizeOfChunkData= ""
        #Command layout: NEXT PSIZE() DSIZE()
        #Step 1: find the 'D' in the inboundString
        try: #step 1 try block
            print "Finding the 'D' in the nextCommand\n"
            for index in range(0,len(inboundString)):
                if(inboundString[index] == "D"):
                    firstOpenParenthesisPos= index + 5 #plus five for the offset between the D and the first open parenthesis
                    break
            if(firstOpenParenthesisPos == 0):
                raise Exception ("No 'D' was found in the nextCommand")
        except Exception as inst:
            print "===================================================================\n"
            print "Exception thrown in Step 1: find the 'D' in the inboundString: "+str(inst)+"\n"
            print "===================================================================\n"
            raise Exception ("Exception was thrown in step 1 of extractSizeOfDataFromNextCommand")
        #Step 2: find the corresponding parenthesis
        try: #Step 2 try block
            print "Finding the corresponding parenthesis\n"
            for index in range(firstOpenParenthesisPos, len(inboundString)):
                if(inboundString[index] == ")"):
                    firstClosingParenthesisPos= index
                    break
            if(firstClosingParenthesisPos == 0):
                raise Exception ("No closing parenthesis found in the nextCommand")
        except Exception as inst:
            print "===================================================================\n"
            print "Exception thrown in Step 2: find corresponding parenthesis: "+str(inst)+"\n"
            print "===================================================================\n"
            raise Exception ("Exception thrown in step 2 of extractSizeOfDataFromNextCommand")
        #Step 3: retreive the data file size
        try: #step 3 try block
            print "Retrieving data file size\n"
            for index in range(firstOpenParenthesisPos+1,firstClosingParenthesisPos):
                sizeOfChunkData+= str(inboundString[index])
            return sizeOfChunkData
        except Exception as inst:
            print "===================================================================\n"
            print "Exception thrown in Step 3: retrieve the data file size: " + str(inst)+"\n"
            print "===================================================================\n"
            raise Exception ("Exception thrown is step 3 of extractSizeOfDataFromNextCommand")
    except Exception as inst:
        print "===================================================================\n"
        print "ERROR in extractSizeOfDataFromNextCommand: " +str(inst)+"\n"
        print "===================================================================\n"
        return 0

def receivePieceOfChunkFromServerByLength(self, lengthOfChunkComponent, networkSocket): #NOTE: this method receives pieces of chunks by their lengths rather than thier filesizes
    try:
        receivedPieceOfChunk = ""
        print "Receiving Piece of CHunk From The Server By Length\n"
        print "Length of PieceOfChunk: "+str(lengthOfChunkComponent)+"\n"
        networkSocket.settimeout(2.0)
        import sys
        while(len(receivedPieceOfChunk) < lengthOfChunkComponent):
            try:
                receivedPieceOfChunk+= str(networkSocket.recv(4096))
                if(len(receivedPieceOfChunk) >= lengthOfChunkComponent):
                    break
                elif not receivedPieceOfChunk:
                    break
                else:
                    print "Length of receivedPieceOfChunk:"+str(len(receivedPieceOfChunk))+"\n"
                    if(len(receivedPieceOfChunk) < lengthOfChunkComponent):
                        #not finished yet
                        fakeVar=True
                        #if(networkSocket.gettimeout() >= 5.0):
                         #   print "Timeout at limit of 5 seconds, no extension will be given\n"
                        #else:
                         #   print "Extending the socket timeout\n"
                          #  networkSocket.settimeout(networkSocket.gettimeout()+0.125)
                          #  print "Socket timeout now set to: " +str(networkSocket.gettimeout())+"\n"
                    else:
                        break
            except Exception as inst:
                if(compareString(str(inst),"timed out",0,0,len("timed out"),len("timed out"))==True):
                    #dont throw error, just keep on receiving
                    print "socket timed out\n"
                    #fakeVar=True
                    break
                else:
                    raise Exception ("Error in receivePieceOfChunkFromServerByLength infinite while loop")
                    break
        if(len(receivedPieceOfChunk) < 1):
            raise Exception ("receivedPieceOfChunk is the empty string!")
        elif(len(receivedPieceOfChunk) < int(lengthOfChunkComponent)):
            raise Exception ("Not all of the Piece of chunk was received\n receivedPieceOfChunk length:"+str(len(receivedPieceOfChunk))+"")
        else:
            print "Finished receiving Piece of chunk from the server. length of receivedPieceOfChunk:"+str(len(receivedPieceOfChunk))+"\n"
    except Exception as inst:
        print "===================================================================\n"
        print "ERROR in receivePieceOfChunkFromServerByLength: "+str(inst)+"\n"
        print "===================================================================\n"
    finally:
        networkSocket.settimeout(0.25)
        print "Socket timeoutout was reset back to default\n"
        return receivedPieceOfChunk

def receivePieceOfChunkFromServer(self, pieceOfChunkFileSize, networkSocket): #NOTE: New component, call this for receiving params or for receiving data
    try:
        receivedPieceOfChunk= ""
        print "Receiving Piece Of Chunk From The Server\n"
        #adjust receive size depending on amount to be received
        presetRecvValue= 0
        if(pieceOfChunkFileSize < 1024):
            presetRecvValue= 256
            print "Using pre-setRecvValue of: 256\n"
        elif(pieceOfChunkFileSize < 4096):
            presetRecvValue= 1024
            print "Using pre-setRecvValue of: 1024\n"
        else:
            presetRecvValue= 4096
            print "Using pre-setRecvValue of: 4096\n"
        print "PieceOfChunkFileSize: "+str(pieceOfChunkFileSize)+"\n"
        import sys
        while(sys.getsizeof(receivedPieceOfChunk) < pieceOfChunkFileSize):
            #try: #recieve try block
            try:
                #print "Current fileSize of receivedPieceOfChunk: "+str(sys.getsizeof(receivedPieceOfChunk))+"\n"
                recvInfo= networkSocket.recv(presetRecvValue)
                if recvInfo:
                    receivedPieceOfChunk+= str(recvInfo)
                else:
                    break
            except Exception as inst:
                if(compareString(str(inst),"timed out",0,0,len("timed out"),len("timed out"))==True):
                    #dont throw an error, keep trying
                    fakeVar=True
                else:
                    raise Exception ("Error in receivePieceOfChunkFrom Server recv try block")
                    break
        if(len(receivedPieceOfChunk) < 1):
            raise Exception ("receivedPieceOfChunk is empty!")
        elif(sys.getsizeof(receivedPieceOfChunk) < pieceOfChunkFileSize):
            raise Exception ("Did not receive all of the Piece of Chunk")
    except Exception as inst:
        print "===================================================================\n"
        print "ERROR in receivePieceOfChunkFromServer: "+str(inst)+"\n"
        print "===================================================================\n"
    finally:
        print "complete receivedPieceOfChunk: "+str(receivedPieceOfChunk)+"\n"
        return receivedPieceOfChunk



#Outbound commands to server functions--------------------------------------
def sendNextChunkCommandToServer(self, networkSocket):
    try:
        print "Sending nextChunk Command to Server\n"
        networkSocket.send("NEXT " + str(self.myIPAddress))
        print "Sent the nextChunk Command to the server\n"
    except Exception as inst:
        print "===================================================================\n"
        print "Exception thrown in sendNextChunkCommandToServer: " + str(inst)+"\n"
        print "===================================================================\n"

def sendFoundSolutionCommandToServer(self, networkSocket):
    try:
        print "Sending foundSolution Command to Server\n"
        networkSocket.send("FOUNDSOLUTION")
        print "Sent FoundSOlution Command to the server\n"
    except Exception as inst:
        print "===================================================================\n"
        print "Exception thrown in sendFoundSolutionCommandToServer: "+ str(inst)+"\n"
        print "===================================================================\n"

def sendCrashedCommandToServer(self, networkSocket):
    try:
        print "Sending Crashed Command to Server\n"
        networkSocket.send("CRASHED " + self.myIPAddress)
        print "Sent Crashed COmmand to the server\n"
    except Exception as inst:
        print "===================================================================\n"
        print "Exception thrown in the sendCrashedCommandToServer: "+str(inst)+"\n"
        print "===================================================================\n"




import socket
from socket import *
import Chunk
import platform

class NetworkClient():

    def __init__(self, inboundpipefromcontroller):
        self.pipe = inboundpipefromcontroller

        self.host = ''
        self.port = 55568
        self.myIPAddress = "127.0.0.1" #defualt to the ping back address
        self.serverIPAddress = "127.0.0.1" #default to the ping back address
        self.serverIssuedDoneCommand = False

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
        '''
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
        '''
        #.........................................................................
        #End of Retrieve the local network IP Address
        #.........................................................................
        import socket
        clientSocket = socket.socket(AF_INET, SOCK_STREAM)

        try: #receive the server ip from the controller
            self.serverIPAddress= receiveServerIPFromController(self)
        except Exception as inst:
            print "===================================================================\n"
            print "Error in receive server ip from the controller: "+(str(inst))+"\n"
            print "===================================================================\n"

        try: #connect to server try block
            clientSocket.connect((self.serverIPAddress, self.port))
            print "Connected to server\n"
            sendConnectedCommandToController(self)
        except Exception as inst:
            print "===================================================================\n"
            print "Error in connect to server try block: " + str(inst) +"\n"
            print "self.serverIPAddress= "+str(self.serverIPAddress)+"\n"
            print "self.port= "+str(self.port)+"\n"
            print "===================================================================\n"
            raise Exception ("Failed to connect to the server")

        #PRIMARY CLIENT WHILE LOOP
        try:
            clientSocket.settimeout(0.25)
            while True: #primary client while loop
                inboundCommandFromServer = "" #initialize the var
                #CHECK FOR INBOUND SERVER COMMANDS SECTION=============================================================
                try: #check for inbound server commands
                    print "Checking for inbound Commands From Server\n"
                    inboundCommandFromServer = receiveCommandFromServer(self, clientSocket)
                except Exception as inst:
                    print "===================================================================\n"
                    print "Error in check for inbound Server Commands Try block: "+str(inst)+"\n"
                    print "===================================================================\n"

                if(len(inboundCommandFromServer) > 0): #if not the empty string, perform the following checks
                    identifiedCommand = False
                    try: #check for the done command from the server
                        if(checkForDoneCommandFromServer(self,inboundCommandFromServer)==True):
                            identifiedCommand= True
                            print "Identified Command as the done command from the server\n"
                            print "Server has Issued the Done Command\n"
                            self.serverIssuedDoneCommand = True
                            break #break out of the main while loop
                    except Exception as inst:
                        print "===================================================================\n"
                        print "Error in checking for done command from the server: "+str(inst)+"\n"
                        print "===================================================================\n"

                    try: #check for nextChunk command from the server
                        if(identifiedCommand == False):
                            if(checkForNextCommandFromServer(self,inboundCommandFromServer)==True):
                                identifiedCommand= True
                                print "Identified Command as the nextChunk Command from the server\n"
                                #fileSizeOfChunkParams = extractSizeOfParamFromNextCommand(self,inboundCommandFromServer)
                                #print "fileSizeOfChunkParams: "+str(fileSizeOfChunkParams)+"\n"
                                #fileSizeOfChunkData = extractSizeOfDataFromNextCommand(self,inboundCommandFromServer)
                                #print "fileSizeOfChunkData: "+str(fileSizeOfChunkData)+"\n"
                                lengthOfChunkParams = extractSizeOfParamFromNextCommand(self, inboundCommandFromServer)
                                lengthOfChunkData = extractSizeOfDataFromNextCommand(self, inboundCommandFromServer)
                                #tempChunkParams = receivePieceOfChunkFromServer(self,fileSizeOfChunkParams, clientSocket)
                                tempChunkParams = receivePieceOfChunkFromServerByLength(self, lengthOfChunkParams, clientSocket)
                                #tempChunkData = receivePieceOfChunkFromServer(self,fileSizeOfChunkData, clientSocket)
                                tempChunkData = receivePieceOfChunkFromServerByLength(self, lengthOfChunkData, clientSocket)
                                outboundChunk = Chunk.Chunk()
                                outboundChunk.params = str(tempChunkParams)
                                outboundChunk.data = str(tempChunkData)
                                sendDoingStuffCommandToController(self) #notify controller that client will be sending a chunk to it
                                sendNextChunkCommandToController(self,outboundChunk)
                    except Exception as inst:
                        print "===================================================================\n"
                        print "Error in checking for nextChunk command from server: " + str(inst)+"\n"
                        print "===================================================================\n"

                    if(identifiedCommand == False):
                        print "Warning: Unknown command received from the server: "+str(inboundCommandFromServer)

                #CHECK FOR INBOUND CONTROLLER COMMANDS SECTION=======================================================
                receivedCommandFromController = "" #initialize thevar
                try: #check for inbound controller commands try block
                    print "Checking for Commands from the Controller\n"
                    if(self.pipe.poll()):
                        receivedCommandFromController= self.pipe.recv()
                        print "Received a Command from the controller\n"
                except Exception as inst:
                    print "===================================================================\n"
                    print "Error in check for inbound commands from controller try block: "+str(inst)+"\n"
                    print "===================================================================\n"

                if(len(receivedCommandFromController) > 0): #if not the empty string
                    identifiedCommand= False
                    try: #checking for found solution command from controller
                        if(checkForFoundSolutionCommandFromController(self, receivedCommandFromController)==True):
                            identifiedCommand = True
                            print "Identified Command as Found Solution Command from the controller\n"
                            sendFoundSolutionCommandToServer(self,clientSocket)
                    except Exception as inst:
                        print "===================================================================\n"
                        print "Error in check for found solution command from controller: "+str(inst)+"\n"
                        print "===================================================================\n"

                    try: #checking for request next chunk command from controller
                        if(identifiedCommand == False):
                            if(checkForRequestNextChunkCommandFromController(self,receivedCommandFromController)==True):
                                identifiedCommand= True
                                print "Identified Command as the requestNextChunk Command from the Controller\n"
                                sendNextChunkCommandToServer(self,clientSocket)
                    except Exception as inst:
                        print "===================================================================\n"
                        print "Error in check for request Next Chunk Command from controller: "+str(inst)+"\n"
                        print "===================================================================\n"

                    try: #check for doingStuff command form controller
                        if(identifiedCommand == False):
                            if(checkForDoingStuffCommandFromController(self,receivedCommandFromController)==True):
                                identifiedCommand= True
                                print "Identified Command as the doingStuff Command from the Controller\n"
                                #The controller parrots this message back to client, no action needed for this
                    except Exception as inst:
                        print "===================================================================\n"
                        print "Error in check for doingStuff Command from controller: "+str(inst)+"\n"
                        print "===================================================================\n"

                    try: #check for done command from the controller
                        if(identifiedCommand == False):
                            if(checkForDoneCommandFromController(self,receivedCommandFromController)==True):
                                identifiedCommand= True
                                print "Identified Command as the done Command from the Controller\n"
                                #This is just a confirmation message, no action is needed for this
                    except Exception as inst:
                        print "===================================================================\n"
                        print "Error in check for done command from the controller: "+str(inst)+"\n"
                        print "===================================================================\n"

                    if(identifiedCommand == False):
                        print "Warning: Received Unknown Command From The Controller: "+str(receivedCommandFromController)+"\n"
            #end of primary client while loop
        except Exception as inst:
            print "===================================================================\n"
            print "Error in Primary client while loop: "+str(inst)+"\n"
            print "===================================================================\n"
        finally:
            if(self.serverIssuedDoneCommand == False):
                try: #send crash message to server, if needed
                    print "Warning: Server has not issued the done command! Sending Crashed Command to the Server\n"
                    sendCrashedCommandToServer(self, clientSocket)
                except Exception as inst:
                    print "===================================================================\n"
                    print "Error in send crash message to server, in finally block: "+str(inst)+"\n"
                    print "===================================================================\n"
            print "Closing the client socket\n"
            clientSocket.close()
            print "Client Socket has been closed\n"
            sendDoneCommandToController(self)
            print "Informed Controller that Client is finished\n"

