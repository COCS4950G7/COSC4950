__author__ = 'chris hamm'
#NetworkServer_r13
#Created: 2/10/2015

#Designed to work with NetworkClient_r13

#NOTES ABOUT THIS REVISION:
    #Goal is to have this revision be easier to diagnose lock problems
    #NO locks are to be acquired in the Main Thread, Client Thread(s), if at all possible
    #ALL locks are to be acquired in the function that needs them, then immeadiately released (also applies for incrementors)
    #Have some sort of time out mechanism for acquiring a nested lock, so that both locks will be released and the program can continue to run
    #Main thread will only handle inbound client connections
    #ClientThread will only handle communication between that client and the server.

#By recommendation, implement with out the command logs

import threading
import thread
import socket
from socket import *

class NetworkServer():

    #CLASS VARS
    host = ''
    port = 55568

    socketLock = threading.RLock()

    def ClientThreadHandler(self, clientSocket, clientAddr, socketLock):
        try:
            receivedCommandFromClient = "" #initialize the receiving variable
            while True:
                try: #check for commands from client
                    #TODO implement the receive mechanism here for inbound client commands
                    print "DEBUG: INSERT THE RECEIVE MECHANISM FOR INBOUND COMMANDS FROM THE CLIENT HERE\n"
                except Exception as inst:
                    print "Error in check for commands from the client in client thread handler: " +str(inst)+"\n"
                try: #Analyzing received command from the client try block
                    #TODO check to make sure the received command is not the empty string
                    print "DEBUG: CHECK TO SEE IF RECEIVED COMMAND IS THE EMOTY STRING HERE\n"
                    try: #checking to see if the next Command was received from the client try block
                        #TODO check to see if the next command was received from the client
                        print "DEBUG: CHECK TO SEE IF THE NEXT COMMAND WAS RECEIVED FROM THE CLIENT HERE\n"
                    except Exception as inst:
                        print "Error in checking to see if the next Command was received from the client in client thread handler: "+str(inst)+"\n"
                    try: #check to see if the found solution command was received from the client
                        #TODO check to see if the found solution command was received from the client
                        print "DEBUG: CHECK TO SEE IF THE FOUNDSOLUTION COMMAND WAS RECEIVED FROM THE CLIENT HERE\n"
                    except Exception as inst:
                        print "Error in check to see if found solution command was received from the client in client thread handler: "+str(inst)+"\n"
                    try: #check to see if the crashed command was received
                        #TODO check to see if the crashed command was received from the client
                        print "DEBUG: CHECK TO SEE IF CRASHED COMMAND WASS RECEIVED HERE\n"
                    except Exception as inst:
                        print "Error in check to see if crashed command was received from client in client thread handler: "+ str(inst)+"\n"
                    #TODO print error and the unknown command here
                    print "DEBUG; PRINT THE ERROR AND UNKNOWN COMMAND HERE\n"
                except Exception as inst:
                    print "Error in Analyzing received command from the client try block in the client thread handler: " +str(inst)+"\n"
        except Exception as inst:
            print "Error in Client Thread Handler: " + str(inst) +"\n"
        finally:
            clientSocket.close()
            print "clientSocket has been closed\n"
    #end of clientthreadhandler

    def __init__(self, inboundpipeconnection):
        self.pipe = inboundpipeconnection #pipe that connects to the controller

        #CREATE THE SOCKET
        serverSocket = socket.socket(AF_INET, SOCK_STREAM)

        try: #try to bind the socket
            serverSocket.bind((self.host, self.port))
        except Exception as inst:
            print "Error: Failed to bind the socket!"

        #START LISTENING TO SOCKET
        serverSocket.listen(5)

        #MAIN THREAD SERVER LOOP
        try: #main thread server loop try block
            serverSocket.settimeout(0.25)
            while True: #Primary main thread server while loop
                #CHECK TO SEE IF A CLIENT IS TRYING TO CONNECT
                try:
                    inboundClientSocket, inboundClientAddr = serverSocket.accept()
                    print "A client has connected!!\n"
                    thread.start_new_thread(self.ClientThreadHandler(inboundClientSocket,inboundClientAddr,self.socketLock))
                except Exception as inst:
                    print "Error in check for client trying to connect try block: " +str(inst)+"\n"

                #CHECK TO SEE IF CONTROLLER HAS SENT A MESSAGE TO SERVER
                try:
                    if(self.pipe.poll()):
                        receivedControllerCommand= self.pipe.recv()
                        print "Received a command from the controller\n"
                        #TODO BEGIN THE IF ELSES HERE
                        try: #checking for nextChunk Command from Controller
                            #TODO
                            print "DEBUG: INSERT CALL TO CHECK FOR NEXTCHUNK COMMAND FROM CONTROLLER HERE\n"
                        except Exception as inst:
                            print "Error in checking for nextChunk COmmand from Controller Try Block: " +str(inst)+"\n"
                        try: #checking for done command form controller
                            #TODO
                            print "DEBUG: INSERT CALL TO CHECK FOR DONE COMMAND FROM CONTROLLER HERE\n"
                        except Exception as inst:
                            print "Error in checking for done command from Controller Try Block: "+str(inst)+"\n"
                        #TODO
                        print "DEBUG: INSERT ERROR MESSAGE AND PRINT OUT OF UNKNOWN COMMAND FROM THE CONTROLLER\n"
                    else: #if there is nothing on the pipe
                        print "There is no command received from the controller\n"
                except Exception as inst:
                    print "Error in check to see if controller has sent a message to server try block: " + str(inst) +"\n"
        except Exception as inst:
            print "Error in Main Thread Server Loop: " +str(inst)+"\n"
        finally:
            serverSocket.close()
            print "The serverSocket has been closed\n"

