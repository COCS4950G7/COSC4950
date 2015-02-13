__author__ = 'chris hamm'
#NetworkClient_r13
#created: 2/10/2015

#Designed to work with NetworkServer_r13

#REVISION NOTES:
    #Moving to a more modular style, no master receive or send function.
    #

#By recommendation, implement without the command logs

import socket
from socket import *

class NetworkClient():

    def __init__(self, inboundpipefromcontroller):
        self.pipe = inboundpipefromcontroller

        host = ''
        port = 55568
        serverIssuedDoneCommand = False

        clientSocket = socket.socket(AF_INET, SOCK_STREAM)

        try: #receive the server ip from the controller
            #TODO insert the call to receive server ip here
            print "DEBUG: INSERT CALL RECEIVE THE SERVER IP HERE\n"
        except Exception as inst:
            print "===================================================================\n"
            print "Error in receive server ip from the controller: "+(str(inst))+"\n"
            print "===================================================================\n"

        try: #connect to server try block
            #TODO insert connect to server function here
            print "DEBUG: INSERT CONNECT TO SERVER FUNCTION HERE\n"
        except Exception as inst:
            print "===================================================================\n"
            print "Error in connect to server try block: " + str(inst) +"\n"
            print "===================================================================\n"

        #PRIMARY CLIENT WHILE LOOP
        try:
            clientSocket.settimeout(0.25)
            while True: #primary client while loop
                #CHECK FOR INBOUND SERVER COMMANDS SECTION
                try: #check for inbound server commands
                    #TODO insert receive server command here
                    print "DEBUG: INSERT RECEIVE SERVER COMMANDS HERE\n"
                except Exception as inst:
                    print "===================================================================\n"
                    print "Error in check for inbound Server Commands Try block: "+str(inst)+"\n"
                    print "===================================================================\n"

                #TODO check to see if received the empty string
                print "DEBUG: CHECK TO SEE IF RECV AN EMPTY STRING HERE\n"
                try: #check for the done command from the server
                    #TODO insert check for done command from server function
                    print "DEBUG: CHECK FOR DONE COMMAND FROM THE SERVER\n"
                except Exception as inst:
                    print "===================================================================\n"
                    print "Error in checking for done command from the server: "+str(inst)+"\n"
                    print "===================================================================\n"

                try: #check for nextChunk command from the server
                    #TODO insert check for nextChunk command from server
                    print "DEBUG: CHECK FOR NEXTCHUNK FROM SERVER HERE\n"
                except Exception as inst:
                    print "===================================================================\n"
                    print "Error in checking for nextChunk command from server: " + str(inst)+"\n"
                    print "===================================================================\n"

                #TODO print error and unknown command here
                print "DEBUG: PRINT OUT ERROR AND UNKNOWN COMMAND HERE\n"

                #CHECK FOR INBOUND CONTROLLER COMMANDS SECTION
                try: #check for inbound controller commands try block
                    #TODO check if there is any commands on the pipe
                    print "DEBUG; CHECK FOR INBOUND COMMANDS FROM CONTROLLER HERE\n"
                except Exception as inst:
                    print "===================================================================\n"
                    print "Error in check for inbound commands from controller try block: "+str(inst)+"\n"
                    print "===================================================================\n"

                #TODO check to see if received the empty string
                print "DEBUG: CHECK TO SEE IF RECEIVED THE EMPTY STRING \n"
                try: #checking for found solution command from controller
                    #TODO check if received the found solution command from the controller
                    print "DEBUG: CHECK TO SEE IF RECEIVED THE FOUND SOLUTION COMMAND FROM THE CONTROLLER\n"
                except Exception as inst:
                    print "===================================================================\n"
                    print "Error in check for found solution command from controller: "+str(inst)+"\n"
                    print "===================================================================\n"

                try: #checking for request next chunk command from controller
                    #TODO check if received the request next chunk command from controller
                    print "DEBUG: CHECK TO SEE IF RECEIVED REQUEST NEXT CHUNK COMMAND\n"
                except Exception as inst:
                    print "===================================================================\n"
                    print "Error in check for request Next Chunk Command from controller: "+str(inst)+"\n"
                    print "===================================================================\n"

                try: #check for doingStuff command form controller
                    #TODO check if doingSTuff command was received
                    print "DEBUG: CHECK IF DOINGSTUFF COMMAND WAS RECEIVED\n"
                except Exception as inst:
                    print "===================================================================\n"
                    print "Error in check for doingStuff Command from controller: "+str(inst)+"\n"
                    print "===================================================================\n"

                try: #check for done command from the controller
                    #TODO check if done command was received form controller
                    print "DEBUG: CHECK IF DONE COMMAND WAS RECEIVED FROM CONTROLLER\n"
                except Exception as inst:
                    print "===================================================================\n"
                    print "Error in check for done command from the controller: "+str(inst)+"\n"
                    print "===================================================================\n"

                #TODO print out error and unknown command from controller
                print "DEBUG: PRINT OUT ERROR AND UNKNOWN COMMAND FROM CONTROLLER HERE\n"
            #end of primary client while loop
        except Exception as inst:
            print "===================================================================\n"
            print "Error in Primary client while loop: "+str(inst)+"\n"
            print "===================================================================\n"
        finally:
            #TODO check to see if server has issued the done command, if not, send crashed message to the server
            try: #send crash message to server, if needed
                #TODO send crash message to server here, if needed
                print "DEBUG: SEND CRASH MESSAGE TO SERVER HERE IF NEEDED\n"
            except Exception as inst:
                print "===================================================================\n"
                print "Error in send crash message to server, in finally block: "+str(inst)+"\n"
                print "===================================================================\n"
            clientSocket.close()
            print "Client Socket has been closed\n"

        #TODO insert class functions here (check and send functions)