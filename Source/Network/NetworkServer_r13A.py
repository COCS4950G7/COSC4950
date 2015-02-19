__author__ = 'chris hamm'
#NetworkServer_r13A
#Created: 2/17/2015

#Designed to work with NetworkClient_r13A


#Changes/Additions made to this revision:
    #Added a IO command stack that contains all IO commands tthe have been sent/received
    #Changed checkforFOundSolutionCOmmandFromClient to look at the first element in the inbound tuple for the foundsolution string
    #Added a extractSolutionFromFOundSolutionTuple function
    #Added theSolution variable that stores what the solution is, this is printed out at the end
    #Added function that sends the solution to the controller
    #Now sends the solution to the controller after sending the found solution command to the coontroller
    #stackOfIOCommands now also stores errors
    #commanted out unused function sendChunkToClient (replaced by " bylength)
    #Optimized for speed (see below)

    #Speed optimization changes:
        #[currently running at 0.1] socket timeouts set to 0.000001 seconds (tried using 0.0000001 but it caused a crash)
        #commented out most print statements
        #[currently running at 0.1] changed the time.sleep(0.25) to time.sleep(0.000001) (tried using 0.0000001 but it caused a crash)



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
                print "========================================================================\n"
                print "Exception thrown in compareString Function: " +str(inst)+"\n"
                print "========================================================================\n"
                return False

def extractSolutionFromFoundSolutionTuple(self, inboundTuple):
    try:
        theSolution = str(inboundTuple[1]) #second element in the tuple
        return theSolution
    except Exception as inst:
        print "===========================================================\n"
        print "Exception thrown in extractSolutionFromFoundSolutionTuple: "+str(inst)+"\n"
        print "===========================================================\n"
        pushCommandOntoTheStackOfIOCommands(self, "EXCEPTION in extractSolutionFromFoundSolutionTuple", "Self", "Self")
        return "" #return empty string

#Stack of IO Commands=======================================================
def pushCommandOntoTheStackOfIOCommands(self, commandName, commandOrigin_Destination, commandDirection):
    try:
        import time
        current_time= time.time()
        #print "Acquiring the stackOfIOCommands Lock"
        self.stackOfIOCommandsLock.acquire()
        #print "Acquired the stackOfIOCommands Lock"
        self.stackOfIOCommands.append((commandName, commandOrigin_Destination, commandDirection, current_time ))#tuple contains name, origin/destination, direction, time
    except Exception as inst:
        print "======================================================\n"
        print "Exception was thrown in pushCommandOntoTheStackOfIOCommands: "+str(inst)+"\n"
        print "=======================================================\n"
        pushCommandOntoTheStackOfIOCommands(self, "EXCEPTION in pushCommandOnToTheStackOfIOCommands", "Self", "Self")
    finally:
        #print "Releasing the stackOfIOCommands Lock"
        self.stackOfIOCommandsLock.release()
        #print "Released the stackOfIOCommands Lock"

#Inbound commands from controller==========================================
def checkForDoneCommandFromController(self, inboundString):
    try:
        #print "Checking for done Command from the Controller\n"
        if(compareString(str(inboundString),"done",0,0,len("done"),len("done"))==True):
            #print "done Command was received from the Controller\n"
            pushCommandOntoTheStackOfIOCommands(self, "done", "Controller","Inbound" )
            return True
        else:
            return False
    except Exception as inst:
        print "========================================================================\n"
        print "Exception thrown in checkForDoneCommandFromController: "+str(inst)+"\n"
        print "========================================================================\n"
        pushCommandOntoTheStackOfIOCommands(self, "EXCEPTION in checkForDoneCommandFromCOntroller", "Controller", "Inbound")
        return False

def checkForNextChunkCommandFromController(self, inboundString):
    try:
        #print "Checking for nextChunk Command from the Controller\n"
        if(compareString(str(inboundString),"nextChunk",0,0,len("nextChunk"),len("nextChunk"))==True):
            #print "nextChunk Command was received from the Controller\n"
            pushCommandOntoTheStackOfIOCommands(self, "nextChunk", "Controller", "Inbound")
            return True
        else:
            return False
    except Exception as inst:
        print "========================================================================\n"
        print "Exception thrown in checkForNextChunkCommandFromController: " +str(inst)+"\n"
        print "========================================================================\n"
        pushCommandOntoTheStackOfIOCommands(self, "EXCEPTION in checkForNextChunkCommandFromController", "Controller", "Inbound")
        return False

def receiveNextChunkFromController(self):
    try:
        #print "Receiving Chunk From the Pipe\n"
        inboundChunk= self.pipe.recv()
       # print "Received the Chunk from the pipe\n"
        pushCommandOntoTheStackOfIOCommands(self, "nextChunk", "Controller", "Inbound")
        return inboundChunk
    except Exception as inst:
        print "========================================================================\n"
        print "ERROR in receiveNextChunkFromController: "+str(inst)+"\n"
        print "========================================================================\n"
        pushCommandOntoTheStackOfIOCommands(self, "ERROR in receiveNextChunkFromController", "Controller", "Inbound")
        return ""

#Outbound commands to controller======================================
def sendNextChunkCommandToController(self):
    try:
       # print "Sending nextChunk Command to the Controller\n"
        self.pipe.send("nextChunk")
        #print "Sent the nextChunk Command to the Controller\n"
        pushCommandOntoTheStackOfIOCommands(self, "nextChunk", "Controller", "Outbound")
    except Exception as inst:
        print "========================================================================\n"
        print "Exception was thrown in sendNextChunkCommandToController: " +str(inst)+"\n"
        print "========================================================================\n"
        pushCommandOntoTheStackOfIOCommands(self, "EXCEPTION in sendNextChunkCommandToController", "Controller", "Outbound")


