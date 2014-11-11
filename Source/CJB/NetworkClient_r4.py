__author__ = 'chris hamm'
#Created on 11/9/2014
#NetworkClient_r4

#Designed to work with NetworkServer_r4

import socket
socketObject= socket.socket() #create a socket object
port = 49200
try:
    done= False
    while(done ==False):
        hostIPAddress = str(raw_input('What is the host IP Address?')) #ask user for the host IP address
        socketObject.connect((hostIPAddress, port)) #try connecting to host
        print("Connected to server");
        print("Cracking Method: ");
        print socketObject.recv(1024) # receive the cracking method from server
        print("New port to connect to: ");
        print socketObject.recv(1024) # receive the new port number from server
except Exception as inst:
    print("An error was thrown");
    print type(inst) #the exception instance
    print inst.args #srguments stored in .args
    print inst #_str_ allows args tto be printed directly
finally:
    socketObject.close()