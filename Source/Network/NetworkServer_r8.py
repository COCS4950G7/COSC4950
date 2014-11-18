__author__ = 'Chris Hamm'
#NetworkServer_r8
#Created on: 11/17/2014

#Redesigned server. Structure has changed so that the server must talk to the controller class

print "Network Server revision 8 is starting up..."
print "WARNING: IP detection does not work on all OS's"
print "         Confirmed to work on Windows 7"
print "         Confirmed to work on Mac OS X"
print "The Server IP Address is: (Function Under Construction)"
print "The Server is using Port: (Function Under Construction)"


#COMMANDS THAT THE CONTROLLER WILL ACCEPT
#   "nextChunk"
#       -controller will send the next chunk to the server
#   "chunkAgain"
#       -controller receives params object with the parameters chunk it needs
#       -controller will request that chunk from dictionary class
#       -controller will send that specific chunk to the server over the pipe
#   "waiting"
#       -controller will do nothing
#   "done"
#       -controller receives the 'done' string from the server over the pipe
#       -controller will determine if it is the key or not
#           -if key is found, controller sends "found" over the pipe to the server, so the server can stop the nodes
#           -if it isnt the key (but we are done), controller sends "notFound" over the pipe to the server, so the server can stop the nodes
