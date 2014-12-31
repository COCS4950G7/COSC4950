__author__ = 'Chris Hamm'
#NetworkServer_r9A
#Created: 12/30/2014

#THIS VERSION ATTEMPTS TO IMPLEMENT A LINUX IP ADDRESS DETECTION

#This is a restructured version of r7A.
#This is modelled after rBugg version

import socket
import platform
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

        #constructor
        def __init__(self, pipeendconnectedtocontroller):
            self.pipe= pipeendconnectedtocontroller

            #socket.AF_INET is a socket address family represented as a pair. (hostname, port). This is the default parameter
            #socket.SOCK_STREAM is the default parameter. This defines the socket type
            self.serverSocket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print "STATUS: Server socket created successfully"

            #Bind the socket to local host and port
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

            try: #getIP tryblock
                print "STATUS: Getting your network IP adddress"
                print "The server's IP address is (THIS MAY NOT WORK ON ALL OS's!): "
                print "(NOTE: This function works on Windows 7)"
                print "(NOTE: This function works on OS X)"
                if(platform.system()=="Windows"):
                    print socket.gethostbyname(socket.gethostname())
                elif(platform.system()=="Linux"):
                    socket.connect(('google.com',0))
                    print socket.getsockname()[0]
                elif(platform.system()=="Darwin"):
                    print socket.gethostbyname(socket.gethostname())
                else:
                    print socket.gethostbyname(socket.gethostname())
            except Exception as inst:
                print "========================================================================================"
                print "ERROR: An exception was thrown in getIP try block"
                print type(inst) #the exception instance
                print inst.args #srguments stored in .args
                print inst #_str_ allows args tto be printed directly
                print "========================================================================================"

            #Start listening to socket
            self.serverSocket.listen(5)
            print "Waiting for initial client to connect..."

            #Waiting for initial Client to connect
            sock, addr= self.serverSocket.accept()
            print "INFO: First client has connected"
            print "INFO: Connected with " + addr[0] + ":" + str(addr[1])
            self.listOfClients.append((sock, addr)) #add the tuple to the list of clients
            print "STATUS: Client successfully added to the list of clients"
            #print str(len(self.listOfClients)) + " Client(s) are currently Connected."

            #Server PRIMARY WHILE LOOP
            try: #server primary while loop try block
                while(self.serverIsRunning==True): #server primary while loop

                    #Check for input from clients
                    print "STATUS: Checking for input from client(s)..."
                    try: #check for client input try block
                        sock.settimeout(2.0)
                        theInput = sock.recv(2048) #listening for input
                        print "INFO: Received a message from a client."
                        if(self.checkForNextCommand(theInput)==True):
                            print "INFO: NEXT command was received"
                        elif(self.checkForFoundSolutionCommand(theInput)==True):
                            print "INFO: FOUNDSOLUTION command was received"
                        elif(self.checkForCrashedCommand(theInput)==True):
                            print "INFO: CRASHED command was received"
                        #elif(self.checkForInvalidCommand(theInput)==True):
                         #   print "INVALIDINPUT command received"
                        elif(self.checkForAltCrashCommand(theInput)==True):
                            print "INFO: ALT CRASH COMMAND received"
                        else:
                            print "ERROR: unknown command received"
                            print "The unknown command: '" + theInput + "'"

                    except socket.timeout as inst:
                        print "STATUS: Socket has timed out. No input from client detected."
                    except Exception as inst:
                        print "========================================================================================"
                        print "ERROR: An exception has been thrown in the Check for client input Try Block"
                        print type(inst) #the exception instance
                        print inst.args #srguments stored in .args
                        print inst #_str_ allows args tto be printed directly
                        print "========================================================================================"

                    #Check for input from controller class
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

                    #Distribute command to clients if needed
                    try: #distribute command try block
                        print "STATUS: Checking to see if a command needs to be send to the clients..."
                    except Exception as inst:
                        print "========================================================================================"
                        print "ERROR: An exception has been thrown in the Distribute command to clients Try Block"
                        print type(inst) #the exception instance
                        print inst.args #srguments stored in .args
                        print inst #_str_ allows args tto be printed directly
                        print "========================================================================================"

                    #Check to see if another client is trying to connect
                    try: #check to see if another client is trying to connect try block
                        print "STATUS: Checking to see if another client is trying to connect..."
                        self.serverSocket.settimeout(2.0)
                        sock, addr =self.serverSocket.accept()
                        print "INFO: Connected with " + addr[0] + ":" + str(addr[1])
                        self.listOfClients.append((sock, addr))
                        print "INFO: Client successfully added to the list of clients"
                        print str(len(self.listOfClients)) + " Client(s) are currently Connected."
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
                #END OF MAIN SERVER LOOP
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
                   # print "Before sending the DONE command"
                   # try:
                   #     self.sendDoneCommandToClient(sock,addr)
                   #     print "Sent DONE command to: " + str(addr)
                   # except Exception as inst:
                   #     print "========================================================================================"
                   #     print "ERROR: An exception has been thrown in the Finally block, sendDoneCommandToServer Try Block"
                   #     print type(inst) #the exception instance
                   #     print inst.args #srguments stored in .args
                   #     print inst #_str_ allows args tto be printed directly
                   #     print "========================================================================================"

            #End of Constructor Block

        #=================================================================================================
        #SERVER-CONTROLLER COMMUNICATION FUNCTIONS
        #This section contains methods that the server will use to communicate with the controller class
        #=================================================================================================
        #Outbound communication with Controller
            #nextChunk
        def sendNextChunkCommandToController(self):
            try:
                self.pipe.send("nextChunk")
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

            #chunkAgain
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

            #waiting
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

            #done
        def sendDoneCommandToController(self):
            try:
                self.pipe.send("done")
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

        #Inbound communication with controller
            #REPLY OT NEXTCHUNK
        def checkForNextChunk(self,inboundString): #check to see if the string contains the next chunk of the problem
            try:
                print "Checking to see if inboundString is the next part of problem..."
                print "The function for this is not finished yet"
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

            #REPLY TO CHUNKAGAIN
        def checkForChunkAgain(self,inboundString): #check to see if the string contains that chunk that was requested
            try:
                print "Checking to see if inboundString is the requested chunk (chunkAgain)..."
                print "The function for this is not finished"
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

            #REPLY TO DONE
        def checkForFound(self,inboundString): #checks to see if the inboundString says it found the key (or if it didnt)
            try:
                print "Checking to see if the key was found..."
                print "The function for this is not finished"
                if(inboundString=="Found"):
                    print "The Controller says that the key has been Found"
                    return True
                elif(inboundString=="notFound"):
                    return False
                else:
                    print "==================================================="
                    print "ERROR: Invalid input from the Controller class"
                    print "The Invalid input: '" + inboundString + "'"
                    print "==================================================="
                    return False
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
        #Outbound communication functions
            #DONE
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

            #next part in cracking problem
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

            #INVALIDCOMMAND
        def sendInvalidCommandToClient(recipientsSocket, recipientIPAddress): #send the INVALIDCOMMAND String to the client
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
                print "============================================================================================="

        #Inbound communication functions
            #NEXT
        def checkForNextCommand(self,inboundString): #checks for the NEXT command
            try:
                if(inboundString=="NEXT"):
                    print "A Client has issued the NEXT command"
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

            #FOUNDSOLUTION
        def checkForFoundSolutionCommand(self,inboundString): #checks for the "FOUNDSOLUTION" string
            try:
                if(inboundString=="FOUNDSOLUTION"):
                    print "A Client has issued the FOUNDSOLUTION command"
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

            #CRASHED
        def checkForCrashedCommand(self,inboundString): #checks for the "CRASHED" Command
            try:
                if(inboundString=="CRASHED"):
                    print "WARNING: A Client has issued the CRASHED command"
                    return True
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

            #INVALIDCOMMAND
                '''
        def checkForInvalidCommand(self,inboundString): #checks for the "INVALIDCOMMAND" string
            try:
                if(inboundString=="INVALIDCOMMAND"):
                    print "ERROR: A Client has issued the INVALIDCOMMAND command"
                    return True
                else:
                    return False
            except Exception as inst:
                print "============================================================================================="
                print "ERROR: An exception was thrown in the Server-Client Inbound checkForInvalidCommand Try Block"
                #the exception instance
                print type(inst)
                #srguments stored in .args
                print inst.args
                #_str_ allows args tto be printed directly
                print inst
                print "============================================================================================="
                '''

            #ALT Crash Command
        def checkForAltCrashCommand(self, inboundString): #checks for the " " string
            try:
                if(inboundString==""):
                    print "WARNING: A Client has issued the ALT CRASH COMMAND"
                    return True
                else:
                    return False
            except Exception as inst:
                print "============================================================================================="
                print "ERROR: An exception was thrown in the Server-Client Inbound checkForAltCrashCommand Try Block"
                #the exception instance
                print type(inst)
                #srguments stored in .args
                print inst.args
                #_str_ allows args tto be printed directly
                print inst
                print "============================================================================================="