def sendDoneCommandToController(self):
    try:
       # print "Sending done Command to the Controller\n"
        self.pipe.send("done")
       # print "Sent the done Command to the Controller\n"
        pushCommandOntoTheStackOfIOCommands(self, "done", "Controller", "Outbound")
    except Exception as inst:
        print "========================================================================\n"
        print "Exception thrown in sendDoneCommandToController: "+str(inst)+"\n"
        print "========================================================================\n"
        pushCommandOntoTheStackOfIOCommands(self, "EXCEPTION in sendDoneCommandToController", "Controller", "Outbound")

def sendSolutionToController(self):
    try:
        #get the solution from the class variable that  stores it
        #print "Sending Solution To Controller\n"
        self.pipe.send(str(self.theSolution))
       # print "Sent solution to the controller\n"
        pushCommandOntoTheStackOfIOCommands(self, "sendSolution", "Controller", "Outbound")
    except Exception as inst:
        print "==================================================================\n"
        print "Exception thrown in sendSolutionToController: "+str(inst)+"\n"
        print "==================================================================\n"
        pushCommandOntoTheStackOfIOCommands(self, "EXCEPTION in sendSolutionToController", "Controller", "Outbound")

#Inbound commands from the client=========================================
def checkForCrashedCommandFromClient(self,inboundData):  #NOTE: This is NOT modelled after the check for crash command in the previous revisions
    try:
       # print "Checking for the Crashed Command from the Client\n"
        if(compareString(str(inboundData),"CRASHED",0,0,len("CRASHED"),len("CRASHED"))==True):
            #print "Crash Command was received from the Client\n"
            pushCommandOntoTheStackOfIOCommands(self, "CRASHED", "Client", "Inbound")
            return True
        else:
            return False
    except Exception as inst:
        print "========================================================================\n"
        print "Exception thrown in checkForCrashedCommandFromClient: " +str(inst)+"\n"
        print "========================================================================\n"
        pushCommandOntoTheStackOfIOCommands(self, "EXCEPTION in checkForCrashedCommandFromClient", "Client", "Inbound")
        return False

def checkForFoundSolutionCommandFromClient(self,inboundData):
    try:
        #print "Checking for the Found Solution Command from the client\n"
        if(compareString(str(inboundData),"FOUNDSOLUTION",0,0,len("FOUNDSOLUTION"),len("FOUNDSOLUTION"))): #access the first element iin the tuple
            #print "FOUNDSOLUTION Command was received from the client\n"
            #Extracting solution from the string
            #inboundData= FOUNDSOLUTION [solution]
            #inboundData[0:14]= FOUNDSOLUTION (including the space)
            #first bracket is at [15]
            openingBracketPos = 15
            closingBracketPos = 15
            theInboundSolution = ""
            for index in range(openingBracketPos, len(inboundData)):
                if(inboundData[index] == "]"):
                   # print "Extraction of solution is complete\n"
                    closingBracketPos= index
                    break
                else:
                    theInboundSolution+= str(inboundData[index])
            if(closingBracketPos == 15): #where it started
                raise Exception("closing bracket not found")
            pushCommandOntoTheStackOfIOCommands(self, "FOUNDSOLUTION", "Client", "Inbound")
            #set the class variab;e that holds the solution
            self.theSolution= theInboundSolution
            return True
        else:
            return False
    except Exception as inst:
        print "========================================================================\n"
        print "Exception thrown in checkForFoundSolutionCommandFromClient: "+str(inst)+"\n"
        print "========================================================================\n"
        pushCommandOntoTheStackOfIOCommands(self, "EXCEPTION in checkForFoundSOlutionCommandFromClient", "Client", "Inbound")
        return False

def checkForNextCommandFromClient(self,inboundData):
    try:
       # print "Checking for the Next command from the client\n"
        if(compareString(str(inboundData),"NEXT",0,0,len("NEXT"),len("NEXT"))):
            #print "NEXT command was received from the client\n"
            pushCommandOntoTheStackOfIOCommands(self, "NEXT", "Client", "Inbound")
            return True
        else:
            return False
    except Exception as inst:
        print "========================================================================\n"
        print "Exception was thrown in checkForNextCommandFromClient: " +str(inst)+"\n"
        print "========================================================================\n"
        pushCommandOntoTheStackOfIOCommands(self, "EXCEPTION in checkForNextCommandFromCLient", "Client", "Inbound")
        return False

def receiveCommandFromClient(self, clientSocket): #NOTE new function, used to receive normal commands
    while True:
        try:
            receivedCommandFromClient = ""
            #print "Acquiring socketLock"
            self.socketLock.acquire()
            #print "Acquired socketLock"
            #print "Checking for inbound client Commands"
            #clientSocket.settimeout(0.25)
            clientSocket.settimeout(0.1)
            #clientSocket.settimeout(0.05)
            #clientSocket.settimeout(0.01)
            #clientSocket.settimeout(0.001)
            #clientSocket.settimeout(0.0001)
            #clientSocket.settimeout(0.00001)
            #clientSocket.settimeout(0.0000001)
            clientInput= clientSocket.recv(4096)
            if(len(clientInput) > 0):
                receivedCommandFromClient= clientInput
                break
            #return command in finally block for this function
        except Exception as inst:
            if(compareString(str(inst),"[Errno 35] Resource temporarily unavailable",0,0,len("[Errno 35] Resource temporarily unavailable"),len("[Errno 35] Resource temporarily unavailable"))==True):
                print "[Errno 35] Resource is not available in receiveCommandFromClient, trying again.\n"
            elif(compareString(str(inst),"timed out",0,0,len("timed out"),len("timed out"))==True):
                #ignore, do no print out error
                break
            else:
                print "===================================================================\n"
                print "ERROR in receiveCommandFromClient: " +str(inst)+"\n"
                print "===================================================================\n"
                pushCommandOntoTheStackOfIOCommands(self, "ERROR in receiveCommandFromClient", "Client", "Inbound")
                receivedCommandFromClient= ""#set to empty string
                break
        finally:
            #print "Releasing socketLock\n"
            self.socketLock.release()
            #print "Released socketLock\n"
            return receivedCommandFromClient


