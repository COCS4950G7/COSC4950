__author__ = 'chris hamm'
#NetworkServer_r4
#Created on 11/8/2014

#NOTE: This revision was started from scratch, so no past changes will be shown here

#THE MASTER TRY BLOCK, DESIGNED TO CATCH ANYTHING
try:
    #SERVER STARTUP: INITIALIZING VARIABLES**************************************************************************
    import socket #importing the socket module
    initialConnectionSocket= socket.socket() #this socket is used to initially connect to the server

    #NOTE: PRIVATE/DYNAMIC PORT NUMBERS ARE BETWEEN 49,152 AND 65,535
    initialPort= 49200 #use this port to initially connect to the server.
    initialConnectionSocket.bind(('',initialPort))  #Binding the socket to that port

    listOfPossiblePorts= [52000, 52001, 52002, 52003, 52004] #this list contains all of the possible ports the server can use to connunicate with clients (except the initial port)
    possiblePortsIndex= 0 #index used to iterate over the list of possible ports
    #THIS SECTION WILL BE CHANGED TO ALLOW FOR MORE THAN 5 CLIENTS

    #IMPORTANT!!!!!!!!!!!!!!!!
    #MAKE SURE TO ADD ANY ADDITIONAL PIECES TO THE FINALLY SECTION AT THE END OF THE CODE!!!!
    #IMPORTANT!!!!!!!!!!!!!!!!

    firstClientSocket= socket.socket() #this socket is used to communicate with the first client after the client has been redirected from the initial socket
    try:
        firstClientPort= listOfPossiblePorts[possiblePortsIndex]
        possiblePortsIndex= 1 + possiblePortsIndex
        firstClientSocket.bind(('',firstClientPort))
    except Exception as inst:
        print("ERROR: problem with firstClientPort/possiblePortsIndex");
        print type(inst) #the exception instance
        print inst.args #srguments stored in .args
        print inst #_str_ allows args tto be printed directly

    secondClientSocket= socket.socket()
    try:
        secondClientPort= listOfPossiblePorts[possiblePortsIndex]
        possiblePortsIndex= 1 + possiblePortsIndex
        secondClientSocket.bind(('',secondClientPort))
    except Exception as inst:
        print("ERROR: problem with secondClientPort/possiblePortsIndex");
        print type(inst) #the exception instance
        print inst.args #srguments stored in .args
        print inst #_str_ allows args tto be printed directly

    thirdClientSocket= socket.socket()
    try:
        thirdClientPort= listOfPossiblePorts[possiblePortsIndex]
        possiblePortsIndex= 1 + possiblePortsIndex
        thirdClientSocket.bind(('',thirdClientPort))
    except Exception as inst:
        print("ERROR: problem with thirdClientPort/possiblePortsIndex");
        print type(inst) #the exception instance
        print inst.args #srguments stored in .args
        print inst #_str_ allows args tto be printed directly

    fourthClientSocket= socket.socket()
    try:
        fourthClientPort= listOfPossiblePorts[possiblePortsIndex]
        possiblePortsIndex= 1 + possiblePortsIndex
        fourthClientSocket.bind(('',fourthClientPort))
    except Exception as inst:
        print("ERROR: problem with fourthClientPort/possiblePortsIndex");
        print type(inst) #the exception instance
        print inst.args #srguments stored in .args
        print inst #_str_ allows args tto be printed directly

    fifthClientSocket= socket.socket()
    try:
        fifthClientPort= listOfPossiblePorts[possiblePortsIndex]
        possiblePortsIndex= 1 + possiblePortsIndex
        fifthClientSocket.bind(('',fifthClientPort))
    except Exception as inst:
        print("ERROR: problem with fifthClientPort/possiblePortsIndex");
        print type(inst) #the exception instance
        print inst.args #srguments stored in .args
        print inst #_str_ allows args tto be printed directly

    #END OF SECTION THAT IS GOING TO BE CHANGED

    #CREATE CUSTOM CLASS OBJECTS TO HOLD THE NESSECARY PARAMETERS FOR EACH CRACKING METHOD TYPE
    class BruteForceParams:
        def _init_(self, inputStartingPoint = None, inputEndingPoint = None):
            self.startingPoint = inputStartingPoint
            self.endingPoint = inputEndingPoint

    class DictionaryParams:
        def _init_(self, inputDictionaryFile= None):
            self.dictionaryFile= inputDictionaryFile

    class RainbowTableParams:
        def _init_(self, inputRainbowTableFile= None):
            self.rainbowTableFile= inputRainbowTableFile
    #END OF CREATING CUSTOM PARAMETER CLASSES
    #CREATE CUSTOM CLIENT CLASS, THIS WILL BE USED TO KEEP TRACK OF WHAT EACH CLIENT IS DOING
    class Client:
        def _init_(self, inputCrackingMethod= None, inputPossiblePortListIndex= None, inputCurrentTask= None):
            self.crackingMethod= inputCrackingMethod  #used to determine what cracking method this client is doing (intented to be used for the all cracking methods setting)
            self.possiblePortListIndex= inputPossiblePortListIndex #used to indicate what the index value of the current port being used is. This is referring to the listOfPossiblePorts (above)
            self.currentTask= inputCurrentTask #this holds the custom parameter class that corresponds to the cracking method so that the server knows what each client is doing
    #END OF CREATING CUSTOM CLIENT CLASS

    #PROMPT USER FOR CRACKING MODE
    try:
        validInput= False #if input is invalid, value needs to be set to false (Default: false)
        while(validInput == False):
            typeOfCracking= int(raw_input('Select what type of cracking method do you want to use (Enter in the Corresponding Number): \n'
                                            '1) Brute-Force \n'
                                            '2) Dictionary \n'
                                            '3) Rainbow Tables \n'
                                            '4) All methods (WARNING: This will require a lot of computers!!) \n'))
            if(typeOfCracking < 1):
                print("--------------------------------------");
                print("Invalid input. Must be greater than 0.");
            elif(typeOfCracking > 4):
                print("--------------------------------------");
                print("Invalid input. Must be less than 5.");
            else:
                validInput= True
    except Exception as inst:
        print("ERROR: invalid numeral for type of cracking input");
        print type(inst) #the exception instance
        print inst.args #srguments stored in .args
        print inst #_str_ allows args tto be printed directly

    if(typeOfCracking == 1):
        print("Brute-Force Cracking method selected. \n");
    elif(typeOfCracking == 2):
        print("Dictionary Cracking method selected. \n");
    elif(typeOfCracking == 3):
        print("Rainbow Table Cracking method selected. \n");
    elif(typeOfCracking == 4):
        print("All methods of cracking have been selected. \n");

    print("Now waiting for nodes to connect...");

except Exception as inst:
        print("ERROR: An exception was thrown!");
        print("Closing all sockets");
        print type(inst) #the exception instance
        print inst.args #srguments stored in .args
        print inst #_str_ allows args tto be printed directly

finally:
    initialConnectionSocket.close()
    firstClientSocket.close()
    secondClientSocket.close()
    thirdClientSocket.close()
    fourthClientSocket.close()
    fifthClientSocket.close()
#END OF THE MASTER TRY CATCH BLOCK FOR SERVER_R4