__author__ = 'chris hamm'
#Created: 11/15/2014
#This is designed to run with NetworkClient_r7

#Updated on 11/16/2014 , still works with client_r7
#Updated on 11/17/2014, still works with client_r7
    #Added in crash handling/notification system  (STILL BEING CONSTRUCTED)
    

try: #Master try block
#=================================================================================================
#SERVER-CONTROLLER COMMUNICATION FUNCTIONS
#This section contains methods that the server will use to communicate with the controller class
#=================================================================================================
    try: #server-controller communication functions try block
        def add_controller_message_to_list(inputString): #call this function called from the controller class to send the server a message
            listOfControllerMessages.append(inputString) #store the string in the list
    except Exception as inst:
        print "============================================================================================="
        print "An exception was thrown in the Server-Controller Communication Functions Try Block"
        print type(inst) #the exception instance
        print inst.args #srguments stored in .args
        print inst #_str_ allows args tto be printed directly
        print "============================================================================================="
#=================================================================================================
#SERVER-CLIENT COMMUNICATION FUNCTIONS
#This section contains methods used by the server to communicate with the clients
#=================================================================================================
    try: #server-client communication functions try block
        print "Insert Function here"
    except Exception as inst:
        print "============================================================================================="
        print "An exception was thrown in the Server-Client Communication Functions Try Block"
        print type(inst) #the exception instance
        print inst.args #srguments stored in .args
        print inst #_str_ allows args tto be printed directly
        print "============================================================================================="
