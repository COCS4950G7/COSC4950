__author__ = 'chris hamm'
#Created on 11/10/2014
#NetworkServer_r5_withThreading

#This revision is not designed to use the special classes that r4 used.
#Sucsessfully connects with a single client (Untested for multiple clients)
#NOT AS COMPLETE AS THE NORMAL r5 VERSION
#This special version of r5 handles clients with threads*********************

#NOTE!!!!!!!!!!!
#RUNS BUT CRASHES AFTER FIRST CLIENT CONNECTS WITH AN UNHANDLED EXCEPTION ERROR AND BAD FILE DESCRIPTOR ERROR

#MASTER TRY BLOCK
try:
    import socket
    import sys #used for the exit command
    from thread import * #used for start_new_thread
    host= '' #Symbolic name, meaning all available interfaces
    port= 49200
    #socket.AF_INET is a socket address family represented as a pair. (hostname, port). This is the default parameter
    #socket.SOCK_STREAM is the default parameter. This defines the socket type
    serverSocket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket was created sucsessfully");

    #Bind socket to local host and port
    try:
        serverSocket.bind((host, port))
    except socket.error as msg:
        print("ERROR: failed to bind (host, port) to serverSocket");
        print("Error code: " + str(msg[0]) + " Message: " + msg[1]);

    print("Socket bind complete");

    #Start listening to socket
    serverSocket.listen(5)
    print("serverSocket is now listening");

    #THIS IS THE THREADING FUNCTION THAT WAS ADDED FOR THIS SPECIAL REVISION
    #This function handles connections. This is used to create threads
    def clientThread(theClient):
        print("Server has entered the clientThread function");

        #infinite loop so that function does not terminate and thread does not end
        while True:
            #receive message from client
            clientData= theClient.recv(1024)
            print("Server has received message from client");
            reply = "Server received the message " + clientData
            if not clientData:
                print("Not clientData");
                break

            theClient.sendall(reply)
            print("Send reply message to client");

        #came out of infinite loop
            theClient.close()
            print("closed theClient inside clientThread function");

    #END OF THREADING FUNCTION

    #Now keep Talking to the client
    serverRunning= True
    while(serverRunning== True):
        #wait to accept connection
        theClient, addr= serverSocket.accept()
        #addr[0] is the ip address
        #addr[1] port number???
        print("Connected with " + addr[0] + ":" + str(addr[1]))
        #start new thread takes 1st arguement as a function name to be run, the second is the tuple of arguements to the function.
        start_new_thread(clientThread, (theClient,))
        print("New thread has been started");
        #verify that the server and client are connected
        theClient.sendto("SERVER VERIFICATION: You are connected", addr);
        print theClient.recv(1024) #listen for client verification

#MASTER EXCEPTION BLOCK
except Exception as inst:
    print("ERROR: An exception has been thrown in the Master Try Block");
    print type(inst) #the exception instance
    print inst.args #srguments stored in .args
    print inst #_str_ allows args tto be printed directly
#MASTER FINALLY BLOCK
finally:
    print("Closing all sockets");
    serverSocket.close()