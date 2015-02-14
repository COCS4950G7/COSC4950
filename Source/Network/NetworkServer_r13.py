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
    stopAllThreads = False #set to true to have all threads break out of their while loops
    listOfCrashedClients = []
    stackOfChunksThatNeedToBeReassigned = []
    stackOfClientsWaitingForNextChunk = []
    dictionaryOfCurrentClientTasks = {} #key is the client's IP Address , the value is the chunk that client is working on
                                        #If you try to access a non-existing key it will throw an error
    #NOTE: NOT GOING TO HAVE A LIST OF CONNECTED CLIENTS, JUST USE THE DICTIONARY OF CURRENT CLIENT TASKS INSTEAD

    socketLock = threading.RLock()

    #START OF CLIENT THREAD HANDLER
    def ClientThreadHandler(self, clientSocket, clientAddr, socketLock):
        try: #CLient THread Handler Try Block
            inboundCommandFromClient = "" #initialize the receiving variable
            while True:
                if(self.stopAllThreads == True):
                    print "Stopping the thread\n"
                    break
                try: #check for commands from client
                    inboundCommandFromClient = self.receiveCommandFromClient(clientSocket)
                except Exception as inst:
                    print "===================================================================\n"
                    print "Error in check for commands from the client in client thread handler: " +str(inst)+"\n"
                    print "===================================================================\n"

                try: #Analyzing received command from the client try block
                    if(len(inboundCommandFromClient) > 0): #ignore if the empty string
                        identifiedCommand = False
                        try: #checking to see if the next Command was received from the client try block
                            if(self.checkForNextCommandFromClient(inboundCommandFromClient)==True):
                                identifiedCommand= True
                                print "Identified inboundCommandFromClient as the Next Command\n"
                                #check to see if there is a chunk that needs to be reassigned
                                if(len(self.stackOfChunksThatNeedToBeReassigned) > 0):
                                    print "There is a chunk that needs to be reassigned.\n"
                                    #TODO extract the ip and port of the client from the inboundCommand
                                    #TODO Send the chunk that needs to be reassigned to the client
                                else:
                                    print "There is no chunk that needs to be reassigned. Requesting nextChunk from the Controller\n"
                                    self.sendNextChunkCommandToController()
                                    print "Adding the client to the stackOfClientsWaitingForNextChunk\n"
                                    #TODO extract the ip address and port of the client from the inboundCommand
                                    #TODO then add the client ip and port to the stackOfClientsWaitingForNextChunk
                        except Exception as inst:
                            print "===================================================================\n"
                            print "Error in checking to see if the next Command was received from the client in client thread handler: "+str(inst)+"\n"
                            print "===================================================================\n"

                        try: #check to see if the found solution command was received from the client
                            if(identifiedCommand == False):
                                if(self.checkForFoundSolutionCommandFromClient(inboundCommandFromClient)==True):
                                    identifiedCommand= True
                                    print "Identified inboundCommandFromClient as the found solution command\n"
                                    for key in self.dictionaryOfCurrentClientTasks.keys():
                                        self.sendDoneCommandToClient(key) #extracts the key from the dictionary and sends the done command to them
                                    print "Setting the thread termination value to true, stopping all threads\n"
                                    self.stopAllThreads = True
                        except Exception as inst:
                            print "===================================================================\n"
                            print "Error in check to see if found solution command was received from the client in client thread handler: "+str(inst)+"\n"
                            print "===================================================================\n"

                        try: #check to see if the crashed command was received
                            if(identifiedCommand == False):
                                if(self.checkForCrashedCommandFromClient(inboundCommandFromClient)==True):
                                    identifiedCommand= True
                                    print "Identified inboundCommandFromClient as the Crashed Command\n"
                                    #TODO extract the clients ip address and port from the inboundCommandFromClient
                                    #TODO add the client's current task (chunk) onto the stackOfChunksThatNeedToBeReassigned
                                    self.addClientToListOfCrashedClients()
                                    #TODO delete the client from the dictionaryOfCurrentClientTasks
                        except Exception as inst:
                            print "===================================================================\n"
                            print "Error in check to see if crashed command was received from client in client thread handler: "+ str(inst)+"\n"
                            print "===================================================================\n"

                        if(identifiedCommand == False):
                            print "Warning: Unknown Command Received from the client: "+str(inboundCommandFromClient)+"\n"
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
                if(self.stopAllThreads == True):
                    print "Stopping Main Thread\n"
                    break
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
                        if(len(receivedControllerCommand) > 0): #ignore the empty string
                            print "Received command from the controller\n"
                            identifiedCommand = False
                            try: #checking for nextChunk Command from Controller
                                if(self.checkForNextChunkCommandFromController(receivedControllerCommand)==True):
                                    identifiedCommand= True
                                    print "Identified receivedControllerCommand as the nextChunk Command\n"
                                    #check to see if a client is waiting for the nextChunk
                                    if(len(self.stackOfClientsWaitingForNextChunk) > 0):
                                        print "A client is waiting for the nextChunk\n"
                                        #TODO send the chunk to the client waiting for the next chunk
                                    else: #if there is no client waiting for the  next chunk
                                        print "No clients are waiting for the nextChunk. Adding chunk to the stackOfChunksThatNeedToBeReassigned\n"
                                        #TODO add the chunk to the stackOfChunksThatNeedToBeReassigned
                            except Exception as inst:
                                print "===================================================================\n"
                                print "Error in checking for nextChunk Command from Controller Try Block: " +str(inst)+"\n"
                                print "===================================================================\n"

                            try: #checking for done command form controller
                                if(identifiedCommand == False):
                                    if(self.checkForDoneCommandFromController(receivedControllerCommand)==True):
                                        identifiedCommand= True
                                        print "Identified receivedControllerCommand as the Done Command\n"
                                        #No further actions are needed for this command
                            except Exception as inst:
                                print "===================================================================\n"
                                print "Error in checking for done command from Controller Try Block: "+str(inst)+"\n"
                                print "===================================================================\n"

                            if(identifiedCommand == False):
                                print "Warning: Unknown Command Received from the Controller: "+str(receivedControllerCommand)+"\n"
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
            self.sendDoneCommandToController()


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

        def sendDoneCommandToController(self):
            try:
                print "Sending done Command to the Controller\n"
                self.pipe.send("done")
                print "Sent the done Command to the Controller\n"
            except Exception as inst:
                print "========================================================================\n"
                print "Exception thrown in sendDoneCommandToController: "+str(inst)+"\n"
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
        def addClientToDictionaryOfCurrentClientTasks(self, clientAddress, clientChunk): #client Address has both the ip address and port
            try:
                self.dictionaryOfCurrentClientTasks[clientAddress] = clientChunk
            except Exception as inst:
                print "========================================================================\n"
                print "ERROR in addClientToDictionaryOfCurrentClientTasks: "+str(inst)+"\n"
                print "========================================================================\n"

        def delClientFromDictionaryOfCurrentClientTasks(self, clientAddress): #clientAddress contains IP and port
            try:
                del self.dictionaryOfCurrentClientTasks[clientAddress]
            except KeyError as inst:
                print "========================================================================\n"
                print "ERROR: " +str(clientAddress)+" does not exist in the dictionaryOfCurrentClientTasks\n"
                print "========================================================================\n"
            except Exception as inst:
                print "========================================================================\n"
                print "ERROR in delClientFromDictionaryOfCurrentClientTasks: "+str(inst)+"\n"
                print "========================================================================\n"

        def getChunkFromDictionaryOfCurrentClientTasks(self, clientAddress): #clientAddress contains IP and port
            try:
                retrievedChunk = self.dictionaryOfCurrentClientTasks[clientAddress]
                return retrievedChunk
            except KeyError as inst:
                print "========================================================================\n"
                print "ERROR: " +str(clientAddress)+" does not exist in the dictionaryOfCurrentClientTasks\n"
                print "========================================================================\n"
                return None
            except Exception as inst:
                print "========================================================================\n"
                print "ERROR in getChunkFromDictionaryOfCurrentClientTasks: "+str(inst)+"\n"
                print "========================================================================\n"
                return None

        #list of Crashed clients functions====================================================================
        def addClientToListOfCrashedClients(self, clientAddress): #clientAddress has the ip and the port
            try:
                self.listOfCrashedClients.append(clientAddress)
            except Exception as inst:
                print "========================================================================\n"
                print "ERROR in addClientToListOfCrashedClients: " + str(inst)+"\n"
                print "========================================================================\n"

        #stackOfChunksThatNeedToBeReassigned functions==========================================================
        def pushChunkOnToStackOfChunksThatNeedToBeReassigned(self, inboundChunk):
            try:
                print "Pushing chunk onto the stackOfChunksThatNeedToBeReassigned\n"
                self.stackOfChunksThatNeedToBeReassigned.append(inboundChunk)
                print "Pushed chunk onto the stackOfChunksThatNeedToBeReassigned\n"
            except Exception as inst:
                print "========================================================================\n"
                print "ERROR in pushChunkOnToStackOfChunksThatNeedToBeReassigned: "+str(inst)+"\n"
                print "========================================================================\n"

        def popChunkFromStackOfChunksThatNeedToBeReassigned(self):
            try:
                poppedChunk = ""
                print "Popping chunk from stackOfChunksThatNeedToBeReassigned\n"
                poppedChunk = self.stackOfChunksThatNeedToBeReassigned.pop()
                print "Popped chunk off the stackOfChunksThatNeedToBeReassigned\n"
                return poppedChunk
            except Exception as inst:
                print "========================================================================\n"
                print "ERROR in popChunkFromStackOfChunksThatNeedToBeReassigned: "+str(inst)+"\n"
                print "========================================================================\n"
                return None

        #stackOfClientsWaitingForNextChunk functions============================================================
        def pushClientOnToStackOfClientsWaitingForNextChunk(self, clientAddress):
            try:
                print "Pushing client on to stackOfClientsWaitingForNextChunk\n"
                self.stackOfClientsWaitingForNextChunk.append(clientAddress)
                print "Pushed client on to stackOfClientsWaitingForNextChunk\n"
            except Exception as inst:
                print "========================================================================\n"
                print "ERROR in pushClientOnToStackOfClientsWaitingForNextChunk: "+str(inst)+"\n"
                print "========================================================================\n"

        def popClientFromStackOfClientsWaitingForNextChunk(self):
            try:
                poppedChunk= ""
                print "Popping client off the stackOfClientsWaitingForNextChunk\n"
                poppedChunk= self.stackOfClientsWaitingForNextChunk.pop()
                print "Popped client off the stackOfClientsWaitingForNextChunk\n"
                return poppedChunk
            except Exception as inst:
                print "========================================================================\n"
                print "ERROR in popClientFromStackOfClientsWaitingForNextChunk: "+str(inst)+"\n"
                print "========================================================================\n"
                return None