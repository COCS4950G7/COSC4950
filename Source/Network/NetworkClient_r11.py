__author__ = 'chris hamm'
#NetworkClient_r11
#Created: 2/2/2015

#Designed to work with NetworkServer_r11

#I THINK I FIXED THIS(below)
    #WARNING BUG!!!!!! Sometimes a client disconnects from server because it claims that it received the 'done' command
    #Suspect that it is because the check for done command is not implemented properly

#Fixed issue (below) by changing how the socket objects are created
    #Has connection issues when trying to connect to the server, Errno 111 'connection refused' but only server and client are on different machines
    #ALTERNATE ERROR FAILS TO CONNECT WITH ERRNO 61, 'connection refused'

from socket import *
import socket
from random import *
import platform
import sys

def compareString(inboundStringA, inboundStringB, startA, startB, endA, endB): #This function is now global
        try:
            posA = startA
            posB = startB
            #add check here (optional)
            if((endA-startA) != (endB-startB)):
                return False
            for x in range(startA,endA):
                tempCharA= inboundStringA[posA]
                tempCharB= inboundStringB[posB]
                if(tempCharA != tempCharB):
                    return False
                posA+= 1
                posB+= 1
            return True
        except Exception as inst:
            print "ERROR in compareString: " + str(inst) +"\n"
            return False

def receiveData(self,networkSocket):
        print "Checking for inbound network data\n"
        networkSocket.settimeout(0.5)
        data = ""
        while True:
            try:
                data = networkSocket.recv(1024)
                if not data:
                    break
                else:
                    print "received data: " + str(data) +"\n" #something is logically wrong with the check for done command
                    #if(checkForDoneCommandFromServer(networkSocket)==True): #check to see if received data is the done command #OLD METHOD
                     #   print "DONE COMMAND RECEIVED!!!!\n"
                     #  break
                    if(checkForDoneCommandFromServer(self,str(data))==True):
                        print "Server has issued the done command\n"
                        break
                    elif(checkForNextChunkParamsFromServer(str(data))==True):
                        print "Received Next Chunk Params From Server\n"
                        break
                    elif(checkForNextChunkDataFromServer(str(data))==True):
                        print "Received Next Chunk Data From Server\n"
                        break
                    else: #then it is an unknown command
                        print "Unknown command received from the server: " + str(data) +"\n"
                        self.incrementUnknownCommandFromServerCounter()
                        break
           # except networkSocket.timeout as inst: #NO LONGER USED
            #    print "Socket has timed out in receiveData\n"
             #   break
            except Exception as inst:
                print "Exception in receive data: " + str(inst) +"\n"
                break
        return data #if data is empty string, nothing was received

def sendData(self,networkSocket, serverIP, outboundMessage): #return true if you need to break out of main client loop, else false
    print "Sending message to Server: " +str(serverIP) +"\n"
    networkSocket.settimeout(0.5)
    while True:
        try:
            networkSocket.sendto(outboundMessage, serverIP)
            print "sent data: " +str(outboundMessage) + " to server: " +str(serverIP) +"\n"
            if(compareString(outboundMessage,"NEXT",0,0,len("NEXT"),len("NEXT"))==True):
                self.incrementNextCommandToServerCounter()
            elif(compareString(outboundMessage,"FOUNDSOLUTION",0,0,len("FOUNDSOLUTION"),len("FOUNDSOLUTION"))==True):
                self.incrementFoundSolutionCommandToServerCounter()
            elif(compareString(outboundMessage,"CRASHED",0,0,len("CRASHED"),len("CRASHED"))==True):
                self.incrementCrashedCommandToServerCounter()
            return False
            #break
        except Exception as inst:
            if(compareString(str(inst),"[Errno 32] Broken pipe",0,0,len("[Errno 32] Broken pipe"),len("[Errno 32] Broken pipe"))):
                print "Broken pipe error detected in sendData\n"
                return True
            else:
                print "Exception in send data: " +str(inst) +"\n"
                return False

