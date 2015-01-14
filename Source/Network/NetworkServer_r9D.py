__author__ = 'chris hamm'
#NetworkServer_r9D
#Created: 1/10/2015

#Added lists for the server to use to keep track of things that have happened and still need to be done
    #(In progress) (May not be implemented) A list of all messages that have been received from clients and who sent them
    #A list that records all of the clients that have crashed (and have been detected as crashed)
    #A list of clients that are waiting for a reply
    #(In Progress) A list of what each client is currently working on
    #(in progress) A list of chunk objects that contains the chunk of a crashed client (chunk added when client crashes, and chunk is removed when a new client is given the chunk)
#Added functions to parse chunk objects (Has now been decided that these will not be needed)
#chunk object path: server-controller -> server (converted to string to be sent over network) -> client (convert back to chunk object) -> client-controller

import socket
import platform
import Chunk
#=================================================================================================
#SERVER CONSTRUCTOR/CLASS DEFINITION
#=================================================================================================
class NetworkServer(): #CLASS NAME WILL NOT CHANGE BETWEEN VERSIONS
        #class variables
        host= '' #Symbolic name, meaning all available interfaces
        port= 49200
        numOfClients= 0
        serverSocket = 0
        serverIsRunning = True
        #list to store the socket and address of every client
        listOfClients = [] #This list is a list of tuples (socket, address)
        listOfControllerMessages = [] #holds a list of strings that have been sent by the controller class
        listOfCrashedClients= [] #records the ip address of any client that has crashed during the last server run
        #listOfInactiveClients = [] #records the ip address of any client who needs something to do
        #dictionary (below) that holds the ip of each client that is waiting for a reply as the key and what it is waiting for as the value
        dictionaryOfClientsWaitingForAReply = {} #Possible values: "NEXTCHUNK", "FOUNDSOLUTION"
        dictionaryOfCurrentClientTasks = {} #dictionary that holds the ip of each client as the key and the chunk it is working on as the value
    

        #--------------------------------------------------------------------------------
        #constructor
        #--------------------------------------------------------------------------------
        def __init__(self, pipeendconnectedtocontroller):
            self.pipe= pipeendconnectedtocontroller

            #socket.AF_INET is a socket address family represented as a pair. (hostname, port). This is the default parameter
            #socket.SOCK_STREAM is the default parameter. This defines the socket type
            self.serverSocket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print "STATUS: Server socket created successfully"

            #..................................................................................
            #Bind the socket to local host and port
            #..................................................................................
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

            #..................................................................................
            #Detect Operating System
            #..................................................................................
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

            #..................................................................................
            #Get the IP Address
            #..................................................................................
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

            #..................................................................................
            #Start listening to socket
            #..................................................................................
            self.serverSocket.listen(5)
            print "Waiting for initial client to connect..."

            #..................................................................................
            #Waiting for initial Client to connect
            #..................................................................................
            sock, addr= self.serverSocket.accept()
            print "INFO: First client has connected"
            print "INFO: Connected with " + addr[0] + ":" + str(addr[1])
            self.listOfClients.append((sock, addr)) #add the tuple to the list of clients
            print "STATUS: Client successfully added to the list of clients"
            #When a client is added, they are also added to the dictionaryOfCurrentClientTasks
            self.dictionaryOfCurrentClientTasks[addr] = "" #Not working on anything, so value is the empty string
            print "STATUS: Client successfully added to the Dictionary of Current Client Tasks"
            #print str(len(self.listOfClients)) + " Client(s) are currently Connected."

            #..................................................................................
            #Server PRIMARY WHILE LOOP
            #..................................................................................
            try: #server primary while loop try block
                while(self.serverIsRunning==True): #server primary while loop

                    #/////////////////////////////////////////////////////////////////////////////////
                    #Check for input from clients
                    #/////////////////////////////////////////////////////////////////////////////////
                    print "STATUS: Checking for input from client(s)..."
                    try: #check for client input try block
                        sock.settimeout(2.0)
                        theInput = sock.recv(2048) #listening for input
                        if(len(theInput) >= 1):
                            print "INFO: Received a message from a client."
                            if(self.checkForNextCommand(theInput)==True):
                                print "INFO: NEXT command was received"
                                self.sendNextChunkCommandToController()
                                print "INFO: Sent the NextChunk Command to the Controller"
                            elif(self.checkForFoundSolutionCommand(theInput)==True):
                                print "INFO: FOUNDSOLUTION command was received"
                                self.sendDoneCommandToController()
                                print "INFO: Sent the Done Command to the Controller"
                            elif(self.checkForCrashedCommand(theInput)==True):
                                print "INFO: CRASHED command was received"
                                #self.listenForCrashedClientIP = True
                            else:
                                print "ERROR: unknown command received"
                                print "The unknown command: '" + theInput + "'"
                        else:
                            print "INFO: The Empty String has been received."
                    except socket.timeout as inst:
                        print "STATUS: Socket has timed out. No input from client detected."
                    except Exception as inst:
                        print "========================================================================================"
                        print "ERROR: An exception has been thrown in the Check for client input Try Block"
                        print type(inst) #the exception instance
                        print inst.args #srguments stored in .args
                        print inst #_str_ allows args tto be printed directly
                        print "========================================================================================"

                    #/////////////////////////////////////////////////////////////////////////////////
                    #Check for input from controller class
                    #/////////////////////////////////////////////////////////////////////////////////
                    print "STATUS: Checking for input from the Controller class..."
                    try: #check for input from controller try block
                        if(self.pipe.poll()):
                            recv = self.pipe.recv()
                            print "INFO: Received a message from the controller"
                            if(self.checkForNextChunk(recv)==True):
                                print "INFO: Received the reply to the NextChunk command"
                            elif(self.checkForChunkAgain(recv)==True):
                                print "INFO: Received the reply to the ChunkAgain command"
                            elif(self.checkForFound(recv)==True):
                                print "INFO: Received reply stating whether the key has been found or not"
                            else:
                                print "ERROR: Received an unknown command from the controller"
                                print "The unknown command: '" + recv + "'"
                        else:
                            print "STATUS: No command was received from the controller class"
                    except Exception as inst:
                        print "========================================================================================"
                        print "ERROR: An exception has been thrown in the Check for input from Controller class Try Block"
                        print type(inst) #the exception instance
                        print inst.args #srguments stored in .args
                        print inst #_str_ allows args tto be printed directly
                        print "========================================================================================"

                    #/////////////////////////////////////////////////////////////////////////////////
                    #Distribute command to clients if needed
                    #/////////////////////////////////////////////////////////////////////////////////
                    try: #distribute command try block
                        print "STATUS: Checking to see if a command needs to be send to the clients..."
                        #check to see if there are any commands that the controller has sent to the server
                        if(len(self.listOfControllerMessages) < 1):
                            print "INFO: There are no new commands from the controller class"
                        else:
                            print "INFO: There are " + str(len(self.listOfControllerMessages)) + " new command(s) from the controller class"
                            for i in range(0,len(self.listOfControllerMessages)):
                                print str(i) + ") " + str(self.listOfControllerMessages[i])
                        print " "
                        print "INFO: " + str(len(self.dictionaryOfClientsWaitingForAReply)) + " Client(s) are currently waiting for a reply"
                        #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                        #Figure out what each of the received commands are and who it needs to go to, then distribute accordingly
                        #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                        print " "
                        print "STATUS: Figuring Out What Each Command Is and Who It Needs To Be Sent To"
                        for i in range(0, len(self.listOfControllerMessages)):
                            print "Command " + str(i) + ") " + str(self.listOfControllerMessages[i])
                            analysisString= str(self.listOfControllerMessages[i])
                            #***************************************************************************************
                            #Looking for NEXTCHUNK command
                            #***************************************************************************************
                            if(analysisString[0:8] == "NEXTCHUNK"): #looking for NEXTCHUNK command
                                try:  #looking for NEXTCHUNK in analysis string try block
                                    print "Command Type: NEXTCHUNK"
                                    #recall that position 9 is a space
                                    #looking for the next space in the string which will be after the ip address
                                    analysisIP= ""
                                    endOfIPPosition= 10
                                    for x in range(10,len(analysisString)):
                                        if(analysisString[x] == " "): #if it is a space
                                            endOfIPPosition= x
                                            break
                                        else:
                                            analysisIP= str(analysisIP + str(analysisString[x]))
                                    print "Need To Send To: " + analysisIP
                                    print "INFO: Looking for matching IP address in listOfClients"
                                    foundMatchingIP= False
                                    for index in range(0,len(self.listOfClients)):
                                        tempSock, tempAddr = self.listOfClients[index]
                                        if(analysisIP == tempAddr):
                                            print "Match was found"
                                            foundMatchingIP= True
                                            break
                                        else:
                                            print "No Match Found Yet. " + str(analysisIP) + "!=" + str(tempAddr)
                                    if(foundMatchingIP==False):
                                        print "WARNING: No Matching IP Address was found for:" + analysisIP
                                    else:
                                        print "STATUS: Sending Message To Client..."
                                        try: #send NEXTCHUNK message to client try block
                                            theMessage= str(analysisString[endOfIPPosition+1:len(analysisString)])
                                            self.sendNextToClient(tempSock,tempAddr,theMessage)
                                            print "STATUS: Sent Message to the client"
                                        except Exception as inst:
                                            print "========================================================================================"
                                            print "ERROR: An exception has been thrown in the Send NEXTCHUNK message to client try block"
                                            print type(inst) #the exception instance
                                            print inst.args #srguments stored in .args
                                            print inst #_str_ allows args tto be printed directly
                                            print "========================================================================================"
                                except Exception as inst:
                                    print "========================================================================================"
                                    print "ERROR: An exception has been thrown in the looking for NEXTCHUNK in analysis string Try Block"
                                    print type(inst) #the exception instance
                                    print inst.args #srguments stored in .args
                                    print inst #_str_ allows args tto be printed directly
                                    print "========================================================================================"
                            #***************************************************************************************
                            #Looking for DONE command
                            #***************************************************************************************
                            elif(analysisString[0:3] == "DONE"): #looking for DONE Command
                                print "Command Type: DONE"
                                print " "
                                print "Function Not Yet Completed, Thinking I might make this issue the done command to all clients"
                                print " "
                            #***************************************************************************************
                            #Command is unknown
                            #***************************************************************************************
                            else: #command is unknown
                                print "WARNING: Received Unknown Command From Controller:" + analysisString
                                print "INFO: Unknown Command is being ignored"
                        print "STATUS: Clearing listOfControllerMessages..."
                        del self.listOfControllerMessages[:]
                        print "STATUS: listOfControllerMessages has been cleared"
                    except Exception as inst:
                        print "========================================================================================"
                        print "ERROR: An exception has been thrown in the Distribute command to clients Try Block"
                        print type(inst) #the exception instance
                        print inst.args #srguments stored in .args
                        print inst #_str_ allows args tto be printed directly
                        print "========================================================================================"

                    #/////////////////////////////////////////////////////////////////////////////////
                    #Check to see if another client is trying to connect
                    #/////////////////////////////////////////////////////////////////////////////////
                    try: #check to see if another client is trying to connect try block
                        print "STATUS: Checking to see if another client is trying to connect..."
                        self.serverSocket.settimeout(2.0)
                        sock, addr =self.serverSocket.accept()
                        print "INFO: Connected with " + addr[0] + ":" + str(addr[1])
                        self.listOfClients.append((sock, addr))
                        print "INFO: Client successfully added to the list of clients"
                        print str(len(self.listOfClients)) + " Client(s) are currently Connected."
                        self.dictionaryOfCurrentClientTasks[addr] = "" #Client has no task currently, so value is the empty string
                        print "STATUS: Client was successfully added to the Dictionary of Current Client Tasks"
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
                #..................................................................................
                #END OF MAIN SERVER LOOP
                #..................................................................................
            except Exception as inst: #Exception for Server Primary While Loop Try Block
                print "========================================================================================"
                print "ERROR: An exception has been thrown in the Server Primary While Loop Try Block"
                print type(inst) #the exception instance
                print inst.args #srguments stored in .args
                print inst #_str_ allows args tto be printed directly
                print "========================================================================================"
            finally:
                print "Closing the socket..."
                self.serverSocket.close()
                print "Socket has been closed"
                for x in range(0, len(self.listOfClients)):
                    (sock, addr) = self.listOfClients[x]
                    sock.sendall("DONE")
                    print "STATUS: Issued the DONE command to client: " + str(addr)
                try:
                    print " "
                    print "Printing List of Crashed Clients"
                    print "---------------------------------"
                    if(len(self.listOfCrashedClients) < 1):
                        print "No Clients Crashed During This Session"
                    else:
                        for x in range(0, len(self.listOfCrashedClients)):
                            print str(x) + ") " + str(self.listOfCrashedClients[x]) + " reported a Crash"
                    print "---------------------------------"
                except Exception as inst:
                    print "========================================================================================"
                    print "ERROR: An exception has been thrown in the Finally Block, in the print List of Crash Clients Section"
                    print type(inst) #the exception instance
                    print inst.args #srguments stored in .args
                    print inst #_str_ allows args tto be printed directly
                    print "========================================================================================"
                try:
                    print " "
                    print "Printing Dictionary Of Clients Waiting For A Reply"
                    print "--------------------------------------------------"
                    if(len(self.dictionaryOfClientsWaitingForAReply) < 1):
                        print "No Clients Are Waiting For A Reply When The Session Ended"
                    else:
                        for key, value in self.dictionaryOfClientsWaitingForAReply.iteritems():
                            print "[" + key + "] =" + value
                    print "--------------------------------"
                except Exception as inst:
                    print "========================================================================================"
                    print "ERROR: An exception has been thrown in the Finally Block, in the print Dictionary of Clients Waiting For A Reply Section"
                    print type(inst) #the exception instance
                    print inst.args #srguments stored in .args
                    print inst #_str_ allows args tto be printed directly
                    print "========================================================================================"
                print " "
            #--------------------------------------------------------------------------------
            #End of Constructor Block
            #--------------------------------------------------------------------------------

        #=================================================================================================
        #SERVER-CONTROLLER COMMUNICATION FUNCTIONS
        #This section contains methods that the server will use to communicate with the controller class
        #=================================================================================================
        #------------------------------------------------------------------------------
        #Outbound communication with Controller
        #------------------------------------------------------------------------------
        #..............................................................................
        #nextChunk
        #..............................................................................
        def sendNextChunkCommandToController(self, clientIP):
            try:
                self.pipe.send("nextChunk " + clientIP)
                print "The NEXTCHUNK command was sent to the Controller"
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
        #..............................................................................
        #chunkAgain
        #..............................................................................
        def sendChunkAgainCommandToController(self):
            try:
                self.pipe.send("chunkAgain")
                print "The CHUNKAGAIN command was sent to the Controller"
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
        #..............................................................................
        #waiting
        #..............................................................................
        def sendWaitingCommandToController(self):
            try:
                self.pipe.send("waiting")
                print "The WAITING command was sent to the Controller"
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
        #..............................................................................
        #done
        #..............................................................................
        def sendDoneCommandToController(self, clientIP):
            try:
                self.pipe.send("done " + clientIP)
                print "The DONE command was sent to the Controller"
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
        #------------------------------------------------------------------------------
        #Inbound communication with controller
        #------------------------------------------------------------------------------
        #..............................................................................
        #REPLY OT NEXTCHUNK
        #..............................................................................
        def checkForNextChunk(self,inboundString): #check to see if the string contains the next chunk of the problem
            try:
                print "STATUS: Checking to see if inboundString is the next part of problem..."
                if(len(inboundString) < 1):
                    return False
                if(inboundString[0:8] == "NEXTCHUNK"):
                    #position 9 will be a space
                    print "INFO: NEXTCHUNK command was received from the controller class"
                    self.listOfControllerMessages.append(str(inboundString))
                    print "INFO: NEXTCHUNK command was added to the listOfControllerMessages"
                    return True
                # if(inboundString[0] == "N"): #OLD METHOD
                 #       if(inboundString[1] == "E"):
                  #          if(inboundString[2] == "X"):
                   #             if(inboundString[3] == "T"):
                    #                if(inboundString[4] == "C"):
                     #                   if(inboundString[5] == "H"):
                      #                      if(inboundString[6] == "U"):
                       #                         if(inboundString[7] == "N"):
                        #                            if(inboundString[8] == "K"):
                         #                               #position 9 will be a space
                          #                              print "INFO: NEXTCHUNK command was received from the controller class"
                           #                             self.listOfControllerMessages.append(str(inboundString))
                            #                            print "INFO: NEXTCHUNK command was added to the listOfControllerMessages"
                             #                           return True
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
        #..............................................................................
        #REPLY TO CHUNKAGAIN
        #..............................................................................
        def checkForChunkAgain(self,inboundString): #check to see if the string contains that chunk that was requested
            try:
                print "Checking to see if inboundString is the requested chunk (chunkAgain)..."
                if(len(inboundString) < 1):
                    return False
                if(inboundString[0:9] == "CHUNKAGAIN"):
                    #position 10 will be a space
                    print "INFO: CHUNKAGAIN command was received from the controller class"
                    self.listOfControllerMessages.append(str(inboundString))
                    print "INFO: CHUNKAGAIN command was added to the listOfControllerMessages"
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
        #..............................................................................
        #REPLY TO DONE
        #..............................................................................
        def checkForFound(self,inboundString): #checks to see if the inboundString says it found the key (or if it didnt)
            try:
                print "STATUS: Checking to see if the key was found..."
                if(len(inboundString) < 1):
                    return False
                if(inboundString[0:4] == "Found"):
                    print "INFO: The Controller Says that the key has been Found"
                    print " "
                    print "This section of the code is NOT FINISHED YET"
                    print " -Need To Issue Done Command To All CLients at this point"
                    return True
                elif(inboundString[0:7] == "notFound"):
                    print "INFO: The Controller says that the key has no been found yet"
                    print " "
                    print "This Section of the code is NOT FINISHED YET"
                    print " -Need to tell client that no solution was found, request for the next chunk"
                    return True
                else:
                    return False
               # if(inboundString=="Found"): #OLD METHOD
                #    print "The Controller says that the key has been Found"
                 #   return True
               # elif(inboundString=="notFound"):
                #    return False
              #  else:
              #      print "==================================================="
               #     print "ERROR: Invalid input from the Controller class"
               #     print "The Invalid input: '" + inboundString + "'"
                #    print "==================================================="
                #    return False
            except Exception as inst:
                print "============================================================================================="
                print "ERROR: An exception was thrown in the Server-Controller Inbound checkForFound Try Block"
                #the exception instance
                print type(inst)
                #srguments stored in .args
                print inst.args
                #_str_ allows args tto be printed directly
                print inst
                print "============================================================================================="

    #=================================================================================================
    #SERVER-CLIENT COMMUNICATION FUNCTIONS
    #This section contains methods used by the server to communicate with the clients
    #=================================================================================================
        #------------------------------------------------------------------------------
        #Outbound communication functions
        #------------------------------------------------------------------------------
        #..............................................................................
        #DONE
        #..............................................................................
        def sendDoneCommandToClient(recipientsSocket, recipientIPAddress): #sends the DONE command to a client
            try:
                recipientsSocket.sendto("DONE", recipientIPAddress)
                print "The DONE command was issued to: " + str(recipientIPAddress)
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
        #..............................................................................
        #next part in cracking problem
        #..............................................................................
        def sendNextToClient(recipientsSocket, recipientIPAddress, theNextPart): #sends the next part of problem to the client
            try:
                recipientsSocket.sendto(theNextPart, recipientIPAddress)
                print "The next part of the problem was sent to: " + str(recipientIPAddress)
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
        #..............................................................................
        #INVALIDCOMMAND (No longer used, Error is thrown instead)
        #..............................................................................
        '''def sendInvalidCommandToClient(recipientsSocket, recipientIPAddress): #send the INVALIDCOMMAND String to the client
            try:
                recipientsSocket.sendto("INVALIDCOMMAND", recipientIPAddress)
                print "The INVALIDINPUT command was issued to: " + str(recipientIPAddress)
            except Exception as inst:
                print "============================================================================================="
                print "ERROR: An exception was thrown in the SServer-Client Outbound sendInvalidCommand Try Block"
                #the exception instance
                print type(inst)
                #srguments stored in .args
                print inst.args
                #_str_ allows args tto be printed directly
                print inst
                print "=============================================================================================" '''
        #------------------------------------------------------------------------------
        #Inbound communication functions
        #------------------------------------------------------------------------------
        #..............................................................................
        #NEXT
        #..............................................................................
        def checkForNextCommand(self,inboundString): #checks for the NEXT command
            try:
                if(inboundString[0:3] == "NEXT"):
                    print "A Client has issued the NEXT command"
                    #position 4 is a space
                    tempIP= ""
                    for i in range(5, len(inboundString)):
                        tempIP= tempIP + inboundString[i]
                    self.dictionaryOfClientsWaitingForAReply[tempIP] = "NEXTCHUNK"
                    print "INFO: Client (" + str(tempIP) + ") was added the dictionaryOfClientsWaitingForAReply"
                    return True
               # if(inboundString[0]=="N"): #OLD METHOD
                #    if(inboundString[1]=="E"):
                 #       if(inboundString[2]=="X"):
                  #          if(inboundString[3]=="T"):
                   #             print "A Client has issued the NEXT command"
                    #            #position 4 is a space
                     #           tempIP= ""
                      #          for i in range(5, len(inboundString)):
                       #             tempIP= tempIP + inboundString[i]
                        #        self.dictionaryOfClientsWaitingForAReply[tempIP] = "NEXTCHUNK"
                         #       print "INFO: Client (" + str(tempIP) + ") was added the dictionaryOfClientsWaitingForAReply"
                          #      return True
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
        #..............................................................................
        #FOUNDSOLUTION
        #..............................................................................
        def checkForFoundSolutionCommand(self,inboundString): #checks for the "FOUNDSOLUTION" string
            try:
                if(inboundString[0:12] == "FOUNDSOLUTION"):
                    print "A Client has issued the FOUNDSOLUTION command"
                    #position 13 is a space
                    tempIP= ""
                    for i in range(14, len(inboundString)):
                        tempIP= tempIP + inboundString[i]
                    self.dictionaryOfClientsWaitingForAReply[tempIP] = "FOUNDSOLUTION"
                    print "INFO: Client (" + str(tempIP) + ") was added to the dictionaryOfClientsWaitingForAReply"
                    return True
               # if(inboundString[0]=="F"): #OLD METHOD
                #    if(inboundString[1]=="O"):
                 #       if(inboundString[2]=="U"):
                  #          if(inboundString[3]=="N"):
                   #             if(inboundString[4]=="D"):
                    #                if(inboundString[5]=="S"):
                     #                   if(inboundString[6]=="O"):
                      #                      if(inboundString[7]=="L"):
                       #                         if(inboundString[8]=="U"):
                        #                            if(inboundString[9]=="T"):
                         #                               if(inboundString[10]=="I"):
                          #                                  if(inboundString[11]=="O"):
                           #                                     if(inboundString[12]=="N"):
                            #                                        print "A Client has issued the FOUNDSOLUTION command"
                             #                                       #position 13 is a space
                              #                                      tempIP= ""
                               #                                     for i in range(14, len(inboundString)):
                                #                                        tempIP= tempIP + inboundString[i]
                                 #                                   self.dictionaryOfClientsWaitingForAReply[tempIP] = "FOUNDSOLUTION"
                                  #                                  print "INFO: Client (" + str(tempIP) + ") was added to the dictionaryOfClientsWaitingForAReply"
                                   #                                 return True
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
        #..............................................................................
        #CRASHED
        #..............................................................................
        def checkForCrashedCommand(self,inboundString): #checks for the "CRASHED" Command
            try:
                if(len(inboundString) < 1):
                    print "INFO: Empty Crashed Message Received."
                    return False
                if(inboundString[0:6] == "CRASHED"):
                    tempCrashIP = ""
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
                            break
                        else:
                            print "INFO: No Match found yet. " + str(tempCrashIP) + " != " + str(tempAddr2)

                    if(foundMatch == False):
                        print "WARNING: No Matching IP address was found in the list of clients"
                        print "INFO: Unable to Find the Crashed IP: " +str(tempCrashIP) + " "
                    return True
                else:
                    return False
                #if(inboundString[0]=="C"): #OLD METHOD
                 #   if(inboundString[1]=="R"):
                  #      if(inboundString[2]=="A"):
                   #         if(inboundString[3]=="S"):
                     #           if(inboundString[4]=="H"):
                    #                if(inboundString[5]=="E"):
                      #                  if(inboundString[6]=="D"):
                       #                     tempCrashIP = ""
                        #                    #position 7 is a space between the ip address and the crashed message
                         #                   for i in range(8, len(inboundString)):
                          #                      if(inboundString[i].isalpha()):
                           #                         print "WARNING: A Non-Numeral Value Was Detected In The Ip Address, Ignoring Remainder of String"
                            #                        break
                             #                   else:
                              #                      tempCrashIP = tempCrashIP + inboundString[i]
                               #             if(len(tempCrashIP) < 1): #if the length is less than one, stop performing an IP check
                                #                return False
                                 #           print "WARNING: A Client has issued the CRASHED command"
                                  #          print "The Crashed Client IP: " + tempCrashIP
                                   #         self.listOfCrashedClients.append(tempCrashIP)
                                    #        print "INFO: The crashed client's IP address has been added to the listOfCrashedClients"
                                     #       #look through listOfConnected clients and find the matching ip address
                                      #      print "STATUS: Looking for matching IP address in list of clients..."
                                       #     foundMatch= False
                                        #    tempAddr2= ""
                                         #   for index in range(0, len(self.listOfClients)):
                                          #      tempSock, tempAddr= self.listOfClients[index] #get socket and ip address of client
                                           #     print "STATUS: Copying list of clients' IP Address to a new string"
                                            #    tempAddr2= str(tempAddr[0])
                                             #   print "STATUS: Comparing IP Addresses..."
                                              #  if(tempCrashIP == tempAddr2):
                                               #     print "INFO: Matching IP address was found in the list of clients"
                                                #    #print "DEBUG: tempAddr=" + str(tempAddr)
                                                 #   del self.listOfClients[index]
                                                  #  print "INFO: The crashed client " + str(tempAddr) + " was removed from the list of clients"
                                                   # foundMatch= True
                                                    #break
                                          #      else:
                                           #         print "INFO: No Match found yet. " + str(tempCrashIP) + " != " + str(tempAddr2)
