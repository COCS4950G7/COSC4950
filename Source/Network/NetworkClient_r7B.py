__author__ = 'Chris Hamm'
#NetworkClient_r7B
#Created: 11/21/2014

#This is a restructured version of r7A

try: #Master Try Block
#===================================================================
#Client constructor/class definition
#===================================================================
    class NetworkClient(): #CLASS NAME WILL NOT CHANGE BETWEEN VERSIONS
        try: #NetworkClient class try block
            #class variables
            import socket
            import platform
            pipeendconnectedtocontroller =0 #This does not stay a number
            port= 49200
            clientSocket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print "server socket created successfully"
           # done= False #useed for the while loop
            serverSaysKeepSearching= True

            #======================================================================================
            #CLIENT-CONTROLLER COMMUNICATION FUNCTIONS
            #This section contains methods the client will use to communicate with the controller class
            #======================================================================================
            try: #client-controller communication functions try block
                #Outbound communication functions with controller
                    #done
                def sendDoneCommandToController(self):
                    self.pipe.send("done")
                    print "The DONE command was sent to the Controller"

                    #connected
                def sendConnectedCommandToCOntroller(self):
                    self.pipe.send("connected")
                    print "The CONNECTED command was sent to the Controller"

                    #doingStuff
                def sendDoingStuffCommandToController(self):
                    self.pipe.send("doingStuff")
                    print "The DOINGSTUFF command was sent to the Controller"

            except Exception as inst:
                print "============================================================================================="
                print "An exception was thrown in the Client-Controller Communication Functions Try Block"
                print type(inst) #the exception instance
                print inst.args #srguments stored in .args
                print inst #_str_ allows args tto be printed directly
                print "============================================================================================="

        #======================================================================================
        #CLIENT-SERVER COMMUNICATION FUNCTIONS
        #This section contains methods the client will use to communicate with the server.
        #======================================================================================
            try: #client-server communication functions try block
                #Outbound communication functions
                    #NEXT
                def sendNextCommandToServer(self):
                    self.clientSocket.send("NEXT") #sends the NEXT command to the serve
                    print "The NEXT command was sent to the server"

                    #FOUNDSOLUTION
                def sendFoundSolutionToServer(self):
                    self.clientSocket.send("FOUNDSOLUTION") #sends the FOUNDSOLUTION command to the server
                    print "The FOUNDSOLUTION command was sent to the server"

                    #CRASHED
                def sendCrashedCommandToServer(self):
                    self.clientSocket.send("CRASHED") #sends the CRASHED command to the server
                    print "The CRASHED command was sent to the server"

                    #INVALIDCOMMAND
                def sendInvalidCommandToServer(self):
                    self.clientSocket.send("INVALIDCOMMAND") #sends INVALIDCOMMAND command to server
                    print "The INVALIDCOMMAND command was sent to the server"

                #Inbound communication functions
                    #DONE
                def checkForDoneCommand(inboundString):
                    if(inboundString=="DONE"):
                        return True
                    else:
                        return False

                    #next part of problem
                #def checkForNextPartOfProblem(inboundString): #checks for the next part of the problem
                    #not sure what to check for here

                    #INVALIDCOMMAND
                def checkForInvalidCommand(inboundString):
                    if(inboundString=="INVALIDCOMMAND"):
                        return True
                    else:
                        return False

            except Exception as inst:
                print "============================================================================================="
                print "An exception was thrown in the Client-Server Communication FUnctions Try Block"
                print type(inst) #the exception instance
                print inst.args #srguments stored in .args
                print inst #_str_ allows args tto be printed directly
                print "============================================================================================="

            #constructor
            def __init__(self,pipeendconnectedtocontroller):
                self.pipe= pipeendconnectedtocontroller

                try: #Main Client Loop
                    try: #getOS try block
                        print "*************************************"
                        print "OS DETECTION:"
                        if(self.platform.system()=="Windows"): #Detecting Windows
                            print self.platform.system()
                            print self.platform.win32_ver()
                        elif(self.platform.system()=="Linux"): #Detecting Linux
                            print self.platform.system()
                            print self.platform.dist()
                        elif(self.platform.system()=="Darwin"): #Detecting OSX
                            print self.platform.system()
                            print self.platform.mac_ver()
                        else:                           #Detecting an OS that is not listed
                            print self.platform.system()
                            print self.platform.version()
                            print self.platform.release()
                        print "*************************************"
                    except Exception as inst:
                        print "========================================================================================"
                        print "ERROR: An exception was thrown in getOS try block"
                        print type(inst) #the exception instance
                        print inst.args #srguments stored in .args
                        print inst #_str_ allows args tto be printed directly
                        print "========================================================================================"

                    #prompt user for the servers IP address
                    serverIPAddress= str(raw_input('What is the host (server) IP Address?'))
                    try:
                        print "Attempting to connect to server"
                        self.clientSocket.connect((serverIPAddress, self.port))
                        print "Successfully connected to server"
                    except self.socket.timeout as msg:
                        print "========================================================================================"
                        print "ERROR: the connection has timed out. Check to see if you entered the correct IP Address."
                        print "Error code: " + str(msg[0]) + " Message: " + msg[1]
                        print "Socket timeout set to: " + self.clientSocket.gettimeout + " seconds"
                        print "========================================================================================"
                    except self.socket.error as msg:
                        print "========================================================================================"
                        print "ERROR: Failed to connect to server"
                        print "Error code: " + str(msg[0]) + " Message: " + msg[1]
                        raise Exception("Failed to connect to server")
                        print "========================================================================================"

                    #Client primary while loop
                    try: #client primary while loop
                        while(serverSaysKeepSearching==True):
                            clientSocket.settimeout(2.0)
                            try: #checking for server commands try block
                                print "Checking for server commands..."
                                theInput= clientSocket.recv(2048)
                                if(theInput=="DONE"):
                                    print " "  #Make this line seperate from the other print statements
                                    print "Server has issued the DONE command."
                                    print " "
                                    serverSaysKeepSearching= False
                                    break

                            except socket.timeout as inst:
                                print "Socket timed out. No new server command"
                            except Exception as inst:
                                print "============================================================================================="
                                print "An exception was thrown in the checking for server commands Try Block"
                                print type(inst) #the exception instance
                                print inst.args #srguments stored in .args
                                print inst #_str_ allows args tto be printed directly
                                print "============================================================================================="

                            #keep performing task
                            #-------------------------
                                #INSERT TASK HERE
                            #-------------------------


                    except Exception as inst:
                        print "============================================================================================="
                        print "An exception was thrown in the Main Client Loop Try Block"
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

except Exception as inst:
    print "============================================================================================="
    print "An exception was thrown in the Master Try Block"
    print type(inst) #the exception instance
    print inst.args #srguments stored in .args
    print inst #_str_ allows args tto be printed directly
    print "============================================================================================="
finally:
    print "REMINDER: clientSocket is not defined outside of the networkClient class"
