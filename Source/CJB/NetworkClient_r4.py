__author__ = 'chris hamm'
#Created on 11/9/2014
#NetworkClient_r4

import socket
socketObject= socket.socket() #create a socket object
port = 49200
try:

    done= False
    while(done ==False):
        hostIPAddress = str(raw_input('What is the host IP Address?')) #ask user for the host IP address
        socketObject.connect((hostIPAddress, port)) #try connecting to host
        print("Connected to server");
except Exception as inst:
    print("An error was thrown");
    print inst
finally:
    socketObject.close()