#
 #                                           if(foundMatch == False):
  #                                              print "WARNING: No Matching IP address was found in the list of clients"
   #                                             print "INFO: Unable to Find the Crashed IP: " +str(tempCrashIP) + " "
    #                                        return True
     #                                   else:
      #                                      return False
       #                             else:
        #                                return False
         #                       else:
          #                          return False
           #                 else:
            #                    return False
             #           else:
              #              return False
               #     else:
                #else:
                  #  return False
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

    #==================================================================================================
    #CHUNK PARSING FUNCTIONS
    #==================================================================================================
        #-------------------------------------------------------------------------------------------------
        #Determine the method being used (bruteforce,dictionary,rainbowmaker,rainbowuser)
        #-------------------------------------------------------------------------------------------------

        #-------------------------------------------------------------------------------------------------
        #Determine the algorithm being used (md5,sha1,sha256,sha512)
        #-------------------------------------------------------------------------------------------------

        #-------------------------------------------------------------------------------------------------
        #Obtain the hash code
        #-------------------------------------------------------------------------------------------------

        #-------------------------------------------------------------------------------------------------
        #Determine the Alphabet Choice (a,A,m,M,d)
        #-------------------------------------------------------------------------------------------------

        #-------------------------------------------------------------------------------------------------
        #Determine the minCharacters (1,10,16)
        #-------------------------------------------------------------------------------------------------

        #-------------------------------------------------------------------------------------------------
        #Determine the maxCharacters (1,10,16)
        #-------------------------------------------------------------------------------------------------

        #-------------------------------------------------------------------------------------------------
        #Determine the Prefix (adf,234,qw3#k)
        #-------------------------------------------------------------------------------------------------

        #-------------------------------------------------------------------------------------------------
        #Determine the File Location (0,1213,23665)
        #-------------------------------------------------------------------------------------------------

        #-------------------------------------------------------------------------------------------------
        #Determine the Width (1,100,100000)
        #-------------------------------------------------------------------------------------------------

        #-------------------------------------------------------------------------------------------------
        #Determine the Height (1,100,10000)
        #-------------------------------------------------------------------------------------------------