#Outbound commands to client==================================================
def sendDoneCommandToClient(self,networkSocket, clientIP):
    #print "Issuing Done Command to Client: " + str(clientIP) +"\n"
    #print "Acquiring socket lock\n"
    self.socketLock.acquire()
    #print "Acquired socketLock\n"
    #networkSocket.settimeout(0.25)
    networkSocket.settimeout(0.1)
    #networkSocket.settimeout(0.05)
    #networkSocket.settimeout(0.01)
    #networkSocket.settimeout(0.001)
    #networkSocket.settimeout(0.0001)
    #networkSocket.settimeout(0.00001)
    #networkSocket.settimeout(0.0000001)
    #print "socket lock acquired\n"
    try: #send try block
       # print "preparing to send done command to client\n"
        networkSocket.send("done")
        #print "sent Done command to client: " +str(clientIP) +"\n"
        pushCommandOntoTheStackOfIOCommands(self, "done", "Client", "Outbound")
    except Exception as inst:
        if(compareString(str(inst),"[Errno 32] Broken pipe",0,0,len("[Errno 32] Broken pipe"),len("[Errno 32] Broken pipe"))):
            print "========================================================================\n"
            print "Exception thrown in sendDoneCommandToClient: Broken pipe error detected in send try block\n"
            print "========================================================================\n"
            pushCommandOntoTheStackOfIOCommands(self, "EXCEPTION in sendDoneCommandToClient: Broken Pipe", "Client", "Outbound")
        else:
            print "========================================================================\n"
            print "Exception in send Done command: " +str(inst) +"\n"
            print "========================================================================\n"
            pushCommandOntoTheStackOfIOCommands(self, "EXCEPTION in sendDoneCommandToClient", "Client", "Outbound")
    finally:
        #print "Releasing the socketLock\n"
        self.socketLock.release()
        #print "Released socketLock\n"

def sendNextCommandToClientByLength(self, clientSocket, chunkObject): #This sends the measurements to the client in length instead of file size
    try:
        #print "Acquiring the socketLock\n"
        self.socketLock.acquire()
        #print "Acquired the socketLock\n"
        chunkParamLength = len(str(chunkObject.params))
        chunkDataLength = len(str(chunkObject.data))
        #Create the command string
        commandString= ""
        try:
            commandString = "NEXT PSIZE("+str(chunkParamLength)+") DSIZE("+str(chunkDataLength)+")\n" #keeping same names, even though it is length
        except Exception as inst:
            print "========================================================================\n"
            print "Error in create command string step of sendNextCommandToCLientByLength: "+str(inst)+"\n"
            print "========================================================================\n"
            pushCommandOntoTheStackOfIOCommands(self, "ERROR in createCommandStringStep of sendNextCommandToClientByLength", "Client", "Outbound")
        #Send command string to the client
        try:
           # print "Sending command string to the client\n"
            clientSocket.send(commandString)
            import time
            #time.sleep(0.25)
            time.sleep(0.1)
           #time.sleep(0.05)
           #time.sleep(0.01)
            #time.sleep(0.001)
            #time.sleep(0.0001)
            #time.sleep(0.00001)
           # time.sleep(0.000001)
            #time.sleep(0.0000001)
           # print "Sent the command string to the client\n"
        except Exception as inst:
            print "========================================================================\n"
            print "Error in send command string to client in sendNextCOmmandToCLientByLength: "+str(inst)+"\n"
            print "========================================================================\n"
            pushCommandOntoTheStackOfIOCommands(self, "ERROR in sendCommandStringToClient of sendNextCommandToClientByLength", "Client", "Outbound")
        #Send the chunk params to the client
        try:
           # print "Sending chunk params to the client\n"
            while True:
                try:
                    clientSocket.send(str(chunkObject.params))
                   # print "Sent chunk params to the client\n"
                    pushCommandOntoTheStackOfIOCommands(self, "next: chunk.params", "Client", "Outbound")
                    break
                except Exception as inst:
                    if(compareString(str(inst),"timed out",0,0,len("timed out"),len("timed out"))==True):
                        #dont throw an error, just try again
                        fakeVar=True
                    else:
                        raise Exception ("Error in sending chunk params to the client in infinite while loop")
                        break
        except Exception as inst:
            print "========================================================================\n"
            print "Error in send chunk params to the client in sendNextCOmmandToClientByLength: "+str(inst)+"\n"
            print "========================================================================\n"
            pushCommandOntoTheStackOfIOCommands(self, "ERROR in sendChunkParamsToClient of sendNextCommandToClientByLength", "Client", "Outbound")
        #send the chunk data to the client
        try:
           # print "Sending chunk data to the client\n"
            while True:
                try:
                    clientSocket.send(str(chunkObject.data))

                    #print "Sent chunk data to the client\n"
                    pushCommandOntoTheStackOfIOCommands(self, "next: chunk.data", "Client", "Outbound")
                    break
                except Exception as inst:
                    if(compareString(str(inst),"timed out",0,0,len("timed out"),len("timed out"))==True):
                        #dont throw error, just try again
                        fakeVar=True
                    else:
                        raise Exception ("Error in sending chunk data to the client in infinite loop")
                    break
        except Exception as inst:
            print "========================================================================\n"
            print "Error in send chunk data to the client in sendNextCOmmandToClientByLength: "+str(inst)+"\n"
            print "========================================================================\n"
            pushCommandOntoTheStackOfIOCommands(self, "ERROR in sendChunkDataToClient of sendNextCommandToClientByLength", "Client", "Outbound")
    except Exception as inst:
        print "========================================================================\n"
        print "ERROR in sendNextCommandToClientByLength: "+str(inst)+"\n"
        print "========================================================================\n"
        pushCommandOntoTheStackOfIOCommands(self, "ERROR in sendNextCommandToClientByLength", "Client", "Outbound")
    finally:
        #print "Releasing the socketLock\n"
        self.socketLock.release()
        #print "Released the socketLock\n"

