__author__ = 'chris hamm'
#sucessor to networkserver_r5
#modified version of r5 that makes the next and done commands functions
#corresponds with network client_r5A

#This revision is not designed to use the special classes that r4 used.
#Sucsessfully connects with a single client and multiple clients!
#Will give clients the NEXT instruction set, when the client requests it

#STILL NEED TO SEND CLIENT A CRASH MESSAGE IF SERVER CRASHES
#STILL NEED TO LISTEN TO SEE IF A CLIENT HAS CRASHED

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

    #ask if debugging messages should be shown
    showDebuggingMessages= str(raw_input('Do you want to display debugging messages? (Enter in the corresponding numeral) \n'
                                         '1) Yes \n'
                                         '2) No \n'))
    if(showDebuggingMessages == "1"):
        print("Debugging messages are turned ON");
    elif(showDebuggingMessages == "2"):
        print("Debugging messages are turned OFF");
    else:
        print("ERROR: Invalid input. Defaulting to Debugging messages turned ON");
        showDebuggingMessages= "1"


    #Bind socket to local host and port
    try:
        serverSocket.bind((host, port))
    except socket.error as msg:
        print("========================================================================================");
        print("ERROR: failed to bind (host, port) to serverSocket");
        print("Error code: " + str(msg[0]) + " Message: " + msg[1]);
        print("========================================================================================");

    if(showDebuggingMessages=="1"):
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
        if(showDebuggingMessages=="1"):
            print("Running Server/Client verification test...");
        theClient.sendto("SERVER VERIFICATION: You are connected", addr);
        if(showDebuggingMessages=="1"):
            print theClient.recv(1024)
        else:
            clientVerify= theClient.recv(1024)
        numOfClients= 1 + numOfClients
        if(showDebuggingMessages=="1"):
            print("Server/Client verification test complete");
        print("Sending client instructions");
        theClient.sendto("Test instruction set", addr);
        print(str(numOfClients) + " clients are connected");

        #if client requests more instructions keyword:NEXT
        try:
            clientRequest = theClient.recv(1024)
            if(clientRequest=="NEXT"):
                if(showDebuggingMessages=="1"):
                    print("Client requested the NEXT instruction set");
                theClient.send("2nd test instruction set");
                if(showDebuggingMessages=="1"):
                    print("Sent client the NEXT instruction set");
                #Need to make this a function that can be called@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
                #Uses the keyword DONE
        #        if(showDebuggingMessages=="1"):
         #           print("Sending the client the DONE command");
         #       #Need to make sure this sends the message to all of the clients@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
                theClient.sendall("DONE");
          #      if(showDebuggingMessages=="1"):
           #         print("DONE command was sent to client");
          #      print("The following clients have stopped from the DONE command:");
           #     #insert for loop here corresponding to numOfClients variable @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
          #      #NEED TO HAVE ERROR Checking here!!!!! what is i dont receive the proper response from client@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
          #      print "Received message: " + theClient.recv(1024)
            elif(clientRequest=="Client has received DONE command, halting all searches"):
                if(showDebuggingMessages=="1"):
                    print("Entered the elif client has received DONE command statement");
            else:
                print("clientRequest was not a NEXT");

        except Exception as inst:
            print("========================================================================================");
            print("ERROR: Exception was thrown in client requests NEXT try block");
            print type(inst) #the exception instance
            print inst.args #srguments stored in .args
            print inst #_str_ allows args tto be printed directly
            print("========================================================================================");


#MASTER EXCEPTION BLOCK
except Exception as inst:
    print("========================================================================================");
    print("ERROR: An exception has been thrown in the Master Try Block");
    print type(inst) #the exception instance
    print inst.args #srguments stored in .args
    print inst #_str_ allows args tto be printed directly
    print("========================================================================================");
#MASTER FINALLY BLOCK
finally:
    print("Closing all sockets");
    serverSocket.close()