def checkForDoneCommandFromServer(self,inboundString):
    try:
        print "Checking for done command from server\n"
        if(compareString(inboundString,"done",0,0,len("done"),len("done"))==True):
            print "Done command was received from the server\n"
            self.incrementNextChunkDataFromServerCounter()
            return True
        else:
            return False
    except Exception as inst:
        print "ERROR in checkForDoneCommandFromServer: " + str(inst) +"\n"
        return False

def checkForNextChunkParamsFromServer(self, inboundString):
    try:
        print "Checking for next chunk params from the server\n"
        if(compareString(inboundString,"nextChunkParams",0,0,len("nextChunkParams"),len("nextChunkParams"))==True):
            print "Received the Next Chunk Params from Server\n"
            self.incrementNextChunkParamsFromServerCounter()
            return True
        else:
            return False
    except Exception as inst:
        print "ERROR in checkForNextChunkParamsFromServer: " +str(inst) +"\n"
        return False

def checkForNextChunkDataFromServer(self, inboundString):
    try:
        print "Checking for next chunk data from the server\n"
        if(compareString(inboundString,"nextChunkData",0,0,len("nextChunkData"),len("nextChunkData"))==True):
            print "Received the Next Chunk Data from Server\n"
            self.incrementNextChunkDataFromServerCounter()
            return  True
        else:
            return False
    except Exception as inst:
        print "ERROR in checkForNextChunkDataFromServer: " + str(inst) +"\n"
        return False


