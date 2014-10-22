__author__ = 'chris'
#chris hamm
#networkServer_r1
#ER Diagram of this is available, talk to Chris Hamm if you want a copy.

#IMPORTANT NOTE: NEED TO INSERT A CHECK TO SEE IF THERE IS NO MORE WORKLOAD TO DISTRIBUTE AND ALL NODES HAVE REPORTED
#NO MATCH FOUND. NEED TO HAVE THE PROGRAM DISPLAY A MESSAGE SAYING THAT THE HASH WAS NOT FOUND




#STARTUP SERVER#########################


#PROMPT USER FOR NUMBER OF NODES AND WHAT MODE (BF, DICTIONARY,ETC)##############################

#(client-side task: startup the nodes
#(client-side task: say "hi" to server)
#WAIT FOR ALL NODES TO CONNECT#######################

    #ARE ALL NODES CONNECTED?#####################

        #IF NO, CONTINUE TO WAIT

        #(client side task: wait for server to reply)
        #IF YES,THEN SAY "return hi" TO ALL NODES


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
