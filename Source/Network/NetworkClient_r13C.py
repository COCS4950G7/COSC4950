__author__ = 'chris hamm'
#NetworkClient_r13C
#Created: 2/20/2015

#Designed to run with NetworkServer_r13C

#IMPORTANT!!!!!!!
    #THIS REVISION HAS BROKEN THE CRASH HANDLING SYSTEM OF SERVER, STILL RUNS THOUGH
    #INSIGNIFICANT SPEED BOOST FROM ADDING QUEUES TO THE CLIENTS
    #REV13B is stable and server still has queues which has a significant speed boost

#Changes to be made to this revision:
    #(Implemented) Add a queue of chunks so that when controller requests the next chunk, controller can work on a stored chunk, for slight speed improvements
    #(Implemented) When client connects to server initially, request for 2 chunks, 1 for crunch now, the other for crunch while waiting for next chunk
    #(Implemented) When client receives a chunk, store it in the queue
    #(Implemented) when controller requests for next chunk, give it a chunk from the queue, then request another chunk from the server



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
            addCommandToListOfIOCommands(self, "ERROR in receiveCommandFromServer", "Self", "Self")
            return "" #the empty string

#FUNCTIONS=========================================================================================
#List of Inbound Command Functions-------------------------------------------------------
def addCommandToListOfIOCommands(self, inboundCommandName, commandOrigin_Destination, directionOfCommand):  #command origin is who sent the command
    try:            #direction of command is inbound or outboound
        import time
        current_time= time.time()
        self.listOfIOCommands.append((inboundCommandName, commandOrigin_Destination, directionOfCommand, current_time)) #holds a tuple of command, origin of command, and time
    except Exception as inst:
        print "========================================================\n"
        print "Exception was thrown in addCommandToListOfIOCommands: "+str(inst)+"\n"
        print "========================================================\n"
        addCommandToListOfIOCommands(self, "EXCEPTION in addCommandToListOfIOCommands", "Self", "Self")


#CompareString function-----------------------------------------
def compareString(inboundStringA, inboundStringB, startA, startB, endA, endB):
    try:
        posA = startA
        posB = startB
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
       # print "Receiving the server IP from the Controller\n"
        tempServerIP= self.pipe.recv()
        #print "Received the server IP from the controller\n"
        addCommandToListOfIOCommands(self,"receiveServerIP", "Controller", "Inbound")
        return tempServerIP
    except Exception as inst:
        print "===================================================================\n"
        print "ERROR in receiveServerIPFromController: " + str(inst) + "\n"
        print "===================================================================\n"
        addCommandToListOfIOCommands(self, "ERROR in receiveServerIPFromController", "Controller", "Inbound")
        return ""

def checkForDoneCommandFromController(self, inboundString):
    try:
       # print "Checking for done command from the Controller\n"
        if(compareString(inboundString, "done",0,0,len("done"), len("done"))==True):
           # print "Received the done command from the controller\n"
            addCommandToListOfIOCommands(self,"done", "Controller", "Inbound")
            return True
        else:
            return False
    except Exception as inst:
        print "===================================================================\n"
        print "ERROR in checkingForDoneCommandFromController: " +str(inst)+"\n"
        print "===================================================================\n"
        addCommandToListOfIOCommands(self, "ERROR in checkingForDoneCommandFromController", "Controller", "Inbound")
        return False

def checkForDoingStuffCommandFromController(self, inboundString):
    try:
       # print "Checking for doingStuff Command from the Controller\n"
        if(compareString(inboundString,"doingStuff",0,0,len("doingStuff"),len("doingStuff"))==True):
            #print "Received doingSTuff COmmand from the COntroller\n"
            addCommandToListOfIOCommands(self, "doingStuff", "Controller", "Inbound")
            return True
        else:
            return False
    except Exception as inst:
        print "===================================================================\n"
        print "ERROR in checkForDoingStuff Command from the Controller: " + str(inst) +"\n"
        print "===================================================================\n"
        addCommandToListOfIOCommands(self, "ERROR in checkForDoingStuffCommandFromController", "Controller", "Inbound")
        return False

