__author__ = 'chris hamm'
#NetworkClient_r5B
#Designed to work with NetworkServer_r5B

#DONT USE THIS VERSION ANYMORE , USE R5 INSTEAD

#This is a varient of NetworkClient_r5 that has been structured in a more modular fashion

#==============================================================================================
#CLIENT COMMANDS
#This section defines what the client commands are and what they do
#==============================================================================================
try: #Client Command try block
   #The NEXT command: tells the server to give the client the next part of the cracking problem.
    def sendNextCommand(resultsOfCurrentPart):
        clientSocket.send("NEXT");
        clientSocket.send(resultsOfCurrentPart); #tell the server what you results where

except Exception as inst:
    print("=============================================================================================");
    print("An exception was thrown in the Client Commands Try Block");
    print type(inst) #the exception instance
    print inst.args #srguments stored in .args
    print inst #_str_ allows args tto be printed directly
    print("=============================================================================================");

#================================================================================================
#CLIENT INPUT CHECKS
#This section contains functions that will check the input from the server
#=================================================================================================
try: #Client input checks try block

    def checkForDoneCommand(theInput): #see if the input is the DONE command
        #print("Checking for the DONE command...");
        if(theInput == "DONE"):
            return True
        else:
            return False
except Exception as inst:
    print("=============================================================================================");
    print("An exception was thrown in the Client Inputs Check Try Block");
    print type(inst) #the exception instance
    print inst.args #srguments stored in .args
    print inst #_str_ allows args tto be printed directly
    print("=============================================================================================");
#================================================================================================
#MAIN CLIENT Setup
#This is the main loop the client goes through
#================================================================================================
try: #main client setup try block
    import socket
    port= 49200
    clientSocket= socket.socket()
    #set the default timeout for trying to connect to a socket
    #clientSocket.settimeout(15.0) #will time out after 15 seconds
    print("clientSocket was sucsessfully created");

    #prompt for the server's ip address
    serverIPAddress= str(raw_input('What is the host (server) IP Address?'))
    try:
        print("Attempting to connect to server");
        clientSocket.connect((serverIPAddress, port))
        print("Sucsessfully connected to server");
    except socket.timeout as msg:
        print("========================================================================================");
        print("ERROR: the connection has timed out. Check to see if you entered the correct IP Address.");
        print("Error code: " + str(msg[0]) + " Message: " + msg[1]);
        print("Socket timeout set to: " + clientSocket.gettimeout + " seconds");
        print("========================================================================================");
    except socket.error as msg:
        print("========================================================================================");
        print("ERROR: Failed to connect to server");
        print("Error code: " + str(msg[0]) + " Message: " + msg[1]);
        raise Exception("Failed to connect to server")
        print("========================================================================================");

    #CLIENT PRIMARY WHILE LOOP
    serverSaysKeepSearching= True
    try: #client primary while loop try block
        while(serverSaysKeepSearching==True):
            #check for server command inputs
            clientSocket.settimeout(5.0)
            try:
                theInput= clientSocket.recv(1024)
                if(checkForDoneCommand(theInput) == True):
                    print("Server has issued the DONE command.");
                    serverSaysKeepSearching= False
                    break
            except socket.timeout as inst:
                print("=============================================================================================");
                print("ERROR: Socket has timed out. No server command has been received.");
                print type(inst) #the exception instance
                print inst.args #srguments stored in .args
                print inst #_str_ allows args tto be printed directly
                print("=============================================================================================");
            except Exception as inst:
                print("=============================================================================================");
                print("An exception was thrown in the check for server commands input Try Block");
                print type(inst) #the exception instance
                print inst.args #srguments stored in .args
                print inst #_str_ allows args tto be printed directly
                print("=============================================================================================");

            #keep performing task
            try: #performing task try block
                print "Crunching numbers..."
            except Exception as inst:
                print("=============================================================================================");
                print("An exception was thrown in the Performing task Try Block");
                print type(inst) #the exception instance
                print inst.args #srguments stored in .args
                print inst #_str_ allows args tto be printed directly
                print("=============================================================================================");

    except Exception as inst:
        print("=============================================================================================");
        print("An exception was thrown in the Primary Client While Loop Try Block");
        print type(inst) #the exception instance
        print inst.args #srguments stored in .args
        print inst #_str_ allows args tto be printed directly
        print("=============================================================================================");

except Exception as inst:
    print("=============================================================================================");
    print("An exception was thrown in the Main Client Setup Try Block");
    print type(inst) #the exception instance
    print inst.args #srguments stored in .args
    print inst #_str_ allows args tto be printed directly
    print("=============================================================================================");
finally:
    print "Closing the socket"
    clientSocket.close()