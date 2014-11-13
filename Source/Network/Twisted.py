__author__ = 'chris'
#Twisted.py
#This file is used to create the auxillery classes that are needed for NetworkServer_r3 and NetworkClient_r3 (and future versions)
#based on this: https://twistedmatrix.com/documents/current/core/howto/servers.html

#NOTICE: IN ORDER TO MAKE THE IMPORT WORK, YOU MUST DOWNLOAD THE TWISTED SOURCE CODE FILES

from twisted.internet.protocol import Protocol

class Echo(Protocol):
    def _init_(self, factory):
        self.factory= factory
    def connectionMade(self): #Displays mesage when you have connected to the server, adds one to the record of number of nodes
        self.factory.numProtocols= self.factory.numProtocols + 1
        self.transport.write("Welcome! There are currently %d open connections. \n" % (self.factory.numProtocols,))
    def connectionLost(self, reason):  #decrements by one to the record of how many nodes are connected
        self.factory.numProtocols = self.factory.numProtocols - 1
    def dataReceived(self, data): #This writes back whatever is written to it, and does not respond to all events
        self.transport.write(data)

class QOTD(Protocol): #This class responds to the initial connection with the well known quote, then terminates the connection
    def connectionMade(self):
        self.transport.write("An apple a day keeps the doctor away \r\n")
        self.transport.loseConnection()