__author__ = 'chris hamm'
#NetworkClient_rX (revision 10)
#Created: 1/27/2015
#Designed to work with NetworkServer_rX

#THINGS ADDED/CHANGED WITH THIS REVISION
    #(Implemented)Removed Chunk Parsing Functions (That are now no longer needed)
    #(Implemented)Removed Main Client Loop
    #(Implemented)Restructure the the Primary While Loop so that when a command is received from either server or controller, the client immeadiately responds to that command (instead of queuing up the commands and executing them one by one)
    #(Implemented)Added a record that records the number of reply to nextchunk the client receives from server
    #(Implemented)Revised the check for server command system
    #(Implemented)Added a record for the number of unknown commands the client receives from controller and from server
    #(Implemented)Added a new communication command for the client to send the next chunk to the controller
    #(Implemented)Added in function to expect a second string from the server after client receives the nextChunk command
    #(Implemented)Added check for FOUNDSOLUTION function for inbound controller messages
    #(Implemented)Added check for requestNextChunk function for inbound controller messages
    #TEMPORARY Added support for legacy command 'next' from the controller
    #TEMPORARY Added support for the legacy command "found"
    #(Implemented)(OBSOLETE)Increased the recv buffer size for recv data from the server
    #(Implemented)Added an extractor for the the second keyword in the nextChunk Command, which is the size of the data in the chunk object
    #(Implemented)Changed the check for foundSolution function so that it checks char by char instead of by the string
    #(Implemented)send the doingStuff command to controller prior to sending the chunk
    #(Implemented)Added a check for doing stuff command (for inbpund command from controller) and also added a record for the command
    #(Implemented)Removed the keywords from the params object before sending it to the controller

#=================================
#Imports
#=================================
import socket
import platform
import Chunk
#=================================
#End of Imports
#=================================

