__author__ = 'chris hamm'
#Created on 11/10/2014
#NetwrokClient_r5

#This is designed to run with NetworkServer_r5 AND NetworkServer_r5_withThreading
#This revision is designed to use a single socket, and just change the ports

#Areas marked with @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ are areas that need to be changed to work in a more optimized fashion

#MASTER TRY BLOCK
try:
    import socket
    port= 49200
    clientSocket= socket.socket()
    #set the default timeout for trying to connect to a socket
    clientSocket.settimeout(20.0) #will time out after 20 seconds
    print("clientSocket was sucsessfully created");

    #prompt for the server's ip address
    serverIPAddress= str(raw_input('What is the host (server) IP Address?'))
    try:
        print("Attempting to connect to server");
        clientSocket.connect((serverIPAddress, port))
        print("Sucsessfully connected to server");
    except socket.timeout as msg:
        print("ERROR: the connection has timed out. Check to see if you entered the correct IP Address.");
        print("Error code: " + str(msg[0]) + " Message: " + msg[1]);
    except socket.error as msg:
        print("ERROR: Failed to connect to server");
        print("Error code: " + str(msg[0]) + " Message: " + msg[1]);

    #print server connection verification message, then send client verification message
    print clientSocket.recv(1024)
    clientSocket.send("CLIENT VERIFICATION: I am connected");
    print("Waiting for server instructions...");
    print "Received instructions: " + str(clientSocket.recv(1024))

    serverSaysKeepSearching= True #set to false when the node needs to be disconnected from network or is done
    while(serverSaysKeepSearching==True):
        #request for the next instruction set
        try: #Need to make into a function that can be called@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
            clientSocket.send("NEXT"); #requesting the next instruction set
            print("Requesting the NEXT instruction set...");
            print "Received instructions: " + str(clientSocket.recv(1024))
        except Exception as inst:
            print("ERROR: Exception thrown in request NEXT instruction set try block");
            print type(inst) #the exception instance
            print inst.args #srguments stored in .args
            print inst #_str_ allows args tto be printed directly
            serverSaysKeepSearching= False

        #check for the DONE command from the server
        try:
            inputServerCommand= clientSocket.recv(1024)
            if(inputServerCommand=="DONE"):
                print("Server has issued the DONE command.");
                serverSaysKeepSearching= False
                print("Telling server that this client has received the DONE command");
                clientSocket.send("Client has received DONE command, halting all searches");
                print("Program has finished");
        except Exception as inst:
            print("ERROR: An error has occurred in the check for servers DONE command try block");
            print type(inst) #the exception instance
            print inst.args #srguments stored in .args
            print inst #_str_ allows args tto be printed directly



#MASTER EXCEPTION BLOCK
except Exception as inst:
    print("An Exception has been thrown in the Master Try Block");
    print type(inst) #the exception instance
    print inst.args #srguments stored in .args
    print inst #_str_ allows args tto be printed directly
#MASTER FINALLY BLOCK
finally:
    print("Closing socket");
    clientSocket.close()