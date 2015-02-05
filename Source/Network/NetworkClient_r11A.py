__author__ = 'Chris Hamm'
#NetworkClient_r11A
#Created: 2/4/2015

__author__ = 'chris hamm'
#NetworkClient_r11
#Created: 2/2/2015

#DEAD REVISION, USING ORIGINAL REVISION 11

from socket import *
from random import *
import sys

def compareString(inboundStringA, inboundStringB, startA, startB, endA, endB): #This function is now global
        posA = startA
        posB = startB
        #add check here
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

def receiveData(networkSocket):
        print "Checking for inbound network data\n"
        networkSocket.settimeout(0.5)
        data = ""
        while True:
            try:
                data = networkSocket.recv(1024)
                if not data:
                    break
                else:
                    print "received data: " + str(data) +"\n"
                    if(checkForDoneCommandFromServer(networkSocket)==True): #check to see if received data is the done command
                        print "DONE COMMAND RECEIVED!!!!\n"
                        break
           # except networkSocket.timeout as inst:
            #    print "Socket has timed out in receiveData\n"
             #   break
            except Exception as inst:
                print "Exception in receive data: " + str(inst) +"\n"
                break
        return data #if data is empty string, nothing was received

def sendData(networkSocket, serverIP, outboundMessage): #return true if you need to break out of main client loop, else false
    print "Sending message to Server: " +str(serverIP) +"\n"
    networkSocket.settimeout(0.5)
    while True:
        try:
            networkSocket.sendto(outboundMessage, serverIP)
            print "sent data: " +str(outboundMessage) + " to server: " +str(serverIP) +"\n"
            return False
            #break
        except Exception as inst:
            if(compareString(str(inst),"[Errno 32] Broken pipe",0,0,len("[Errno 32] Broken pipe"),len("[Errno 32] Broken pipe"))):
                print "Broken pipe error detected in sendData\n"
                #networkSocket.close()
                #sys.exit(1)
                #print "Socket has been closed and program exitted.\n"
                #break
                return True
            else:
                print "Exception in send data: " +str(inst) +"\n"
                return False

def checkForDoneCommandFromServer(networkSocket):
    print "Checking for server issued done command\n"
    networkSocket.settimeout(0.5)
    while True:
        try:
            data = networkSocket.recv(1024)
            if not data:
                break
            else:
                print "Received Done Command From Server\n"
                return True
                break
        #except networkSocket.timeout as inst:
         #   print "Socket has timed out in checkForDoneCommandFromServer."
          #  break
        except Exception as inst:
            print "Exception in checkForDoneCommandFromServer: " +str(inst) +"\n"
            break
    return False

class NetworkClient():
    if __name__ == '__main__':

        host = 'localhost'
        port = 55568
        buf = 1024

        addr = (host, port)

        clientsocket = socket(AF_INET, SOCK_STREAM)

        clientsocket.connect(addr)
        print "Connected to server\n"
        myNumber= randint(0,10) #temporary to show that it is a different thread running
        while 1:
            #data = raw_input(">> ") #part of the original example
            #data = "me " +str(myNumber) + "\n"
            data = "NEXT"
            if not data:
                break
            else:
                #clientsocket.send(data) #OLD SNED METHOD
                exitMainLoop= sendData(clientsocket,addr,data)
                if(exitMainLoop == True):
                    print "Breaking out of Main Loop\n"
                    break
                if(checkForDoneCommandFromServer(clientsocket)==True):
                    break
                data = receiveData(clientsocket)
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
        clientsocket.close()