def checkForFoundSolutionCommandFromController(self, inboundString):
    try:
        #print "Checking for foundSolution Command from the Controller\n"
        if(compareString(inboundString,"foundSolution",0,0,len("foundSolution"),len("foundSolution"))==True):
            #print "Received foundSolution command from the controller\n"
            addCommandToListOfIOCommands(self, "foundSolution", "Controller", "Inbound")
            return True
        else:
            return False
    except Exception as inst:
        print "===================================================================\n"
        print "ERROR in checkForFoundSolutionCommandFromController: " + str(inst) +"\n"
        print "===================================================================\n"
        addCommandToListOfIOCommands(self, "ERROR in checkForFoundSolutionCommandFromController", "Controller", "Inbound")
        return False

def receiveSolutionFromController(self, networkSocket):
    while True:
        try:
            receivedSolution= ""
            controllerInput= self.pipe.recv()
            if(len(controllerInput) > 0):
                receivedSolution= controllerInput
                addCommandToListOfIOCommands(self, "receiveSolution", "Controller", "Inbound")
                #NOTE: This will cut off the string if the solution is too long
                import sys
                if(sys.getsizeof(receivedSolution) >= 4000):
                    print "----------------------------------------------------------------------------------------\n"
                    print "WARNING: size of solution is getting/or is too large. Max fileSize of solution is 4096.\n Your solution fileSize is: "+str(sys.getsizeof(receivedSolution))+"\n"
                    print "----------------------------------------------------------------------------------------\n"
                    addCommandToListOfIOCommands(self, "WARNING: size of solution is/getting to large", "Controller", "Inbound")
                return receivedSolution
                break
            else:
                #print "Waiting for Controller to send the solution\n"
                fakeVar=True
        except Exception as inst:
            if(compareString(str(inst),"timed out",0,0,len("timed out"),len("timed out"))==True):
                import sys
                if(sys.getsizeof(receivedSolution) > 0):
                    return receivedSolution
                    break
                else:
                    fakeVar=True
                    #print "The socket has timed out\n"
                    import sys
                    #print "size of receivedSolution: "+str(sys.getsizeof(receivedSolution))+"\n"
            else:
                print "===================================================================\n"
                print "ERROR in receiveSolutionFromController: "+str(inst)+"\n"
                print "===================================================================\n"
                addCommandToListOfIOCommands(self, "ERROR in receiveSolutionFromController", "Controller", "Inbound")
                return ""
                break

def checkForRequestNextChunkCommandFromController(self, inboundString):
    try:
       # print "Checking for requestNextChunk Command from the Controller\n"
        if(compareString(inboundString,"requestNextChunk",0,0,len("requestNextChunk"),len("requestNextChunk"))==True):
            #print "Received requestNextChunk Command from the controller\n"
            addCommandToListOfIOCommands(self, "requestNextChunk", "Controller", "Inbound")
            return True
        else:
            return False
    except Exception as inst:
        print "===================================================================\n"
        print "ERROR in checkForRequestNextChunk Command from Controller: " + str(inst) +"\n"
        print "===================================================================\n"
        addCommandToListOfIOCommands(self, "ERROR in checkForRequestNextChunkCommandFromController", "Controller", "Inbound")
        return False

#Outbound commands to controller functions-----------------------------------------------------
def sendNextChunkCommandToController(self, inboundChunk):
    try:
       # print "Sending nextChunk Command to the Controller\n"
        self.pipe.send(inboundChunk)
       # print "Sent nextChunk Command to the controller\n"
        addCommandToListOfIOCommands(self, "nextChunk", "Controller", "Outbound")
    except Exception as inst:
        print "===================================================================\n"
        print "ERROR in sendNextChunkCommandToController: " + str(inst)+"\n"
        print "===================================================================\n"
        addCommandToListOfIOCommands(self, "ERROR in sendNextChunkCommandToController", "Controller", "Outbound")

