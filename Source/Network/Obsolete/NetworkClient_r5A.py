__author__ = 'chris hamm'
#Created on 11/11/2014
#NetwrokClient_r5A

#DONT USE THIS VERSION ANYMORE , USE R5 INSTEAD

#This is designed to run with NetworkServer_r5A
#This revision is designed to use a single socket, and just change the ports

#STILL NEEDS TO HAVE THE CLIENT TELLS THE SERVER THAT IT CRASHED!!!!!!
#STILL NEED TO LISTEN TO SEE IF SERVER CRASHED!!!!!!!!!!!
#OUT OF SYNC WITH THE SERVER WHEN DEBUGGING MESSAGES ARE TURNED OFF
#Areas marked with @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ are areas that need to be changed to work in a more optimized fashion

#MASTER TRY BLOCK
try:
    import socket
    port= 49200
    clientSocket= socket.socket()
    #set the default timeout for trying to connect to a socket
    clientSocket.settimeout(15.0) #will time out after 15 seconds
    print("clientSocket was sucsessfully created");

    #prompt user if they want debugging messages turned on
    showDebuggingMessages= str(raw_input('Do you want to display the debugging messages? (Enter in corresponding numeral) \n'
                                         '1) Yes \n'
                                         '2) No (This option DOES NOT WORK, it throws an error and CRASHES) \n'))
    if(showDebuggingMessages=="1"):
        print("Debugging messages are turned ON");
    elif(showDebuggingMessages=="2"):
        print("Debugging messages are turned OFF");
    else:
        print("ERROR: Invalid input. Defaulting to debugging messages turned ON");
        showDebuggingMessages="1"

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
        print("========================================================================================");

    #print server connection verification message, then send client verification message
    if(showDebuggingMessages=="1"):
        print clientSocket.recv(1024)
    else:
        serverVerification= clientSocket.recv(1024)

    clientSocket.send("CLIENT VERIFICATION: I am connected");
    print("Waiting for server instructions...");
    if(showDebuggingMessages=="1"):
        print "Received instructions: " + str(clientSocket.recv(1024))

    serverSaysKeepSearching= True #set to false when the node needs to be disconnected from network or is done
    while(serverSaysKeepSearching==True):
        #request for the next instruction set
        try: #Need to make into a function that can be called@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
            clientSocket.send("NEXT"); #requesting the next instruction set
            print("Requesting the NEXT instruction set...");
            if(showDebuggingMessages=="1"):
                print "Received instructions: " + str(clientSocket.recv(1024))
            else:
                myNewInstructions= clientSocket.recv(1024)
        except socket.timeout as msg:
            print("========================================================================================");
            print("ERROR: the connection has timed out. Thrown from inside request NEXT instruction set try block");
            print("Error code: " + str(msg[0]) + " Message: " + msg[1]);
            print("Socket timeout set to: " + clientSocket.gettimeout + " seconds");
            serverSaysKeepSearching= False
            print("========================================================================================");
        except Exception as inst:
            print("========================================================================================");
            print("ERROR: Exception thrown in request NEXT instruction set try block");
            print type(inst) #the exception instance
            print inst.args #srguments stored in .args
            print inst #_str_ allows args tto be printed directly
            serverSaysKeepSearching= False
            #raise Exception("manual error 2 being thrown")
            print("========================================================================================");

        #check for the DONE command from the server
        try:
            inputServerCommand= clientSocket.recv(1024)
            if(inputServerCommand=="DONE"):
                if(showDebuggingMessages=="1"):
                    print("Server has issued the DONE command.");
                serverSaysKeepSearching= False
                if(showDebuggingMessages=="1"):
                    print("Telling server that this client has received the DONE command");
                clientSocket.send("Client has received DONE command, halting all searches");
                print("Program has finished by the DONE command");
            else:
                print("server command is not DONE");
        except socket.timeout as msg:
            print("========================================================================================");
            print("ERROR: the connection has timed out. Thrown inside check for servers DONE command try block");
            print("Error code: " + str(msg[0]) + " Message: " + msg[1]);
            print("Socket timeout set to: " + clientSocket.gettimeout + " seconds");
            serverSaysKeepSearching= False
            print("========================================================================================");
        except Exception as inst:
            print("========================================================================================");
            print("ERROR: An error has occurred in the check for servers DONE command try block");
            print type(inst) #the exception instance
            print inst.args #srguments stored in .args
            print inst #_str_ allows args tto be printed directly
            serverSaysKeepSearching= False
            #raise Exception("manual error 1 being thrown")
            print("========================================================================================");



#MASTER EXCEPTION BLOCK
except Exception as inst:
    print("========================================================================================");
    print("An Exception has been thrown in the Master Try Block");
    print type(inst) #the exception instance
    print inst.args #srguments stored in .args
    print inst #_str_ allows args tto be printed directly
    print("========================================================================================");
#MASTER FINALLY BLOCK
finally:
    print("Closing socket");
    clientSocket.close()