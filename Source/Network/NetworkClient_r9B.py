__author__ = 'chris hamm'
#NetworkClient_r9B
#Created: 1/3/2015

#this version improves the crash detection system by telling the server the ip address of the client that crashed in the CRASHED command message.

import socket
import platform
import Chunk

#===================================================================
#Client constructor/class definition
#===================================================================
#CLASS NAME WILL NOT CHANGE BETWEEN VERSIONS
class NetworkClient():
    #class variables
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

    #constructor
    def __init__(self, pipeendconnectedtocontroller):
        self.pipe = pipeendconnectedtocontroller

        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print "STATUS: client socket created successfully"

        try: #Main Client Loop
            print "STATUS: Entering Main Client Loop"

            #getOS try block
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

            #get the client IP address of this machine
            try: #get client IP try block
                print "STATUS: Getting your Network IP address"
                if(platform.system()=="Windows"):
                    self.myIPAddress = socket.gethostbyname(socket.gethostname())
                    print str(self.myIPAddress)
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
                    print self.myIPAddress
                elif(platform.system()=="Darwin"):
                    self.myIPAddress= socket.gethostbyname(socket.gethostname())
                    print self.myIPAddress
                else:
                    #NOTE MAY REMOVE  THIS AND USE THE LINUX IP DETECTION METHOD FOR THIS IN THE FUTURE
                    print "INFO: The system has detected that you are not running Windows, OS X, or Linux."
                    print "INFO: Using generic IP address retrieval method"
                    self.myIPAddress = socket.gethostbyname(socket.gethostname())
                    print self.myIPAddress
            except Exception as inst:
                print "========================================================================================"
                print "ERROR: An exception was thrown in get client IP try block"
                print type(inst)
                print inst.args
                print inst
                print "========================================================================================"

            #Retreive the server's IP from the controller class
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
                #print "========================================================================================"

            self.sendConnectedCommandToCOntroller()

            #Client primary while loop
            try:
                #This should probably be 'while server days not done'
                #   since we might be just waiting on server, before we get a job (or in-between)
                #   Just my thoughts though --CJB
                while self.serverSaysKeepSearching:
                    self.clientSocket.settimeout(2.0)

                    ######################## SERVER-CLIENT Communication #############################################

                    #checking for server commands try block
                    try:
                        print "STATUS: Checking for server commands..."
                        theInput = self.clientSocket.recv(2048)
                        if theInput == "DONE":
                            self.sendDoneCommandToController()

                            #Make this line seperate from the other print statements
                            print " "
                            print "INFO: Server has issued the DONE command."
                            print " "
                            self.serverSaysKeepSearching = False
                            self.serverIssuedDoneCommand = True
                            break
                        #If the server wants to give us the next chunk, take it
                        #Server should be sending "NEXT" -> params -> data in seperate strings all to us
                        elif theInput == "NEXT":
                            try:
                                #and store it locally till controller is ready for it
                                self.chunk.params = self.clientSocket.recv(2048)
                                self.chunk.data = self.clientSocket.recv(2048)
                                #let controller know we're ready to give it a chunk
                                self.sendDoingStuffCommandToController()

                                #send chunk object to controller
                                self.pipe.send(self.chunk)

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

                    ########################## Client - Controller Communication #########################################
                    #check for controller commands
                    print "STATUS: Checking for controller commands... "
                    if(self.pipe.poll()):
                        recv = self.pipe.recv()  #Gets stuck on this line ##########
                        print "INFO: Received a controller command"
                        #if controller says next, say "next" to server
                        if(recv == "next"):
                            print "INFO: Received next command from controller"
                            self.sendNextCommandToServer()
                        #if controller says "found" then send "found" and the key to the server
                        elif(recv == "found"):
                            print "INFO: Received found command from controller"
                            print "STATUS: Retrieving key"
                            if(self.pipe.poll()):
                                self.key = self.pipe.recv()
                                print "INFO: the key has been received"
                                self.sendFoundSolutionToServer()
                        else:
                            print "ERROR: unknown command was received"
                            print "The unknown command: '" + recv + "'"
                    else:
                        print "INFO: No command was received from the controller class"


                #end of server says keep searching while loop
            except Exception as inst:
                print "============================================================================================="
                print "ERROR: An exception was thrown in the Client Primary Loop Try Block"
                print type(inst) #the exception instance
                print inst.args #srguments stored in .args
                print inst #_str_ allows args tto be printed directly
                print "============================================================================================="

        except Exception as inst:
            print "============================================================================================="
            print "ERROR: An exception was thrown in the Main Client Loop Try Block"
            print type(inst) #the exception instance
            print inst.args #srguments stored in .args
            print inst #_str_ allows args tto be printed directly
            print "============================================================================================="
        finally:
            if(self.serverIssuedDoneCommand == False):
                print "ERROR: Quitting before Done Command was Issued. Sending CRASH Command to server."
                self.sendCrashedCommandToServer()
                print "INFO: CRASH Command was sent to the server"
            print "Closing the socket"
            self.clientSocket.close() #closes the socket safely
            print "Socket has been closed"
            print " "

        #End of constructor block

    #======================================================================================
    #CLIENT-SERVER COMMUNICATION FUNCTIONS
    #This section contains methods the client will use to communicate with the server.
    #======================================================================================

    #Outbound communication functions

        #NEXT
    def sendNextCommandToServer(self):
        #sends the NEXT command to the serve
        try:
            self.clientSocket.send("NEXT")
            print "INFO: The NEXT command was sent to the server"

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

        #FOUNDSOLUTION
    def sendFoundSolutionToServer(self):
        #sends the FOUNDSOLUTION command to the server, and key
        try:
            self.clientSocket.send("FOUNDSOLUTION")
            self.clientSocket.send(self.key)
            print "INFO: The FOUNDSOLUTION command was sent to the server as well as the key"
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

        #CRASHED
    def sendCrashedCommandToServer(self):
        #sends the CRASHED command to the server

        #NOTICE: THIS COMMAND IS NOT IMPLEMENTED OR DOES NOT WORK, BUT STILL SENDS EMPTY STRING TO SERVER!!!!!!!
        try:
            self.clientSocket.send("CRASHED")
            print " "
            print "INFO: The CRASHED command was sent to the server"
            self.clientSocket.send(" " + self.myIPAddress)
            print "INFO: The IP Address of the crashed client was sent to the server."
            print " "
            self.clientSocket.send("") #clear the recv socket
            print "INFO: Empty String Sent to Server to Clear the recv socket"
            print " "
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

        #INVALIDCOMMAND
    def sendInvalidCommandToServer(self):
        #sends INVALIDCOMMAND command to server
        try:
            self.clientSocket.send("INVALIDCOMMAND")
            print "INFO: The INVALIDCOMMAND command was sent to the server"
        except Exception as inst:
            print "============================================================================================="
            print "ERROR: An exception was thrown in the Client-Server sendInvalidCommand Function Try Block"
            #the exception instance
            print type(inst)
            #srguments stored in .args
            print inst.args
            #_str_ allows args tto be printed directly
            print inst
            print "============================================================================================="

    #Inbound communication functions
        #DONE
    def checkForDoneCommand(self, inboundString):
        try:
            if inboundString == "DONE":
                print "INFO: Received the DONE command"
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

        #next part of problem

        #not sure what to check for here

        #INVALIDCOMMAND
    def checkForInvalidCommand(self, inboundString):
        try:
            if inboundString == "INVALIDCOMMAND":
                print "INFO: Received the INVALIDCOMMAND command"
                return True
            else:
                return False
        except Exception as inst:
            print "============================================================================================="
            print "ERROR: An exception was thrown in the Client-Server checkForInvalidCommand Function Try Block"
            #the exception instance
            print type(inst)
            #srguments stored in .args
            print inst.args
            #_str_ allows args tto be printed directly
            print inst
            print "============================================================================================="

    #======================================================================================
    #CLIENT-CONTROLLER COMMUNICATION FUNCTIONS
    #This section contains methods the client will use to communicate with the controller class
    #======================================================================================

    #Outbound communication functions with controller
        #done

    def sendDoneCommandToController(self):
        try:
            self.pipe.send("done")
            print "INFO: The DONE command was sent to the Controller"
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

        #connected
    def sendConnectedCommandToCOntroller(self):
        try:
            self.pipe.send("connected")
            print "INFO: The CONNECTED command was sent to the Controller"
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

        #doingStuff
    def sendDoingStuffCommandToController(self):
        try:
            self.pipe.send("doingStuff")
            print "INFO: The DOINGSTUFF command was sent to the Controller"
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

        ######### NEW CODE########################################
        #serverIP
    def receiveServerIPFromController(self):
        try:
            #self.pipe.send("doingStuff")
            print "INFO: Waiting to receive the serverIP from Controller (function block)"
            self.serverIP = self.pipe.recv()
            print "INFO: The ServerIP was received from the Controller (function block)"
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