def sendDoneCommandToController(self):
    try:
       # print "Sending done Command to the Controller\n"
        self.pipe.send("done")
        #print "Sent done Command to the controller\n"
        addCommandToListOfIOCommands(self, "done", "Controller", "Outbound")
    except Exception as inst:
        print "===================================================================\n"
        print "ERROR in sendDoneCommandToController: " + str(inst)+"\n"
        print "===================================================================\n"
        addCommandToListOfIOCommands(self, "ERROR in sendDoneCommandToController", "Controller", "Outbound")

def sendConnectedCommandToController(self):
    try:
       # print "Sending connected Command to the Controller\n"
        self.pipe.send("connected")
       # print "Sent connected command to the controller\n"
        addCommandToListOfIOCommands(self, "connected", "Controller", "Outbound")
    except Exception as inst:
        print "===================================================================\n"
        print "ERROR in sendConnectedCommandToController: " + str(inst)+"\n"
        print "===================================================================\n"
        addCommandToListOfIOCommands(self, "ERROR in sendConnectedCommandToController", "Controller", "Outbound")

def sendDoingStuffCommandToController(self):
    try:
        #print "Sending doingStuff Command to the Controller\n"
        self.pipe.send("doingStuff")
       # print "Sent doingSTuff Command to the Controller\n"
        addCommandToListOfIOCommands(self, "doingStuff", "Controller", "Outbound")
    except Exception as inst:
        print "===================================================================\n"
        print "ERROR in sendDoingStuffCommandToController: " + str(inst)+ "\n"
        print "===================================================================\n"
        addCommandToListOfIOCommands(self, "ERROR in sendDoingStuffCommandToController", "Controller", "Outbound")

#Inbound commands from server functions-----------------------------------------------------------
def checkForDoneCommandFromServer(self,inboundString):
    try:
      #  print "Checking for done command from server\n"
        if(compareString(inboundString,"done",0,0,len("done"),len("done"))==True):
           # print "Done command was received from the server\n"
            addCommandToListOfIOCommands(self, "done", "Server", "Inbound")
            self.serverIssuedDoneCommand = True
            return True
        else:
            return False
    except Exception as inst:
        print "===================================================================\n"
        print "ERROR in checkForDoneCommandFromServer: " + str(inst) +"\n"
        print "===================================================================\n"
        addCommandToListOfIOCommands(self, "ERROR in checkForDOneCOmmandFromServer", "Server", "Inbound")
        return False

def checkForNextCommandFromServer(self, inboundString): #NOTE: Different than previous revisions, this only checks for the NEXT keyword
    try:
        #print "Checking for nextCommand from server\n"
        if(compareString(inboundString,"NEXT",0,0,len("NEXT"),len("NEXT"))==True):
            #print "Next Command was received from the server\n"
            addCommandToListOfIOCommands(self, "NEXT", "Server", "Inbound")
            return True
        else:
            return False
    except Exception as inst:
        print "===================================================================\n"
        print "ERROR in checking for nextCommand from the server: " +str(inst)+"\n"
        print "===================================================================\n"
        addCommandToListOfIOCommands(self, "ERROR in checkingForNextCommandFromServer", "Server", "Inbound")
        return False

