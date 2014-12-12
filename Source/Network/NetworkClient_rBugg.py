__author__ = 'Chris Hamm'
#NetworkClient_rBugg
#Created: 11/21/2014

#This is a restructured version of r7A

#NOTES: SOCKET IS NOT CLOSED WHEN FINISHED!!!

#SUPERCEDED BY r9!!!!

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
    #This does not stay a number
    port = 49200
    clientSocket = 0
    serverSaysKeepSearching = True
    serverIP = "127.0.1.1"
    chunk = Chunk.Chunk()
    key = 0

    #constructor
    def __init__(self, pipeendconnectedtocontroller):
        self.pipe = pipeendconnectedtocontroller

        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print "client socket created successfully"

        try: #Main Client Loop
            print "Entering Main Client Loop"

            #getOS try block
            try:
                print "*************************************"
                print "    Network Client"
                print "*************************************"
                print "OS DETECTION:"

                #Detecting Windows
                if platform.system() == "Windows":
                    print platform.system()
                    print platform.win32_ver()

                #Detecting Linux
                elif platform.system() == "Linux":
                    print platform.system()
                    print platform.dist()

                #Detecting OSX
                elif platform.system() == "Darwin":
                    print platform.system()
                    print platform.mac_ver()

                #Detecting an OS that is not listed
                else:
                    print platform.system()
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

            #Retreive the server's IP from the controller class


            try:
                print "Attempting to get serverIP from controller"
                self.receiveServerIPFromController()
                print "sucessfully received serverIP from controller"
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
                print "Attempting to connect to server"
                self.clientSocket.connect((self.serverIP, self.port))
                print "Successfully connected to server"

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
                        print "Checking for server commands..."
                        theInput = self.clientSocket.recv(2048)
                        if theInput == "DONE":

                            self.sendDoneCommandToController()

                            #Make this line seperate from the other print statements
                            print " "
                            print "Server has issued the DONE command."
                            print " "
                            serverSaysKeepSearching = False
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
                                print "An exception was thrown in the checking for server commands Try Block"
                                #the exception instance
                                print type(inst)
                                #srguments stored in .args
                                print inst.args
                                #_str_ allows args tto be printed directly
                                print inst
                                print "============================================================================================="

                    except socket.timeout as inst:
                        print "Socket timed out. No new server command"

                    except Exception as inst:
                        print "============================================================================================="
                        print "An exception was thrown in the checking for server commands Try Block"
                        #the exception instance
                        print type(inst)
                        #srguments stored in .args
                        print inst.args
                        #_str_ allows args tto be printed directly
                        print inst
                        print "============================================================================================="

                    ########################## Client - Controller Communication #########################################
                    #check for controller commands
                    recv = self.pipe.recv()

                    #If controller says 'next', say 'next' to server
                    if recv == "next":

                        self.sendNextCommandToServer()

                    #if controller says 'found' then send 'found' and key to server
                    elif recv == "found":

                        self.key = self.pipe.recv()

                        self.sendFoundSolutionToServer()

            except Exception as inst:
                print "============================================================================================="
                print "An exception was thrown in the Client Primary Loop Try Block"
                print type(inst) #the exception instance
                print inst.args #srguments stored in .args
                print inst #_str_ allows args tto be printed directly
                print "============================================================================================="

        except Exception as inst:
            print "============================================================================================="
            print "An exception was thrown in the Main Client Loop Try Block"
            print type(inst) #the exception instance
            print inst.args #srguments stored in .args
            print inst #_str_ allows args tto be printed directly
            print "============================================================================================="
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
            print "The NEXT command was sent to the server"

        except Exception as inst:
            print "============================================================================================="
            print "An exception was thrown in the Client-Server Communication FUnctions Try Block"
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
            print "The FOUNDSOLUTION command was sent to the server"
        except Exception as inst:
            print "============================================================================================="
            print "An exception was thrown in the Client-Server Communication FUnctions Try Block"
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
        #NOTICE: THIS COMMAND IS NOT IMPLEMENTED OR DOES NOT WORK, BUT STILL SENDS EMPTY STRING TO SERVER!
        try:
            self.clientSocket.send("CRASHED")
            print "The CRASHED command was sent to the server"
        except Exception as inst:
            print "============================================================================================="
            print "An exception was thrown in the Client-Server Communication FUnctions Try Block"
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
            print "The INVALIDCOMMAND command was sent to the server"
        except Exception as inst:
            print "============================================================================================="
            print "An exception was thrown in the Client-Server Communication FUnctions Try Block"
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
                return True
            else:
                return False
        except Exception as inst:
            print "============================================================================================="
            print "An exception was thrown in the Client-Server Communication FUnctions Try Block"
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
                return True
            else:
                return False
        except Exception as inst:
            print "============================================================================================="
            print "An exception was thrown in the Client-Server Communication FUnctions Try Block"
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
            print "The DONE command was sent to the Controller"
        except Exception as inst:
            print "============================================================================================="
            print "An exception was thrown in the Client-Controller Communication Functions Try Block"
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
            print "The CONNECTED command was sent to the Controller"
        except Exception as inst:
            print "============================================================================================="
            print "An exception was thrown in the Client-Controller Communication Functions Try Block"
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
            print "The DOINGSTUFF command was sent to the Controller"
        except Exception as inst:
            print "============================================================================================="
            print "An exception was thrown in the Client-Controller Communication Functions Try Block"
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
            print "Attempting to get serverIP from Controller (function block)"
            self.serverIP = self.pipe.recv()
            print "The ServerIP was received from the Controller (function block)"
        except Exception as inst:
            print "============================================================================================="
            print "An exception was thrown in the Client-Controller Communication Functions Try Block"
            #the exception instance
            print type(inst)
            #srguments stored in .args
            print inst.args
            #_str_ allows args tto be printed directly
            print inst
            print "============================================================================================="

# To Be Deleted, since they don't have their try blocks anymore
'''
except Exception as inst:
    print "============================================================================================="
    print "An exception was thrown in the Network Client class Try Block"
    print type(inst) #the exception instance
    print inst.args #srguments stored in .args
    print inst #_str_ allows args tto be printed directly
    print "============================================================================================="
finally:
    print "Closing the socket"
    clientSocket.close()
'''
'''
except Exception as inst:
    print "============================================================================================="
    print "An exception was thrown in the Master Try Block"
    print type(inst) #the exception instance
    print inst.args #srguments stored in .args
    print inst #_str_ allows args tto be printed directly
    print "============================================================================================="
finally:
    print "Program has ended"
'''
