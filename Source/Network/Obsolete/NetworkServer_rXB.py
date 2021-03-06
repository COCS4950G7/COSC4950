__author__ = 'chris hamm'
#NetworkServer_rXB (revision 10)
#Created: 2/1/2015
#Designed to work with NetworkClient_rXB

#IMPORTANT!!!
    #A glitch has been detected in the server. The server will only communication with the last client it talked too. (THIS INCLUDES THE DONE COMMAND!)

#CHANGES MADE IN THIS REVISION
    #(In progress) Integrate multithreading
#CHANGES FROM LAST REVISION
    #(Not implemented yet)Tell controller when the server is done
    #TEMPORARY commented out many print statements to try to improve speed

#====================================
#Imports
#====================================
import socket
from socket import *
import platform
import Chunk
from thread import *
#====================================
#End of Imports
#====================================

#==============================================================
#NetworkServer Class Definition
#==============================================================
class NetworkServer(): #CLASS NAME WILL NOT CHANGE BETWEEN VERSIONS
    #-------------------------------------------------------------------
    #NetworkServer Class Variables
    #-------------------------------------------------------------------
    host= '' #Symbolic name, meaning all available interfaces
    port= 49200
    numOfClients= 0
    serverSocket = 0
    serverIsRunning = True
    #list to store the socket and address of every client
    listOfClients = [] #This list is a list of tuples (socket, address)
    listOfCrashedClients= [] #records the ip address of any client that has crashed during the last server run
    #Changed from list of clients waiting for a reply
    stackOfClientsWaitingForNextChunk = [] #the stack
    #NOTES ABOUT THE STACK:
        #stackOfClientsWaitingForNextChunk.append(Object) #Is how to push onto the stack
        #object = stack.pop() #Is how you pop the stack
    stackOfChunksThatNeedToBeReassigned = [] #a stack
    numOfThreads = 0
    dictionaryOfCurrentClientTasks = {} #dictionary that holds the ip of each client as the key and the chunk it is working on as the value
    recordOfNumberOfIPAddressesThatHaventBeenFound = 0 #if an ip address cannot be found when server is looking for a match, this counter gets incremented
    recordOfOutboundCommandsFromServerToController = {} #dictionary that records how many times the server has issued a command to the controller
    recordOfInboundCommandsFromControllerToServer = {} #dictionary that records how many times the server received a command from the controller
    recordOfOutboundCommandsFromServerToClient = {} #dictionary that records how many times the server has issued a command to the client
    recordOfInboundCommandsFromClientToServer = {} #dictionary that records how many times the server received a command from from the client(s)
    #-------------------------------------------------------------------
    #End of NetworkServer Class Variables
    #-------------------------------------------------------------------

    #-------------------------------------------------------------------
    #NetworkServer Class Constructor
    #-------------------------------------------------------------------
    def __init__(self, pipeendconnectedtocontroller):
        self.pipe= pipeendconnectedtocontroller

        #socket.AF_INET is a socket address family represented as a pair. (hostname, port). This is the default parameter
        #socket.SOCK_STREAM is the default parameter. This defines the socket type
        import socket
        self.serverSocket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print "STATUS: Server socket created successfully"

        #.........................................................................
        #Bind the Socket to local host and port
        #.........................................................................
        try: #Bind socket try block
            self.serverSocket.bind((self.host,self.port))
            print "STATUS: Socket bind complete."
        except socket.error as inst:
            print "========================================================================================"
            print "ERROR: failed to bind (host, port) to serverSocket"
            print type(inst) #the exception instance
            print inst.args #srguments stored in .args
            print inst #_str_ allows args tto be printed directly
            print "========================================================================================"
            raise Exception("Could not bind to socket! Server Must Shut Down.")
        #.........................................................................
        #End of Bind the Socket to local host and port
        #.........................................................................

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

        #.........................................................................
        #Initialize the Record Counters
        #.........................................................................
        print "STATUS: Initializing the Record Counters..."
        self.recordOfOutboundCommandsFromServerToController['nextChunk'] = 0
        self.recordOfOutboundCommandsFromServerToController['chunkAgain'] = 0
        self.recordOfOutboundCommandsFromServerToController['waiting'] = 0
        self.recordOfOutboundCommandsFromServerToController['done'] = 0
        self.recordOfOutboundCommandsFromServerToClient['DONE'] = 0
        self.recordOfOutboundCommandsFromServerToClient['nextChunk'] = 0
        self.recordOfOutboundCommandsFromServerToClient['nextChunkData'] = 0
        self.recordOfInboundCommandsFromControllerToServer['REPLY_TO_NEXT_CHUNK'] = 0
        self.recordOfInboundCommandsFromControllerToServer['REPLY_TO_CHUNK_AGAIN'] = 0
        self.recordOfInboundCommandsFromControllerToServer['REPLY_TO_DONE'] = 0
        self.recordOfInboundCommandsFromControllerToServer['Chunk_Objects'] = 0
        self.recordOfInboundCommandsFromControllerToServer['Unknown'] = 0
        self.recordOfInboundCommandsFromClientToServer['NEXT'] = 0
        self.recordOfInboundCommandsFromClientToServer['FOUNDSOLUTION'] = 0
        self.recordOfInboundCommandsFromClientToServer['CRASHED'] = 0
        self.recordOfInboundCommandsFromClientToServer['Unknown'] = 0
        #print "INFO: Successfully initialized the Record Counters"

        #.........................................................................
        #End of Initialize the Record Counters
        #.........................................................................

        #.........................................................................
        #Start Listening to the Socket
        #.........................................................................
        self.serverSocket.listen(5)
        print "STATUS: Waiting for initial client to connect..."
        #.........................................................................
        #End of Start Listening to the Socket
        #.........................................................................

        #.........................................................................
        #Wait for initial client to connect
        #.........................................................................
        '''
        sock, addr= self.serverSocket.accept()
        #print "INFO: First client has connected"
        print "INFO: Connected with " + addr[0] + ":" + str(addr[1])
        try:
            #creating a new thread. calling clientthread function
            start_new_thread((clientthread(sock), (sock,)))
        except Exception as inst:
            print "============================================================================================="
            print "ERROR: An exception was thrown in the wait for initial client to connect multithread Try Block"
            #the exception instance
            print type(inst)
            #srguments stored in .args
            print inst.args
            #_str_ allows args tto be printed directly
            print inst
            print "============================================================================================="
        self.listOfClients.append((sock, addr)) #add the tuple to the list of clients
        #print "STATUS: Client successfully added to the list of clients"
        #When a client is added, they are also added to the dictionaryOfCurrentClientTasks
        self.dictionaryOfCurrentClientTasks[addr] = "" #Not working on anything, so value is the empty string
        #print "STATUS: Client successfully added to the Dictionary of Current Client Tasks"
        #.........................................................................
        #End of Wait for initial client to connect
        #.........................................................................
        '''
        #.........................................................................
        #Start of Primary Server While Loop
        #.........................................................................
        try: #server primary while loop try block
            while(self.serverIsRunning==True): #server primary while loop
            #/////////////////////////////////////////////////////////////////////////////
            #Check to see if another client is trying to connect
            #/////////////////////////////////////////////////////////////////////////////
                try: #check to see if another client is trying to connect try block
                    print "STATUS: Checking to see if another client is trying to connect..."
                    self.serverSocket.settimeout(0.25)
                    sock, addr =self.serverSocket.accept()
                    print "INFO: Connected with " + addr[0] + ":" + str(addr[1])
                    self.listOfClients.append((sock, addr))
                    try:
                        start_new_thread(self.clientthread, (sock,))
                    except Exception as inst:
                        print "========================================================================================"
                        print "ERROR: An exception has been thrown in the Check to see if another client is trying to connect Try Block"
                        print type(inst) #the exception instance
                        print inst.args #srguments stored in .args
                        print inst #_str_ allows args tto be printed directly
                        print "========================================================================================"

                    #print "INFO: Client successfully added to the list of clients"
                    print str(len(self.listOfClients)) + " Client(s) are currently Connected."
                    self.dictionaryOfCurrentClientTasks[addr] = "" #Client has no task currently, so value is the empty string
                    #print "STATUS: Client was successfully added to the Dictionary of Current Client Tasks"
                except socket.timeout as inst:
                    print "STATUS: Socket timed out. No client is trying to connect."
                except Exception as inst:
                    print "========================================================================================"
                    print "ERROR: An exception has been thrown in the Check to see if another client is trying to connect Try Block"
                    print type(inst) #the exception instance
                    print inst.args #srguments stored in .args
                    print inst #_str_ allows args tto be printed directly
                    print "========================================================================================"
                finally:
                    print "INFO: Currently, there are " + str(len(self.listOfClients)) + " clients currently connected"
            #/////////////////////////////////////////////////////////////////////////////
            #End of Check to see if another client is trying to connect
            #/////////////////////////////////////////////////////////////////////////////
            #/////////////////////////////////////////////////////////////////////////////
            #Check for input from clients
            #/////////////////////////////////////////////////////////////////////////////
            #'''GOAL: Want server to respond immeadiately when it receives a command from a client'''
                print "STATUS: Checking for input from client(s)..."
                try: #check for client input try block
                    #sock.settimeout(0.25)
                    self.serverSocket.settimeout(0.25)
                    #theInput = sock.recv(2048) #listening for input
                    theInput =""
                    checkingForClientInput= True
                    while checkingForClientInput==True:
                        try:
                            theInput = self.serverSocket.recv(2048)
                            if not theInput:
                                checkingForClientInput= False
                                break
                        except socket.timeout as inst:
                            checkingForClientInput= False
                            break
                        except Exception as inst:
                            checkingForClientInput= True

                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                #If Command is the Empty String (do not expect a chunk object)
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                    if(len(theInput) >= 1):
                        print "INFO: Received a message from a client."
                    else: #theInput has a length of 0
                        print "WARNING: The Empty String has been received."
                        raise Exception("Empty String is not a Command, ignoring input. This is Just a Warning.")
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                #End of If Command is the Empty String
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                #Check for NEXT Command
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                    if(self.checkForNextCommand(theInput)==True):
                    #************************************************************************************
                    #If it is the NEXT Command
                    #************************************************************************************
                        print "INFO: NEXT command was received"

                        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                        #Check to see if stack of chunks that need to be reassigned is empty
                        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                            #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                            #If stack is not empty, then send the top chunk on the stack to the client that is requesting the nextChunk
                            #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                        tempIP= ""
                        #print "STATUS: Extracting The Clients IP"
                        for i in range(5, len(theInput)):
                            tempIP+= theInput
                        #print "INFO: Successfully Extracted the Clients IP"
                        if(len(self.stackOfChunksThatNeedToBeReassigned) > 0):
                            print "STATUS: Preparing to send chunk (from stack of chunks that need to be reassigned) to client..."
                                #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
                                #Save a copy of the chunk being sent to the client in the dictionary of clientsCurrentTask
                                #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
                            #position 4 is a space
                            #Extracting the clients IP
                            #print "STATUS: Extracting The Clients IP"
                            #for i in range(5, len(theInput)):
                            #    tempIP+= theInput
                            #print "INFO: Successfully Extracted the Clients IP"
                            self.dictionaryOfCurrentClientTasks[tempIP] = self.stackOfChunksThatNeedToBeReassigned.pop() #pop the stack
                            #print "INFO: Successfully added the chunk from stack of chunks that need to be reassigned to the dictionary of current clients tasks"
                            #retreive socket information
                            print "STATUS: Looking for matching IP Address in list of Clients..."
                            foundMatch= False
                            tempAddr2= ""
                            for index in range(0, len(self.listOfClients)):
                                tempSock, tempAddr= self.listOfClients[index] #get socket and ip address of client
                                #print "STATUS: Copying list of clients' IP Address to a new string"
                                tempAddr2= str(tempAddr[0])
                                #print "STATUS: Comparing IP Addresses..."
                                if(tempIP == tempAddr2):
                                    print "INFO: Matching IP address was found in the list of clients"
                                    foundMatch= True
                                    break
                                else:
                                    print "INFO: No Match found yet. " + str(tempIP) + " != " + str(tempAddr2)

                            if(foundMatch == False):
                                print "WARNING: No Matching IP address was found in the list of clients"
                                print "INFO: Unable to Find the Client's IP: " +str(tempIP) + " "
                                self.recordOfNumberOfIPAddressesThatHaventBeenFound+= 1
                            else:
                                #send chunk to client
                                print "STATUS: Sending Chunk to the Client..."
                                try:
                                    self.sendNextToClient(tempSock,tempIP, self.dictionaryOfCurrentClientTasks[tempIP].params)
                                except socket.error as inst:
                                    i#f(str(inst) == "[Errno 35] Resource temporarily unavailable"):
                                    import time
                                    time.sleep(0)
                                    print "WARNING: 2nd attempt to sendNextToClient"
                                    self.serverSocket.settimeout(0.25) #reset timeout
                                    self.sendNextToClient(tempSock, tempIP, self.dictionaryOfCurrentClientTasks[tempIP].params)
                                    continue
                            #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                            #Else If stack empty, then send a nextChunk message to the controller and add the client to the stack of clients waiting for nextChunk
                            #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                        else:
                            print "I/O: Sending a nextChunk request to the Controller..."
                            try:
                                self.sendNextChunkCommandToController() #request the next chunk
                            except socket.error as inst:
                                #if(str(inst) == "[Errno 35] Resource temporarily unavailable"):
                                import time
                                time.sleep(0)
                                print "WARNING: 2nd attempt to sendNextChunkToController"
                                self.serverSocket.settimeout(0.25) #reset the timeout
                                self.sendNextChunkCommandToController()
                                continue
                            self.stackOfClientsWaitingForNextChunk.append(tempIP) #push client onto the stack
                            #print "INFO: Client successfully added to the stack of clients waiting for nextChunk"
                        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                        #End of Check to see if stack of chunks that need to be reassigned is empty
                        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                    #************************************************************************************
                    #End of If it is the Next Command
                    #************************************************************************************
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                #End of Check for NEXT Command
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                #Check for FOUNDSOLUTION Command
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                    elif(self.checkForFoundSolutionCommand(theInput)==True):
                        print "INFO: FOUNDSOLUTION Command was received from the Client"
                        print "STATUS: Issuing the DONE Command to all clients..."
                        for x in range(0, len(self.listOfClients)):
                            (sock, addr) = self.listOfClients[x]
                            sock.sendall("DONE")
                            print "INFO: Issued the DONE command to client: " + str(addr)
                        print "INFO: Finished Issuing the DONE Commands"
                        print "STATUS: Shutting down the Server Looping Variables..."
                        self.serverIsRunning= False
                        print "INFO: Server Looping Variables have been shut down"
                    #************************************************************************************
                    #(MAY be obsolete) I think this should only used in the client
                    #************************************************************************************
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                #End of Check for FOUNDSOLUTION Command
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                #Check for CRASHED Command
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                    elif(self.checkForCrashedCommand(theInput)==True):
                        print "INFO: CRASHED command was received"
                    #************************************************************************************
                    #THIS IS NOW DONE IN THE CHECK FOR CRASHED COMMAND FUNCTION
                    #If it is the CRASHED Command, add the chunk that client was working on to the stack of chunks that need to be reassigned
                    #************************************************************************************
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                #End of Check for CRASHED Command
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                #If Command is Unknown, print Error
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                    else:
                        print "ERROR: unknown command received"
                        print "The unknown command: '" + theInput + "'"
                        self.recordOfInboundCommandsFromClientToServer['Unknown'] = (self.recordOfInboundCommandsFromClientToServer['Unknown'] + 1)
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                #End of If Command is Unknown, print Error
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                except socket.timeout as inst:
                    print "STATUS: Socket has timed out. No input from client detected."
                except Exception as inst:
                    print "========================================================================================"
                    print "ERROR: An exception has been thrown in the Check for client input Try Block"
                    print type(inst) #the exception instance
                    print inst.args #srguments stored in .args
                    print inst #_str_ allows args tto be printed directly
                    print "========================================================================================"
            #/////////////////////////////////////////////////////////////////////////////
            #End of Check for input from Clients
            #/////////////////////////////////////////////////////////////////////////////
                finally:
                    print "INFO: There are currently " + str(len(self.stackOfClientsWaitingForNextChunk)) + " clients waiting for nextChunk"
                    print "INFO: There are currently " + str(len(self.stackOfChunksThatNeedToBeReassigned)) + " chunks waiting to be reassigned"

            #/////////////////////////////////////////////////////////////////////////////
            #Check for input from controller class
            #/////////////////////////////////////////////////////////////////////////////
            #'''GOAL: Want server to respond immeadiately when it receives a command from the controller class'''
            #'''GOAL: Change the recv function so that server expects two messages from controller, a string, then a chunk object'''
                print "STATUS: Checking for input from the Controller class..."
                try: #check for input from controller try block
                    if(self.pipe.poll()):
                        recv = self.pipe.recv()
                        print "INFO: Received a message from the controller"
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                #Check for reply to next chunk command
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                        if(self.checkForNextChunk(recv)==True):
                            print "STATUS: Waiting for corresponding chunk object..."
                    #************************************************************************************
                    #If it is the reply to next chunk command, receive the chunk object
                    #************************************************************************************
                            chunkrecv = self.pipe.recv()
                            print "INFO: Received the chunk object"
                            self.recordOfInboundCommandsFromControllerToServer['Chunk_Objects'] = (self.recordOfInboundCommandsFromControllerToServer['Chunk_Objects'] + 1)
                        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                        #If stack of client waiting for nextChunk is not empty, then send chunk info to that client on top of the stack, remove client from stack
                        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                            if(len(self.stackOfClientsWaitingForNextChunk) > 0):
                                print "STATUS: Preparing to send nextChunk object to Client Waiting for nextChunk..."
                                #chunkParams= chunkrecv.params #NO LONGER NEEDED
                                #print "INFO: Copied parameters from chunk object"
                                #print "DEBUG: Size of stack of clientsWaitingForNextChunk: " + str(len(self.stackOfClientsWaitingForNextChunk))
                                tempIP = str(self.stackOfClientsWaitingForNextChunk.pop()) #pop the stack
                                #print "DEBUG: Removing NEXT and a space from tempIP"
                                #tempIP= tempIP[5:len(tempIP)] #NEEDED ON THE CLIENTSIDE
                                #print "DEBUG: find first invalid char and marking it"
                                firstInvalidCharIndex = 5
                                for x in range(5,len(tempIP)):
                                    if(tempIP[x].isalpha()==True):
                                        firstInvalidCharIndex= x
                                        #print "DEBUG: firstInvalidChar=" + str(firstInvalidCharIndex)
                                        break
                                    elif(tempIP[x].isspace()==True):
                                        firstInvalidCharIndex= x
                                        #print "DEBUG: firstInvalidChar=" + str(firstInvalidCharIndex)
                                        break
                                #if still zero, keep entire string
                                if(firstInvalidCharIndex == 5):
                                    #keep tempIP at the same value
                                    print "INFO: tempIP does not need to be cropped"
                                else:
                                    tempIP= tempIP[5:firstInvalidCharIndex]
                                #print "DEBUG: tempIP after popping and cropping:" + str(tempIP)
                                #retreive socket information
                                print "STATUS: Looking for matching IP Address in list of Clients..."
                                foundMatch= False
                                tempAddr2= ""
                                tempSock= ""
                                for index in range(0, len(self.listOfClients)):
                                    tempSock, tempAddr= self.listOfClients[index] #get socket and ip address of client
                                    tempPort= tempAddr[1] #copy the port information
                                    #print "DEBUG: tempPort=" + str(tempPort)
                                    #print "STATUS: Copying list of clients' IP Address to a new string"
                                    tempAddr2= str(tempAddr[0])
                                    #print "STATUS: Comparing IP Addresses..."
                                    #print "DEBUG: tempAddr2=" + str(tempAddr2)
                                    #print "DEBUG: tempIP=" + str(tempIP)
                                    if(tempIP == tempAddr2):
                                        print "INFO: Matching IP address was found in the list of clients"
                                        foundMatch= True
                                        break
                                    else:
                                        print "INFO: No Match found yet. " + str(tempIP) + " != " + str(tempAddr2)

                                if(foundMatch == False):
                                    print "WARNING: No Matching IP address was found in the list of clients"
                                    print "INFO: Unable to Find the Client's IP: " +str(tempIP) + " "
                                    self.recordOfNumberOfIPAddressesThatHaventBeenFound+= 1
                                else:
                                    #print "STATUS: Copying chunk object to dictionaryOfCurrentClientTasks..."
                                    self.dictionaryOfCurrentClientTasks[tempIP] = chunkrecv
                                    #print "INFO: Successfully saved chunk object to dictionaryOfCurrentClientTasks"
                                    print "STATUS: Measuring the file size of the params..."
                                    import sys
                                    paramsDataSize= sys.getsizeof(self.dictionaryOfCurrentClientTasks[tempIP])
                                    #print "INFO: The file size of the params is: " + str(paramsDataSize) + " bytes"
                                    print "STATUS: Measuring the file size of the corresponding data of the chunk..."
                                    import sys
                                    dataFileSize = sys.getsizeof(chunkrecv.data)# THIS METHOD SEEMS TO WORK
                                    #print "INFO: The file size of the corresponding data is: " + str(dataFileSize) + " bytes"
                                    print "STATUS: Sending nextChunk to client"
                                    #add the NEXT key word into the string so client will recognize it
                                    #add in the SIZE keyword, where the size is inside the parenthesis
                                    tempMessage= "NEXT " + "SIZE(" + str((dataFileSize)) + ") " +str(self.dictionaryOfCurrentClientTasks[tempIP].params)
                                    self.sendNextToClient(tempSock, tempIP, tempPort, tempMessage)
                                    #print "DEBUG: chunk params being sent to client=" + str(tempMessage)
                                    print "INFO: Successfully sent the nextChunk to the client"
                                    print "STATUS: Sending the corresponding data for that chunk to client..."
                                    self.sendNextDataToClient(tempSock, tempIP, tempPort, chunkrecv.data)
                                    #print "DEBUG: chunk data being sent to the client=" + str(chunkrecv.data)
                                    print "INFO: Successfully sent the corresponding chunk data to the client"
                            #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                            #Save a copy the chunk being sent to the client to the dictionary of clientCurrentTasks
                            #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                        #Else if stack of clients waiting for nextChunk is empty, then store the chunk in stack of chunks that need to be reassigned
                        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                            else:
                                print "STATUS: No Clients are waiting for nextChunk. Chunk is being added to stack of chunks that need to be reassigned."
                                self.stackOfChunksThatNeedToBeReassigned.append(chunkrecv) #push chunk on to the stack
                                #print "INFO: Successfully pushed chunk on to the stack."
                    #************************************************************************************
                    #Once received chunk object, send info to the client in the waiting for nextChunk stack (DONE ABOVE)
                    #************************************************************************************
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                #End of Check for reply to next chunk command
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                #Check for reply to chunkAgain Command
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                        elif(self.checkForChunkAgain(recv)==True):
                            print "INFO: Waiting for corresponding chunk object..."
                    #************************************************************************************
                    #If it is the reply to chunkAgain command, receive the chunk object (May be obsolete if server holds the chunks)
                    #************************************************************************************
                            chunkrecv = self.pipe.recv()
                            print "INFO: Received the chunk object"
                            print "WARNING: THIS FUNCTION IS NOT FINISHED"
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                #End of Check for reply to chunkAgain Command
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                #Check for reply to done command
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                        elif(self.checkForDone(recv)==True):
                            print "INFO: Received DONE Command from the controller"
                            print "WARNING: THIS FUNCTION IS NOT FINISHED"
                    #************************************************************************************
                    #(NOT SURE ABOUT THIS) Receive chunk object????
                    #************************************************************************************
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                #End of Check for reply to done command
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                #If Command is unknown, print out Error
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                        else:
                            print "ERROR: unknown command received"
                            print "The unknown command: '" + recv + "'"
                            self.recordOfInboundCommandsFromControllerToServer['Unknown'] = (self.recordOfInboundCommandsFromControllerToServer['Unknown'] + 1)
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                #End of If Command is Unknown, print Error
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                    else:
                        print "INFO: No command was received from the controller"
                except Exception as inst:
                    print "========================================================================================"
                    print "ERROR: An exception has been thrown in the Check for input from Controller class Try Block"
                    print type(inst) #the exception instance
                    print inst.args #srguments stored in .args
                    print inst #_str_ allows args tto be printed directly
                    print "========================================================================================"
            #/////////////////////////////////////////////////////////////////////////////
            #End of Check for input from controller class
            #/////////////////////////////////////////////////////////////////////////////

            #'''GOAL: To have this section (below) be removed, and have the above sections immeadiately respond to any received commands, instead of queuing the commands, then executing them'''
            #/////////////////////////////////////////////////////////////////////////////
            #Distribute Command(s) to Client(s) if needed (OBSOLETE)
            #/////////////////////////////////////////////////////////////////////////////
            #/////////////////////////////////////////////////////////////////////////////
            #End of Distribute Command(s) to Client(s) if needed
            #/////////////////////////////////////////////////////////////////////////////
            #'''GOAL: Remove the section above'''


        #.........................................................................
        #End of Primary Server While Loop
        #.........................................................................
        except Exception as inst: #Exception for Server Primary While Loop Try Block
            print "========================================================================================"
            print "ERROR: An exception has been thrown in the Server Primary While Loop Try Block"
            print type(inst) #the exception instance
            print inst.args #srguments stored in .args
            print inst #_str_ allows args tto be printed directly
            print "========================================================================================"
        #.........................................................................
        #Finally Block (where socket is closed)
        #.........................................................................
        finally:
            #/////////////////////////////////////////////////////////////////////////////
            #Close the Socket
            #/////////////////////////////////////////////////////////////////////////////
            print "Closing the socket..."
            self.serverSocket.close()
            print "Socket has been closed"
            #/////////////////////////////////////////////////////////////////////////////
            #End of Close the Socket
            #/////////////////////////////////////////////////////////////////////////////

            #/////////////////////////////////////////////////////////////////////////////
            #Issue DONE command to all clients
            #/////////////////////////////////////////////////////////////////////////////
            print "STATUS: Issuing the DONE command to clients..."
            for x in range(0, len(self.listOfClients)):
                (sock, addr) = self.listOfClients[x]
                sock.sendall("DONE")
                print "INFO: Issued the DONE command to client: " + str(addr)
            print "STATUS: Finished Issuing the DONE command to clients"
            #/////////////////////////////////////////////////////////////////////////////
            #End of Issue DONE command to all clients
            #/////////////////////////////////////////////////////////////////////////////

            #/////////////////////////////////////////////////////////////////////////////
            #Print List of Crashed Clients
            #/////////////////////////////////////////////////////////////////////////////
            try:
                print " "
                print "Printing List of Crashed Clients"
                print "---------------------------------"
                if(len(self.listOfCrashedClients) < 1):
                    print "No Clients Crashed During This Session"
                else:
                    for x in range(0, len(self.listOfCrashedClients)):
                        print str(x) + ") " + str(self.listOfCrashedClients[x]) + " reported a Crash"
                print "(END OF LIST OF CRASHED CLIENTS)"
                print "---------------------------------"
            except Exception as inst:
                print "========================================================================================"
                print "ERROR: An exception has been thrown in the Finally Block, in the print List of Crash Clients Section"
                print type(inst) #the exception instance
                print inst.args #srguments stored in .args
                print inst #_str_ allows args tto be printed directly
                print "========================================================================================"
            #/////////////////////////////////////////////////////////////////////////////
            #End of Print list of Crashed Clients
            #/////////////////////////////////////////////////////////////////////////////

            #/////////////////////////////////////////////////////////////////////////////
            #Print Stack of Clients Waiting for nextChunk
            #/////////////////////////////////////////////////////////////////////////////
            try:
                print " "
                print "Printing Stack Of Clients Waiting For nextChunk"
                print "--------------------------------------------------"
                if(len(self.stackOfClientsWaitingForNextChunk) < 1):
                    print "No Clients Are Waiting For NextChunk When The Session Ended"
                else:
                    print "The following clients where waiting for nextChunk:"
                    while(len(self.stackOfClientsWaitingForNextChunk) > 0):
                        tempIP = self.stackOfClientsWaitingForNextChunk.pop() #pop the stack
                        print "   " + str(tempIP)
                print "(END OF STACK OF CLIENTS WAITING FOR NEXTCHUNK)"
                print "--------------------------------"
            except Exception as inst:
                print "========================================================================================"
                print "ERROR: An exception has been thrown in the Finally Block, in the print Dictionary of Clients Waiting For A Reply Section"
                print type(inst) #the exception instance
                print inst.args #srguments stored in .args
                print inst #_str_ allows args tto be printed directly
                print "========================================================================================"
            #/////////////////////////////////////////////////////////////////////////////
            #End of Print Stack of clients waiting for nextChunk
            #/////////////////////////////////////////////////////////////////////////////

            #'''GOAL: Remove this data structure (below) and replace with new data structures (Listed right above this)'''
            #/////////////////////////////////////////////////////////////////////////////
            #Print list of clients waiting for a reply
            #/////////////////////////////////////////////////////////////////////////////
            #/////////////////////////////////////////////////////////////////////////////
            #End of Print list of Clients waiting for a reply
            #/////////////////////////////////////////////////////////////////////////////
            #'''GOAL: Remove the above data structure'''

            #'''GOAL: Remove this data structure (below) since no longer needed'''
            #/////////////////////////////////////////////////////////////////////////////
            #Print list of Controller Messages
            #/////////////////////////////////////////////////////////////////////////////
            #/////////////////////////////////////////////////////////////////////////////
            #End of print list of Controller Messages
            #/////////////////////////////////////////////////////////////////////////////
            #'''GOAL: Remove the above data structure'''

            #/////////////////////////////////////////////////////////////////////////////
            #Print contents of the dictionaryOfCurrentClientTasks
            #/////////////////////////////////////////////////////////////////////////////
            try:
                print " "
                print "Printing the Contents of the dictionaryOfCurrentClientTasks"
                print "----------------------------------------------------------------"
                print "[key]        [value]"
                for key, value in self.dictionaryOfCurrentClientTasks.iteritems():
                    print str(key), str(value)
                print "(END OF PRINTING CONTENTS OF THE DICTIONARYOFCURRENTCLIENTTASKS)"
                print "----------------------------------------------------------------"
            except Exception as inst:
                print "========================================================================================"
                print "ERROR: An exception has been thrown in the Finally Block, in the print Dictionary of Current CLient Tasks Section"
                print type(inst) #the exception instance
                print inst.args #srguments stored in .args
                print inst #_str_ allows args tto be printed directly
                print "========================================================================================"
            #/////////////////////////////////////////////////////////////////////////////
            #End of Print contents of the dictionaryOfCurrentClientTasks
            #/////////////////////////////////////////////////////////////////////////////

            #/////////////////////////////////////////////////////////////////////////////
            #Print Number of IP address that server was not able to find
            #/////////////////////////////////////////////////////////////////////////////
            print " "
            print "Printing Number of IP Addresses that Server Could Not Find"
            print "----------------------------------------------------------"
            if(self.recordOfNumberOfIPAddressesThatHaventBeenFound < 1):
                print "Server was able to find all of the IP addresses."
            else:
                print "Server could not find " + str(self.recordOfNumberOfIPAddressesThatHaventBeenFound) + " IP Addresses"
            print "(END OF PRINTING NUMBER OF IP ADDRESSES SERVER COULD NOT FIND)"
            print "----------------------------------------------------------"
            #/////////////////////////////////////////////////////////////////////////////
            #End of Print Number of IP Addresses that server was not able to find
            #/////////////////////////////////////////////////////////////////////////////

            #/////////////////////////////////////////////////////////////////////////////
            #Print Command Records
            #/////////////////////////////////////////////////////////////////////////////
            try:
                print " "
                print "COMMAND RECORDS: Part 1/4"
                print "Printing Record of OutBound Commands from Server to Controller"
                print "----------------------------------------------------------------"
                #print nextChunk records
                if(self.recordOfOutboundCommandsFromServerToController['nextChunk'] > 0):
                    print "# of nextChunk Commands sent from Server to Controller: " + str(self.recordOfOutboundCommandsFromServerToController['nextChunk'])
                else:
                    print "# of nextChunk Commands sent from Server to Controller: 0"
                #print chunkAgain records
                if(self.recordOfOutboundCommandsFromServerToController['chunkAgain'] > 0):
                    print "# of chunkAgain Commands sent from Server to Controller: " + str(self.recordOfOutboundCommandsFromServerToController['chunkAgain'])
                else:
                    print "# of chunkAgain Commands sent from Server to Controller: 0"
                #print waiting records
                if(self.recordOfOutboundCommandsFromServerToController['waiting'] > 0):
                    print "# of waiting Commands sent from Server to Controller: " + str(self.recordOfOutboundCommandsFromServerToController['waiting'])
                else:
                    print "# of waiting Commands sent from Server to Controller: 0"
                #print done records
                if(self.recordOfOutboundCommandsFromServerToController['done'] > 0):
                    print "# of done Commands sent from Server to Controller: " + str(self.recordOfOutboundCommandsFromServerToController['done'])
                else:
                    print "# of done Commands sent from Server to Controller: 0"
                print "(END OF RECORD OF OUTBOUND COMMANDS FROM SERVER TO CONTROLLER)"
                print "---------------------------------------------------------------"
            except Exception as inst:
                print "========================================================================================"
                print "ERROR: An exception has been thrown in the Finally Block, in the print Record of Outbound Commands from Server to Controller Section"
                print type(inst) #the exception instance
                print inst.args #srguments stored in .args
                print inst #_str_ allows args tto be printed directly
                print "========================================================================================"
            try:
                print " "
                print "COMMAND RECORDS: Part 2/4"
                print "Printing Record of Outbound Commands from Server to Client(s)"
                print "------------------------------------------------------------"
                #print the DONE records
                if(self.recordOfOutboundCommandsFromServerToClient['DONE'] > 0):
                    print "# of DONE Commands sent from Server to Client(s): " + str(self.recordOfOutboundCommandsFromServerToClient['DONE'])
                else:
                    print "# of DONE Commands sent from Server to Client(s): 0"
                #print the nextChunk records
                if(self.recordOfOutboundCommandsFromServerToClient['nextChunk'] > 0):
                    print "# of nextChunk Commands sent from Server to Client(s): " + str(self.recordOfOutboundCommandsFromServerToClient['nextChunk'])
                else:
                    print "# of nextChunk Commands sent from Server to Client(s): 0"
                #print the nextChunkData records
                if(self.recordOfOutboundCommandsFromServerToClient['nextChunkData'] > 0):
                    print "# of nextChunkData Commands sent from Server to Client(s): " + str(self.recordOfOutboundCommandsFromServerToClient['nextChunkData'])
                else:
                    print "# of nextChunkData Commands sent from Server to Client(s): 0"
                print "(END OF RECORD OF OUTBOUND COMMANDS FROM SERVER TO CLIENT"
                print "-----------------------------------------------------------"
            except Exception as inst:
                print "========================================================================================"
                print "ERROR: An exception has been thrown in the Finally Block, in the print Record of Outbound Commands from Server to Client(s) Section"
                print type(inst) #the exception instance
                print inst.args #srguments stored in .args
                print inst #_str_ allows args tto be printed directly
                print "========================================================================================"
            try:
                print " "
                print "COMMAND RECORDS: Part 3/4"
                print "Printing Record of Inbound Commands from Controller to Server"
                print "--------------------------------------------------------------"
                #print the REPLY TO NEXT CHUNK
                if(self.recordOfInboundCommandsFromControllerToServer['REPLY_TO_NEXT_CHUNK'] > 0):
                    print "# of REPLY TO NEXT CHUNK Commands received from Controller: " + str(self.recordOfInboundCommandsFromControllerToServer['REPLY_TO_NEXT_CHUNK'])
                else:
                    print "# of REPLY TO NEXT CHUNK Commands received from Controller: 0"
                #print the REPLY TO CHUNK AGAIN
                if(self.recordOfInboundCommandsFromControllerToServer['REPLY_TO_CHUNK_AGAIN'] > 0):
                    print "# of REPLY TO CHUNK AGAIN Commands received from Controller: " + str(self.recordOfInboundCommandsFromControllerToServer['REPLY_TO_CHUNK_AGAIN'])
                else:
                    print "# of REPLY TO CHUNK AGAIN Commands received from Controller: 0"
                #print the REPLY TO DONE
                if(self.recordOfInboundCommandsFromControllerToServer['REPLY_TO_DONE'] > 0):
                    print "# of REPLY TO DONE Commands reeived from Controller: " + str(self.recordOfInboundCommandsFromControllerToServer['REPLY_TO_DONE'])
                else:
                    print "# of REPLY TO DONE Commands received from Controller: 0"
                #print the Chunk Objects
                if(self.recordOfInboundCommandsFromControllerToServer['Chunk_Objects'] > 0):
                    print "# of Chunk Objects received from Controller: " + str(self.recordOfInboundCommandsFromControllerToServer['Chunk_Objects'])
                else:
                    print "# of Chunk Objects received from Controller: 0"
                #print the Unknowns
                if(self.recordOfInboundCommandsFromControllerToServer['Unknown'] > 0):
                    print "# of Unknown Commands received from Controller: " + str(self.recordOfInboundCommandsFromControllerToServer['Unknown'])
                else:
                    print "# of Unknown Commands received from Controller: 0"
                print "(END OF RECORD OF INBOUND COMMANDS FROM THE CONTROLLER)"
                print "------------------------------------------------------------"
            except Exception as inst:
                print "========================================================================================"
                print "ERROR: An exception has been thrown in the Finally Block, in the print Record of Inbound Commands from Controller Section"
                print type(inst) #the exception instance
                print inst.args #srguments stored in .args
                print inst #_str_ allows args tto be printed directly
                print "========================================================================================"
            try:
                print " "
                print "COMMANDS RECORDS: Part 4/4"
                print "Printing Inbound Commands from Client(s) to Server"
                print "----------------------------------------------------"
                #print NEXT
                if(self.recordOfInboundCommandsFromClientToServer['NEXT'] > 0):
                    print "# of NEXT Commands received from Client(s): " + str(self.recordOfInboundCommandsFromClientToServer['NEXT'])
                else:
                    print "# of NEXT Commands received from Client(s): 0"
                #print FOUNDSOLUTION
                if(self.recordOfInboundCommandsFromClientToServer['FOUNDSOLUTION'] > 0):
                    print "# of FOUNDSOLUTION Commands received from Client(s): " + str(self.recordOfInboundCommandsFromClientToServer['FOUNDSOLUTION'])
                else:
                    print "# of FOUNDSOLUTION COmmands received from Client(s): 0"
                #print CRASHED
                if(self.recordOfInboundCommandsFromClientToServer['CRASHED'] > 0):
                    print "# of CRASHED Commands received from Client(s): " + str(self.recordOfInboundCommandsFromClientToServer['CRASHED'])
                else:
                    print "# of CRASHED Commands received from Client(s): 0"
                #print the Unknowns
                if(self.recordOfInboundCommandsFromClientToServer['Unknown'] > 0):
                    print "# of Unknown Commands received from Client(s): " + str(self.recordOfInboundCommandsFromClientToServer['Unknown'])
                else:
                    print "# of Unknown Commands received from Client(s): 0"
                print "(END OF RECORD OF INBOUND COMMANDS FROM CLIENT(S))"
                print "------------------------------------------------------"
            except Exception as inst:
                print "========================================================================================"
                print "ERROR: An exception has been thrown in the Finally Block, in the print Record of Inbound Commands from Client(s) Section"
                print type(inst) #the exception instance
                print inst.args #srguments stored in .args
                print inst #_str_ allows args tto be printed directly
                print "========================================================================================"
            print " "
            #/////////////////////////////////////////////////////////////////////////////
            #End of print command Records
            #/////////////////////////////////////////////////////////////////////////////

        #.........................................................................
        #End of Finally Block (where socket is closed)
        #.........................................................................

    #-------------------------------------------------------------------
    #End of NetworkServer Class Constructor
    #-------------------------------------------------------------------

    #-------------------------------------------------------------------
    #Defined Communication Functions
    #-------------------------------------------------------------------
        #.........................................................................
        #Server-Controller Communication Functions
        #.........................................................................
            #/////////////////////////////////////////////////////////////////////////////
            #Outbound Functions
            #/////////////////////////////////////////////////////////////////////////////
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                #Send nextChunk Command to Controller
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    def sendNextChunkCommandToController(self):
        try:
            self.pipe.send("nextChunk")
            print "I/O: The NEXTCHUNK command was sent to the Controller"
            #increment record counter
            self.recordOfOutboundCommandsFromServerToController['nextChunk'] = (self.recordOfOutboundCommandsFromServerToController['nextChunk'] + 1)
        except Exception as inst:
            print "============================================================================================="
            print "ERROR: An exception was thrown in the Server-Controller Outbound sendNextChunkCommand Try Block"
            #the exception instance
            print type(inst)
            #srguments stored in .args
            print inst.args
            #_str_ allows args tto be printed directly
            print inst
            print "============================================================================================="
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                #Send chunkAgain Command to Controller (MAY BE OBSOLETE ON THE SERVER SIDE)
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    def sendChunkAgainCommandToController(self):
        try:
            self.pipe.send("chunkAgain")
            print "I/O: The CHUNKAGAIN command was sent to the Controller"
            #increment the record counter
            self.recordOfOutboundCommandsFromServerToController['chunkAgain'] = (self.recordOfOutboundCommandsFromServerToController['chunkAgain'] + 1)
        except Exception as inst:
            print "============================================================================================="
            print "ERROR: An exception was thrown in the Server-Controller Outbound sendChunkAgainCommand Try Block"
            #the exception instance
            print type(inst)
            #srguments stored in .args
            print inst.args
            #_str_ allows args tto be printed directly
            print inst
            print "============================================================================================="
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                #Send Waiting Command to Controller (MAY BE OBSOLETE ON THE SERVER SIDE)
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    def sendWaitingCommandToController(self):
        try:
            self.pipe.send("waiting")
            print "I/O: The WAITING command was sent to the Controller"
            #increment the record counter
            self.recordOfOutboundCommandsFromServerToController['waiting'] = (self.recordOfOutboundCommandsFromServerToController['waiting'] + 1)
        except Exception as inst:
            print "============================================================================================="
            print "ERROR: An exception was thrown in the Server-Controller Outbound sendWaitingCommend  Try Block"
            #the exception instance
            print type(inst)
            #srguments stored in .args
            print inst.args
            #_str_ allows args tto be printed directly
            print inst
            print "============================================================================================="
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                #Send Done Command to Controller
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    def sendDoneCommandToController(self):
        try:
            self.pipe.send("done ")
            print "I/O: The DONE command was sent to the Controller"
            #increment the record counter
            self.recordOfOutboundCommandsFromServerToController['done'] = (self.recordOfOutboundCommandsFromServerToController['done'] + 1)
        except Exception as inst:
            print "============================================================================================="
            print "ERROR: An exception was thrown in the Server-Controller Outbound sendDoneCommand Try Block"
            #the exception instance
            print type(inst)
            #srguments stored in .args
            print inst.args
            #_str_ allows args tto be printed directly
            print inst
            print "============================================================================================="
            #/////////////////////////////////////////////////////////////////////////////
            #End of Outbound Functions
            #/////////////////////////////////////////////////////////////////////////////

            #/////////////////////////////////////////////////////////////////////////////
            #Inbound Functions
            #/////////////////////////////////////////////////////////////////////////////
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                #Check for nextChunk Command
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    def checkForNextChunk(self,inboundString): #check to see if the string contains the next chunk of the problem
        try:
            print "STATUS: Checking to see if inboundString is nextChunk..."
            if(len(inboundString) < 1):
                return False
            if inboundString == "nextChunk":
                #position 9 will be a space
                print "I/O: NEXTCHUNK command was received from the controller class"
                self.recordOfInboundCommandsFromControllerToServer['REPLY_TO_NEXT_CHUNK'] = (self.recordOfInboundCommandsFromControllerToServer['REPLY_TO_NEXT_CHUNK'] + 1)
                return True
            else:
                return False
        except Exception as inst:
            print "============================================================================================="
            print "ERROR: An exception was thrown in the Server-Controller Inbound checkForNextChunk Try Block"
            #the exception instance
            print type(inst)
            #srguments stored in .args
            print inst.args
            #_str_ allows args tto be printed directly
            print inst
            print "============================================================================================="
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                #Check for chunkAgain Command (MAY BE OBSOLETE ON THE SERVER SIDE)
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    def checkForChunkAgain(self,inboundString): #check to see if the string contains that chunk that was requested
        try:
            print "STATUS: Checking to see if inboundString is chunkAgain..."
            if(len(inboundString) < 1):
                return False
            if(inboundString[0:9] == "CHUNKAGAIN"):
                #position 10 will be a space
                print "I/O: CHUNKAGAIN command was received from the controller class"
                self.recordOfInboundCommandsFromControllerToServer['REPLY_TO_CHUNK_AGAIN'] = (self.recordOfInboundCommandsFromControllerToServer['REPLY_TO_CHUNK_AGAIN'] + 1)
                return True
            else:
                return False
        except Exception as inst:
            print "============================================================================================="
            print "ERROR: An exception was thrown in the Server-Controller Inbound checkForChunkAgain Try Block"
            #the exception instance
            print type(inst)
            #srguments stored in .args
            print inst.args
            #_str_ allows args tto be printed directly
            print inst
            print "============================================================================================="
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                #Check for found command (reply to done) (MAY BE OBSOLETE ON THE SERVER SIDE)
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    def checkForDone(self,inboundString):
        try:
            print "STATUS: Checking to see if inboundString is Done..."
            if(len(inboundString) < 1):
                return False
            #if(inboundString[0:3] == "done"): #OLD METHOD
            if(inboundString[0] == "d"):
                if(inboundString[1] == "o"):
                    if(inboundString[2] == "n"):
                        if(inboundString[3] == "e"):
                            print "I/O: DONE Command was received from the controller class"
                            self.recordOfInboundCommandsFromControllerToServer['REPLY_TO_DONE'] = (self.recordOfInboundCommandsFromControllerToServer['REPLY_TO_DONE'] + 1)
                            return True
            else:
                return False
        except Exception as inst:
            print "============================================================================================="
            print "ERROR: An exception was thrown in the Server-Controller Inbound checkForDone Try Block"
            #the exception instance
            print type(inst)
            #srguments stored in .args
            print inst.args
            #_str_ allows args tto be printed directly
            print inst
            print "============================================================================================="
            #/////////////////////////////////////////////////////////////////////////////
            #End of Inbound Functions
            #/////////////////////////////////////////////////////////////////////////////
        #.........................................................................
        #End of Server-Controller Communication Functions
        #.........................................................................

        #.........................................................................
        #Server-Client Communication Functions
        #.........................................................................
            #/////////////////////////////////////////////////////////////////////////////
            #Outbound Functions
            #/////////////////////////////////////////////////////////////////////////////
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                #Send Done Command to Client
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    def sendDoneCommandToClient(self,recipientsSocket, recipientIPAddress): #sends the DONE command to a client
        try:
            recipientsSocket.sendto("DONE", recipientIPAddress)
            print "I/O: The DONE command was issued to: " + str(recipientIPAddress)
            #increment the record counter
            self.recordOfOutboundCommandsFromServerToClient['DONE'] = (self.recordOfOutboundCommandsFromServerToClient['DONE'] + 1)
        except Exception as inst:
            print "============================================================================================="
            print "ERROR: An exception was thrown in the Server-Client Outbound sendDoneCommand Try Block"
            #the exception instance
            print type(inst)
            #srguments stored in .args
            print inst.args
            #_str_ allows args tto be printed directly
            print inst
            print "============================================================================================="
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                #Send nextChunk Command to Client (the next part of the problem)
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    def sendNextToClient(self,recipientsSocket, recipientIPAddress, recipientPort, theNextPart): #sends the next part of problem to the client
        try:
            recipientsSocket.sendto(theNextPart, (recipientIPAddress, recipientPort))
            print "I/O: The nextChunk of the problem was sent to: " + str(recipientIPAddress)
            #increment the record counter
            self.recordOfOutboundCommandsFromServerToClient['nextChunk'] = (self.recordOfOutboundCommandsFromServerToClient['nextChunk'] + 1)
        except Exception as inst:
            print "============================================================================================="
            print "ERROR: An exception was thrown in the Server-Client Outbound sendNext Try Block"
            #the exception instance
            print type(inst)
            #srguments stored in .args
            print inst.args
            #_str_ allows args tto be printed directly
            print inst
            print "============================================================================================="
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                #Send the data for nextChunk to the client
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    def sendNextDataToClient(self,recipientSocket, recipientIPAddress, recipientPort, theNextData):
        try:
            recipientSocket.sendto(str(theNextData),(recipientIPAddress, recipientPort))
            print "I/O: The corresponding data has been sent to: " + str(recipientIPAddress)
            #increment the counter
            self.recordOfOutboundCommandsFromServerToClient['nextChunkData'] = (self.recordOfOutboundCommandsFromServerToClient['nextChunkData'] + 1)
        except Exception as inst:
            print "============================================================================================="
            print "ERROR: An exception was thrown in the Server-Client Outbound sendNextData Try Block"
            #the exception instance
            print type(inst)
            #srguments stored in .args
            print inst.args
            #_str_ allows args tto be printed directly
            print inst
            print "============================================================================================="
            #/////////////////////////////////////////////////////////////////////////////
            #End of Outbound Functions
            #/////////////////////////////////////////////////////////////////////////////

            #/////////////////////////////////////////////////////////////////////////////
            #Inbound Functions
            #/////////////////////////////////////////////////////////////////////////////
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                #Check for Next Command
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    def checkForNextCommand(self,inboundString): #checks for the NEXT command
        try:
            if(len(inboundString) < 1):
                return False
            if(inboundString[0]=="N"):
                if(inboundString[1]=="E"):
                    if(inboundString[2]=="X"):
                        if(inboundString[3]=="T"):
                            print "I/O: A Client has issued the NEXT command"
                            #position 4 is a space
                            #tempIP= ""  #THIS IS NOW DONE IN THE SERVER LOOP
                            #for i in range(5, len(inboundString)):
                             #   tempIP= tempIP + inboundString[i]
                            #self.stackOfClientsWaitingForNextChunk.append(tempIP) #pushing ip onto the stack
                            self.recordOfInboundCommandsFromClientToServer['NEXT'] = (self.recordOfInboundCommandsFromClientToServer['NEXT'] + 1)
                            return True
            else:
                return False
        except Exception as inst:
            print "============================================================================================="
            print "ERROR: An exception was thrown in the Server-Client Inbound checkForNextCommand Try Block"
            #the exception instance
            print type(inst)
            #srguments stored in .args
            print inst.args
            #_str_ allows args tto be printed directly
            print inst
            print "============================================================================================="
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                #Check for FoundSolution Command (MAY BE OBSOLETE ON THE SERVER SIDE)
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    def checkForFoundSolutionCommand(self,inboundString): #checks for the "FOUNDSOLUTION" string
        try:
            #if(inboundString[0:12] == "FOUNDSOLUTION"): #OLD METHOD
            if(len(inboundString) < 1):
                return False
            if(inboundString[0] == "F"):
                if(inboundString[1] == "O"):
                    if(inboundString[2] == "U"):
                        if(inboundString[3] == "N"):
                            if(inboundString[4] == "D"):
                                if(inboundString[5] == "S"):
                                    if(inboundString[6] == "O"):
                                        if(inboundString[7] == "L"):
                                            if(inboundString[8] == "U"):
                                                if(inboundString[9] == "T"):
                                                    if(inboundString[10] == "I"):
                                                        if(inboundString[11] == "O"):
                                                            if(inboundString[12] == "N"):
                                                                print "I/O: A Client has issued the FOUNDSOLUTION command"
                                                                #position 13 is a space
                                                                #tempIP= ""  #THIS IS NOW DONE IN SERVER LOOP
                                                                #for i in range(14, len(inboundString)):
                                                                #    tempIP= tempIP + inboundString[i]
                                                                #self.stackOfClientsWaitingForNextChunk.append(tempIP) #pushing ip onto the stack
                                                                self.recordOfInboundCommandsFromClientToServer['FOUNDSOLUTION'] = (self.recordOfInboundCommandsFromClientToServer['FOUNDSOLUTION'] + 1)
                                                                return True
            else:
                return False
        except Exception as inst:
            print "============================================================================================="
            print "ERROR: An exception was thrown in the Server-Client Inbound checkForFoundSolutionCommand Try Block"
            #the exception instance
            print type(inst)
            #srguments stored in .args
            print inst.args
            #_str_ allows args tto be printed directly
            print inst
            print "============================================================================================="
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                #Check for Crashed Command
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    def checkForCrashedCommand(self,inboundString): #checks for the "CRASHED" Command
        try:
            if(len(inboundString) < 1):
                return False
            if(inboundString[0]=="C"):
                if(inboundString[1]=="R"):
                    if(inboundString[2]=="A"):
                        if(inboundString[3]=="S"):
                            if(inboundString[4]=="H"):
                                if(inboundString[5]=="E"):
                                    if(inboundString[6]=="D"):
                                        tempCrashIP = ""   #THIS STAYS IN THE CRASH COMMAND SECTION
                                        #position 7 is a space between the ip address and the crashed message
                                        for i in range(8, len(inboundString)):
                                            if(inboundString[i].isalpha()):
                                                print "WARNING: A Non-Numeral Value Was Detected In The Ip Address, Ignoring Remainder of String"
                                                break
                                            else:
                                                tempCrashIP = tempCrashIP + inboundString[i]
                                        if(len(tempCrashIP) < 1): #if the length is less than one, stop performing an IP check
                                            return False
                                        print "WARNING: A Client has issued the CRASHED command"
                                        print "The Crashed Client IP: " + tempCrashIP
                                        self.listOfCrashedClients.append(tempCrashIP)
                                        print "INFO: The crashed client's IP address has been added to the listOfCrashedClients"
                                        #look through listOfConnected clients and find the matching ip address
                                        print "STATUS: Looking for matching IP address in list of clients..."
                                        foundMatch= False
                                        tempAddr2= ""
                                        for index in range(0, len(self.listOfClients)):
                                            tempSock, tempAddr= self.listOfClients[index] #get socket and ip address of client
                                            print "STATUS: Copying list of clients' IP Address to a new string"
                                            tempAddr2= str(tempAddr[0])
                                            print "STATUS: Comparing IP Addresses..."
                                            if(tempCrashIP == tempAddr2):
                                                print "INFO: Matching IP address was found in the list of clients"
                                                #print "DEBUG: tempAddr=" + str(tempAddr)
                                                del self.listOfClients[index]
                                                print "INFO: The crashed client " + str(tempAddr) + " was removed from the list of clients"
                                                foundMatch= True
                                                print "STATUS: Adding this client's chunk to the stack of chunks the need to be reassigned..."
                                                self.stackOfChunksThatNeedToBeReassigned.append(self.dictionaryOfCurrentClientTasks[tempAddr]) #push crashed clients chunk onto the stack
                                                print "INFO: Successfully pushed the crashed client's chunk onto the stack"
                                                self.recordOfInboundCommandsFromClientToServer['CRASHED'] = (self.recordOfInboundCommandsFromClientToServer['CRASHED'] + 1)
                                                break
                                            else:
                                                print "INFO: No Match found yet. " + str(tempCrashIP) + " != " + str(tempAddr2)

                                        if(foundMatch == False):
                                            print "WARNING: No Matching IP address was found in the list of clients"
                                            print "INFO: Unable to Find the Crashed IP: " +str(tempCrashIP) + " "
                                            self.recordOfNumberOfIPAddressesThatHaventBeenFound+= 1
                                        return True
                                    else:
                                        return False
                                else:
                                    return False
                            else:
                                return False
                        else:
                            return False
                    else:
                        return False
                else:
                    return False
            else:
              return False
        except Exception as inst:
            print "============================================================================================="
            print "ERROR: An exception was thrown in the Server-Client Inbound checkForCrashedCommand Try Block"
            #the exception instance
            print type(inst)
            #srguments stored in .args
            print inst.args
            #_str_ allows args tto be printed directly
            print inst
            print "============================================================================================="
            #/////////////////////////////////////////////////////////////////////////////
            #End of Inbound Functions
            #/////////////////////////////////////////////////////////////////////////////
        #.........................................................................
        #End of Server-Client Communication Functions
        #.........................................................................
    #-------------------------------------------------------------------
    #End of Defined Communication Functions
    #-------------------------------------------------------------------
    #-------------------------------------------------------------------
    #Client Thread function
    #-------------------------------------------------------------------
    def clientthread(self,inputSocket):
        try:
            data = ""
            #infinite loop so that the function does not terminate and tread does not end
            #self.numOfThreads+= 1
            '''
            while True:
                #sending message to connected client
                import time
                time.sleep(0.25)
                messageSent= False
                while messageSent == False:
                    try:
                        inputSocket.send('You have spawned a new thread!') #send the string
                        messageSent= True
                    except socket.error as inst:
                        messageSent= False
                        #if(str(inst) == "[Errno 35] Resource temporarily unavailable"):
                        #time.sleep(0)
                        #print "WARNING: 2nd attempt at sending test message"
                        #self.serverSocket.settimeout(0.25) #reset timeout
                        #inputSocket.send('You have spawned a new thread!')
                        #continue
                        #raise inst
                #receiving from the client
                '''
            while True:
                #check for client input
                messageReceived= False
                while messageReceived == False:
                    try:
                        data = inputSocket.recv(2048)
                        if not data:
                            messageReceived= True
                    except Exception as inst:
                        messageReceived= False
                    if(len(data) < 1):
                        unusedVar=True
                    elif(self.compareString(str(data),"NEXT",0,0,len("NEXT"),len("NEXT"))):
                        try:
                            print "Received the NEXT Command from client"
                            self.sendNextChunkCommandToController()
                        except socket.error as inst:
                            import time
                            time.sleep(0)
                            print "WARNING: 2nd attempt at sending nextChunkCommandToController"
                            self.serverSocket.settimeout(0.25) #reset timeout
                            self.sendNextChunkCommandToController()
                    else:
                        print "Other command received: " + str(data)
                #check for controller input
                if(self.pipe.poll()):
                    inputString= ""
                    receivedString= False
                    while receivedString==False:
                        try:
                            inputString= self.pipe.recv()
                            receivedString= True
                            print "received something on the pipe^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"
                        except Exception as inst:
                            receivedString=False
                    if(self.compareString(inputString,"nextChunk",0,0,len("nextChunk"),len("nextChunk"))):
                        receivedData= False
                        inputData= ""
                        while receivedData==False:
                            try:
                                inputData= self.pipe.recv()
                                receivedData= True
                            except Exception as inst:
                                receivedData= False
                        print "I FOUND IT!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
                        #if(len(self.stackOfClientsWaitingForNextChunk) > 0):


        except IndexError as inst:
            print "============================================================================================="
            print "ERROR: An IndexError was thrown in the Client Thread function Try Block"
            #the exception instance
            print type(inst)
            #srguments stored in .args
            print inst.args
            #_str_ allows args tto be printed directly
            print inst
            print " "
            print "string: '" +str(data) +"'"
            print "============================================================================================="
        except Exception as inst:
            print "============================================================================================="
            print "ERROR: An exception was thrown in the Client Thread function Try Block"
            #the exception instance
            print type(inst)
            #srguments stored in .args
            print inst.args
            #_str_ allows args tto be printed directly
            print inst
            print "============================================================================================="
    #-------------------------------------------------------------------
    #End of client thread function
    #-------------------------------------------------------------------
    def compareString(self,inboundStringA, inboundStringB, startA, startB, endA, endB):
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
#==============================================================
#End of NetworkServer Class Definition
#==============================================================