def extractSizeOfParamFromNextCommand(self, inboundString): #NOTE: New component to extract the file size of the params from the next command
    try: #THIS can also extract the length of params from the next command
       # print "Extracting size of Params from the next Command\n"
        firstOpenParenthesisPos= 0
        firstClosingParenthesisPos= 0
        sizeOfChunkParams = ""
        #Command layout: "NEXT PSIZE() DSIZE()"
        #Step 1: find the first Open Parenthesis, which immeadiately follows the PSIZE
        try: #step 1 try block
           # print "Finding the first Open Parenthesis\n"
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
            addCommandToListOfIOCommands(self, "EXCEPTION in STep 1 of ExtractSizeOfParams", "Server", "Inbound")
            raise Exception ("Exception thrown in step 1 of extractSizeOfParamsFromNextCommand")
        #Step 2: find the corresponding closing parenthesis
        try: #Step 2 try block
            #print "Finding the corresponding closing parenthesis\n"
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
            addCommandToListOfIOCommands(self, "EXCEPTION in STep 2 of ExtractSizeOfParams", "Server", "Inbound")
            raise Exception ("Exception thrown in Step 2 of extractSizeOfParamsFromNextCommand")
        #Step 3: retreive the params file size
        try: #step 3 try block
           # print "Retreiving the params file size\n"
            for index in range(firstOpenParenthesisPos+1,firstClosingParenthesisPos):
                sizeOfChunkParams+= str(inboundString[index])
            return sizeOfChunkParams
        except Exception as inst:
            print "===================================================================\n"
            print "Exception thrown in Step 3: retreive the params file size: "+str(inst)+"\n"
            print "===================================================================\n"
            addCommandToListOfIOCommands(self, "EXCEPTION in STep 3 of ExtractSizeOfParams", "Server", "Inbound")
            raise Exception ("Exception thrown in Step 3 of extractSizeOfParamsFromNextCommand")
    except Exception as inst:
        print "===================================================================\n"
        print "ERROR in extractSizeOfParamsFromNextCommand: " +str(inst)+"\n"
        print "===================================================================\n"
        addCommandToListOfIOCommands(self, "ERROR in ExtractSizeOfParams", "Server", "Inbound")
        return 0 #return filesize of zero if there was an error

def extractSizeOfDataFromNextCommand(self, inboundString): #NOTE: this is a new component. This can also extract the length of Data from the next command
    try:
        #print "Extracting size of data from next Command\n"
        firstOpenParenthesisPos = 0
        firstClosingParenthesisPos = 0
        sizeOfChunkData= ""
        #Command layout: NEXT PSIZE() DSIZE()
        #Step 1: find the 'D' in the inboundString
        try: #step 1 try block
           # print "Finding the 'D' in the nextCommand\n"
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
            addCommandToListOfIOCommands(self, "EXCEPTION in STep 1 of ExtractSizeOfData", "Server", "Inbound")
            raise Exception ("Exception was thrown in step 1 of extractSizeOfDataFromNextCommand")
        #Step 2: find the corresponding parenthesis
        try: #Step 2 try block
           # print "Finding the corresponding parenthesis\n"
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
            addCommandToListOfIOCommands(self, "EXCEPTION in STep 2 of ExtractSizeOfData", "Server", "Inbound")
            raise Exception ("Exception thrown in step 2 of extractSizeOfDataFromNextCommand")
        #Step 3: retreive the data file size
        try: #step 3 try block
            #print "Retrieving data file size\n"
            for index in range(firstOpenParenthesisPos+1,firstClosingParenthesisPos):
                sizeOfChunkData+= str(inboundString[index])
            return sizeOfChunkData
        except Exception as inst:
            print "===================================================================\n"
            print "Exception thrown in Step 3: retrieve the data file size: " + str(inst)+"\n"
            print "===================================================================\n"
            addCommandToListOfIOCommands(self, "EXCEPTION in STep 3 of ExtractSizeOfData", "Server", "Inbound")
            raise Exception ("Exception thrown is step 3 of extractSizeOfDataFromNextCommand")
    except Exception as inst:
        print "===================================================================\n"
        print "ERROR in extractSizeOfDataFromNextCommand: " +str(inst)+"\n"
        print "===================================================================\n"
        addCommandToListOfIOCommands(self, "ERROR in ExtractSizeOfData", "Server", "Inbound")
        return 0

