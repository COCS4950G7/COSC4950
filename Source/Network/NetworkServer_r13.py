__author__ = 'chris hamm'
#NetworkServer_r13
#Created: 2/10/2015

#Designed to work with NetworkClient_r13

#NOTES ABOUT THIS REVISION:
    #Goal is to have this revision be easier to diagnose lock problems
    #NO locks are to be acquired in the Main Thread, Client Thread(s), if at all possible
    #ALL locks are to be acquired in the function that needs them, then immeadiately released (also applies for incrementors)
    #Have some sort of time out mechanism for acquiring a nested lock, so that both locks will be released and the program can continue to run
    #Main thread will only handle inbound client connections
    #ClientThread will only handle communication between that client and the server.

#By recommendation, implement with out the command logs

#MAJOR CHANGE IN SENDNEXTCOMMANDTOCLIENT function

#TODO still need a variable to indicate when all of the threads need to stop running (aka break from their while loop)

import threading
import thread
import socket
from socket import *
import sys

class NetworkServer():

    #CLASS VARS
    host = ''
    port = 55568
    myIPAddress = '127.0.0.1' #default to ping back address
    listOfCrashedClients = []
    dictionaryOfCurrentClientTasks = {} #key is the client's IP Address , the value is the chunk that client is working on
                                        #If you try to access a non-existing key it will throw an error
    #NOTE: NOT GOING TO HAVE A LIST OF CONNECTED CLIENTS, JUST USE THE DICTIONARY OF CURRENT CLIENT TASKS INSTEAD

    socketLock = threading.RLock()

    #START OF CLIENT THREAD HANDLER
    def ClientThreadHandler(self, clientSocket, clientAddr, socketLock):
        try: #CLient THread Handler Try Block
            receivedCommandFromClient = "" #initialize the receiving variable
            while True:
                try: #check for commands from client
                    #TODO implement the receive mechanism here for inbound client commands
                    print "DEBUG: INSERT THE RECEIVE MECHANISM FOR INBOUND COMMANDS FROM THE CLIENT HERE\n"
                except Exception as inst:
                    print "===================================================================\n"
                    print "Error in check for commands from the client in client thread handler: " +str(inst)+"\n"
                    print "===================================================================\n"

                try: #Analyzing received command from the client try block
                    #TODO check to make sure the received command is not the empty string
                    print "DEBUG: CHECK TO SEE IF RECEIVED COMMAND IS THE EMOTY STRING HERE\n"
                    #TODO else if received command is not the empty string, perform these checks
                    try: #checking to see if the next Command was received from the client try block
                        #TODO check to see if the next command was received from the client
                        print "DEBUG: CHECK TO SEE IF THE NEXT COMMAND WAS RECEIVED FROM THE CLIENT HERE\n"
                    except Exception as inst:
                        print "===================================================================\n"
                        print "Error in checking to see if the next Command was received from the client in client thread handler: "+str(inst)+"\n"
                        print "===================================================================\n"

                    try: #check to see if the found solution command was received from the client
                        #TODO check to see if the found solution command was received from the client
                        print "DEBUG: CHECK TO SEE IF THE FOUNDSOLUTION COMMAND WAS RECEIVED FROM THE CLIENT HERE\n"
                    except Exception as inst:
                        print "===================================================================\n"
                        print "Error in check to see if found solution command was received from the client in client thread handler: "+str(inst)+"\n"
                        print "===================================================================\n"

                    try: #check to see if the crashed command was received
                        #TODO check to see if the crashed command was received from the client
                        print "DEBUG: CHECK TO SEE IF CRASHED COMMAND WASS RECEIVED HERE\n"
                    except Exception as inst:
                        print "===================================================================\n"
                        print "Error in check to see if crashed command was received from client in client thread handler: "+ str(inst)+"\n"
                        print "===================================================================\n"

                    #TODO else, if command is not recognized, print error and the unknown command here
                    print "DEBUG; PRINT THE ERROR AND UNKNOWN COMMAND HERE\n"
                except Exception as inst:
                    print "===================================================================\n"
                    print "Error in Analyzing received command from the client try block in the client thread handler: " +str(inst)+"\n"
                    print "===================================================================\n"

        except Exception as inst:
            print "===================================================================\n"
            print "Error in Client Thread Handler: " + str(inst) +"\n"
            print "===================================================================\n"

        finally:
            clientSocket.close()
            print "clientSocket has been closed\n"
    #end of clientthreadhandler

    #START OF INITIAL SERVER SETUP
    def __init__(self, inboundpipeconnection):
        self.pipe = inboundpipeconnection #pipe that connects to the controller

        #CREATE THE SOCKET
        serverSocket = socket.socket(AF_INET, SOCK_STREAM)

        try: #try to bind the socket
            serverSocket.bind((self.host, self.port))
        except Exception as inst:
            print "===================================================================\n"
            print "Critical Error: Failed to bind the socket: "+str(inst)+"\n"
            print "Suggestion: Close this application, then reopen this application and try again\n"
            print "===================================================================\n"

        #START LISTENING TO SOCKET
        serverSocket.listen(5)

        #MAIN THREAD SERVER LOOP
        try: #main thread server loop try block
            serverSocket.settimeout(0.25)
            while True: #Primary main thread server while loop
                #CHECK TO SEE IF A CLIENT IS TRYING TO CONNECT
                try:
                    inboundClientSocket, inboundClientAddr = serverSocket.accept()
                    print "A client has connected!!\n"
                    thread.start_new_thread(self.ClientThreadHandler(inboundClientSocket,inboundClientAddr,self.socketLock))
                except Exception as inst:
                    print "===================================================================\n"
                    print "Error in check for client trying to connect try block: " +str(inst)+"\n"
                    print "===================================================================\n"

                #CHECK TO SEE IF CONTROLLER HAS SENT A MESSAGE TO SERVER
                try:
                    if(self.pipe.poll()):
                        receivedControllerCommand= self.pipe.recv()
                        print "Received a command from the controller\n"
                        #TODO Check to make sure that the received command is not the empty string
                        #TODO if recieved command is not the empty string, perform these checks
                        try: #checking for nextChunk Command from Controller
                            #TODO insert check for nextChunk Command from comntroller here
                            print "DEBUG: INSERT CALL TO CHECK FOR NEXTCHUNK COMMAND FROM CONTROLLER HERE\n"
                        except Exception as inst:
                            print "===================================================================\n"
                            print "Error in checking for nextChunk COmmand from Controller Try Block: " +str(inst)+"\n"
                            print "===================================================================\n"

                        try: #checking for done command form controller
                            #TODO insert check for done Command from controller here
                            print "DEBUG: INSERT CALL TO CHECK FOR DONE COMMAND FROM CONTROLLER HERE\n"
                        except Exception as inst:
                            print "===================================================================\n"
                            print "Error in checking for done command from Controller Try Block: "+str(inst)+"\n"
                            print "===================================================================\n"

                        #TODO else if the command was not recognized, print error and display the unknown command
                        print "DEBUG: INSERT ERROR MESSAGE AND PRINT OUT OF UNKNOWN COMMAND FROM THE CONTROLLER\n"
                    else: #if there is nothing on the pipe
                        print "There is no command received from the controller\n"
                except Exception as inst:
                    print "===================================================================\n"
                    print "Error in check to see if controller has sent a message to server try block: " + str(inst) +"\n"
                    print "===================================================================\n"

        except Exception as inst:
            print "===================================================================\n"
            print "Error in Main Thread Server Loop: " +str(inst)+"\n"
            print "===================================================================\n"

        finally:
            print "Preparing to close the socket\n"
            serverSocket.close()
            print "The serverSocket has been closed\n"
            #TODO insert command call to let the controller know that server is finished

        #FUNCTIONS==========================================================================
        def compareString(inboundStringA, inboundStringB, startA, startB, endA, endB):
            try:
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
            except Exception as inst:
                print "========================================================================\n"
                print "Exception thrown in compareString Function: " +str(inst)+"\n"
                print "========================================================================\n"
                return False

        #Inbound commands from controller==========================================
        def checkForDoneCommandFromController(self, inboundString):
            try:
                print "Checking for done Command from the Controller\n"
                if(compareString(inboundString,"done",0,0,len("done"),len("done"))==True):
                    print "done Command was received from the Controller\n"
                    return True
                else:
                    return False
            except Exception as inst:
                print "========================================================================\n"
                print "Exception thrown in checkForDoneCommandFromController: "+str(inst)+"\n"
                print "========================================================================\n"
                return False

        def checkForNextChunkCommandFromController(self, inboundString):
            try:
                print "Checking for nextChunk Command from the Controller\n"
                if(compareString(inboundString, "nextChunk",0,0,len("nextChunk"),len("nextChunk"))==True):
                    print "nextChunk Command was received from the Controller\n"
                    return True
                else:
                    return False
            except Exception as inst:
                print "========================================================================\n"
                print "Exception thrown in checkForNextChunkCommandFromController: " +str(inst)+"\n"
                print "========================================================================\n"
                return False

        #Outbound commands to controller======================================
        def sendNextChunkCommandToController(self):
            try:
                print "Sending nextChunk Command to the Controller\n"
                self.pipe.send("nextChunk")
                print "Sent the nextChunk Command to the Controller\n"
            except Exception as inst:
                print "========================================================================\n"
                print "Exception was thrown in sendNextChunkCommandToController: " +str(inst)+"\n"
                print "========================================================================\n"

        #Inbound commands from the client=========================================
        def checkForCrashedCommandFromClient(self,inboundData):  #NOTE: This is NOT modelled after the check for crash command in the previous revisions
            try:
                print "Checking for the Crashed Command from the Client\n"
                if(compareString(inboundData,"CRASHED",0,0,len("CRASHED"),len("CRASHED"))==True):
                    print "Crash Command was received from the Client\n"
                    return True
                else:
                    return False
            except Exception as inst:
                print "========================================================================\n"
                print "Exception thrown in checkForCrashedCommandFromClient: " +str(inst)+"\n"
                print "========================================================================\n"
                return False

        def checkForFoundSolutionCommandFromClient(self,inboundData):
            try:
                print "Checking for the Found Solution Command from the client\n"
                if(compareString(inboundData,"FOUNDSOLUTION",0,0,len("FOUNDSOLUTION"),len("FOUNDSOLUTION"))):
                    print "FOUNDSOLUTION Command was received from the client\n"
                    return True
                else:
                    return False
            except Exception as inst:
                print "========================================================================\n"
                print "Exception thrown in checkForFoundSolutionCommandFromClient: "+str(inst)+"\n"
                print "========================================================================\n"
                return False

        def checkForNextCommandFromClient(self,inboundData):
            try:
                print "Checking for the Next command from the client\n"
                if(compareString(inboundData,"NEXT",0,0,len("NEXT"),len("NEXT"))):
                    print "NEXT command was received from the client\n"
                    return True
                else:
                    return False
            except Exception as inst:
                print "========================================================================\n"
                print "Exception was thrown in checkForNextCommandFromClient: " +str(inst)+"\n"
                print "========================================================================\n"
                return False

        def receiveCommandFromClient(self, clientSocket): #NOTE new function, used to receive normal commands
            try:
                print "Acquiring socketLock\n"
                self.socketLock.acquire()
                print "Acquired socketLock\n"
                receivedCommandFromClient= ""
                print "Checking for inbound client Commands\n"
                clientInput= clientSocket.recv(4096)
                if(len(clientInput) > 0):
                    receivedCommandFromClient= clientInput
                #return command in finally block for this function
            except Exception as inst:
                print "===================================================================\n"
                print "ERROR in receiveCommandFromClient: " +str(inst)+"\n"
                print "===================================================================\n"
                receivedCommandFromClient= ""#set to empty string
            finally:
                print "Releasing socketLock\n"
                self.socketLock.release()
                print "Released socketLock\n"
                return receivedCommandFromClient


        #Outbound commands to client==================================================
        def sendDoneCommandToClient(self,networkSocket, clientIP):
            print "Issuing Done Command to Client: " + str(clientIP) +"\n"
            print "Acquiring socket lock\n"
            self.socketLock.acquire()
            print "Acquired socketLock\n"
            networkSocket.settimeout(0.25)
            print "socket lock acquired\n"
            try: #send try block
                print "preparing to send done command to client\n"
                networkSocket.send("done")
                print "sent Done command to client: " +str(clientIP) +"\n"
            except Exception as inst:
                if(compareString(str(inst),"[Errno 32] Broken pipe",0,0,len("[Errno 32] Broken pipe"),len("[Errno 32] Broken pipe"))):
                    print "========================================================================\n"
                    print "Exception thrown in sendDoneCommandToClient: Broken pipe error detected in send try block\n"
                    print "========================================================================\n"
                else:
                    print "========================================================================\n"
                    print "Exception in send Done command: " +str(inst) +"\n"
                    print "========================================================================\n"
            finally:
                print "Releasing the socketLock\n"
                self.socketLock.release()
                print "Released socketLock\n"

        def sendNextCommandToClient(self,clientSocket,chunkParams,chunkData): #NOTE: This is NOT modelled after the previous revision of sendNextCommandToCLient!!!
            try: #Main sendNextCommandToClient Try Block
                print "Acquiring socketLock\n"
                self.socketLock.acquire()
                print "Acquired socketLock\n"
                chunkParamsSize = 0 #initialize var
                chunkDataSize = 0 #initialize var
                commandString = "" #initializing var, this will hold the NEXT keyword and the file size of the chunk pieces
                #Pre-Step 1 (Measure the filesize of chunkParams and chunkData--------------------------------------
                try: #Measuring filesize of chunkParams and chunkData try block
                    print "Measuring filesize of chunkParams\n"
                    chunkParamsSize = sys.getsizeof(chunkParams)
                    print "filesize of chunkParams: " +str(chunkParamsSize)+"\n"
                    print "Measuring filesize of chunkData\n"
                    chunkDataSize = sys.getsizeof(chunkData)
                    print "filesize of chunkData: "+str(chunkDataSize)+"\n"
                    print "Creating the commandString\n"
                    commandString = "NEXT PSIZE("+str(chunkParamsSize)+") DSIZE("+str(chunkDataSize)+")\n" #PSIZE is the size of chunkParams and DSIZE is the size of chunkData
                    print "Finished creating the commandString\n"
                except Exception as inst:
                    print "========================================================================\n"
                    print "Inside the sendNextCommandToClient function\n"
                    print "Exception thrown in Pre-Step 1: Measuring filesize of chunkParams and chunkData Try Block: " +str(inst)+"\n"
                    print "========================================================================\n"
                    raise Exception ("Exception thrown in Pre-Step 1")
                #Step 1 (Send the commandString to the client)---------------------------------------------------------
                try: #send commandString to client try block
                    print "Sending commandString to the client\n"
                    clientSocket.send(commandString)
                    print "Sent the commandString to the client\n"
                except Exception as inst:
                    print "========================================================================\n"
                    print "Inside the sendNextCommandToClient function\n"
                    print "Exception was thrown in Step 1: send commandString to client: "+str(inst)+"\n"
                    print "========================================================================\n"
                    raise Exception ("Exception thrown in STep 1")
                #Step 2 (send the chunkParams to the client)-----------------------------------------------------------
                try: #send chunkParams to the client try block
                    print "Sending chunkParams to the client\n"
                    clientSocket.send(chunkParams)
                    print "Sent chunkParams to the client\n"
                except Exception as inst:
                    print "========================================================================\n"
                    print "Inside the sendNextCommandToCLient function\n"
                    print "Exception thrown in Step 2: send chunkParams to client: "+str(inst)+"\n"
                    print "========================================================================\n"
                    raise Exception ("Exception thrown in Step 2")
                #Step 3 (send the chunkData to the client------------------------------------------------------------
                try:
                    print "Sending chunkData to the client\n"
                    clientSocket.send(chunkData)
                    print "Sent chunkData to the client\n"
                except Exception as inst:
                    print "========================================================================\n"
                    print "Inside the sendNextCommandToCLient function\n"
                    print "Exception was thrown in STep 3: send chunkData to client: "+str(inst)+"\n"
                    print "========================================================================\n"
                    raise Exception ("Exception thrown in STep 3")
            except Exception as inst:
                print "========================================================================\n"
                print "Exception was thrown in Main sendNextCommandToClient Try Block: " +str(inst)+"\n"
                print "========================================================================\n"
            finally:
                print "Releasing socketLock\n"
                self.socketLock.release()
                print "Released socketLock\n"

        #dictionaryOfCurrentClientTasks functions================================================================
        #TODO insert functions that operate on the dictionaryOfCurrentClientTasks
            #TODO function to add a client to the dictionary
            #TODO function to remove a client from the dictionary
            #TODO function to check to see if a client is in the dictionary (using the check for a keyerror)
            #TODO function to get the chunk object from a client's key in the dictionary

        #list of CRashed clients functions====================================================================
        #TODO insert add function