class NetworkClient:

    #client records-------
    #outbound commands sent to server
    nextCommandToServerCounter = 0
    foundSolutionCommandToServerCounter = 0
    crashedCommandToServerCounter = 0

    #inbound commands from server
    doneCommandFromServerCounter = 0
    nextChunkParamsFromServerCounter = 0
    nextChunkDataFromServerCounter = 0
    unknownCommandFromServerCounter = 0

    #outbound commands sent to controller
    nextChunkCommandToControllerCounter = 0 #not yet implemented, only incrementor and print record statement
    doneCommandToControllerCounter = 0 #not yet implemented, only incrementor and print record statement
    connectedCommandToControllerCounter = 0 #not yet implemented, only incrementor and print record statement
    doingStuffCommandToControllerCounter = 0 #not yet implemented, only incrementor and print record statement

    #inbound commands from controller
    receiveServerIPFromControllerCounter = 0 #not yet implemented, only incrementor and print record statement
    doingStuffCommandFromControllerCounter = 0 #not yet implemented, only incrementor and print record statement
    foundSolutionCommandFromControllerCounter = 0 #not yet implemented, only incrementor and print record statement
    requestNextChunkCommandFromControllerCounter = 0 #not yet implemented yet, only incrementor and print record statement

    #considering putting in a counter for number of exceptions thrown (for each exception type)
        #counter for how many times you have broken out of the main loop and not received the done command

    #increment counter functions
    def incrementNextCommandToServerCounter(self):
        self.nextCommandToServerCounter += 1

    def incrementFoundSolutionCommandToServerCounter(self):
        self.foundSolutionCommandToServerCounter+= 1

    def incrementCrashedCommandToServerCounter(self):
        self.crashedCommandToServerCounter+= 1

    def incrementDoneCommandFromServerCounter(self):
        self.doneCommandFromServerCounter+= 1

    def incrementNextChunkParamsFromServerCounter(self):
        self.nextChunkParamsFromServerCounter+= 1

    def incrementNextChunkDataFromServerCounter(self):
        self.nextChunkDataFromServerCounter+= 1

    def incrementUnknownCommandFromServerCounter(self):
        self.unknownCommandFromServerCounter+= 1

    def incrementNextChunkCommandToControllerCounter(self):
        self.nextChunkCommandToControllerCounter+= 1

    def incrementDoneCommandToControllerCounter(self):
        self.doneCommandToControllerCounter+= 1

    def incrementConnectedCommandToControllerCounter(self):
        self.connectedCommandToControllerCounter+= 1

    def incrementDoingStuffCommandToControllerCounter(self):
        self.doingStuffCommandToControllerCounter+= 1

    def incrementReceiveServerIPFromControllerCounter(self):
        self.receiveServerIPFromControllerCounter+= 1

    def incrementDoingStuffCommandFromControllerCounter(self):
        self.doingStuffCommandFromControllerCounter+= 1

    def incrementFoundSolutionCommandFromControllerCounter(self):
        self.foundSolutionCommandFromControllerCounter+= 1

    def incrementRequestNextChunkCommandFromControllerCounter(self):
        self.requestNextChunkCommandFromControllerCounter+= 1
    #end of increment counter functions

    def __init__(self):
        if __name__ == '__main__':
            try: #Main try block
                #host = 'localhost' #old connection method
                host = '' #new connection method
                port = 55568
                buf = 1024

                #.........................................................................
                #Detect the Operating System
                #.........................................................................
                try: #getOS try block
                    print "*************************************"
                    print "    Network Client"
                    print "*************************************"
                    print "OS DETECTION:"
                    if(platform.system()=="Windows"): #Detecting Windows
                        print platform.system()
                        print platform.win32_ver()
                    elif(platform.system()=="Linux"): #Detecting Linux
                        print platform.system()
                        print platform.dist()
                    elif(platform.system()=="Darwin"): #Detecting OSX
                        print platform.system()
                        print platform.mac_ver()
                    else:                           #Detecting an OS that is not listed
                        print platform.system()
                        print platform.version()
                        print platform.release()
                    print "*************************************"
                except Exception as inst:
                    print "========================================================================================"
                    print "ERROR: An exception was thrown in getOS try block"
                    print type(inst) #the exception instance
                    print inst.args #srguments stored in .args
                    print inst #_str_ allows args tto be printed directly
                    print "========================================================================================"
                #......................................
                #End of detect OS
                #......................................

                #.........................................................................
                #Retrieve the local network IP Address
                #.........................................................................
                try: #getIP tryblock
                    print "STATUS: Getting your network IP adddress"
                    if(platform.system()=="Windows"):
                        print socket.gethostbyname(socket.gethostname())
                    elif(platform.system()=="Linux"):
                        #Source: http://stackoverflow.com/questions/11735821/python-get-localhost-ip
                        #Claims that this works on linux and windows machines
                        import fcntl
                        import struct
                        import os

                        def get_interface_ip(ifname):
                            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                            return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s',ifname[:15]))[20:24])
                        #end of def
                        def get_lan_ip():
                            ip = socket.gethostbyname(socket.gethostname())
                            if ip.startswith("127.") and os.name != "nt":
                                interfaces = ["eth0","eth1","eth2","wlan0","wlan1","wifi0","ath0","ath1","ppp0"]
                                for ifname in interfaces:
                                    try:
                                        ip = get_interface_ip(ifname)
                                        print "IP address was retrieved from the " + str(ifname) + " interface."
                                        break
                                    except IOError:
                                        pass
                            return ip
                        #end of def
                        print get_lan_ip()
                    elif(platform.system()=="Darwin"):
                        print socket.gethostbyname(socket.gethostname())
                    else:
                        #NOTE: MAY REMOVE THIS AND REPLACE WITH THE LINUX DETECTION METHOD
                        print "INFO: The system has detected that you are not running Windows, OS X, or Linux."
                        print "INFO: System is using a generic IP detection method"
                        print socket.gethostbyname(socket.gethostname())
                except Exception as inst:
                    print "========================================================================================"
                    print "ERROR: An exception was thrown in getIP try block"
                    print type(inst) #the exception instance
                    print inst.args #srguments stored in .args
                    print inst #_str_ allows args tto be printed directly
                    print "========================================================================================"
                #.........................................................................
                #End of Retrieve the local network IP Address
                #.........................................................................

                addr = (host, port)

                #clientsocket = socket(AF_INET, SOCK_STREAM) #old create socket method
                clientsocket = socket.socket(AF_INET, SOCK_STREAM) #new create socket method
                try:
                    serverIP= raw_input('What is the Servers IP Address?')
                except Exception as inst:
                    print "ERROR in get serverIP try block: " + str(inst) + "\n"
                try:
                    #clientsocket.connect(addr)
                    clientsocket.connect((serverIP,port))
                    print "Connected to server\n"
                except Exception as inst:
                    print "ERROR in connect to server: " + str(inst) +"\n"
                myNumber= randint(0,3) #temporary to show that it is a different thread running
                #data = "NEXT" #start by sending NEXT to server
                while 1:
                    #data = raw_input(">> ") #part of the original example
                    #data = "me " +str(myNumber) + "\n"
                    if(myNumber == 0): #TEMPORARY, used for testing command records
                        data = "NEXT"
                    elif(myNumber == 1):
                        data = "FOUNDSOLUTION"
                    elif(myNumber == 2):
                        data = "CRASHED"
                    else:
                        data = "Unknown"
                    if not data:
                        break
                    else:
                        #clientsocket.send(data) #OLD SNED METHOD
                        exitMainLoop= sendData(self,clientsocket,addr,data)
                        if(exitMainLoop == True):
                            print "Breaking out of Main Loop\n"
                            break
                       # if(checkForDoneCommandFromServer(self,data)==True): #MOVED BELOW
                        #    break
                        data = receiveData(self,clientsocket)
                        #if(checkForDoneCommandFromServer(self,data)==True): #RECEIVEDATA TAKES CARE OF THIS FUNCTION
                         #   break
                        if(data != ""):
                            print "Received message from server: " + str(data) +"\n"
                        #data = clientsocket.recv(buf) #OLD RECV METHOD
                        #if not data:
                        #    break    
                        #else:
                         #   if(compareString(data,"You sent me: me 2",0,0,len("You sent me: me 2"),len("You sent me: me 2"))):
                         #       print "received the me 2 command from the server\n"
                         #   else:
                         #       print "did not receive the me 2 command." + str(data)
            except Exception as inst:
                print "ERROR in main try block: " + str(inst) +"\n"
            finally:
                clientsocket.close()
                print "Socket has been closed\n"
                print "----------------------Outbound Commands To Server-----------------\n"
                print "# of Next Commands Sent To Server: " + str(self.nextCommandToServerCounter) +"\n"
                print "# of Found Solution Commands Sent To Server: " +str(self.foundSolutionCommandToServerCounter) +"\n"
                print "# of Crashed  Commands Sent To Server: " + str(self.crashedCommandToServerCounter) +"\n"
                print "----------------------Inbound Commands From Server----------------\n"
                print "# of Done Commands Received From Server: " + str(self.doneCommandFromServerCounter) +"\n"
                print "# of next Chunk Params Received From Server: " + str(self.nextChunkParamsFromServerCounter) +"\n"
                print "# of next Chunk Data Received From Server: " + str(self.nextChunkDataFromServerCounter) + "\n"
                print "# of Unknown Commands Received From Server: " + str(self.unknownCommandFromServerCounter) +"\n"
                print "----------------------Outbound Commands To Controller---------------------\n"
                print "# of next Chunk Commands Sent to Controller: " + str(self.nextChunkCommandToControllerCounter) + "\n"
                print "# of Done Commands Sent To Controller: " + str(self.doneCommandToControllerCounter) + "\n"
                print "# of Connected Commands Sent to Controller: " + str(self.connectedCommandToControllerCounter) +"\n"
                print "# of doingStuff Commands Sent to Controller: " + str(self.doingStuffCommandToControllerCounter) +"\n"
                print "----------------------Inbound Commands From Controller-----------------------\n"
                print "# of Receive Server IP From Controller Commands: " + str(self.receiveServerIPFromControllerCounter) +"\n"
                print "# of doingStuff Commands Received From Controller: " + str(self.doingStuffCommandFromControllerCounter) +"\n"
                print "# of foundSolution Commands Received From Controller: " + str(self.foundSolutionCommandFromControllerCounter)+"\n"
                print "# of requestNextChunk Commands Received From Controller: " + str(self.requestNextChunkCommandFromControllerCounter)+"\n"


NetworkClient()