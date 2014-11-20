__author__ = 'chris hamm'
#NetworkClient_r7A
#Created: 11/19/2014

#===================================================================================
#REVISION NOTES:
#   This revision takes the code from NetworkClient_r7 and modifies it to fit our
#   new design layout using the controller class.
#   This is designed to work with NetworkServer_r7A
#   NetworkClient_r8 has been abandoned.
#===================================================================================

#-----------------------------------------------------------------------------------
#NOTES FROM THE CONTROLLER CLASS:

#client receives the user-inputted server IP as a string
#once client connects to server, client sends over the pipe "connected" to the controller

#COMMANDS THAT THE CONTROLLER WILL ACCEPT
#   "done"
#       -controller joins subprocess and goes back to the start screen
#   "connected"
#       -controller prints "nodeConnectedToScreen" ie: does nothing
#   "doingStuff"
#       -controller prints "nodeDoingStuffScreen" ie: does nothing
#-------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------
#NOTES FROM THE SERVER:
#
#COMMANDS THE SERVER WILL ACCEPT
#   "NEXT"
#       -the server will give the client the next part of the cracking problem
#   "FOUNDSOLUTION"
#       -the server will issue the DONE command to all of the clients
#   "CRASHED"
#       -the client is telling the server that it (the client) has crashed
#   "INVALIDCOMMAND"
#       -if the client receives an invalid command, it returns this string to the server
#-------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------------
#COMMANDS/THINGS THE CLIENT WILL ACCEPT
#   "DONE"
#       -server issues the done command to all clients and all clients stop what they are doing
#   the next part of the cracking problem
#       -server gives the client the next part of the cracking problem
#   "INVALIDCOMMAND"
#       -if the server receives an invalid command from the client, then the server returns this string
#-------------------------------------------------------------------------------------------

try: #Master try block
#======================================================================================
#CLIENT-CONTROLLER COMMUNICATION FUNCTIONS
#This section contains methods the client will use to communicate with the controller class
#======================================================================================
    try: #client-controller communication functions try block
        print "Insert functions here"
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
        def sendNextCommandToServer():
            clientSocket.send("NEXT") #sends the NEXT command to the serve
            print "The NEXT command was sent to the server"

            #FOUNDSOLUTION
        def sendFoundSolutionToServer():
            clientSocket.send("FOUNDSOLUTION") #sends the FOUNDSOLUTION command to the server
            print "The FOUNDSOLUTION command was sent to the server"

            #CRASHED
        def sendCrashedCommandToServer():
            clientSocket.send("CRASHED") #sends the CRASHED command to the server
            print "The CRASHED command was sent to the server"

            #INVALIDCOMMAND
        def sendInvalidCommandToServer():
            clientSocket.send("INVALIDCOMMAND") #sends INVALIDCOMMAND command to server
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

#======================================================================================
#Main Client Loop
#======================================================================================
    try: #Main client loop try block
        import socket
        port= 49200
        clientSocket= socket.socket()
        print "clientSocket successfully created"

        #prompt user for the servers IP address
        serverIPAddress= str(raw_input('What is the host (server) IP Address?'))
        try:
            print "Attempting to connect to server"
            clientSocket.connect((serverIPAddress, port))
            print "Successfully connected to server"
        except socket.timeout as msg:
            print "========================================================================================"
            print "ERROR: the connection has timed out. Check to see if you entered the correct IP Address."
            print "Error code: " + str(msg[0]) + " Message: " + msg[1]
            print "Socket timeout set to: " + clientSocket.gettimeout + " seconds"
            print "========================================================================================"
        except socket.error as msg:
            print "========================================================================================"
            print "ERROR: Failed to connect to server"
            print "Error code: " + str(msg[0]) + " Message: " + msg[1]
            raise Exception("Failed to connect to server")
            print "========================================================================================"

        #Client primary while loop
        serverSaysKeepSearching= True
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
                    #I commented the extra print lines out to make this look more clean
                   # print "============================================================================================="
                    print "Socket timed out. No new server command"
                   # print type(inst) #the exception instance
                   # print inst.args #srguments stored in .args
                   # print inst #_str_ allows args tto be printed directly
                   # print "============================================================================================="
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

except Exception as inst: #Exception for Master Try Block
    print "============================================================================================="
    print "An exception was thrown in Master Try Block"
    print type(inst) #the exception instance
    print inst.args #srguments stored in .args
    print inst #_str_ allows args tto be printed directly
    print "============================================================================================="
finally:
    print "Closing socket"
    clientSocket.close()
