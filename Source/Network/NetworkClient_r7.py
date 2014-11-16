__author__ = 'chris hamm'
#Created: 11/15/2014

#This is designed to work with NetworkServer_r7

try: #Master try block
#======================================================================================
#Main Client Loop
#======================================================================================
    try: #Main client loop try block
        import socket
        port= 49200
        clientSocket= socket.socket()
        print "clientSocket successfully created"

        #prompt user for the servers IP address
        serverIPAddress= str(raw_input('What is the host (server) IP Address?'))
        try:
            print "Attempting to connect to server"
            clientSocket.connect((serverIPAddress, port))
            print "Successfully connected to server"
        except socket.timeout as msg:
            print "========================================================================================"
            print "ERROR: the connection has timed out. Check to see if you entered the correct IP Address."
            print "Error code: " + str(msg[0]) + " Message: " + msg[1]
            print "Socket timeout set to: " + clientSocket.gettimeout + " seconds"
            print "========================================================================================"
        except socket.error as msg:
            print "========================================================================================"
            print "ERROR: Failed to connect to server"
            print "Error code: " + str(msg[0]) + " Message: " + msg[1]
            raise Exception("Failed to connect to server")
            print "========================================================================================"

        #Client primary while loop
        serverSaysKeepSearching= True
        try: #client primary while loop
            while(serverSaysKeepSearching==True):
                clientSocket.settimeout(2.0)
                try: #checking for server commands try block
                    print "Checking for server commands..."
                    theInput= clientSocket.recv(2048)

                except socket.timeout as inst:
                    print "============================================================================================="
                    print "Socket timed out. No new server command"
                    print type(inst) #the exception instance
                    print inst.args #srguments stored in .args
                    print inst #_str_ allows args tto be printed directly
                    print "============================================================================================="
                except Exception as inst:
                    print "============================================================================================="
                    print "An exception was thrown in the checking for server commands Try Block"
                    print type(inst) #the exception instance
                    print inst.args #srguments stored in .args
                    print inst #_str_ allows args tto be printed directly
                    print "============================================================================================="

                #keep performing task
                #-------------------------
                    #INSERT TASK HERE
                #-------------------------


        except Exception as inst:
            print "============================================================================================="
            print "An exception was thrown in the Main Client Loop Try Block"
            print type(inst) #the exception instance
            print inst.args #srguments stored in .args
            print inst #_str_ allows args tto be printed directly
            print "============================================================================================="

    except Exception as inst:
        print "============================================================================================="
        print "An exception was thrown in the Main Client Loop Try Block"
        print type(inst) #the exception instance
        print inst.args #srguments stored in .args
        print inst #_str_ allows args tto be printed directly
        print "============================================================================================="

except Exception as inst:
    print "============================================================================================="
    print "An exception was thrown in Master Try Block"
    print type(inst) #the exception instance
    print inst.args #srguments stored in .args
    print inst #_str_ allows args tto be printed directly
    print "============================================================================================="
finally:
    print "Closing socket"
    clientSocket.close()
