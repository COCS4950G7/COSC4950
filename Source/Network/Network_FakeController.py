__author__ = 'Chris Hamm'
#Network_FakeController

#This is used to simulate the controller class since i cant modify the existing one
#and I need to test the Network classes
#This also allows for me to manually select which network class I want to start up

#FLAW: if you launch client, you can't pass the server's ip to it!!!


from time import time
import sys
import os
from multiprocessing import Process, Pipe, Lock

import NetworkClient_r9
import NetworkServer_r9B

#try:
class Network_FakeController():
    #class variables
    selectingTheNetworkClass = True
    selectedNetworkClass = 0
    networkServer = 0
    networkClient = 0

    #lock = Lock()
    controllerPipe, networkPipe = Pipe()

    #defining network sub-processes
    networkServer = Process(target=NetworkServer_r9B.NetworkServer, args=(networkPipe,))
    networkClient = Process(target=NetworkClient_r9.NetworkClient, args=(networkPipe,))



    #constructor
    def __init__(self):

        print " "
        print "Starting up the FakeController class"
        print " "

        #ask which network class you want to start up
        while self.selectingTheNetworkClass == True:
            self.selectedNetworkClass = str(raw_input('Which network class you want to start? (Enter in the corresponding numeral): \n'
                                                      '1) NetworkServer \n'
                                                      '2) NetworkClient \n'))
            if(self.selectedNetworkClass == "1"):
                print "Starting NetworkServer..."
                self.networkServer.start()
                self.selectingTheNetworkClass = False
            elif(self.selectedNetworkClass == "2"):
                print "Starting NetworkClient..."
                self.networkClient.start()
                self.selectingTheNetworkClass = False
            else:
                print "ERROR: Invalid input"
                print " "

        #end of while loop

    #end of constructor

Network_FakeController()

