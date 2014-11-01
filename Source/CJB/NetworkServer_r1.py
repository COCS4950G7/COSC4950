__author__ = 'chris'
#chris hamm
#networkServer_r1
#CREATED: 10/22/2014
#ER Diagram of this is available, talk to Chris Hamm if you want a copy.

#IMPORTANT NOTE: NEED TO INSERT A CHECK TO SEE IF THERE IS NO MORE WORKLOAD TO DISTRIBUTE AND ALL NODES HAVE REPORTED
#NO MATCH FOUND. NEED TO HAVE THE PROGRAM DISPLAY A MESSAGE SAYING THAT THE HASH WAS NOT FOUND

    #Nov 1 2014 Chris Hamm
        # Added the basic connection code
        # Server now stores the IP addresses of all the connect nodes
        # Server now prompts user for how many nodes there will be
        # Server waits for all nodes to connect
        # Multiple new status lines have been added in for debugging purposes


#STARTUP SERVER#########################
import socket #import the socket module
socketObject= socket.socket() #create a socket object
port= 12397 #reserving a port for the service
socketObject.bind(('',port)) #bind to port

#PROMPT USER FOR NUMBER OF NODES AND WHAT MODE (BF, DICTIONARY,ETC)##############################
numOfNodes = raw_input('How many nodes will there be?') #store how many nodes there will be
print ("Number of Nodes: " + str(numOfNodes)); #tell user how many nodes have been set to wait for
print ("Now waiting for nodes to connect");
#(client-side task: startup the nodes
#(client-side task: say "hi" to server)
#WAIT FOR ALL NODES TO CONNECT#######################
numOfConnectedNodes = 0 #a counter to count how many nodes have connected
listOfConnectedIPAddresses = []; #contains the ip addresses of all connected nodes
socketObject.listen(5) #wait for client connection
while True:
    c,addr = socketObject.accept() #Establish a connection with the client
    print "Got connection from", addr
    listOfConnectedIPAddresses.append(addr) #add the node's ip address to the list
    c.send("Your IP address (" + str(addr) + ") has been added to the servers List!")
    print ("The node IP " + str(addr) + " has been added to the listOfConnectedIPAddresses");
    c.send("Thank you for connecting!")
    ++numOfConnectedNodes #increment numOfConnectedNodes

    #ARE ALL NODES CONNECTED?#####################

    #IF NO, CONTINUE TO WAIT
    if((numOfNodes - numOfConnectedNodes) > 0):
        c.send("Still waiting for " + str(numOfNodes - numOfConnectedNodes) + " nodes to connect." )
        print("Still waiting for " + str(numOfNodes - numOfConnectedNodes) + " nodes to connect.");
    #(client side task: wait for server to reply)
    #IF YES,THEN SAY "return hi" TO ALL NODES
    else:
        c.send("All nodes have connected to the server!")
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
