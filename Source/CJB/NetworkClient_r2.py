__author__ = 'Chris_Hamm'
#NetworkClient_r2.py
#CREATED ON: NOV 2 2014


     #Nov 1 2014 Chris Hamm (FROM PREVIOUS REVISION)
        # Asks for the user to input what the host's ip address is
        # Has basic error handing for trying to connect to an invalid host
        # NO LONGER REQUIRES HOST TO HAVE A STATIC IP ADDRESS

    #Nov 2 2014 -Chris Hamm (CURRENT REVISION)
        #Can now receive multiple lines from the server and display them
        #(UNTESTED) Will tell the server that there was an exception on the clients end and that the client must disconnect
        #FUTURE DESIGN CHANGE PLANNED - Have the client node always listen for messages from the server

try:

    #STARTUP NODES####################
    import socket #import socket module
    socketObject= socket.socket() #create a socket object
    port = 12397 #Reserve a port for service

    #HAVE USER INPUT THE SERVER IP ADDRESS###############################3
    hostIPAddress = str(raw_input('What is the host IP Address?')) #ask user for the host IP address
    try:
        socketObject.connect((hostIPAddress, port)) #try connecting to host
        print socketObject.recv(1024)
        print socketObject.recv(1024)
        print socketObject.recv(1024) #each of these lines prints out a message that the server has provided


    except Exception as inst:
            print ("An Exception was thrown");
            socketObject.send("CLIENT: An exception was thrown! Disconnecting From server"); #tell server that an error occured and node must disconnect
            print type(inst) #the exception instance
            print inst.args #srguments stored in .args
            print inst #_str_ allows args tto be printed directly
            socketObject.close()


        #HAS THE SERVER REPLIED?##########

            #IF NO, THEN CONTINUE WAITING

            #IF YES, THEN WAIT FOR SERVER COMMAND OR DONE

                #WAS THE "done" COMMAND RECEIVED?##################

                    #IF YES, THEN DISPLAY "FINISHED" AND THE RESULTS THAT WHERE GIVEN BY THE DONE COMMAND

                    #IF NO,THEN:

                        #WAS A SERVER COMMAND RECEIVED?#######################

                            #IF NO, THEN CONTINUE WAITING

                            #IF YES, THEN EXECUTE SERVER COMMAND

                                #HAS THIS NODE GONE PAST THE ENDHASH VALUE?#########################

                                    #(server-side task: wait for node to reply)
                                    #(server-side subtask: was no match found?)
                                    #IF YES, THEN TELL THE SERVER "no match found"
                                    #THEN CONTINUE WAITING

                                    #IF NO,THEN:

                                        #DOES THE HASH MATCH THE DESIRED HASH?########################

                                            #(server-side task: wait for node to reply)
                                            #(server-side subtask: was the node status updated?)
                                            #IF NO, THEN TELL THE SERVER THE NODE'S STATUS (STATUS UPDATE)
                                            #THEN CONTINUE TO EXECUTE THE SERVERS COMMAND

                                            #(server-side task: wait for node to reply)
                                            #(server-side subtask: was match found?)
                                            #IF YES, THEN TELL THE SERVER "Found match"
                                            #THEN DISPLAY "FINISHED" PLUS THE RESULTS THE NODE FOUND
except Exception as inst:
            print ("An Exception has occured.");
            print type(inst) #the exception instance
            print inst.args #srguments stored in .args
            print inst #_str_ allows args tto be printed directly
            socketObject.close()