#=================================================================================================
#Main Server Loop
#=================================================================================================
    try: #Main sever loop try block
        import socket
        host= '' #Symbolic name, meaning all available interfaces
        port= 49200
        numOfClients= 0
        #socket.AF_INET is a socket address family represented as a pair. (hostname, port). This is the default parameter
        #socket.SOCK_STREAM is the default parameter. This defines the socket type
        serverSocket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        print "socket created successfully"
    except Exception as inst:
        print "============================================================================================="
        print "ERROR: An exception was thrown in the Main Server Try Block"
        print type(inst) #the exception instance
        print inst.args #srguments stored in .args
        print inst #_str_ allows args tto be printed directly
        print "============================================================================================="

    #Bind the socket to local host and port
    try: #Bind socket try block
        serverSocket.bind((host,port))
        print "Socket bind complete."
    except socket.error as inst:
        print "========================================================================================"
        print "ERROR: failed to bind (host, port) to serverSocket"
        print type(inst) #the exception instance
        print inst.args #srguments stored in .args
        print inst #_str_ allows args tto be printed directly
        print "========================================================================================"
        raise Exception("Could not bind to socket")

    #-----------------------------
    #INSERT method to get the cracking type from the controller HERE
    #Display the cracking method type HERE
    #-----------------------------
    try: #getIP tryblock
        print "The server's IP address is (THIS MAY NOT BE CROSS PLATFORM!!): "
        print "(This function works on Windows 7)"
        print socket.gethostbyname(socket.gethostname())
    except Exception as inst:
        print "========================================================================================"
        print "ERROR: An exception was thrown in getIP try block"
        print type(inst) #the exception instance
        print inst.args #srguments stored in .args
        print inst #_str_ allows args tto be printed directly
        print "========================================================================================"

    #Start listening to socket
    serverSocket.listen(5)
    print "Waiting for initial client to connect..."

    #list to store the socket and address of every client
    listOfClients = [] #This list is a list of tuples (socket, address)
    listOfControllerMessages = [] #holds a list of strings that have been sent by the controller class

    #Waiting for initial Client to connect
    sock, addr= serverSocket.accept()
    print "First client has connected"
    print "Connected with " + addr[0] + ":" + str(addr[1])
    listOfClients.append((sock, addr)) #add the tuple to the list of clients
    print "Client successfully added to the list of clients"
    print str(len(listOfClients)) + " Client(s) are currently Connected."

    #Server PRIMARY WHILE LOOP
    serverIsRunning = True
    try: #server primary while loop try block
        while(serverIsRunning==True): #server primary while loop

            #Check for input from clients
            print "Checking for input from client(s)..."
            try: #check for client input try block
                sock.settimeout(2.0)
                theInput = sock.recv(2048) #listening for input
                print "Received a message from a client."

            except socket.timeout as inst:
                print "========================================================================================"
                print "Socket has timed out. No input from client detected."
                print type(inst) #the exception instance
                print inst.args #srguments stored in .args
                print inst #_str_ allows args tto be printed directly
                print "========================================================================================"
            except Exception as inst:
                print "========================================================================================"
                print "ERROR: An exception has been thrown in the Check for client input Try Block"
                print type(inst) #the exception instance
                print inst.args #srguments stored in .args
                print inst #_str_ allows args tto be printed directly
                print "========================================================================================"

            #Check for input from controller class
            try: #check for input from controller try block
                print "Checking for input from the Controller class..."
                if(len(listOfControllerMessages) > 0): #if the list has something in it
                    print "Received the following input from the Controller class:"
                    for x in range (0, len(listOfControllerMessages)):
                        print str(listOfControllerMessages[x]) #print out the string
                    del listOfControllerMessages[:] #deletes all elements in the listOfControllerMessages
                    print "list of controller messages has been emptied"
                else:
                    print "No input was received from the Controller class"

            except Exception as inst:
                print "========================================================================================"
                print "ERROR: An exception has been thrown in the Check for input from Controller class Try Block"
                print type(inst) #the exception instance
                print inst.args #srguments stored in .args
                print inst #_str_ allows args tto be printed directly
                print "========================================================================================"

            #Distribute command to clients if needed
            try: #distribute command try block
                print "Checking to see if a command needs to be send to the clients..."
            except Exception as inst:
                print "========================================================================================"
                print "ERROR: An exception has been thrown in the Distribute command to clients Try Block"
                print type(inst) #the exception instance
                print inst.args #srguments stored in .args
                print inst #_str_ allows args tto be printed directly
                print "========================================================================================"

            #Check to see if another client is trying to connect
            try: #check to see if another client is trying to connect try block
                print "Checking to see if another client is trying to connect..."
                serverSocket.settimeout(2.0)
                sock, addr =serverSocket.accept()
                print "Connected with " + addr[0] + ":" + str(addr[1])
                listOfClients.append((sock, addr))
                print "Client successfully added to the list of clients"
                print str(len(listOfClients)) + " Client(s) are currently Connected."

            except socket.timeout as inst:
                print "========================================================================================"
                print "Socket timed out. No client is trying to connect."
                print type(inst) #the exception instance
                print inst.args #srguments stored in .args
                print inst #_str_ allows args tto be printed directly
                print "========================================================================================"
            except Exception as inst:
                print "========================================================================================"
                print "ERROR: An exception has been thrown in the Check to see if another client is trying to connect Try Block"
                print type(inst) #the exception instance
                print inst.args #srguments stored in .args
                print inst #_str_ allows args tto be printed directly
                print "========================================================================================"
        #END OF MAIN SERVER LOOP

    except Exception as inst:
        print "========================================================================================"
        print "ERROR: An exception has been thrown in the Server Primary While Loop Try Block"
        print type(inst) #the exception instance
        print inst.args #srguments stored in .args
        print inst #_str_ allows args tto be printed directly
        print "========================================================================================"

except Exception as inst:
    print "========================================================================================"
    print "ERROR: An exception has been thrown in the Master Try Block"
    print type(inst) #the exception instance
    print inst.args #srguments stored in .args
    print inst #_str_ allows args tto be printed directly
    print "========================================================================================"
    #insert send crash message to clients here
finally:
    print "Closing socket"
    serverSocket.close()
    print "listOfClients currently contains: "
    for x in range(0, len(listOfClients)):
        (sock, addr) = listOfClients[x]
        print " " + str(x) + ") socket:" + str(sock) + " address:" + str(addr)
        sock.sendall("DONE")
        print "Send DONE command to client"