''' THIS COMMAND HAS BEEN REPLACED BY sendNextCommandToClientByLength
def sendNextCommandToClient(self,clientSocket,chunkObject): #NOTE: This is NOT modelled after the previous revision of sendNextCommandToCLient!!!
    try: #Main sendNextCommandToClient Try Block
        #print "Acquiring socketLock\n"
        self.socketLock.acquire()
        #print "Acquired socketLock\n"
       # print "Type of the chunkObject: "+str(type(chunkObject))+"\n"
        chunkParams = str(chunkObject.params)
        chunkData = str(chunkObject.data)
        chunkParamsSize = 0 #initialize var
        chunkDataSize = 0 #initialize var
        commandString = "" #initializing var, this will hold the NEXT keyword and the file size of the chunk pieces
        #Pre-Step 1 (Measure the filesize of chunkParams and chunkData--------------------------------------
        try: #Measuring filesize of chunkParams and chunkData try block
           # print "Measuring filesize of chunkParams\n"
            chunkParamsSize = sys.getsizeof(chunkParams)
           # print "filesize of chunkParams: " +str(chunkParamsSize)+"\n"
           # print "Measuring filesize of chunkData\n"
            chunkDataSize = sys.getsizeof(chunkData)
            #print "filesize of chunkData: "+str(chunkDataSize)+"\n"
           # print "Creating the commandString\n"
            commandString = "NEXT PSIZE("+str(chunkParamsSize)+") DSIZE("+str(chunkDataSize)+")\n" #PSIZE is the size of chunkParams and DSIZE is the size of chunkData
           # print "Finished creating the commandString\n"
        except Exception as inst:
            print "========================================================================\n"
            print "Inside the sendNextCommandToClient function\n"
            print "Exception thrown in Pre-Step 1: Measuring filesize of chunkParams and chunkData Try Block: " +str(inst)+"\n"
            print "========================================================================\n"
            pushCommandOntoTheStackOfIOCommands(self, "EXCEPTION in Pre-Step 1 of sendNextCommandToClient", "Client", "Outbound")
            raise Exception ("Exception thrown in Pre-Step 1")
        #Step 1 (Send the commandString to the client)---------------------------------------------------------
        try: #send commandString to client try block
            #print "Sending commandString to the client\n"
            clientSocket.send(commandString)
           # print "Sent the commandString to the client\n"
        except Exception as inst:
            print "========================================================================\n"
            print "Inside the sendNextCommandToClient function\n"
            print "Exception was thrown in Step 1: send commandString to client: "+str(inst)+"\n"
            print "========================================================================\n"
            #self.listOfServerErrors.append(str(inst))
            raise Exception ("Exception thrown in STep 1")
        #Step 2 (send the chunkParams to the client)-----------------------------------------------------------
        try: #send chunkParams to the client try block
           # print "Sending chunkParams to the client\n"
            while True:
                try:
                    clientSocket.send(chunkParams)
                   # print "Sent chunkParams to client\n"
                    break
                except Exception as inst:
                    if(compareString(str(inst),"timed out",0,0,len("timed out"), len("timed out"))==True):
                        #dont throw error or this, just try again
                        fakeVar=True
                    else:
                        raise Exception ("Error in sending chunkParams to client")
                        break
        except Exception as inst:
            print "========================================================================\n"
            print "Inside the sendNextCommandToCLient function\n"
            print "Exception thrown in Step 2: send chunkParams to client: "+str(inst)+"\n"
            print "========================================================================\n"
            raise Exception ("Exception thrown in Step 2")
        #Step 3 (send the chunkData to the client------------------------------------------------------------
        try:
            #print "Sending chunkData to the client\n"
            while True:
                try:
                    clientSocket.send(chunkData)
                   # print "Sent chunkData to the client\n"
                    break
                except Exception as inst:
                    if(compareString(str(inst),"timed out",0,0,len("timed out"),len("timed out"))==True):
                        #dont throw error, just try again
                        fakeVar=True
                    else:
                        raise Exception ("Error in sending chunkData to client")
                        break
        except Exception as inst:
            print "========================================================================\n"
            print "Inside the sendNextCommandToCLient function\n"
            print "Exception was thrown in STep 3: send chunkData to client: "+str(inst)+"\n"
            print "========================================================================\n"
            raise Exception ("Exception thrown in STep 3")
    except Exception as inst:
        print "========================================================================\n"
        print "Exception was thrown in Main sendNextCommandToClient Try Block: " +str(inst)+"\n"
    finally:
        #print "Releasing socketLock\n"
        self.socketLock.release()
        #print "Released socketLock\n"
'''