#================================================================
#NetworkClient Class Definition
#================================================================
class NetworkClient():
    #-------------------------------------------------------------------
    #NetworkClient Class Variables
    #-------------------------------------------------------------------
    pipe = 0
    port = 49200
    clientSocket = 0
    serverSaysKeepSearching = True
    serverIssuedDoneCommand = False
    serverIP = "127.0.1.1"
    myOperatingSystem = None
    myIPAddress = "127.0.1.1"
    chunk = Chunk.Chunk()
    key = 0
    recordOfOutboundCommandsFromClientToController = {} #dictionary that keeps a record of how many commands were sent to the controller
    recordOfOutboundCommandsFromClientToServer = {} #dictionary that keeps a record of how many commands were sent to the server
    recordOfInboundCommandsFromController = {} #dictionary that keeps a record of how many commands were received from the controller
    recordOfInboundCommandsFromServer = {} #dictionary that keeps a record of how many commands were received from the server
    #-------------------------------------------------------------------
    #End of NetworkClient Class Variables
    #-------------------------------------------------------------------

    #-------------------------------------------------------------------
    #NetworkClient Class Constructor
    #-------------------------------------------------------------------
    def __init__(self, pipeendconnectedtocontroller):
        self.pipe = pipeendconnectedtocontroller
        #........................................................................
        #Create Socket
        #........................................................................
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print "STATUS: client socket created successfully"
        #........................................................................
        #End of Create Socket
        #........................................................................

        #........................................................................
        #Detect the Operating System
        #........................................................................
        try:
            print "*************************************"
            print "    Network Client"
            print "*************************************"
            print "OS DETECTION:"

            #Detecting Windows
            if platform.system() == "Windows":
                print platform.system()
                self.myOperatingSystem = "Windows"
                print platform.win32_ver()

            #Detecting GNU/Linux
            elif platform.system() == "Linux":
                print platform.system()
                self.myOperatingSystem = "Linux"
                print platform.dist()

            #Detecting OSX
            elif platform.system() == "Darwin":
                print platform.system()
                self.myOperatingSystem = "Darwin"
                print platform.mac_ver()

            #Detecting an OS that is not listed
            else:
                print platform.system()
                self.myOperatingSystem = "Other"
                print platform.version()
                print platform.release()

            print "*************************************"

        except Exception as inst:
            print "========================================================================================"
            print "ERROR: An exception was thrown in getOS try block"
            #the exception instance
            print type(inst)
            #arguments stored in .args
            print inst.args
            #_str_ allows args to be printed directly
            print inst
            print "========================================================================================"
        #........................................................................
        #End of Detect the Operating System
        #........................................................................

        #........................................................................
        #Retreive the local network IP Address
        #........................................................................
        try: #get client IP try block
            print "STATUS: Getting your Network IP address"
            if(platform.system()=="Windows"):
                self.myIPAddress = socket.gethostbyname(socket.gethostname())
                print "My IP Address: " + str(self.myIPAddress)
            elif(platform.system()=="Linux"):
                import fcntl
                import struct
                import os

                def get_interface_ip(ifname):
                    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', ifname[:15]))[20:24])
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
                self.myIPAddress = get_lan_ip()
                print "My IP Address: " + str(self.myIPAddress)
            elif(platform.system()=="Darwin"):
                self.myIPAddress= socket.gethostbyname(socket.gethostname())
                print "My IP Address: " + str(self.myIPAddress)
            else:
                #NOTE MAY REMOVE  THIS AND USE THE LINUX IP DETECTION METHOD FOR THIS IN THE FUTURE
                print "INFO: The system has detected that you are not running Windows, OS X, or Linux."
                print "INFO: Using generic IP address retrieval method"
                self.myIPAddress = socket.gethostbyname(socket.gethostname())
                print "My IP Address: " + str(self.myIPAddress)
        except Exception as inst:
            print "========================================================================================"
            print "ERROR: An exception was thrown in get client IP try block"
            print type(inst)
            print inst.args
            print inst
            print "========================================================================================"
        #........................................................................
        #End of Retreive the local network IP Address
        #........................................................................

        #........................................................................
        #Initialize the Record Counters
        #........................................................................
        self.recordOfOutboundCommandsFromClientToController['done'] = 0
        self.recordOfOutboundCommandsFromClientToController['connected'] = 0
        self.recordOfOutboundCommandsFromClientToController['doingStuff'] = 0
        self.recordOfOutboundCommandsFromClientToController['nextChunk'] = 0
        self.recordOfOutboundCommandsFromClientToServer['NEXT'] = 0
        self.recordOfOutboundCommandsFromClientToServer['FOUNDSOLUTION'] = 0
        self.recordOfOutboundCommandsFromClientToServer['CRASHED'] = 0
        self.recordOfInboundCommandsFromController['serverIP'] = 0
        self.recordOfInboundCommandsFromController['FOUNDSOLUTION'] = 0
        self.recordOfInboundCommandsFromController['REQUESTNEXTCHUNK'] = 0
        self.recordOfInboundCommandsFromController['doingStuff'] = 0
        self.recordOfInboundCommandsFromController['Unknown'] = 0
        self.recordOfInboundCommandsFromServer['DONE'] = 0
        self.recordOfInboundCommandsFromServer['REPLY_TO_NEXTCHUNK'] = 0
        self.recordOfInboundCommandsFromServer['NEXTCHUNKDATA'] = 0
        self.recordOfInboundCommandsFromServer['Unknown'] = 0
        #........................................................................
        #End of Initialize the Record Counters
        #........................................................................

        #........................................................................
        #Retreive the Server's IP Address from the Controller Class
        #........................................................................
        try:  #get serverIP try block
            print "STATUS: Attempting to get serverIP from controller"
            self.receiveServerIPFromController()
            print "STATUS: Successfully received serverIP from controller"
        except Exception as inst:
            print "========================================================================================"
            print "ERROR: An exception was thrown in serverIP try block"
            #the exception instance
            print type(inst)
            #arguments stored in .args
            print inst.args
            #_str_ allows args to be printed directly
            print inst
            print "========================================================================================"
        #........................................................................
        #End of Retreive the Server's IP Address from the Controller Class
        #........................................................................

        #........................................................................
        #Connect to the server
        #........................................................................
        try:
            print "STATUS: Attempting to connect to server"
            self.clientSocket.connect((self.serverIP, self.port))
            print "STATUS: Successfully connected to server"

        except socket.timeout as msg:
            print "========================================================================================"
            print "ERROR: the connection has timed out. Check to see if you entered the correct IP Address."
            print "Error code: " + str(msg[0]) + " Message: " + msg[1]
            print "Socket timeout set to: " + self.clientSocket.gettimeout + " seconds"
            print "========================================================================================"
        except socket.error as msg:
            print "========================================================================================"
            print "ERROR: Failed to connect to server"
            print "Error code: " + str(msg[0]) + " Message: " + msg[1]
            raise Exception("Failed to connect to server")
            print "========================================================================================"
        #........................................................................
        #End of Connect to the server
        #........................................................................

        #........................................................................
        #Send Connected command to the Controller
        #........................................................................
        self.sendConnectedCommandToCOntroller()
        #........................................................................
        #End of Send the Connected Command to the Controller
        #........................................................................

        #........................................................................
        #Start of Client Primary While Loop
        #........................................................................
        try:
                while self.serverSaysKeepSearching:
                    #self.clientSocket.settimeout(2.0) #MOVED BELOW
            #///////////////////////////////////////////////////////////////////////////
            #Check for Server Commands
            #///////////////////////////////////////////////////////////////////////////
            #'''GOAL: Want to have client respond immeadiately when it receives a command from server'''
                    try: #checking for server commands try block
                        print "STATUS: Checking for server commands..."
                        self.clientSocket.settimeout(0.25)
                        theInput = self.clientSocket.recv(2048)
                        if(len(theInput) > 1):
                            #if theInput == "DONE": #OLD METHOD
                            if(self.checkForDoneCommand(theInput)==True):
                                print "INFO: Received DONE Command from the server"
                                self.sendDoneCommandToController()
                                print " "
                                print "INFO: Server has issued the DONE command."
                                print " "
                                self.serverSaysKeepSearching = False
                                self.serverIssuedDoneCommand = True
                                break
                            #If the server wants to give us the next chunk, take it
                            #Server should be sending "NEXT" -> params -> data in seperate strings all to us
                            elif(self.checkForNextCommand(theInput)==True):
                                try:
                                    print "INFO: Received the NextChunk from the Server"
                                    #print "DEBUG: theInput:" + str(theInput)
                                    print "STATUS: Extracting chunk data file size from nextChunk Command..."
                                    #position[0:4] = 'NEXT '
                                    #position[5:9] = 'SIZE('
                                    #end of file size is marked by the closing parenthesis
                                    dataChunkFileSize = ""
                                    closingParenthesisLocation = 0
                                    for x in range(10,len(theInput)):
                                        if(theInput[x] == ")"):
                                            #print "DEBUG: closing parenthesis for dataChunkFileSize found at pos:" + str(x)
                                            closingParenthesisLocation= x
                                            break
                                        else:
                                            dataChunkFileSize+= str(theInput[x])
                                    print "INFO: the dataChunkFileSize is " + str(dataChunkFileSize) + " bytes"
                                    print "STATUS: Finished extracting dataChunkFileSize"
                                    print "STATUS: Removing keywords from params..."
                                    theInput= theInput[(closingParenthesisLocation+2):len(theInput)] #remove space after closing parenthesis as well as the keywords
                                    print "DEBUG: theInput after removing keywords:" + str(theInput)
                                    print "INFO: Finished removing keywords"
                                    print "STATUS: Waiting for the corresponding data from the server"
                                    tempData= "" #declare the variable
                                    try: #receive corresponding data from the server try block
                                        #tempData = self.clientSocket.recv(268435456) #2^28 #OLD METHOD
                                        tempData= self.clientSocket.recv((int(dataChunkFileSize)*10)) #set recv buffer equal to the size of the data object
                                        print "INFO: Received data from the server."
                                        #print "DEBUG: tempData=" + str(tempData)
                                        self.recordOfInboundCommandsFromServer['NEXTCHUNKDATA'] = (self.recordOfInboundCommandsFromServer['NEXTCHUNKDATA'] + 1)
                                    except Exception as inst:
                                        print "============================================================================================="
                                        print "ERROR: An exception was thrown in the receive corresponding data from the server Try Block"
                                        #the exception instance
                                        print type(inst)
                                        #srguments stored in .args
                                        print inst.args
                                        #_str_ allows args tto be printed directly
                                        print inst
                                        print "============================================================================================="
                                    #print "STATUS: Removing the NEXT keyword from the message..." #THE FUNCTION ABOVE PERFORMS THIS TASK
                                    #remove 'NEXT '
                                    #position 4 is a space
                                    #modifiedMessage= str(theInput[5:len(theInput)])
                                    #print "INFO: Successfully removed the NEXT keyword from the message"
                                    print "STATUS: Creating a new chunk object (to be sent to the controller)..."
                                    #make new chunk object
                                    tempChunk = Chunk.Chunk()
                                    #set the params for the chunk object
                                    tempChunk.params = theInput
                                    #set the data for the chunk object
                                    tempChunk.data = tempData
                                    print "INFO: Chunk object successfully created"
                                    print "STATUS: Sending doingStuff Command to Controller..."
                                    self.sendDoingStuffCommandToController()
                                    print "INFO: doingStuff Command was sent to controller"
                                    print "STATUS: Sending chunk object to the controller..."
                                    self.sendNextChunkToController(tempChunk)
                                    print "INFO: Finished sending chunk to the controller"

                                    #and store it locally till controller is ready for it #OLD METHOD
                                    #self.chunk.params = self.clientSocket.recv(2048)
                                    #self.chunk.data = self.clientSocket.recv(2048)
                                    #let controller know we're ready to give it a chunk
                                    #self.sendDoingStuffCommandToController()
                                    #send chunk object to controller
                                    #self.pipe.send(self.chunk)

                                except Exception as inst:
                                    print "============================================================================================="
                                    print "ERROR: An exception was thrown in the checking for server commands Try Block"
                                    #the exception instance
                                    print type(inst)
                                    #srguments stored in .args
                                    print inst.args
                                    #_str_ allows args tto be printed directly
                                    print inst
                                    print "============================================================================================="
                            else:
                                print "ERROR: Received Unknown Command From The Server"
                                print "The unknown command: '" + theInput + "'"
                                self.recordOfInboundCommandsFromServer['Unknown'] = (self.recordOfInboundCommandsFromServer['Unknown'] + 1)
                        else:
                            print "INFO: Received Empty String From Server."

                    except socket.timeout as inst:
                        print "STATUS: Socket timed out. No new server command"

                    except Exception as inst:
                        print "============================================================================================="
                        print "ERROR: An exception was thrown in the checking for server commands Try Block"
                        #the exception instance
                        print type(inst)
                        #srguments stored in .args
                        print inst.args
                        #_str_ allows args tto be printed directly
                        print inst
                        print "============================================================================================="
            #///////////////////////////////////////////////////////////////////////////
            #End of Check for Server Commands
            #///////////////////////////////////////////////////////////////////////////

            #///////////////////////////////////////////////////////////////////////////
            #Check for Controller Commands
            #///////////////////////////////////////////////////////////////////////////
            #'''GOAL: Want to have client respond immeadiately when it receives a command from the controller'''
                    print "STATUS: Checking for controller commands... "
                    if(self.pipe.poll()):
                        recv = self.pipe.recv()
                        print "INFO: Received a controller command"
                        if(self.checkForRequestNextChunkCommand(recv)==True):
                            print "INFO: Received request next chunk command from controller"
                            self.sendNextCommandToServer()
                        elif(recv == "next"):
                            print " "
                            print "WARNING: THE 'next' COMMAND IS OBSOLETE!!!! PLEASE USE 'requestNextChunk' INSTEAD"
                            print " "
                            self.sendNextCommandToServer()
                            print "WARNING: The nextChunkCommand was still sent to the Server..."
                            print " "
                        elif(recv == "found"):
                            print " "
                            print "WARNING: THE 'found' COMMAND IS OBSOLETE!!!!!! PLEASE USE 'foundSolution' INSTEAD"
                            print " "
                            self.sendFoundSolutionToServer()
                            print "WARNING: The foundSolutionCommand was still sent to the server..."
                            print " "
                        elif(self.checkForFoundSolutionCommand(recv)==True):
                            print "INFO: Received Found Solution command from controller"
                            print "STATUS: Sending Found Solution Command to the Server..."
                            self.sendFoundSolutionToServer()
                            print "INFO: Sent Found Solution Command to the Server"
                        elif(self.checkForDoingStuffCommand(recv)==True):
                            print "INFO: Received doingStuff Command from controller"
                            print "INFO: Controller has parroted the doingStuff Command."
                        else:
                            print "ERROR: unknown command was received"
                            print "The unknown command: '" + recv + "'"
                            self.recordOfInboundCommandsFromController['Unknown'] = (self.recordOfInboundCommandsFromController['Unknown'] + 1)
                    else:
                        print "INFO: No command was received from the controller class"
            #///////////////////////////////////////////////////////////////////////////
            #End of Check for Controller Commands
            #///////////////////////////////////////////////////////////////////////////
        except Exception as inst:
            print "============================================================================================="
            print "ERROR: An exception was thrown in the Client Primary Loop Try Block"
            print type(inst) #the exception instance
            print inst.args #srguments stored in .args
            print inst #_str_ allows args tto be printed directly
            print "============================================================================================="
        #........................................................................
        #End of Client Primary While Loop
        #........................................................................

        #........................................................................
        #Start of NetworkClient Finally Block
        #........................................................................
        finally:
            #///////////////////////////////////////////////////////////////////////////
            #If exitting before server issues the Done Command, print out Error
            #///////////////////////////////////////////////////////////////////////////
            if(self.serverIssuedDoneCommand == False):
                print "ERROR: Quitting before Done Command was Issued. Sending CRASH Command to server."
                self.sendCrashedCommandToServer()
                print "INFO: CRASH Command was sent to the server"
                #SEND MESSAGE AGAIN JUST IN CASE
                #self.sendCrashedCommandToServer()
                #print "INFO: Aux Crash Command was sent to the server" #THIS FUNCTION IS NOW OBSOLETE!!!!!!!!!
            #///////////////////////////////////////////////////////////////////////////
            #End of if exitting before server issues the Done Command, print out Error
            #///////////////////////////////////////////////////////////////////////////

            #///////////////////////////////////////////////////////////////////////////
            #Close the Socket
            #///////////////////////////////////////////////////////////////////////////
            print "Closing the socket"
            self.clientSocket.close() #closes the socket safely
            print "Socket has been closed"
            print " "
            #///////////////////////////////////////////////////////////////////////////
            #End of Close the Socket
            #///////////////////////////////////////////////////////////////////////////

            #///////////////////////////////////////////////////////////////////////////
            #Print Command Records
            #///////////////////////////////////////////////////////////////////////////
            try:
                print " "
                print "COMMAND RECORDS: Part 1/4"
                print "Printing Outbound Commands From Client to Controller"
                print "-----------------------------------------------------"
                #print done
                if(self.recordOfOutboundCommandsFromClientToController['done'] > 0):
                    print "# of done Commands sent to Controller: " + str(self.recordOfOutboundCommandsFromClientToController['done'])
                else:
                    print "# of done Commands sent to Controller: 0"
                #print connected
                if(self.recordOfOutboundCommandsFromClientToController['connected'] > 0):
                    print "# of connected Commands sent to Controller: " + str(self.recordOfOutboundCommandsFromClientToController['connected'])
                else:
                    print "# of connected Commands sent to Controller: 0"
                #print doingStuff
                if(self.recordOfOutboundCommandsFromClientToController['doingStuff'] > 0):
                    print "# of doingStuff Commands sent to Controller: " + str(self.recordOfOutboundCommandsFromClientToController['doingStuff'])
                else:
                    print "# of doingStuff Commands sent to Controller: 0"
                #print nextChunk
                if(self.recordOfOutboundCommandsFromClientToController['nextChunk'] > 0):
                    print "# of nextChunk Commands sent to the Controller: " + str(self.recordOfOutboundCommandsFromClientToController['nextChunk'])
                else:
                    print "# of nextChunk Commands sent to the Controller: 0"
                print "(END OF OUTBOUND COMMANDS FROM CLIENT TO CONTROLLER)"
                print "-------------------------------------------------------"
            except Exception as inst:
                print "============================================================================================="
                print "ERROR: An exception was thrown in the Finally Block, Print Outbound commands from client to controller section"
                print type(inst) #the exception instance
                print inst.args #srguments stored in .args
                print inst #_str_ allows args tto be printed directly
                print "============================================================================================="
            try:
                print " "
                print "COMMAND RECORDS: Part 2/4"
                print "Printing Outbound Commands From Client To Server"
                print "--------------------------------------------------"
                #print NEXT
                if(self.recordOfOutboundCommandsFromClientToServer['NEXT'] > 0):
                    print "# of NEXT Commands sent to Server: " + str(self.recordOfOutboundCommandsFromClientToServer['NEXT'])
                else:
                    print "# of NEXT Commands sent to Server: 0"
                #print FOUNDSOLUTION
                if(self.recordOfOutboundCommandsFromClientToServer['FOUNDSOLUTION'] > 0):
                    print "# of FOUNDSOLUTION Commands sent to Server: " + str(self.recordOfOutboundCommandsFromClientToServer['FOUNDSOLUTION'])
                else:
                    print "# of FOUNDSOLUTION Commands sent to to Server: 0"
                #print CRASHED
                if(self.recordOfOutboundCommandsFromClientToServer['CRASHED'] > 0):
                    print "# of CRASHED Commands sent to Server: " + str(self.recordOfOutboundCommandsFromClientToServer['CRASHED'])
                else:
                    print "# of CRASHED Commands sent to Server: 0"
                print "(END OF OUTBOUND COMMANDS FROM CLIENT TO SERVER)"
                print "--------------------------------------------------"
            except Exception as inst:
                print "============================================================================================="
                print "ERROR: An exception was thrown in the Finally Block, Print Outbound Commands From Client to Server Section"
                print type(inst) #the exception instance
                print inst.args #srguments stored in .args
                print inst #_str_ allows args tto be printed directly
                print "============================================================================================="
            try:
                print " "
                print "COMMAND RECORDS: Part 3/4"
                print "Printing Inbound Commands From The Controller"
                print "-----------------------------------------------"
                #print serverIP
                if(self.recordOfInboundCommandsFromController['serverIP'] > 0):
                    print "# of serverIP Commands  received from Controller: " + str(self.recordOfInboundCommandsFromController['serverIP'])
                else:
                    print "# of serverIP Commands received from Controller: 0"
                #print FOUNDSOLUTION
                if(self.recordOfInboundCommandsFromController['FOUNDSOLUTION'] > 0):
                    print "# of FOUNDSOLUTION Commands received from Controller: " + str(self.recordOfInboundCommandsFromController['FOUNDSOLUTION'])
                else:
                    print "# of FOUNDSOLUTION Commands received from Controller: 0"
                #print REQUESTNEXTCHUNK
                if(self.recordOfInboundCommandsFromController['REQUESTNEXTCHUNK'] > 0):
                    print "# of REQUESTNEXTCHUNK Commands received from Controller: " + str(self.recordOfInboundCommandsFromController['REQUESTNEXTCHUNK'])
                else:
                    print "# of REQUESTNEXTCHUNK Commands received from Controller: 0"
                #print doingStuff
                if(self.recordOfInboundCommandsFromController['doingStuff'] > 0):
                    print "# of doingStuff Commands received from Controller: " + str(self.recordOfInboundCommandsFromController['doingStuff'])
                else:
                    print "# of doingStuff Commands received from Controller: 0"
                #print Unknown
                if(self.recordOfInboundCommandsFromController['Unknown'] > 0):
                    print "# of Unknown Commands received from Controller: " + str(self.recordOfInboundCommandsFromController['Unknown'])
                else:
                    print "# of Unknown Commands received from Controller: 0"
                print "(END OF INBOUND COMMANDS FROM CONTROLLER)"
                print "-----------------------------------------------"
            except Exception as inst:
                print "============================================================================================="
                print "ERROR: An exception was thrown in the Finally Block, Print Inbound Commands from Controller Section"
                print type(inst) #the exception instance
                print inst.args #srguments stored in .args
                print inst #_str_ allows args tto be printed directly
                print "============================================================================================="
            try:
                print " "
                print "COMMAND RECORDS: Part 4/4"
                print "Printing Inbound Commands from the Server"
                print "-----------------------------------------------"
                #print DONE
                if(self.recordOfInboundCommandsFromServer['DONE'] > 0):
                    print "# of DONE Commands received from the Server: " + str(self.recordOfInboundCommandsFromServer['DONE'])
                else:
                    print "# of DONE Commands received from the Server: 0"
                #print reply to nextchunk
                if(self.recordOfInboundCommandsFromServer['REPLY_TO_NEXTCHUNK'] > 0):
                    print "# of REPLY_TO_NEXTCHUNK Commands received from the Server: " + str(self.recordOfInboundCommandsFromServer['REPLY_TO_NEXTCHUNK'])
                else:
                    print "# of REPLY_TO_NEXTCHUNK Commands received from the Server: 0"
                #print nextChunkData
                if(self.recordOfInboundCommandsFromServer['NEXTCHUNKDATA'] > 0):
                    print "# of NEXTCHUNKDATA Commands received from the Server: " + str(self.recordOfInboundCommandsFromServer['NEXTCHUNKDATA'])
                else:
                    print "# of NEXTCHUNKDATA Commands received from the Server: 0"
                #print Unknown
                if(self.recordOfInboundCommandsFromServer['Unknown'] > 0):
                    print "# of Unknown Commands received from Server: " + str(self.recordOfInboundCommandsFromServer['Unknown'])
                else:
                    print "# of Unknown Commands received from Server: 0"
                print "(END OF INBOUND COMMANDS FROM THE SERVER)"
                print "------------------------------------------------"
            except Exception as inst:
                print "============================================================================================="
                print "ERROR: An exception was thrown in the Finally Block, Print Inbound Commands from the Server Section"
                print type(inst) #the exception instance
                print inst.args #srguments stored in .args
                print inst #_str_ allows args tto be printed directly
                print "============================================================================================="
            #///////////////////////////////////////////////////////////////////////////
            #End of Print Command Records
            #///////////////////////////////////////////////////////////////////////////
        #........................................................................
        #End of NetworkClient Finally Block
        #........................................................................
    #-------------------------------------------------------------------
    #End of NetworkClient Class Constructor
    #-------------------------------------------------------------------

    #-------------------------------------------------------------------
    #Defined Communication Functions
    #-------------------------------------------------------------------
        #........................................................................
        #Client-Server Communication Functions
        #........................................................................
            #///////////////////////////////////////////////////////////////////////////
            #Outbound Communication Functions
            #///////////////////////////////////////////////////////////////////////////
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                #NEXT
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    def sendNextCommandToServer(self):
        #sends the NEXT command to the serve
        try:
            self.clientSocket.send("NEXT " + self.myIPAddress)
            print "INFO: The NEXT command was sent to the server"
            self.recordOfOutboundCommandsFromClientToServer['NEXT'] = (self.recordOfOutboundCommandsFromClientToServer['NEXT'] + 1)
        except Exception as inst:
            print "============================================================================================="
            print "ERROR: An exception was thrown in the Client-Server sendNextCommand Function Try Block"
            #the exception instance
            print type(inst)
            #srguments stored in .args
            print inst.args
            #_str_ allows args tto be printed directly
            print inst
            print "============================================================================================="

                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                #FOUNDSOLUTION
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    def sendFoundSolutionToServer(self):
        #sends the FOUNDSOLUTION command to the server, and key
        try:
            self.clientSocket.send("FOUNDSOLUTION " + str(self.myIPAddress))
            self.clientSocket.send(str(self.key))
            print "INFO: The FOUNDSOLUTION command was sent to the server as well as the key"
            self.recordOfOutboundCommandsFromClientToServer['FOUNDSOLUTION'] = (self.recordOfOutboundCommandsFromClientToServer['FOUNDSOLUTION'] + 1)
        except Exception as inst:
            print "============================================================================================="
            print "ERROR: An exception was thrown in the Client-Server sendFoundSolution Function Try Block"
            #the exception instance
            print type(inst)
            #srguments stored in .args
            print inst.args
            #_str_ allows args tto be printed directly
            print inst
            print "============================================================================================="

                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                #CRASHED
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    def sendCrashedCommandToServer(self):
        #sends the CRASHED command to the server
        try:
            self.clientSocket.send("CRASHED " + self.myIPAddress)
            print " "
            print "INFO: The IP Address of the crashed client was sent to the server."
            print " "
            self.recordOfOutboundCommandsFromClientToServer['CRASHED'] = (self.recordOfOutboundCommandsFromClientToServer['CRASHED'] + 1)
        except Exception as inst:
            print "============================================================================================="
            print "ERROR: An exception was thrown in the Client-Server sendCrashedCommand Function Try Block"
            #the exception instance
            print type(inst)
            #srguments stored in .args
            print inst.args
            #_str_ allows args tto be printed directly
            print inst
            print "============================================================================================="
            #///////////////////////////////////////////////////////////////////////////
            #End of Outbound Communication Functions
            #///////////////////////////////////////////////////////////////////////////

            #///////////////////////////////////////////////////////////////////////////
            #Inbound Communication Functions
            #///////////////////////////////////////////////////////////////////////////
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                #DONE
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    def checkForDoneCommand(self, inboundString):
        try:
            #if inboundString[0:3] == "DONE": #OLD WAY
            if(inboundString[0] == "D"):
                if(inboundString[1] == "O"):
                    if(inboundString[2] == "N"):
                        if(inboundString[3] == "E"):
                            print "INFO: Received the DONE command from the server"
                            self.recordOfInboundCommandsFromServer['DONE'] = (self.recordOfInboundCommandsFromServer['DONE'] + 1)
                            return True
            else:
                return False
        except Exception as inst:
            print "============================================================================================="
            print "ERROR: An exception was thrown in the Client-Server checkForDoneCommand Function Try Block"
            #the exception instance
            print type(inst)
            #srguments stored in .args
            print inst.args
            #_str_ allows args tto be printed directly
            print inst
            print "============================================================================================="

                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                #NEXT
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    def checkForNextCommand(self,inboundString):
        try:
            #if inboundString[0:4] == "NEXT ": #OLD METHOD
            if(len(inboundString) < 1):
                return False
            if(inboundString[0] == "N"):
                if(inboundString[1] == "E"):
                    if(inboundString[2] == "X"):
                        if(inboundString[3] == "T"):
                            print "INFO: Received the NEXT (chunk) command from the server"
                            self.recordOfInboundCommandsFromServer['REPLY_TO_NEXTCHUNK'] = (self.recordOfInboundCommandsFromServer['REPLY_TO_NEXTCHUNK'] + 1)
                            return True
            else:
                return False
        except Exception as inst:
            print "============================================================================================="
            print "ERROR: An exception was thrown in the Client-Server checkForNextCommand Function Try Block"
            #the exception instance
            print type(inst)
            #srguments stored in .args
            print inst.args
            #_str_ allows args tto be printed directly
            print inst
            print "============================================================================================="
                #INVALID COMMAND HAS BEEN OMITTED
            #///////////////////////////////////////////////////////////////////////////
            #End of Inbound Communication FUnctions
            #///////////////////////////////////////////////////////////////////////////
        #........................................................................
        #End of Client-Server Communication Functions
        #........................................................................

        #........................................................................
        #Client-Controller Communication Functions
        #........................................................................
            #///////////////////////////////////////////////////////////////////////////
            #Outbound Communication Functions
            #///////////////////////////////////////////////////////////////////////////
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                #nextChunk
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    def sendNextChunkToController(self, inboundChunk):
        try:
            self.pipe.send(inboundChunk)
            print "INFO: The nextChunk was sent to the Controller"
            self.recordOfOutboundCommandsFromClientToController['nextChunk'] = (self.recordOfOutboundCommandsFromClientToController['nextChunk'] + 1)
        except Exception as inst:
            print "============================================================================================="
            print "ERROR: An exception was thrown in the Client-Controller sendNextChunkToController Function Try Block"
            #the exception instance
            print type(inst)
            #srguments stored in .args
            print inst.args
            #_str_ allows args tto be printed directly
            print inst
            print "============================================================================================="
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                #DONE
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    def sendDoneCommandToController(self):
        try:
            self.pipe.send("done")
            print "INFO: The DONE command was sent to the Controller"
            self.recordOfOutboundCommandsFromClientToController['done'] = (self.recordOfOutboundCommandsFromClientToController['done'] + 1)
        except Exception as inst:
            print "============================================================================================="
            print "ERROR: An exception was thrown in the Client-Controller sendDoneCommand Function Try Block"
            #the exception instance
            print type(inst)
            #srguments stored in .args
            print inst.args
            #_str_ allows args tto be printed directly
            print inst
            print "============================================================================================="

                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                #CONNECTED
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    def sendConnectedCommandToCOntroller(self):
        try:
            self.pipe.send("connected")
            print "INFO: The CONNECTED command was sent to the Controller"
            self.recordOfOutboundCommandsFromClientToController['connected'] = (self.recordOfOutboundCommandsFromClientToController['connected'] + 1)
        except Exception as inst:
            print "============================================================================================="
            print "ERROR: An exception was thrown in the Client-Controller sendConnectedCommand Function Try Block"
            #the exception instance
            print type(inst)
            #srguments stored in .args
            print inst.args
            #_str_ allows args tto be printed directly
            print inst
            print "============================================================================================="

                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                #DOINGSTUFF
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    def sendDoingStuffCommandToController(self):
        try:
            self.pipe.send("doingStuff")
            print "INFO: The DOINGSTUFF command was sent to the Controller"
            self.recordOfOutboundCommandsFromClientToController['doingStuff'] = (self.recordOfOutboundCommandsFromClientToController['doingStuff'] + 1)
        except Exception as inst:
            print "============================================================================================="
            print "ERROR: An exception was thrown in the Client-Controller sendDoingStuffCommand Function Try Block"
            #the exception instance
            print type(inst)
            #srguments stored in .args
            print inst.args
            #_str_ allows args tto be printed directly
            print inst
            print "============================================================================================="
            #///////////////////////////////////////////////////////////////////////////
            #End of Outbound Communication Functions
            #///////////////////////////////////////////////////////////////////////////

            #///////////////////////////////////////////////////////////////////////////
            #Inbound Communication Functions
            #///////////////////////////////////////////////////////////////////////////
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                #SERVER IP
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    def receiveServerIPFromController(self):
        try:
            print "INFO: Waiting to receive the serverIP from Controller (function block)"
            self.serverIP = self.pipe.recv()
            print "INFO: The ServerIP was received from the Controller (function block)"
            self.recordOfInboundCommandsFromController['serverIP'] = (self.recordOfInboundCommandsFromController['serverIP'] + 1)

        except Exception as inst:
            print "============================================================================================="
            print "ERROR: An exception was thrown in the Client-Controller receiveServerIP Function Try Block"
            #the exception instance
            print type(inst)
            #srguments stored in .args
            print inst.args
            #_str_ allows args tto be printed directly
            print inst
            print "============================================================================================="
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                #DOINGSTUFF
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    def checkForDoingStuffCommand(self,inboundString):
        try:
            print "STATUS: Checking for doingStuff Command..."
            if(len(inboundString) < 1):
                return False
            if(self.compareString("doingStuff",inboundString,0,0,len("doingStuff"),len(inboundString))==True):
                print "I/O: Received the doingStuff Command from the Controller"
                self.recordOfInboundCommandsFromController['doingStuff'] = (self.recordOfInboundCommandsFromController['doingStuff'] + 1)
                return True
            else:
                return False
        except Exception as inst:
            print "============================================================================================="
            print "ERROR: An exception was thrown in the Client-Controller inbound checkForDoingStuffCommand Function Try Block"
            #the exception instance
            print type(inst)
            #srguments stored in .args
            print inst.args
            #_str_ allows args tto be printed directly
            print inst
            print "============================================================================================="
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                #FOUNDSOLUTION
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    def checkForFoundSolutionCommand(self,inboundString):
        try:
            print "STATUS: Checking for Found Solution Command..."
            if(len(inboundString) < 1):
                return False
            #if(inboundString[0:12] == "foundSolution"): #OLD METHOD
            if(inboundString[0] == "f"):
                if(inboundString[1] == "o"):
                    if(inboundString[2] == "u"):
                        if(inboundString[3] == "n"):
                            if(inboundString[4] == "d"):
                                if(inboundString[5] == "S"):
                                    if(inboundString[6] == "o"):
                                        if(inboundString[7] == "l"):
                                            if(inboundString[8] == "u"):
                                                if(inboundString[9] == "t"):
                                                    if(inboundString[10] == "i"):
                                                        if(inboundString[11] == "o"):
                                                            if(inboundString[12] == "n"):
                                                                print "I/O: Received the Found Solution Command from the Controller"
                                                                self.recordOfInboundCommandsFromController['FOUNDSOLUTION'] = (self.recordOfInboundCommandsFromController['FOUNDSOLUTION'] + 1)
                                                                return True
            else:
                return False
        except Exception as inst:
            print "============================================================================================="
            print "ERROR: An exception was thrown in the Client-Controller inbound checkForFoundSolutionCommand Function Try Block"
            #the exception instance
            print type(inst)
            #srguments stored in .args
            print inst.args
            #_str_ allows args tto be printed directly
            print inst
            print "============================================================================================="

                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                #REQUESTNEXTCHUNK
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    def checkForRequestNextChunkCommand(self,inboundString):
        try:
            print "STATUS: Checking for Request Next Chunk Command..."
            if(len(inboundString) < 1):
                return False
            #if(inboundString[0:15] == "requestNextChunk"):
            #if(inboundString[0:15] is "requestNextChunk"):
            #if()
            if(self.compareString("requestNextChunk",inboundString,0,0,len("requestNextChunk"),len(inboundString))==True):
                print "I/O: Received the Request Next Chunk Command from the Controller"
                self.recordOfInboundCommandsFromController['REQUESTNEXTCHUNK'] = (self.recordOfInboundCommandsFromController['REQUESTNEXTCHUNK']+1)
                return True
            else:
                return False
        except Exception as inst:
            print "============================================================================================="
            print "ERROR: An exception was thrown in the Client-Controller inbound checkForRequestNextChunkCommand Function Try Block"
            #the exception instance
            print type(inst)
            #srguments stored in .args
            print inst.args
            #_str_ allows args tto be printed directly
            print inst
            print "============================================================================================="
            #///////////////////////////////////////////////////////////////////////////
            #End of Inbound Communication FUnctions
            #///////////////////////////////////////////////////////////////////////////
        #........................................................................
        #End of Client-Controller Communication Functions
        #........................................................................
    #-------------------------------------------------------------------
    #End of Defined Communication Functions
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


#================================================================
#End of NetworkClient Class Definition
#================================================================