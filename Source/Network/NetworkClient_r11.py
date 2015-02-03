__author__ = 'chris hamm'
#NetworkClient_r11
#Created: 2/2/2015

from socket import *

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


class NetworkClient:
    if __name__ == '__main__':

        host = 'localhost'
        port = 55567
        buf = 1024

        addr = (host, port)

        clientsocket = socket(AF_INET, SOCK_STREAM)

        clientsocket.connect(addr)
        print "Connected to server"
        from random import *
        myNumber= randint(0,10) #temporary to show that it is a different thread running
        while 1:
            #data = raw_input(">> ") #part of the original example
            data = "me " +str(myNumber) + "\n"
            if not data:
                break
            else:
                clientsocket.send(data)
                data = clientsocket.recv(buf)
                if not data:
                    break
                else:
                    if(compareString(data,"You sent me: me 2",0,0,len("You sent me: me 2"),len("You sent me: me 2"))):
                        print "received the me 2 command from the server\n"
                    else:
                        print "did not receive the me 2 command." + str(data)
        clientsocket.close()
