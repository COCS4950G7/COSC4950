__author__ = 'chris hamm'
#NetworkClient_r8
#Created on:11/17/2014
###############################################
#THIS REVISION/CONCEPT WAS ABANDONED
###############################################

#This restructured client operates by communicating with the controller class as a primary method of communication
#New concept:
#   -Current State: states what the clients are currently doing

print "Network Client revision 8 is starting up..."
print "WARNING: IP detection does not work on all OS's"
print "         Confirmed to work on Windows 7"
print "         Confirmed to work on Mac OS X"
print "Your IP Address is: (Function Under Construction)"
print "You are using the Port: (Function Under Construction)"
#this is a current state
print "Starting up..."


#client receives the user-inputted server IP as a string
#once client connects to server, client sends over the pipe "connected" to the controller

#COMMANDS THAT THE CONTROLLER WILL ACCEPT
#   "done"
#       -controller joins subprocess and goes back to the start screen
#   "connected"
#       -controller prints "nodeConnectedToScreen" ie: does nothing
#   "doingStuff"
#       -controller prints "nodeDoingStuffScreen" ie: does nothing

#==========================================================================
#BEGINNING OF MASTER TRY BLOCK
#==========================================================================
#Master Try Block
try: #Master try block
    print "Finished booting"
    #==========================================================================================
    #GLOBAL VARIABLES
    #==========================================================================================
    #currentState








#Master except block
except Exception as inst:
    print "============================================================================================="
#   This is a current state also
    print "Current State: CRASHED" ##############################################################Client State
    print "An exception was thrown in Master Try Block"
    print type(inst) #the exception instance
    print inst.args #srguments stored in .args
    print inst #_str_ allows args tto be printed directly
    print "============================================================================================="
finally:
