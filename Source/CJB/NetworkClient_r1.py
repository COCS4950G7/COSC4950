__author__ = 'chris'
#chris hamm
#NetworkClient_r1
#CREATED: 10/22/2014
#ER Diagram of this is available, talk to Chris Hamm if you want a copy.

    #Nov 1 2014 Chris Hamm
        # Asks for the user to input what the host's ip address is
        # Has basic error handing for trying to connect to an invalid host
        # NO LONGER REQUIRES HOST TO HAVE A STATIC IP ADDRESS

try:

    #STARTUP NODES####################
    import socket #import socket module
    socketObject= socket.socket() #create a socket object
    port = 12397 #Reserve a port for service

    #HAVE USER INPUT THE SERVER IP ADDRESS###############################3
    hostIPAddress = str(raw_input('What is the host IP Address?')) #ask user for the host IP address
    try:
        socketObject.connect((hostIPAddress, port)) #try connecting to host


    except Exception as inst:
            print ("An Exception was thrown");
            print type(inst) #the exception instance
            print inst.args #srguments stored in .args
            print inst #_str_ allows args tto be printed directly
            socketObject.close()
    #(server-side task: wait for all nodes to connect to server)
    #SAY "hi" TO THE SERVER####################################3

    #(server-side task: say "return hi" to all nodes)
    #WAIT FOR SERVER TO REPLY##################################3

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
            print ("An Exception was thrown");
            print type(inst) #the exception instance
            print inst.args #srguments stored in .args
            print inst #_str_ allows args tto be printed directly
            socketObject.close()
#finally:
        #print ("Closing socket");
        #socketObject.close()