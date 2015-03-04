__author__ = 'chris hamm'
#NetworkServer_r5B
#Designed to work with NetworkClient_r5B

#This is a varient of NetworkServer_r5 that has been structured in a more modular fashion

#===========================================================================================
#SERVER COMMANDS
# This section defines what the server commands are and what they do (for example the DONE command)
#===========================================================================================
try: #Server Commands try block
    #The DONE Command: This function sends all clients the DONE command along with a message from the server
    def sendDoneCommand(additionalMessage, messageRecipient):
        serverSocket.sendto("DONE", messageRecipient); #issueing the DONE command
        serverSocket.sendto(additionalMessage, messageRecipient); #sending the additional message

    def sendConnectionVerification(messageRecipient):
        serverSocket.sendto("SEVER CONNECTION VERIFICATION MESSAGE", messageRecipient);

except Exception as inst:
    print("=============================================================================================");
    print("An exception was thrown in the Server Commands Try Block");
    print type(inst) #the exception instance
    print inst.args #srguments stored in .args
    print inst #_str_ allows args tto be printed directly
    print("=============================================================================================");


#============================================================================================
#SERVER INPUT CHECKS
#This section has functions that the server will use to check what the input from the client was,
# so the server can respond accordingly. For example: receiving the NEXT command , server needs to give client more cracking material
#============================================================================================
try: #server input checks try block

    def checkForNextCommand(theInput):
        print("Checking For the Next Command...");
        if(theInput == "NEXT"):
            return True
        else:
            return False

    def checkForFoundSolutionCommand(theInput):
        print("Checking For the Found Solution Command...");
        if(theInput== "FOUNDSOLUTION"):
            return True
        else:
            return False

    def checkForEmptyInput(theInput): #see if the input is empty
        print("Checking to see if input is empty...");
        if(theInput== ""):
            return True
        else:
            return False

except Exception as inst:
    print("=============================================================================================");
    print("An exception was thrown in the Server Input Checks Try Block");
    print type(inst) #the exception instance
    print inst.args #srguments stored in .args
    print inst #_str_ allows args tto be printed directly
    print("=============================================================================================");

#============================================================================================
#MAIN SERVER LOOP
# This is the main loop that the server goes through, listening for client requests, accepting new clients and more
#============================================================================================
try: #Main server loop try block
    import socket
    import random
    host= '' #Symbolic name, meaning all available interfaces
    port= 49200
    numOfClients= 0
    #socket.AF_INET is a socket address family represented as a pair. (hostname, port). This is the default parameter
    #socket.SOCK_STREAM is the default parameter. This defines the socket type
    serverSocket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #serverSocket.setblocking(0)

    print("Socket was created successfully");

    #Bind the socket to local host and port
    try: #Bind socket try block
        serverSocket.bind((host,port))
        print("Socket bind complete.");
    except socket.error as inst:
        print("========================================================================================");
        print("ERROR: failed to bind (host, port) to serverSocket");
        print type(inst) #the exception instance
        print inst.args #srguments stored in .args
        print inst #_str_ allows args tto be printed directly
        print("========================================================================================");
        raise Exception("Could not bind to socket")

    #Start listening to socket
    serverSocket.listen(5)
    print("Now waiting for the initial client to connect...");

    #WAIT FOR FIRST CLIENT TO CONNECT
    #wait for client to connect

    theNewClient, addr= serverSocket.accept()
    print("First client has connected");
    print("Connected with " + addr[0] + ":" + str(addr[1]));


    #The servers primary while loop
    serverIsRunning= True #set to false to exit the while loop
    try: #Server primary while loop try block
        while(serverIsRunning==True):
            #CHECK FOR CLIENT COMMAND INPUTS
            #check to see if FOUNDSOLUTION was received
            try: #check for command  inputs try block

                print("Checking for input from client(s)...");
                theNewClient.settimeout(5.0)
                try:
                    theInput= theNewClient.recv(1024) #GETS STUCK HERE
                                                #2ndary error, need a new name for each new client
                    if(checkForFoundSolutionCommand(theInput) == True):
                        print("FOUNDSOLUTION command has been received!");
                    #check to see if NEXT command was received
                    elif(checkForNextCommand(theInput) == True):
                        print("NEXT command has been received!");
                    #check to see if theInput is empty
                    elif(checkForEmptyInput(theInput) == True):
                        print("theInput is Empty!");
                except socket.timeout as inst:
                    print("========================================================================================");
                    print("ERROR: Socket timed out. No input was detected.");
                    print type(inst) #the exception instance
                    print inst.args #srguments stored in .args
                    print inst #_str_ allows args tto be printed directly
                    print("========================================================================================");

            except Exception as inst:
                print("========================================================================================");
                print("ERROR: problem inside the check for command inputs try block");
                print type(inst) #the exception instance
                print inst.args #srguments stored in .args
                print inst #_str_ allows args tto be printed directly
                print("========================================================================================");
            #DISTRIBUTE COMMAND TO CLIENTS IF NEEDED
            try: #distribute command to clients try block
                magicNumber= random.randrange(0,5) #including zero but smaller than five
                if(magicNumber==0):
                    print "Server did not issue any commands"
                elif(magicNumber==1):
                    print "Server has issued the DONE command"
                    theNewClient.sendall("DONE")
                    print "DONE command successfully sent"
                    serverIsRunning=False
                    print "Server is no longer running. Job finished."
                    break
                else:
                    print "Server did not issue any commands"

            except Exception as inst:
                print("========================================================================================");
                print("ERROR: problem inside the distribute command to clients try block");
                print type(inst) #the exception instance
                print inst.args #srguments stored in .args
                print inst #_str_ allows args tto be printed directly
                print("========================================================================================");

            #CHECK TO SEE IF ANOTHER CLIENT IS TRYING TO CONNECT
            #wait for client to connect
            try: #check to see if another client is trying to connect
                serverSocket.settimeout(2.0)
                print("Checking to see if more clients are trying to connect...");
                theNewClient, addr= serverSocket.accept()
                print("Connected with " + addr[0] + ":" + str(addr[1]));
            except socket.timeout as inst:
                print("========================================================================================");
                print("ERROR: socket timed out. No clients are trying to connect");
                print type(inst) #the exception instance
                print inst.args #srguments stored in .args
                print inst #_str_ allows args tto be printed directly
                print("========================================================================================");
            except Exception as inst:
                print("========================================================================================");
                print("ERROR: problem finding additional client to connect");
                print type(inst) #the exception instance
                print inst.args #srguments stored in .args
                print inst #_str_ allows args tto be printed directly
                print("========================================================================================");


    except Exception as inst:
        print("=============================================================================================");
        print("An exception was thrown in Servers Primary While Loop Try Block");
        print type(inst) #the exception instance
        print inst.args #srguments stored in .args
        print inst #_str_ allows args tto be printed directly
        serverIsRunning=False
        print("=============================================================================================");

except Exception as inst:
    print("=============================================================================================");
    print("An exception was thrown in the Main Server Loop Try Block");
    print type(inst) #the exception instance
    print inst.args #srguments stored in .args
    print inst #_str_ allows args tto be printed directly
    print("=============================================================================================");
finally:
    #print("Sending DONE command to clients");
    #sendDoneCommand("The Server has thrown an exception",addr);
    print("Closing the socket");
    serverSocket.close()