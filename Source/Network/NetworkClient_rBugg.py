__author__ = 'Chris Hamm'
#NetworkClient_r7B
#Created: 11/21/2014

#This is a restructured version of r7A


import socket
import platform

#try: #Master Try Block
#===================================================================
#Client constructor/class definition
#===================================================================
#CLASS NAME WILL NOT CHANGE BETWEEN VERSIONS
class NetworkClient():
    #try: #NetworkClient class try block
    #class variables
    pipe = 0
    #This does not stay a number
    #pipeendconnectedtocontroller = 0
    port = 49200
    clientSocket = 0
   # done= False #useed for the while loop
    serverSaysKeepSearching = True
    serverIP = "127.0.1.1"

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

            #prompt user for the servers IP address
            #serverIPAddress = raw_input('What is the host (server) IP Address?')

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

                    #checking for server commands try block
                    try:
                        print "Checking for server commands..."
                        theInput = self.clientSocket.recv(2048)
                        #if theInput == "DONE":
                        if self.checkForDoneCommand(theInput):
                            #Make this line seperate from the other print statements
                            print " "
                            print "Server has issued the DONE command."
                            print " "
                            serverSaysKeepSearching = False
                            break
                        #There should be more elifs with client-controller stuff
                        #  ie: if server says here's that chunk you asked for, or other stuff

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

                    #keep performing task
                    #-------------------------
                        #INSERT TASK HERE
                    #-------------------------

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
    #try: #client-server communication functions try block
    #print "Inside the client server comm block"
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
        #sends the FOUNDSOLUTION command to the server
        try:
            self.clientSocket.send("FOUNDSOLUTION")
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
    #def checkForNextPartOfProblem(inboundString): #checks for the next part of the problem
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
    #try: #client-controller communication functions try block
    #print "Inside the client controller comm block"
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
