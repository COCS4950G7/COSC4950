__author__ = 'chris hamm'
class CommandRecords():
    numberOfNextCommandsFromClients = 0
    numberOfDoneCommandsSentToClients = 0
    def __init__(self):
        self.numberOfNextCommandsFromClients= self.numberOfNextCommandsFromClients
        self.numberOfDoneCommandsSentToClients= self.numberOfDoneCommandsSentToClients

    def getNumberOfNextCommandsFromClients(self):
        return self.numberOfNextCommandsFromClients

    def incrementNumberOfNextCommandsFromClients(self):
        self.numberOfNextCommandsFromClients+= 1

    def getNumberOfDoneCommandsSentToClients(self):
        return self.numberOfDoneCommandsSentToClients

    def incrementNumberOfDoneCommandsSentToClients(self):
        self.numberOfDoneCommandsSentToClients+= 1

#END OF COMMAND RECORDS