#dictionaryOfCurrentClientTasks functions================================================================
def addClientToDictionaryOfCurrentClientTasks(self, clientAddress, clientChunk): #client Address has both the ip address and port
    try:
        self.dictionaryOfCurrentClientTasks[clientAddress] = clientChunk
    except Exception as inst:
        print "========================================================================\n"
        print "ERROR in addClientToDictionaryOfCurrentClientTasks: "+str(inst)+"\n"
        print "========================================================================\n"
        pushCommandOntoTheStackOfIOCommands(self, "ERROR in addClientToDictionaryOfCurrentClientTasks", "Self", "Self")

def delClientFromDictionaryOfCurrentClientTasks(self, clientAddress): #clientAddress contains IP and port
    try:
        del self.dictionaryOfCurrentClientTasks[clientAddress]
    except KeyError as inst:
        print "========================================================================\n"
        print "ERROR: " +str(clientAddress)+" does not exist in the dictionaryOfCurrentClientTasks\n"
        print "========================================================================\n"
        pushCommandOntoTheStackOfIOCommands(self, "ERROR (Key Error) in delClientFromDictionaryOfCurrentClientTasks", "Self", "Self")
    except Exception as inst:
        print "========================================================================\n"
        print "ERROR in delClientFromDictionaryOfCurrentClientTasks: "+str(inst)+"\n"
        print "========================================================================\n"
        pushCommandOntoTheStackOfIOCommands(self, "ERROR in delClientFromDictionaryOfCurrentClientTasks", "Self", "Self")

def getChunkFromDictionaryOfCurrentClientTasks(self, clientAddress): #clientAddress contains IP and port
    try:
        retrievedChunk = self.dictionaryOfCurrentClientTasks[clientAddress]
        return retrievedChunk
    except KeyError as inst:
        print "========================================================================\n"
        print "ERROR: " +str(clientAddress)+" does not exist in the dictionaryOfCurrentClientTasks\n"
        print "========================================================================\n"
        pushCommandOntoTheStackOfIOCommands(self, "ERROR (Key Error) in getClientFromDictionaryOfCurrentClientTasks", "Self", "Self")
        return "" #changed from none
    except Exception as inst:
        print "========================================================================\n"
        print "ERROR in getChunkFromDictionaryOfCurrentClientTasks: "+str(inst)+"\n"
        print "========================================================================\n"
        pushCommandOntoTheStackOfIOCommands(self, "ERROR in getClientFromDictionaryOfCurrentClientTasks", "Self", "Self")
        return "" #changed from none

def setChunkToDictionaryOfCurrentClientTasks(self, clientAddr, chunkObject):
    try:
        self.dictionaryOfCurrentClientTasks[clientAddr] = chunkObject
    except Exception as inst:
        print "=======================================================================\n"
        print "ERROR in setChunkToDIctionaryOfCurrentCLientTasks: " +str(inst)+"\n"
        print "=======================================================================\n"
        pushCommandOntoTheStackOfIOCommands(self, "ERROR in setClientFromDictionaryOfCurrentClientTasks", "Self", "Self")


#list of Crashed clients functions====================================================================
def addClientToListOfCrashedClients(self, clientAddress): #clientAddress has the ip and the port
    try:
        self.listOfCrashedClients.append(clientAddress)
    except Exception as inst:
        print "========================================================================\n"
        print "ERROR in addClientToListOfCrashedClients: " + str(inst)+"\n"
        print "========================================================================\n"
        pushCommandOntoTheStackOfIOCommands(self, "ERROR in addClientToListOfCrashedClients", "Self", "Self")

#stackOfChunksThatNeedToBeReassigned functions==========================================================
def pushChunkOnToStackOfChunksThatNeedToBeReassigned(self, inboundChunk):
    try:
        #print "Pushing chunk onto the stackOfChunksThatNeedToBeReassigned\n"
        self.stackOfChunksThatNeedToBeReassigned.append(inboundChunk)
       # print "Pushed chunk onto the stackOfChunksThatNeedToBeReassigned\n"
    except Exception as inst:
        print "========================================================================\n"
        print "ERROR in pushChunkOnToStackOfChunksThatNeedToBeReassigned: "+str(inst)+"\n"
        print "========================================================================\n"
        pushCommandOntoTheStackOfIOCommands(self, "ERROR in pushChunksOnToStackOfChunksThatNeedToBeReassigned", "Self", "Self")

def popChunkFromStackOfChunksThatNeedToBeReassigned(self):
    try:
        poppedChunk = ""
       # print "Popping chunk from stackOfChunksThatNeedToBeReassigned\n"
        poppedChunk = self.stackOfChunksThatNeedToBeReassigned.pop()
       # print "Popped chunk off the stackOfChunksThatNeedToBeReassigned\n"
        return poppedChunk
    except Exception as inst:
        print "========================================================================\n"
        print "ERROR in popChunkFromStackOfChunksThatNeedToBeReassigned: "+str(inst)+"\n"
        print "========================================================================\n"
        pushCommandOntoTheStackOfIOCommands(self, "ERROR in popChunkFromStackOfChunksThatNeedToBeReassigned", "Self", "Self")
        return "" #changed from none

#stackOfClientsWaitingForNextChunk functions============================================================
def pushClientOnToStackOfClientsWaitingForNextChunk(self, clientSocket, clientAddress):
    try:
        #print "Pushing client on to stackOfClientsWaitingForNextChunk\n"
        self.stackOfClientsWaitingForNextChunk.append((clientSocket,clientAddress)) #holds a tuple
       # print "Pushed client on to stackOfClientsWaitingForNextChunk\n"
    except Exception as inst:
        print "========================================================================\n"
        print "ERROR in pushClientOnToStackOfClientsWaitingForNextChunk: "+str(inst)+"\n"
        print "========================================================================\n"
        pushCommandOntoTheStackOfIOCommands(self, "ERROR in pushClientOnToStackOfClientsWaitingForNextChunk", "Self", "Self")

def popClientFromStackOfClientsWaitingForNextChunk(self):
    try:
        poppedClient= ""
       # print "Popping client off the stackOfClientsWaitingForNextChunk\n"
        poppedClient= self.stackOfClientsWaitingForNextChunk.pop()
       # print "Popped client off the stackOfClientsWaitingForNextChunk\n"
        return poppedClient
    except Exception as inst:
        print "========================================================================\n"
        print "ERROR in popClientFromStackOfClientsWaitingForNextChunk: "+str(inst)+"\n"
        print "========================================================================\n"
        pushCommandOntoTheStackOfIOCommands(self, "ERROR in popClientFromStackOfClientsWaitingForNextChunk", "Self", "Self")
        return "" #changed from none


import threading
import thread
from socket import *
import sys
import platform

class NetworkServer():

    #CLASS VARS
    host = ''
    port = 55568
    myIPAddress = '127.0.0.1' #default to ping back address
    stopAllThreads = False #set to true to have all threads break out of their while loops
    listOfCrashedClients = []
    theSolution = "" #holds the solution if found
    stackOfIOCommands = [] #holds a record all the IO commands that have been sent through server
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
                    #print "MAIN THREAD: Stopping the thread\n"
                   # print "Sending done command to connected client\n"
                    sendDoneCommandToClient(self, clientSocket, clientAddr)
                    break
                try: #check for commands from client
                    inboundCommandFromClient = receiveCommandFromClient(self,clientSocket)
                except Exception as inst:
                    print "===================================================================\n"
                    print "Error in check for commands from the client in client thread handler: " +str(inst)+"\n"
                    print "===================================================================\n"
                    pushCommandOntoTheStackOfIOCommands(self, "ERROR in checkForCommandsFromTheClientInClientThreadHeader", "Self", "Self")

                try: #Analyzing received command from the client try block
                    if(len(inboundCommandFromClient) > 0): #ignore if the empty string
                        identifiedCommand = False
                        try: #checking to see if the next Command was received from the client try block
                            if(checkForNextCommandFromClient(self,inboundCommandFromClient)==True):
                                identifiedCommand= True
                                #print "Identified inboundCommandFromClient as the Next Command\n"
                                #check to see if there is a chunk that needs to be reassigned
                                if(len(self.stackOfChunksThatNeedToBeReassigned) > 0):
                                    #print "There is a chunk that needs to be reassigned."
                                    tempChunk = popChunkFromStackOfChunksThatNeedToBeReassigned(self)
                                    sendNextCommandToClientByLength(self, clientSocket, tempChunk)
                                    try:
                                        tempChunk = getChunkFromDictionaryOfCurrentClientTasks(self,clientAddr)
                                        #if suceed, set value
                                        setChunkToDictionaryOfCurrentClientTasks(self,clientAddr,tempChunk)
                                    except Exception as inst:
                                        #add client to the dictionary
                                        addClientToDictionaryOfCurrentClientTasks(self,clientAddr,tempChunk)
                                else:
                                    #print "There is no chunk that needs to be reassigned. Requesting nextChunk from the Controller"
                                    sendNextChunkCommandToController(self)
                                    #print "Adding the client to the stackOfClientsWaitingForNextChunk"
                                    pushClientOnToStackOfClientsWaitingForNextChunk(self,clientSocket, clientAddr)
                        except Exception as inst:
                            print "===================================================================\n"
                            print "Error in checking to see if the next Command was received from the client in client thread handler: "+str(inst)+"\n"
                            print "===================================================================\n"
                            pushCommandOntoTheStackOfIOCommands(self, "ERROR in checkingForNextCommandFromClient", "Self", "Self")

                        try: #check to see if the found solution command was received from the client
                            if(identifiedCommand == False):
                                if(checkForFoundSolutionCommandFromClient(self,inboundCommandFromClient)==True):
                                    identifiedCommand= True
                                   # print "Identified inboundCommandFromClient as the found solution command\n"
                                    for key in self.dictionaryOfCurrentClientTasks.keys():
                                        sendDoneCommandToClient(self,clientSocket, key) #extracts the key from the dictionary and sends the done command to them
                                   # print "Setting the thread termination value to true, stopping all threads\n"
                                   # print "Acquiring stopAllThreads Lock\n"
                                    self.stopAllThreadsLock.acquire()
                                   # print "Acquired stopAllThreads Lock\n"
                                    self.stopAllThreads = True
                                    #print "Releasing stopAllThreads Lock\n"
                                    self.stopAllThreadsLock.release()
                                   # print "Released stopAllThreads Lock\n"
                                   # print "A client has found the solution!!!!!\n"
                                    break
                        except Exception as inst:
                            print "===================================================================\n"
                            print "Error in check to see if found solution command was received from the client in client thread handler: "+str(inst)+"\n"
                            print "===================================================================\n"
                            pushCommandOntoTheStackOfIOCommands(self, "ERROR in checkForFoundSOlutionCommandFromClient", "Self", "Self")

                        try: #check to see if the crashed command was received
                            if(identifiedCommand == False):
                                if(checkForCrashedCommandFromClient(self,inboundCommandFromClient)==True):
                                    identifiedCommand= True
                                   # print "Identified inboundCommandFromClient as the Crashed Command\n"
                                    tempChunk = getChunkFromDictionaryOfCurrentClientTasks(self,clientAddr)
                                    pushChunkOnToStackOfChunksThatNeedToBeReassigned(self,tempChunk)
                                    addClientToListOfCrashedClients(self, clientAddr)
                                    delClientFromDictionaryOfCurrentClientTasks(self,clientAddr)
                        except Exception as inst:
                            print "===================================================================\n"
                            print "Error in check to see if crashed command was received from client in client thread handler: "+ str(inst)+"\n"
                            print "===================================================================\n"
                            pushCommandOntoTheStackOfIOCommands(self, "ERROR in checkForCrashedCommandFromClient", "Self", "Self")

                        if(identifiedCommand == False):
                            #print "Warning: Unknown Command Received from the client: "+str(inboundCommandFromClient)+"\n"
                            pushCommandOntoTheStackOfIOCommands(self, "UNKNOWN: "+str(inboundCommandFromClient), "Client", "Inbound")
                except Exception as inst:
                    print "===================================================================\n"
                    print "Error in Analyzing received command from the client try block in the client thread handler: " +str(inst)+"\n"
                    print "===================================================================\n"
                    pushCommandOntoTheStackOfIOCommands(self, "ERROR in Analyzing received command from the Client", "Self", "Self")

        except Exception as inst:
            print "===================================================================\n"
            print "Error in Client Thread Handler: " + str(inst) +"\n"
            print "===================================================================\n"
            pushCommandOntoTheStackOfIOCommands(self, "ERROR in client Thread Handler", "Self", "Self")

        finally:
            clientSocket.close()
            #print "clientSocket has been closed\n"
            #print "this thread has closed.\n"
    #end of clientthreadhandler

    #START OF INITIAL SERVER SETUP
    def __init__(self, inboundpipeconnection):
        #CLASS VARS
        self.pipe = inboundpipeconnection #pipe that connects to the controller
        self.stopAllThreadsLock = thread.allocate_lock()
        self.stackOfIOCommandsLock = thread.allocate_lock()

        #CREATE THE SOCKET
        import socket
        serverSocket = socket.socket(AF_INET, SOCK_STREAM)

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
            pushCommandOntoTheStackOfIOCommands(self, "ERROR in getOS try block", "Self", "Self")

        #get the IP address
        try: #getIP tryblock
           # print "STATUS: Getting your network IP adddress"
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
               # print "INFO: The system has detected that you are not running Windows, OS X, or Linux."
               # print "INFO: System is using a generic IP detection method"
                print socket.gethostbyname(socket.gethostname())
        except Exception as inst:
            print "========================================================================================"
            print "ERROR: An exception was thrown in getIP try block"
            print type(inst) #the exception instance
            print inst.args #srguments stored in .args
            print inst #_str_ allows args tto be printed directly
            print "========================================================================================"
            pushCommandOntoTheStackOfIOCommands(self, "ERROR in getIP try block", "Self", "Self")

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
            #serverSocket.settimeout(0.25)
            serverSocket.settimeout(0.1)
            #serverSocket.settimeout(0.05)
            #serverSocket.settimeout(0.01)
            #serverSocket.settimeout(0.001)
            #serverSocket.settimeout(0.0001)
            #serverSocket.settimeout(0.00001)
            #serverSocket.settimeout(0.000001)
            #serverSocket.settimeout(0.0000001)
           # print "MAIN THREAD: Waiting for client(s) to connect\n"
            while True: #Primary main thread server while loop
                if(self.stopAllThreads == True):
                    #print "MAIN THREAD: Stopping Main Thread\n"
                    break
                #CHECK TO SEE IF A CLIENT IS TRYING TO CONNECT
                try:
                    #print "MAIN THREAD: Checking to see if client is trying to connect\n"
                    inboundClientSocket, inboundClientAddr = serverSocket.accept()
                    #print "MAIN THREAD: A client has connected!!\n"
                    thread.start_new_thread(self.ClientThreadHandler, (inboundClientSocket,inboundClientAddr,self.socketLock))
                except Exception as inst:
                    if(compareString(str(inst),"timed out",0,0,len("timed out"),len("timed out"))==True):
                        #do not display an error message
                        fakeVar= True
                    else:
                        print "===================================================================\n"
                        print "MAIN THREAD: Error in check for client trying to connect try block: " +str(inst)+"\n"
                        print "===================================================================\n"
                        pushCommandOntoTheStackOfIOCommands(self, "Main Thread ERROR in checkForClientTryingToConnect" , "Self", "Self")

                #CHECK TO SEE IF CONTROLLER HAS SENT A MESSAGE TO SERVER
                try:
                   # print "MAIN THREAD: Checking for Commands from the controller\n"
                    if(self.pipe.poll()):
                        receivedControllerCommand= self.pipe.recv()
                        if(receivedControllerCommand is not None): #ignore the empty string
                            #print "MAIN THREAD: Received command from the controller\n"
                            identifiedCommand = False
                            try: #checking for nextChunk Command from Controller
                                if(checkForNextChunkCommandFromController(self,receivedControllerCommand)==True):
                                    identifiedCommand= True
                                   # print "MAIN THREAD: Identified receivedControllerCommand as the nextChunk Command\n"
                                    #check to see if a client is waiting for the nextChunk
                                    if(len(self.stackOfClientsWaitingForNextChunk) > 0):
                                       # print "MAIN THREAD: A client is waiting for the nextChunk\n"
                                        tempClientSocket, tempClientAddress= popClientFromStackOfClientsWaitingForNextChunk(self)
                                        outboundChunk = receiveNextChunkFromController(self)
                                        sendNextCommandToClientByLength(self, tempClientSocket, outboundChunk)
                                        try:
                                            tempChunk = getChunkFromDictionaryOfCurrentClientTasks(self,tempClientAddress)
                                            #if, suceeds, override the old chunk
                                            setChunkToDictionaryOfCurrentClientTasks(self,tempClientAddress,outboundChunk)
                                        except Exception as inst:
                                            #add it if there is not key for that client yet
                                            addClientToDictionaryOfCurrentClientTasks(self,tempClientAddress, outboundChunk)
                                    else: #if there is no client waiting for the  next chunk
                                        #print "MAIN THREAD: No clients are waiting for the nextChunk. Adding chunk to the stackOfChunksThatNeedToBeReassigned"
                                        pushChunkOnToStackOfChunksThatNeedToBeReassigned(self,receivedControllerCommand)
                            except Exception as inst:
                                print "===================================================================\n"
                                print "MAIN THREAD: Error in checking for nextChunk Command from Controller Try Block: " +str(inst)+"\n"
                                print "===================================================================\n"
                                pushCommandOntoTheStackOfIOCommands(self, "Main Thread ERROR in checkingForNextChunkCommand from Controller", "Self", "Self")

                            try: #checking for done command form controller
                                if(identifiedCommand == False):
                                    if(checkForDoneCommandFromController(self,receivedControllerCommand)==True):
                                        identifiedCommand= True
                                       # print "MAIN THREAD: Identified receivedControllerCommand as the Done Command\n"
                                        #No further actions are needed for this command
                            except Exception as inst:
                                print "===================================================================\n"
                                print "MAIN THREAD: Error in checking for done command from Controller Try Block: "+str(inst)+"\n"
                                print "===================================================================\n"
                                pushCommandOntoTheStackOfIOCommands(self, "Main Thread ERROR in checkingForDoneCommand from COntroller", "Self", "Self")

                            if(identifiedCommand == False):
                               # print "MAIN THREAD: Warning: Unknown Command Received from the Controller: "+str(receivedControllerCommand)+"\n"
                                pushCommandOntoTheStackOfIOCommands(self, "UNKNOWN: "+str(receivedControllerCommand), "Controller", "Inbound")
                    else: #if there is nothing on the pipe
                        #Do not display the message
                        fakeVar=True
                       # print "MAIN THREAD: There is no command received from the controller\n"
                except Exception as inst:
                    if(compareString(str(inst),"timed out",0,0,len("timed out"),len("timed out"))==True):
                        #Do not print out an error message
                        fakeVar= True
                    else:
                        print "===================================================================\n"
                        print "MAIN THREAD: Error in check to see if controller has sent a message to server try block: " + str(inst) +"\n"
                        print "===================================================================\n"
                        pushCommandOntoTheStackOfIOCommands(self, "Main Thread ERROR in checkToSeeIfControllerHasSentAMessage", "Self", "Self")

        except Exception as inst:
            print "===================================================================\n"
            print "MAIN THREAD: Error in Main Thread Server Loop: " +str(inst)+"\n"
            print "===================================================================\n"
            pushCommandOntoTheStackOfIOCommands(self, "Main Thread ERROR in Main Thread Server Loop", "Self", "Self")
        finally:
            #print "Setting stop variable to stop all threads"
            #print "Acquiring stopAllThreads Lock\n"
            self.stopAllThreadsLock.acquire()
            #print "Acquired stopAllThreads Lock\n"
            self.stopAllThreads = True
            #print "Releasing stopAllThreads Lock\n"
            self.stopAllThreadsLock.release()
            #print "Released stopAllThreads Lock\n"
            #print "Sending done command to all clients, server is finished\n"
            #serverSocket.settimeout(0.25)
            serverSocket.settimeout(0.1)
            #serverSocket.settimeout(0.05)
            #serverSocket.settimeout(0.01)
            #serverSocket.settimeout(0.001)
            #serverSocket.settimeout(0.0001)
            #serverSocket.settimeout(0.00001)
            #serverSocket.settimeout(0.000001)
            #serverSocket.settimeout(0.0000001)
            for key in self.dictionaryOfCurrentClientTasks.keys(): #This is potentially replaced by the sendDoneCommand in thread
                try:
                    self.socketLock.acquire()
                    serverSocket.sendall("done")
                    self.socketLock.release()
                   # print "Sent done command to: " + str(key)+"\n"
                except Exception as inst:
                    if(compareString(str(inst),"timed out",0,0,len("timed out"),len("timed out"))==True):
                        #print "Timed out while sending 'done' command to "+ str(key)+"\n"
                        fakeVar=True
                    else:
                        print "===========================================================\n"
                        print "MAIN THREAD ERROR in finally block send done command to clients: " +str(inst)+"\n"
                        print "============================================================\n"
                        pushCommandOntoTheStackOfIOCommands(self, "Main Thread ERROR in finally block sendDoneCommand", "Self", "Self")
            #print "MAIN THREAD: Preparing to close the socket\n"
            serverSocket.close()
           # print "MAIN THREAD: The serverSocket has been closed\n"
            sendDoneCommandToController(self)
           # print "MAIN THREAD: Informed the Controller that Server has finished\n"
            sendSolutionToController(self) #solution is saved in the class variable
            print "-----------------------Stack of IO Commands---------------------------------\n"
            for index in range(0,len(self.stackOfIOCommands)):
                tempCommandName, tempOrigin_Destination, tempCommandDirection, tempTime = self.stackOfIOCommands.pop(0)
                if(compareString(tempCommandDirection, "Inbound",0,0,len("Inbound"),len("Inbound"))==True):
                    print str(tempCommandDirection)+" command: "+str(tempCommandName)+" was received from: "+str(tempOrigin_Destination)+" at: "+str(tempTime)
                else: #if outbound
                    print str(tempCommandDirection)+" command: "+str(tempCommandName)+" was sent to: "+str(tempOrigin_Destination)+" at: "+str(tempTime)
            print "-----------------------End of Stack of IO Commands------------------------\n"

            print "The Solution is: '"+str(self.theSolution)+"'\n"






