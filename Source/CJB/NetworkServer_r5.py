__author__ = 'chris hamm'
#Created on 11/10/2014
#NetworkServer_r5

#This revision is not designed to use the special classes that r4 used.
#Sucsessfully connects with a single client and multiple clients!
#Will give clients the NEXT instruction set, when the client requests it

#Areas marked with @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ are areas that need to be changed to work more in an optimized fashion

#MASTER TRY BLOCK
try:
    import socket
    host= '' #Symbolic name, meaning all available interfaces
    port= 49200
    numOfClients= 0
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

    #Talk to the client
    serverRunning= True
    while(serverRunning== True):
        #wait to accept connection
        theClient, addr= serverSocket.accept()
        #addr[0] is the ip address
        #addr[1] port number???
        print("Connected with " + addr[0] + ":" + str(addr[1]))
        #verify that the server and client are connected
        print("Running Server/Client verification test...");
        theClient.sendto("SERVER VERIFICATION: You are connected", addr);
        print theClient.recv(1024)
        numOfClients= 1 + numOfClients
        print("Server/Client verification test complete");
        print("Sending client instructions");
        theClient.sendto("Test instruction set", addr);
        print(str(numOfClients) + " clients are connected");

        #if client requests more instructions keyword:NEXT
        try:
            clientRequest = theClient.recv(1024)
            if(clientRequest=="NEXT"):
                print("Client requested the NEXT instruction set");
                theClient.send("2nd test instruction set");
                print("Sent client the NEXT instruction set");
                #Need to make this a function that can be called@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
                #Uses the keyword DONE
                print("Sending the client the DONE command");
                #Need to make sure this sends the message to all of the clients@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
                theClient.sendall("DONE");
                print("DONE command was sent to client");
                print("The following clients have stopped:");
                #insert for loop here corresponding to numOfClients variable @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
                print "Received message: " + theClient.recv(1024)

        except Exception as inst:
            print("ERROR: Exception was thrown in client requests NEXT try block");
            print type(inst) #the exception instance
            print inst.args #srguments stored in .args
            print inst #_str_ allows args tto be printed directly


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