def receivePieceOfChunkFromServerByLength(self, lengthOfChunkComponent, networkSocket): #NOTE: this method receives pieces of chunks by their lengths rather than thier filesizes
    try:
        receivedPieceOfChunk = ""
        #print "Receiving Piece of CHunk From The Server By Length\n"
       # print "Length of PieceOfChunk: "+str(lengthOfChunkComponent)+"\n"
        import sys
        while(len(receivedPieceOfChunk) < int(lengthOfChunkComponent)):
            try:
                receivedPieceOfChunk+= str(networkSocket.recv(512))#this works very well, the key is the small receive size
                if(len(receivedPieceOfChunk) >= int(lengthOfChunkComponent)):
                    break
                else:
                    #print "Received "+str(len(receivedPieceOfChunk))+" characters so far\n"
                    fakeVar=True
            except Exception as inst:
                if(compareString(str(inst),"timed out",0,0,len("timed out"),len("timed out"))==True):
                    #dont throw error, just keep on receiving
                    if(len(receivedPieceOfChunk) < 1):
                        fakeVar=True
                        #keep looping
                       # print "Error: receivedString in the empty string\n"
                    else:
                        #print "socket timed out\n"
                        #fakeVar=True
                        break
                else:
                    raise Exception ("Error in receivePieceOfChunkFromServerByLength infinite while loop")
                    break
        addCommandToListOfIOCommands(self, "receivePieceOfChunk", "Server", "Inbound")
        if(len(receivedPieceOfChunk) < 1):
            raise Exception ("receivedPieceOfChunk is the empty string!")
        elif(len(receivedPieceOfChunk) < int(lengthOfChunkComponent)):
            raise Exception ("Not all of the Piece of chunk was received\n receivedPieceOfChunk length:"+str(len(receivedPieceOfChunk))+"\n"
            +"expectedPieceOfChunk length:"+str(lengthOfChunkComponent))
        elif(len(receivedPieceOfChunk) == lengthOfChunkComponent):
            raise Exception ("Received extra information !!!!!! \n receivedPieceOfChunk length:"+str(len(receivedPieceOfChunk))+"")
        else:
            #print "Finished receiving Piece of chunk from the server. length of receivedPieceOfChunk:"+str(len(receivedPieceOfChunk))+"\n"
            fakeVar=True
    except Exception as inst:
        print "===================================================================\n"
        print "ERROR in receivePieceOfChunkFromServerByLength: "+str(inst)+"\n"
        print "===================================================================\n"
        addCommandToListOfIOCommands(self, "ERROR in receivePieceOfChunkFromServerByLength", "Server", "Inbound")
    finally:
        networkSocket.settimeout(0.25)
        #print "Socket timeout was reset back to default\n"
        return receivedPieceOfChunk

#Outbound commands to server functions--------------------------------------
def sendNextChunkCommandToServer(self, networkSocket):
    try:
        #print "Sending nextChunk Command to Server\n"
        networkSocket.send("NEXT " + str(self.myIPAddress))
        #print "Sent the nextChunk Command to the server\n"
        addCommandToListOfIOCommands(self, "nextChunk", "Server", "Outbound")
    except Exception as inst:
        print "===================================================================\n"
        print "Exception thrown in sendNextChunkCommandToServer: " + str(inst)+"\n"
        print "===================================================================\n"
        addCommandToListOfIOCommands(self, "EXCEPTION in sendNextChunkCommandToServer", "Server", "Outbound")

def sendFoundSolutionCommandToServer(self, networkSocket, theInboundSolution):
    try:
       # print "Sending foundSolution Command to Server\n"
        combinedStrings= "FOUNDSOLUTION [" + str(theInboundSolution)+"]"
        networkSocket.send(combinedStrings) #also send the solution to the server
       # print "Sent FoundSOlution Command to the server\n"
        addCommandToListOfIOCommands(self, "FOUNDSOLUTION", "Server", "Outbound")
    except Exception as inst:
        print "===================================================================\n"
        print "Exception thrown in sendFoundSolutionCommandToServer: "+ str(inst)+"\n"
        print "===================================================================\n"
        addCommandToListOfIOCommands(self, "EXCEPTION in sendFoundSOlutionCommandToServer", "Server", "Outbound")

def sendCrashedCommandToServer(self, networkSocket):
    try:
       # print "Sending Crashed Command to Server\n"
        networkSocket.send("CRASHED " + self.myIPAddress)
       # print "Sent Crashed COmmand to the server\n"
        addCommandToListOfIOCommands(self, "Crashed", "Server", "Outbound")
    except Exception as inst:
        print "===================================================================\n"
        print "Exception thrown in the sendCrashedCommandToServer: "+str(inst)+"\n"
        print "===================================================================\n"
        addCommandToListOfIOCommands(self, "EXCEPTION in sendCrashedCommandToServer", "Server", "Outbound")


from socket import *
import Chunk
import platform
import Queue

