__author__ = 'chris hamm'
#NetworkClient_r8
#Created on:11/17/2014
###############################################
#THIS REVISION/CONCEPT WAS ABANDONED
###############################################

#This restructured client operates by communicating with the controller class as a primary method of communication
print "Network Client revision 8 is starting up..."
print "WARNING: IP detection does not work on all OS's"
print "         Confirmed to work on Windows 7"
print "         Confirmed to work on Mac OS X"
print "Your IP Address is: (Function Under Construction)"
print "You are using the Port: (Function Under Construction)"


#client receives the user-inputted server IP as a string
#once client connects to server, client sends over the pipe "connected" to the controller

#COMMANDS THAT THE CONTROLLER WILL ACCEPT
#   "done"
#       -controller joins subprocess and goes back to the start screen
#   "connected"
#       -controller prints "nodeConnectedToScreen" ie: does nothing
#   "doingStuff"
#       -controller prints "nodeDoingStuffScreen" ie: does nothing
