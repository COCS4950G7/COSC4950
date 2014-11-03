__author__ = 'Chris_Hamm'
#NetworkServer_r2
#CREATED ON NOV 2 2014

    #Nov 1 2014 Chris Hamm (FROM PREVIOUS REVISION)
            # Added the basic connection code
            # Server now stores the IP addresses of all the connect nodes
            # Server now prompts user for how many nodes there will be
            # Server waits for all nodes to connect
            # Multiple new status lines have been added in for debugging purposes
            # Server has exception handling while waiting for nodes to connect

    #Nove 2 2014 Chris Hamm (CURRENT REVISION)
            #(UNTESTED) If server throws an exception, it sends a message to all nodes before closing the socket
            #(UNTESTED) Server prompts user to select what type of cracking method you will be performing
            #(UNTESTED) Server informs the client nodes about what cracking mode the server is running

#STARTUP SERVER#########################
import socket #import the socket module
socketObject= socket.socket() #create a socket object
port= 12397 #reserving a port for the service
socketObject.bind(('',port)) #bind to port

#PROMPT USER FOR NUMBER OF NODES AND WHAT MODE (BF, DICTIONARY,ETC)##############################
numOfNodes = int(raw_input('How many nodes will there be? ')) #store how many nodes there will be
print ("Number of Nodes: " + str(numOfNodes)); #tell user how many nodes have been set to wait for
print ("Now waiting for nodes to connect.");

#PROMPT USER FOR WHAT MODE WILL THE SERVER BE RUNNING
typeOfCracking = int(raw_input('What cracking method are you using? (Enter the appropriate Number) \n '
                               '1) Brute-Force \n' #1 represents Brute-Force
                               '2) Dictionary \n' #2 represents Dictionary Attacks
                               '3) Rainbow Tables')) #3 represents Rainbow Tables


#(client-side task: startup the nodes
#(client-side task: say "hi" to server)
#WAIT FOR ALL NODES TO CONNECT#######################
numOfConnectedNodes = int(0) #a counter to count how many nodes have connected
listOfConnectedIPAddresses = []; #contains the ip addresses of all connected nodes
socketObject.listen(5) #wait for client connection
while True:
    c,addr = socketObject.accept() #Establish a connection with the client
    print "Got connection from", addr
    listOfConnectedIPAddresses.append(addr) #add the node's ip address to the list
    c.send("Your IP address (" + str(addr) + ") has been added to the servers List!")
    print ("The node IP " + str(addr) + " has been added to the listOfConnectedIPAddresses");
    #TELL CLIENTS WHAT MODE THE SERVER IS RUNNING
    if(typeOfCracking == 1):
        c.send("Server is in Brute-Force Mode");
    elif(typeOfCracking == 2):
        c.send("Server is in Dictionary Mode");
    elif(typeOfCracking == 3):
        c.send("Server is in Rainbow Table Mode");
    else:
        print("ERROR: invalid typeOfCracking value");
    c.send("Thank you for connecting!")
    numOfConnectedNodes += 1 #increment numOfConnectedNodes

    #ARE ALL NODES CONNECTED?#####################
    try:
        #IF NO, CONTINUE TO WAIT
        if(numOfNodes - numOfConnectedNodes > 0):
            c.send("Still waiting for " + str(numOfNodes - numOfConnectedNodes) + " nodes to connect." )
            print("Still waiting for " + str(numOfNodes - numOfConnectedNodes) + " nodes to connect.");
        #(client side task: wait for server to reply)
        #IF YES,THEN SAY "return hi" TO ALL NODES
        else:
            print("Still waiting for " + str(numOfNodes - numOfConnectedNodes) + " nodes to connect.");
            print("All nodes have connected to the server!");
            c.close() #OMIT THIS IN FUTURE!!!!
    except Exception as inst:
        print ("An Exception was thrown");
        c.send("Server: An Exception has been thrown. Server shutting down."); #display message to all nodes that the server had an error
        print type(inst) #the exception instance
        print inst.args #srguments stored in .args
        print inst #_str_ allows args tto be printed directly
        c.close()


#SPLIT WORKLOAD INTO MANY EQUALLY SIZED PIECES###############################


#(client-side task: wait for server command or Done)
#GIVE PIECE OF WORKLOAD TO EACH NODE##########################################

#(client-side task: executing server command)
#WAIT FOR A NODE TO REPLY############################################

    #DID NODE FIND A MATCH?################

        #(client-side task: wait for server command or done)
        #IF YES, THEN TELL ALL NODES "done" PLUS THE RESULTS

        #IF NO,THEN:

            #DID NODE REPORT NO MATCH FOUND?##############

                #IF YES, THEN GIVE THE NODE ANOTHER PIECE OF THE WORKLOAD (IF ANY REMAINS)
                #THEN, CONTINUE TO WAIT

                #IF NO, THEN:

                    #DID THE NODE GIVE A STATUS UPDATE?#################

                        #IF NO, THEN CONTINUE TO WAIT

                        #IF YES, UPDATE THE PROGRESS DISPLAY
                        #THEN CONTINUE WAITING