class NetworkClient():

    def __init__(self, inboundpipefromcontroller):
        #CLASS VARS
        self.pipe = inboundpipefromcontroller
        self.host = ''
        self.port = 55568
        self.myIPAddress = "127.0.0.1" #defualt to the ping back address
        self.serverIPAddress = "127.0.0.1" #default to the ping back address
        self.listOfIOCommands = [] #keeps a record of what commands have been received from controller and server
        self.queueOfInboundChunks = Queue.Queue() #queue that holds the inbbound chunks, acts as the buffer
        self.controllerWaitingForChunk = False
        self.serverIssuedDoneCommand = False
        self.solutionWasFound = False
        self.solutionString = ""#stores what the solution was if found

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
            addCommandToListOfIOCommands(self, "ERROR in getOS try block", "Self", "Self")
        #......................................
        #End of detect OS
        #......................................

        import socket
        clientSocket = socket.socket(AF_INET, SOCK_STREAM)

        try: #receive the server ip from the controller
            self.serverIPAddress= receiveServerIPFromController(self)
        except Exception as inst:
            print "===================================================================\n"
            print "Error in receive server ip from the controller: "+(str(inst))+"\n"
            print "===================================================================\n"
            addCommandToListOfIOCommands(self, "ERROR in receiveServerIPFromController", "Self", "Self")

        try: #connect to server try block
            clientSocket.connect((self.serverIPAddress, self.port))
           # print "Connected to server\n"
            sendConnectedCommandToController(self)
        except Exception as inst:
            print "===================================================================\n"
            print "Error in connect to server try block: " + str(inst) +"\n"
            print "self.serverIPAddress= "+str(self.serverIPAddress)+"\n"
            print "self.port= "+str(self.port)+"\n"
            print "===================================================================\n"
            addCommandToListOfIOCommands(self, "ERROR in connectToServer", "Self", "Self")
            raise Exception ("Failed to connect to the server")

        #REQUEST TWO CHUNKS FROM THE SERVER TO STORE IN THE QUEUE
        sendNextChunkCommandToServer(self, clientSocket)
        sendNextChunkCommandToServer(self, clientSocket)

        #PRIMARY CLIENT WHILE LOOP
        try:
            clientSocket.settimeout(0.25)
            while True: #primary client while loop
                inboundCommandFromServer = "" #initialize the var
                #CHECK FOR INBOUND SERVER COMMANDS SECTION=============================================================
                try: #check for inbound server commands
                    #print "Checking for inbound Commands From Server\n"
                    inboundCommandFromServer = receiveCommandFromServer(self, clientSocket)
                except Exception as inst:
                    print "===================================================================\n"
                    print "Error in check for inbound Server Commands Try block: "+str(inst)+"\n"
                    print "===================================================================\n"
                    addCommandToListOfIOCommands(self, "ERROR in checkForInboundServerCommands", "Self", "Self")

                if(len(inboundCommandFromServer) > 0): #if not the empty string, perform the following checks
                    identifiedCommand = False
                    try: #check for the done command from the server
                        if(checkForDoneCommandFromServer(self,inboundCommandFromServer)==True):
                            identifiedCommand= True
                           # print "Identified Command as the done command from the server\n"
                           # print "Server has Issued the Done Command\n"
                            self.serverIssuedDoneCommand = True
                            break #break out of the main while loop
                    except Exception as inst:
                        print "===================================================================\n"
                        print "Error in checking for done command from the server: "+str(inst)+"\n"
                        print "===================================================================\n"
                        addCommandToListOfIOCommands(self, "ERROR in checkingForDoneCommandFromServer", "Self", "Self")

                    try: #check for nextChunk command from the server
                        if(identifiedCommand == False):
                            if(checkForNextCommandFromServer(self,inboundCommandFromServer)==True):
                                identifiedCommand= True
                               # print "Identified Command as the nextChunk Command from the server\n"
                                lengthOfChunkParams = extractSizeOfParamFromNextCommand(self, inboundCommandFromServer)
                                lengthOfChunkData = extractSizeOfDataFromNextCommand(self, inboundCommandFromServer)
                                tempChunkParams = receivePieceOfChunkFromServerByLength(self, lengthOfChunkParams, clientSocket)

                                tempChunkData = receivePieceOfChunkFromServerByLength(self, lengthOfChunkData, clientSocket)
                                outboundChunk = Chunk.Chunk()
                                outboundChunk.params = str(tempChunkParams)
                                outboundChunk.data = str(tempChunkData)
                                #store in queue regardless of conditions
                                self.queueOfInboundChunks.put(outboundChunk) #put chunk into the queue
                                #if controller is waiting, send to controller
                                if(self.controllerWaitingForChunk == True):
                                    sendDoingStuffCommandToController(self) #notify controller that client will be sending a chunk to it
                                    sendNextChunkCommandToController(self, self.queueOfInboundChunks.get(0)) #send the chunk to the controller
                                    self.controllerWaitingForChunk = False

                    except Exception as inst:
                        print "===================================================================\n"
                        print "Error in checking for nextChunk command from server: " + str(inst)+"\n"
                        print "===================================================================\n"
                        addCommandToListOfIOCommands(self, "ERROR in checkingForNextChunkFromServer", "Self", "Self")

                    if(identifiedCommand == False):
                       # print "Warning: Unknown command received from the server: "+str(inboundCommandFromServer)
                        addCommandToListOfIOCommands(self, "UNKNOWN Command", "Server", "Inbound")

                #CHECK FOR INBOUND CONTROLLER COMMANDS SECTION=======================================================
                receivedCommandFromController = "" #initialize thevar
                try: #check for inbound controller commands try block
                   # print "Checking for Commands from the Controller\n"
                    if(self.pipe.poll()):
                        receivedCommandFromController= self.pipe.recv()
                       # print "Received a Command from the controller\n"
                except Exception as inst:
                    print "===================================================================\n"
                    print "Error in check for inbound commands from controller try block: "+str(inst)+"\n"
                    print "===================================================================\n"
                    addCommandToListOfIOCommands(self, "ERROR in checkForInboundCOmmandsFromCOntroller", "Self", "Self")

                if(len(receivedCommandFromController) > 0): #if not the empty string
                    identifiedCommand= False
                    try: #checking for found solution command from controller
                        if(checkForFoundSolutionCommandFromController(self, receivedCommandFromController)==True):
                            identifiedCommand = True
                           # print "Identified Command as Found Solution Command from the controller\n"
                            self.solutionWasFound= True
                            self.serverIssuedDoneCommand = True #set this so a crash report wont be sent to the server
                            #print "Listening for the solution from the Controller...\n"
                            theInboundSolution= receiveSolutionFromController(self, clientSocket)
                           # print "Solution was received. The solution is: '"+str(theInboundSolution)+"'\n"
                            sendFoundSolutionCommandToServer(self, clientSocket, str(theInboundSolution))#send the solution also
                          #  print "Sent Found solution command to the servere"
                            self.solutionString= str(theInboundSolution)
                    except Exception as inst:
                        print "===================================================================\n"
                        print "Error in check for found solution command from controller: "+str(inst)+"\n"
                        print "===================================================================\n"
                        addCommandToListOfIOCommands(self, "ERROR in checkForFoundSOlutionCommandFromController", "Self", "Self")

                    try: #checking for request next chunk command from controller
                        if(identifiedCommand == False):
                            if(checkForRequestNextChunkCommandFromController(self,receivedCommandFromController)==True):
                                identifiedCommand= True
                                print "Identified Command as the requestNextChunk Command from the Controller\n"
                                if(self.queueOfInboundChunks.empty()):
                                    print "Queue is empty: controller is now waiting"
                                    self.controllerWaitingForChunk = True
                                    sendNextChunkCommandToServer(self,clientSocket)
                                else:
                                    print "chunk in queue is being sent to the controller"
                                    tempChunk = self.queueOfInboundChunks.get(0)
                                    sendDoingStuffCommandToController(self)
                                    sendNextChunkCommandToController(self, tempChunk)
                                    sendNextChunkCommandToServer(self, clientSocket)
                    except Exception as inst:
                        print "===================================================================\n"
                        print "Error in check for request Next Chunk Command from controller: "+str(inst)+"\n"
                        print "===================================================================\n"
                        addCommandToListOfIOCommands(self, "ERROR in checkForRequestNextChunkCommandFromController", "Self", "Self")

                    try: #check for doingStuff command form controller
                        if(identifiedCommand == False):
                            if(checkForDoingStuffCommandFromController(self,receivedCommandFromController)==True):
                                identifiedCommand= True
                                #print "Identified Command as the doingStuff Command from the Controller\n"
                                #The controller parrots this message back to client, no action needed for this
                    except Exception as inst:
                        print "===================================================================\n"
                        print "Error in check for doingStuff Command from controller: "+str(inst)+"\n"
                        print "===================================================================\n"
                        addCommandToListOfIOCommands(self, "ERROR in checkForDoingStuffCommandFromCOntroller", "Self", "Self")

                    try: #check for done command from the controller
                        if(identifiedCommand == False):
                            if(checkForDoneCommandFromController(self,receivedCommandFromController)==True):
                                identifiedCommand= True
                               # print "Identified Command as the done Command from the Controller\n"
                                #This is just a confirmation message, no action is needed for this
                    except Exception as inst:
                        print "===================================================================\n"
                        print "Error in check for done command from the controller: "+str(inst)+"\n"
                        print "===================================================================\n"
                        addCommandToListOfIOCommands(self, "ERROR in checkForDoneCommandFromController", "Self", "Self")

                    if((identifiedCommand == False) and (self.solutionWasFound == False)):
                       # print "Warning: Received Unknown Command From The Controller: "+str(receivedCommandFromController)+"\n"
                        addCommandToListOfIOCommands(self, "UNKNOWN: "+str(receivedCommandFromController), "Controller", "Inbound")
                    elif((identifiedCommand == False) and (self.solutionWasFound == True)):
                       # print "The Solution is '" + str(receivedCommandFromController)+"'\n"
                        self.solutionString= str(receivedCommandFromController)
                        break
            #end of primary client while loop
        except Exception as inst:
            print "===================================================================\n"
            print "Error in Primary client while loop: "+str(inst)+"\n"
            print "===================================================================\n"
            addCommandToListOfIOCommands(self, "ERROR in PrimaryClientWhileLoop", "Self", "Self")
        finally:
            if(self.serverIssuedDoneCommand == False):
                try: #send crash message to server, if needed
                   # print "Warning: Server has not issued the done command! Sending Crashed Command to the Server\n"
                    sendCrashedCommandToServer(self, clientSocket)
                except Exception as inst:
                    print "===================================================================\n"
                    print "Error in send crash message to server, in finally block: "+str(inst)+"\n"
                    print "===================================================================\n"
                    addCommandToListOfIOCommands(self, "ERROR in sendCrashedMessageToServerFinallyBlock", "Self", "Self")
           # print "Closing the client socket\n"
            clientSocket.close()
           # print "Client Socket has been closed\n"
            sendDoneCommandToController(self)
            #print "Informed Controller that Client is finished\n"
            print "------------------Printing ListOfIOCommands-------------------\n"
            for index in range(0,len(self.listOfIOCommands)):
                tempCommand, tempOrigin, tempDirection, tempTime= self.listOfIOCommands[index]
                if(compareString(tempDirection, "Inbound",0,0,len("Inbound"),len("Inbound"))==True):
                    print str(tempDirection)+ " command: "+str(tempCommand)+" was received from: "+str(tempOrigin)+" at: "+str(tempTime)
                else: #direction is outbound
                    print str(tempDirection)+" command: "+str(tempCommand)+" was sent to: "+str(tempOrigin)+" at: "+str(tempTime)
            print "----------------End of List of IO Commands--------------------------\n"
            print "Value of self.solutionWasFound: "+str(self.solutionWasFound)+"\n"
            if(self.solutionWasFound == True):
                print "The solution is: '"+str(self.solutionString)+"'\n"
            else:
                print "This Node did not find the solution\n"



