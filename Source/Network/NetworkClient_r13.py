__author__ = 'chris hamm'
#NetworkClient_r13
#created: 2/10/2015

#Designed to work with NetworkServer_r13

#REVISION NOTES:
    #Moving to a more modular style, no master receive or send function.
    #

#By recommendation, implement without the command logs


import socket
from socket import *

class NetworkClient():

    def __init__(self, inboundpipefromcontroller):
        self.pipe = inboundpipefromcontroller

        host = ''
        port = 55568
        myIPAddress = '127.0.0.1' #defualt to the ping back address
        serverIPAddress = '127.0.0.1' #default to the ping back address
        serverIssuedDoneCommand = False

        clientSocket = socket.socket(AF_INET, SOCK_STREAM)

        try: #receive the server ip from the controller
            #TODO insert the call to receive server ip here
            print "DEBUG: INSERT CALL RECEIVE THE SERVER IP HERE\n"
        except Exception as inst:
            print "===================================================================\n"
            print "Error in receive server ip from the controller: "+(str(inst))+"\n"
            print "===================================================================\n"

        try: #connect to server try block
            #TODO insert connect to server function here
            print "DEBUG: INSERT CONNECT TO SERVER FUNCTION HERE\n"
        except Exception as inst:
            print "===================================================================\n"
            print "Error in connect to server try block: " + str(inst) +"\n"
            print "===================================================================\n"

        #PRIMARY CLIENT WHILE LOOP
        try:
            clientSocket.settimeout(0.25)
            while True: #primary client while loop
                #CHECK FOR INBOUND SERVER COMMANDS SECTION=============================================================
                try: #check for inbound server commands
                    #TODO insert receive server command here
                    print "DEBUG: INSERT RECEIVE SERVER COMMANDS HERE\n"
                except Exception as inst:
                    print "===================================================================\n"
                    print "Error in check for inbound Server Commands Try block: "+str(inst)+"\n"
                    print "===================================================================\n"

                #TODO check to see if received the empty string
                print "DEBUG: CHECK TO SEE IF RECV AN EMPTY STRING HERE\n"
                #TODO else if received string is not empty, perform these checks
                try: #check for the done command from the server
                    #TODO insert check for done command from server function
                    print "DEBUG: CHECK FOR DONE COMMAND FROM THE SERVER\n"
                except Exception as inst:
                    print "===================================================================\n"
                    print "Error in checking for done command from the server: "+str(inst)+"\n"
                    print "===================================================================\n"

                try: #check for nextChunk command from the server
                    #TODO insert check for nextChunk command from server
                    print "DEBUG: CHECK FOR NEXTCHUNK FROM SERVER HERE\n"
                except Exception as inst:
                    print "===================================================================\n"
                    print "Error in checking for nextChunk command from server: " + str(inst)+"\n"
                    print "===================================================================\n"

                #TODO else, the command is not recognized, print error and unknown command here
                print "DEBUG: PRINT OUT ERROR AND UNKNOWN COMMAND HERE\n"

                #CHECK FOR INBOUND CONTROLLER COMMANDS SECTION=======================================================
                try: #check for inbound controller commands try block
                    #TODO check if there is any commands on the pipe
                    print "DEBUG; CHECK FOR INBOUND COMMANDS FROM CONTROLLER HERE\n"
                except Exception as inst:
                    print "===================================================================\n"
                    print "Error in check for inbound commands from controller try block: "+str(inst)+"\n"
                    print "===================================================================\n"

                #TODO check to see if received the empty string
                print "DEBUG: CHECK TO SEE IF RECEIVED THE EMPTY STRING \n"
                #TODO else if recieved string is not empty, perform these checks
                try: #checking for found solution command from controller
                    #TODO check if received the found solution command from the controller
                    print "DEBUG: CHECK TO SEE IF RECEIVED THE FOUND SOLUTION COMMAND FROM THE CONTROLLER\n"
                except Exception as inst:
                    print "===================================================================\n"
                    print "Error in check for found solution command from controller: "+str(inst)+"\n"
                    print "===================================================================\n"

                try: #checking for request next chunk command from controller
                    #TODO check if received the request next chunk command from controller
                    print "DEBUG: CHECK TO SEE IF RECEIVED REQUEST NEXT CHUNK COMMAND\n"
                except Exception as inst:
                    print "===================================================================\n"
                    print "Error in check for request Next Chunk Command from controller: "+str(inst)+"\n"
                    print "===================================================================\n"

                try: #check for doingStuff command form controller
                    #TODO check if doingSTuff command was received
                    print "DEBUG: CHECK IF DOINGSTUFF COMMAND WAS RECEIVED\n"
                except Exception as inst:
                    print "===================================================================\n"
                    print "Error in check for doingStuff Command from controller: "+str(inst)+"\n"
                    print "===================================================================\n"

                try: #check for done command from the controller
                    #TODO check if done command was received form controller
                    print "DEBUG: CHECK IF DONE COMMAND WAS RECEIVED FROM CONTROLLER\n"
                except Exception as inst:
                    print "===================================================================\n"
                    print "Error in check for done command from the controller: "+str(inst)+"\n"
                    print "===================================================================\n"

                #TODO else, if command is not recognized, print out error and unknown command from controller
                print "DEBUG: PRINT OUT ERROR AND UNKNOWN COMMAND FROM CONTROLLER HERE\n"
            #end of primary client while loop
        except Exception as inst:
            print "===================================================================\n"
            print "Error in Primary client while loop: "+str(inst)+"\n"
            print "===================================================================\n"
        finally:
            if(self.serverIssuedDoneCommand == False):
                try: #send crash message to server, if needed
                    #TODO if server has not issued the done command, then send crash message to server here
                    print "DEBUG: SEND CRASH MESSAGE TO SERVER HERE IF NEEDED\n"
                except Exception as inst:
                    print "===================================================================\n"
                    print "Error in send crash message to server, in finally block: "+str(inst)+"\n"
                    print "===================================================================\n"
            print "Closing the client socket\n"
            clientSocket.close()
            print "Client Socket has been closed\n"
            #TODO insert command call here to inform the controller that the client in finished

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
                self.serverIP= self.pipe.recv()
                print "Received the server IP from the controller\n"
            except Exception as inst:
                print "===================================================================\n"
                print "ERROR in receiveServerIPFromController: " + str(inst) + "\n"
                print "===================================================================\n"

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
            try:
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
                    for index in range(firstOpenParenthesisPos+1,firstClosingParenthesisPos-1):
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

        def extractSizeOfDataFromNextCommand(self, inboundString): #NOTE: this is a new component
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
                    for index in range(firstOpenParenthesisPos+1,firstClosingParenthesisPos-1):
                        sizeOfChunkData+= str(inboundString)
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

        def receivePieceOfChunkFromServer(self, pieceOfChunkFileSize): #NOTE: New component, call this for receiving params or for receiving data
            try:
                receivedPieceOfChunk= ""
                print "Receiving piece of chunk from the server\n"
                while(sys.getsizeof(receivedPieceOfChunk) < pieceOfChunkFileSize):
                    recvInfo= self.clientSocket.recv(4096)
                    if recvInfo:
                        receivedPieceOfChunk+= str(recvInfo)
                    else:
                        break
                if(len(receivedPieceOfChunk) < 1):
                    raise Exception ("receivedPieceOfChunk is empty!")
                return receivedPieceOfChunk
            except Exception as inst:
                print "===================================================================\n"
                print "ERROR in receivePieceOfChunkFromServer: "+str(inst)+"\n"
                print "===================================================================\n"
                return "" #the empty string

        def receiveCommandFromServer(self): #NOTE used for normal recv
            try:
                receivedCommand= ""
                print "Checking for command from the server\n"
                serverInput= self.clientSocket.recv(4096)
                if(len(serverInput) > 0):
                    receivedCommand= serverInput
                return receivedCommand
            except Exception as inst:
                print "===================================================================\n"
                print "ERROR in receiveCommandFromServer: "+str(inst)+"\n"
                print "===================================================================\n"
                return "" #the empty string

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