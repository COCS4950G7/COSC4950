#   Controller.py

#   This is the main class that 'controls'
#   the other classes by acting as a go-between
#   with the GUI and the actual worker classes

#   Chris Bugg
#   10/7/14

#   Update - 10/11/14 (Latest_Stable_Versions)
#               -> Main layout is complete, just needs more actual methods
#               ->  from supporting classes.

#   NOTE: Diagrams of the layout (approximate names) are at bottom of file

#   Update - 10/30/14 (Latest_Stable_Versions)
#               -> Works in Console-only mode with Dictionary class (single-user only)
#                   -> use "-c" argument to activate console-only mode
#               -> More friendly UI, W/TIMER, AND STATUS BAR!!!!!

#   ############################ W I P ###########################

#Imports
from time import time
import sys
import os
from multiprocessing import Process, Pipe

#import GUI

from Chunk import Chunk
from Dictionary import Dictionary
#from Brute_Force import Brute_Force
from NetworkClient_r9E import NetworkClient
from NetworkServer_r9E import NetworkServer
from RainbowMaker import RainbowMaker
from RainbowUser import RainbowUser


class Controller():

    #Class variables
    done = False
    rainbowMaker = RainbowMaker()
    rainbowUser = RainbowUser()
    dictionary = Dictionary()
    #brute_force = Brute_Force()

    controllerPipe, networkPipe = Pipe()

    #Defining network sub-processes as class variables that are instances of the network objects
    networkServer = Process(target=NetworkServer, args=(networkPipe,))
    networkClient = Process(target=NetworkClient, args=(networkPipe,))

    #Initializing variable to a default value
    serverIP = "127.0.1.1"

    #tempGUI Variables
    state = "startScreen"

    clock = 0
    colidingClock = 0
    colidingClock2 = 0

    #Constructor
    def __init__(self):

        args = sys.argv

        #If we didn't get the argument "-c" in command-line
        if not args.pop() == "-c":

            x=2 #Placeholder
            #run in standard GUI mode
            #GUI.GUI()

        #if we did get the argument "-c" in command-line
        else:

            #Loop till we're done
            while not self.done:

                #Get current screen
                state = self.state

                #Clear the screen and re-draw
                os.system('cls' if os.name == 'nt' else 'clear')

                #run in console-only mode
                print "...Console-Only Mode..."

                #Lots of if statements

                #############################################
                #############################################
                #if we're at the start state
                if state == "startScreen":

                    #What did the user pick? (Node, Server, Single, Exit)
                    print "============="
                    print "startScreen"
                    print
                    print "(Node)"
                    print "(Server)"
                    print "(Single)"
                    print
                    print "(Exit)"
                    userInput = raw_input("Choice: ")

                    #Sterolize inputs
                    goodNames = {"Node", "node", "Server", "server", "Single", "single", "Exit", "exit"}
                    while not userInput in goodNames:

                        print "Input Error!"

                        userInput = raw_input("Try Again: ")

                    #If user picks Node, tell GUI to go to Node start screen
                    if userInput in ("Node", "node"):

                        self.state = "nodeStartScreen"

                    elif userInput in ("Server", "server"):

                        self.state = "serverStartScreen"

                    elif userInput in ("single", "Single"):

                        self.state = "singleStartScreen"

                    else:

                        #We're done
                        self.done = True

                ##################################################################################
                ###################################### NODE ######################################
                ################################################################################## vvv

                #############################################
                #############################################
                #if we're at the node start state (Screen)
                elif state == "nodeStartScreen":

                    #What did the user pick? (Be a node, Back, Exit)
                    print "============="
                    print "nodeStartScreen"
                    print

                    #Get the server's IP:
                    self.serverIP = raw_input("What's the server's IP: ")

                    print "Ready?"
                    print "(Node)"
                    print "(Back)"
                    print "(Exit)"
                    userInput = raw_input("Choice: ")

                    #Sterolize inputs
                    goodNames = {"Node", "node", "back", "Back", "Exit", "exit"}
                    while not userInput in goodNames:

                        print "Input Error!"

                        userInput = raw_input("Try Again: ")

                    if userInput in ("Node", "node"):

                        self.state = "nodeConnectingScreen"

                    elif userInput in ("Back", "back"):

                        self.state = "startScreen"

                    else:

                        #We're done
                        self.done = True

                #############################################
                #############################################
                #if we're at the node connecting... state (Screen)
                elif state == "nodeConnectingScreen":

                    #Start up the networkServer class (as sub-process in the background)
                    #self.networkClient = Process(target=NetworkClient.NetworkClient(self.networkPipe))
                    self.networkClient.start()

                    #What did the user pick? (Be a Node, Back, Exit)
                    ###userInput = GUI.getInput()
                    print "============="
                    print "nodeConnectingScreen"
                    print

                    #userInput = raw_input("Choice: ")

                    #wait for server connection
                    #then switch to nodeConnectedToScreen

                    #Send the server IP over the pipe to network class
                    self.controllerPipe.send(self.serverIP)

                    #Get response from network class, (looking for "connected")
                    rec = self.controllerPipe.recv()

                    #Stuff for those pretty status pictures stuff
                    starCounter = 0
                    whiteL = ""
                    whiteR = "            "

                    #While not connected, print a "connecting" bar
                    while not rec == "connected":

                        #Clear the screen and re-draw
                        os.system('cls' if os.name == 'nt' else 'clear')
                        #Ohhh, pretty status pictures
                        print "Connecting--> [" + whiteL + "*" + whiteR + "]"
                        if starCounter > 11:
                            starCounter = 0
                            whiteL = ""
                            whiteR = "            "
                        else:
                            starCounter += 1
                            whiteL = whiteL + " "
                            whiteR = whiteR[:-1]

                    #Got connected, so switch screens
                    self.state = "nodeConnectedToScreen"

                #############################################
                #############################################
                #if we're at the node connected state (Screen)
                elif state == "nodeConnectedToScreen":

                    #First command that requests
                    self.controllerPipe.send("next")

                    done = False

                    #While the current job is not done
                    while not done:

                        #Receive the next (or first) command
                        rec = self.controllerPipe.recv()

                        #If the server says we're done
                        if rec == "done":

                            self.controllerPipe.send("done")

                            #Exit our loop and go to next screen
                            done = True

                        #If the server says we're connected (or still connected)
                        elif rec == "connected":

                            self.controllerPipe.send("connected")

                            #Clear the screen and re-draw
                            os.system('cls' if os.name == 'nt' else 'clear')
                            print "============="
                            print "nodeConnectedToScreen"

                        #If the server says we're doing stuff
                        elif rec == "doingStuff":

                            self.controllerPipe.send("doingStuff")

                            #Clear the screen and re-draw
                            os.system('cls' if os.name == 'nt' else 'clear')
                            print "============="
                            print "nodeDoingStuffScreen"

                            #'chunk' is an object that has attributes 'params' and 'data' (both are strings for network passing)

                            #Receive our chunk object
                            chunk = self.controllerPipe.recv()

                            #Get the params as a list from chunk object
                            paramsList = chunk.params.split()

                            ##### add other types later
                            if paramsList[0] == "dictionary":

                                #This is the client's dictionary class,
                                #   and this is where it searches (will be unresponsive during search)
                                self.dictionary.find(chunk)

                                #If it's found something
                                if self.dictionary.isFound():

                                    #get the key from local dictionary class
                                    key = self.dictionary.showKey()

                                    #send "found" over pipe to networkClient
                                    self.controllerPipe.send("found")

                                    #send the key we found to networkClient
                                    self.controllerPipe.send(key)

                                    #stop searching and get done
                                    done = True

                                else:

                                    #if it didn't find anything (but is done)
                                    #get next command (which might be chunk or done or something else)
                                    self.controllerPipe.send("next")

                            elif paramsList[0] == "rainbowmaker":

                                #This line will be unreponsive during creation
                                chunkOfDone = self.rainbowMaker.create(chunk)

                                #Tell the server we're done, and here's a chunk
                                self.controllerPipe.send("doneChunk")

                                #Send the server the chunk of done
                                self.controllerPipe.send(chunkOfDone)

                                #Ask the server for another chunk
                                self.controllerPipe.send("next")

                    self.networkClient.join()
                    #self.networkClient.terminate()

                    #Go back to the nodeStart screen since we're done here
                    self.state = "nodeStartScreen"

                #############################################
                #############################################
                #Ignore for now, implemented in nodeConnectedScreen
                #if we're at the node doing stuff state (Screen)
                elif state == "nodeDoingStuffScreen":

                    #What did the user pick? (Be a Node, Back, Exit)
                    ###userInput = GUI.getInput()
                    print "============="
                    print "nodeDoingStuffScreen"
                    print "(back)"
                    print "(Exit)"
                    userInput = raw_input("Choice: ")

                    #wait to get done with our stuff
                    #then switch to nodeConnectedToScreen or nodeConnectingScreen depending

                    if userInput == "back":

                        ###GUI.setState("nodeStartScreen")
                        self.state = "nodeStartScreen"

                    else:

                        #We're done
                        self.done = True

                ####################################################################################
                ###################################### SERVER ######################################
                #################################################################################### vvv

                #############################################
                #############################################
                #if we're at the Server start state (Screen)
                elif state == "serverStartScreen":

                    #What did the user pick? (Brute-Force, Rainbow, Back, Exit)
                    print "============="
                    print "serverStartScreen"
                    print
                    print "(bruteForce)"
                    print "(rainbowMake)"
                    print "(rainbowUser)"
                    print "(dictionary)"
                    print
                    print "(back)"
                    print "(Exit)"
                    userInput = raw_input("Choice: ")

                    #Sterolize inputs
                    goodNames = {"bruteForce", "brute", "rainbowMake", "make", "rainbowUser", "use", "dictionary", "dic", "back", "Back", "Exit", "exit"}
                    while not userInput in goodNames:

                        print "Input Error!"

                        userInput = raw_input("Try Again: ")

                    if userInput in ("bruteForce", "brute"):

                        self.state = "serverBruteForceScreen"

                    elif userInput in ("rainbowMake", "make"):

                        self.state = "serverRainMakerScreen"

                    elif userInput in ("rainbowUser", "use"):

                        self.state = "serverRainUserScreen"

                    elif userInput in ("dictionary", "dic"):

                        self.state = "serverDictionaryScreen"

                    elif userInput in ("back", "Back"):

                        self.state = "startScreen"

                    else:

                        #We're done
                        self.done = True

                ###################################### BRUTE-FORCE (SERVER) ######################################

                #############################################
                #############################################
                #if we're at the serverBruteForceScreen state (Screen)
                elif state == "serverBruteForceScreen":

                    #What did the user pick? (Crack it!, Back, Exit)
                    #userInput = GUI.getInput()

                    if userInput == "crackIt":

                        #GUI.setState("serverBruteSearchingScreen")
                        x=1
                        #get info from GUI and pass to Brute_Force class

                    elif userInput == "back":
                        x=1
                        #GUI.setState("serverForceScreen")

                    else:

                        #We're done
                        self.done = True

                #############################################
                #############################################
                #if we're at the serverBruteSearchingScreen state (Screen)
                elif state == "serverBruteSearchingScreen":

                    #display results and wait for user interaction

                    #What did the user pick? (Crack it!, Back, Exit)
                    #userInput = GUI.getInput()

                    if userInput == "back":
                        x=1
                        #GUI.setState("serverBruteForceScreen")

                    else:

                        #We're done
                        self.done = True

                #############################################
                #############################################
                #if we're at the serverBruteFoundScreen state (Screen)
                elif state == "serverBruteFoundScreen":

                    #display results and wait for user interaction

                    #What did the user pick? (Crack it!, Back, Exit)
                    #userInput = GUI.getInput()

                    if userInput == "back":
                        x=1
                        #GUI.setState("serverBruteForceScreen")

                    else:

                        #We're done
                        self.done = True

                #############################################
                #############################################
                #if we're at the serverBruteNotFoundScreen state (Screen)
                elif state == "serverBruteNotFoundScreen":

                    #display results and wait for user interaction

                    #What did the user pick? (Crack it!, Back, Exit)
                    #userInput = GUI.getInput()

                    if userInput == "back":
                        x=1
                        #GUI.setState("serverBruteForceScreen")

                    else:

                        #We're done
                        self.done = True

                ###################################### RAINBOW USER (SERVER) ######################################

                #############################################
                #############################################
                #if we're at the serverRainUserScreen state (Screen)
                elif state == "serverRainUserScreen":

                    #What did the user pick? (Crack it!, Back, Exit)
                    ###userInput = GUI.getInput()
                    print "============="
                    print "serverRainUserScreen"
                    print "(crackIt)"
                    print "(back)"
                    print "(Exit)"
                    userInput = raw_input("Choice: ")

                    if userInput == "crackIt":

                        ###GUI.setState("serverRainUserSearchingScreen")
                        self.state = "serverRainUserSearchingScreen"

                        #get info from GUI and pass to Brute_Force class

                    elif userInput == "back":

                        ###GUI.setState("serverStartScreen")
                        self.state = "serverStartScreen"

                    else:

                        #We're done
                        self.done = True

                #############################################
                #############################################
                #if we're at the serverRainUserSearchingScreen state (Screen)
                elif state == "serverRainUserSearchingScreen":

                    #display results and wait for user interaction

                    #What did the user pick? (Crack it!, Back, Exit)
                    ###userInput = GUI.getInput()
                    print "============="
                    print "serverRainUserSearchingScreen"
                    print "(back)"
                    print "(Exit)"
                    userInput = raw_input("Choice: ")

                    if userInput == "back":

                        ###GUI.setState("serverRainUserScreen")
                        self.state = "serverRainUserScreen"

                    else:

                        #We're done
                        self.done = True

                #############################################
                #############################################
                #if we're at the serverRainUserFoundScreen state (Screen)
                elif state == "serverRainUserFoundScreen":

                    #display results and wait for user interaction

                    #What did the user pick? (Crack it!, Back, Exit)
                    ###userInput = GUI.getInput()
                    print "============="
                    print "serverRainUserFoundScreen"
                    print "(back)"
                    print "(Exit)"
                    userInput = raw_input("Choice: ")

                    if userInput == "back":

                        ###GUI.setState("serverRainUserScreen")
                        self.state = "serverRainUserScreen"

                    else:

                        #We're done
                        self.done = True

                #############################################
                #############################################
                #if we're at the serverRainUserNotFoundScreen state (Screen)
                elif state == "serverRainUserNotFoundScreen":

                    #display results and wait for user interaction

                    #What did the user pick? (Crack it!, Back, Exit)
                    ###userInput = GUI.getInput()
                    print "============="
                    print "serverRainUserNotFoundScreen"
                    print "(back)"
                    print "(Exit)"
                    userInput = raw_input("Choice: ")

                    if userInput == "back":

                        ###GUI.setState("serverRainUserScreen")
                        self.state = "serverRainUserScreen"

                    else:

                        #We're done
                        self.done = True

                ###################################### RAINBOW MAKER (SERVER) ######################################

                #############################################
                #############################################
                #if we're at the serverRainMakerScreen state (Screen)
                elif state == "serverRainMakerScreen":

                    print "============="
                    print "serverRainMakerScreen"
                    print

                    #Get the algorithm
                    print "What's the algorithm: "
                    print "(md5)"
                    print "(sha1)"
                    print "(sha256)"
                    print "(sha512)"
                    print
                    algo = raw_input("Choice: ")

                    #Sterolize inputs
                    goodNames = {"md5", "sha1", "sha256", "sha512"}
                    while not algo in goodNames:

                        print "Input Error!"

                        algo = raw_input("Try Again: ")

                    #Set algorithm of RainbowMaker to user input of 'algo'
                    self.rainbowMaker.setAlgorithm(algo)

                    #Get the Number of chars of key
                    print
                    numChars = raw_input("How many characters will the key be? ")
                    while not self.isInt(numChars):

                        print "Input Error, Not an Integer!"

                        numChars = raw_input("Try Again: ")

                    self.rainbowMaker.setNumChars(numChars)

                    #Get the alphabet to be used
                    print
                    print "What's the alphabet: "
                    print "0-9(d)"
                    print "a-z(a)"
                    print "A-Z(A)"
                    print "a-z&A-Z(m)"
                    print "a-z&A-Z&0-9(M)"
                    print
                    alphabet = raw_input("Choice: ")

                    #Sterolize inputs
                    goodNames = {"d", "a", "A", "m", "M"}
                    while not alphabet in goodNames:

                        print "Input Error!"

                        alphabet = raw_input("Try Again: ")
                    self.rainbowMaker.setAlphabet(alphabet)

                    #Get dimensions
                    print
                    chainLength = raw_input("How long will the chains be? ")
                    while not self.isInt(chainLength):

                        print "Input Error, Not an Integer!"

                        chainLength = raw_input("Try Again: ")

                    print
                    numRows = raw_input("How many rows will there be? ")
                    while not self.isInt(numRows):

                        print "Input Error, Not an Integer!"

                        numRows = raw_input("Try Again: ")

                    self.rainbowMaker.setDimensions(chainLength, numRows)

                    #Get the file name
                    print
                    fileName = raw_input("What's the file name: ")
                    self.rainbowMaker.setFileName(fileName)

                    #Get the go-ahead
                    print
                    print "Ready to go?"
                    print
                    print "(Create)"
                    print
                    print "(Back)"
                    print "(Exit)"
                    userInput = raw_input("Choice: ")

                    #Sterolize inputs
                    goodNames = {"Create", "create", "Back", "back", "Exit", "exit"}
                    while not userInput in goodNames:

                        print "Input Error!"

                        userInput = raw_input("Try Again: ")

                    if userInput in ("Create", "create"):

                        self.state = "serverRainMakerSearchingScreen"

                    elif userInput in ("Back", "back"):

                        self.state = "serverStartScreen"

                    else:

                        #We're done
                        self.done = True

                #############################################
                #############################################
                #if we're at the serverRainMakerSearchingScreen state (Screen)
                elif state == "serverRainMakerSearchingScreen":

                    #display results and wait for user interaction
                    print "============="
                    print "serverRainMakerSearchingScreen"

                    #Start up the networkServer class (as sub-process in the background)
                    self.networkServer.start()

                    self.clock = time()


                    #rainbowMaker2 = RainbowMaker()

                    #Give new rainbowMaker (node) info it needs through a string (sent over network)
                    #rainbowMaker2.setVariables(self.rainbowMaker.serverString())
                    paramsChunk = self.rainbowMaker.makeParamsChunk()

                    #Get the file ready (put info in first line)
                    self.rainbowMaker.setupFile()

                    #Stuff for those pretty status pictures stuff
                    starCounter = 0
                    whiteL = ""
                    whiteR = "            "

                    #While we haven't gotten all through the file or found the key...
                    while not self.rainbowMaker.isDone():

                        #Clear the screen and re-draw
                        os.system('cls' if os.name == 'nt' else 'clear')
                        #Ohhh, pretty status pictures
                        print "Creating--> [" + whiteL + "*" + whiteR + "]"
                        if starCounter > 11:
                            starCounter = 0
                            whiteL = ""
                            whiteR = "            "
                        else:
                            starCounter += 1
                            whiteL = whiteL + " "
                            whiteR = whiteR[:-1]


                        #What's the server saying:
                        rec = self.controllerPipe.recv()

                        #If the server needs a chunk, give one. (this should be the first thing server says)
                        if rec == "nextChunk":

                            self.controllerPipe.send("nextChunk")

                            self.controllerPipe.send(paramsChunk)

                        #If the server needs a chunk again
                        elif rec == "chunkAgain":

                            #Get the parameters of the chunk (non-function for rainbowmaker)
                            params = self.controllerPipe.recv()

                            self.controllerPipe.send("chunkAgain")

                            self.controllerPipe.send(paramsChunk)

                        #if the server is waiting for nodes to finish
                        elif rec == "waiting":

                            self.controllerPipe.send("waiting")

                            #Placeholder
                            chrisHamm = True

                        #If the server has a done Chunk
                        elif rec == "doneChunk":

                            chunkOfDone = self.controllerPipe.recv()

                            self.controllerPipe.send("doneChunk")

                            self.rainbowMaker.putChunkInFile(chunkOfDone)

                        #Serve up the next chunk from the server-side dictionary class
                        #chunkList = self.rainbowMaker.getNextChunk()

                        #Size of chunks (number of rows to create) you want the nodes (node in this case) to do
                        #IE: number of total rows user picked divided into __ different chunks
                        #chunkSize = self.rainbowMaker.numRows()/100

                        #and process it using the node-side client
                        #chunkOfDone = rainbowMaker2.create(paramsChunk)

                        #Then give the result back to the server
                        #self.rainbowMaker.putChunkInFile(chunkOfDone)

                    elapsed = (time() - self.clock)
                    self.clock = elapsed

                    #Let the network  class know to be done
                    self.controllerPipe.send("done")

                    #Done, next screen
                    self.state = "serverRainMakerDoneScreen"

                #############################################
                #############################################
                #if we're at the serverRainMakerDoneScreen state (Screen)
                elif state == "serverRainMakerDoneScreen":

                    #display results and wait for user interaction
                    print "============="
                    print "singleRainMakerDoneScreen"

                    print "We just made ", self.rainbowMaker.getFileName()
                    print "With chain length of ", self.rainbowMaker.getLength()
                    print "And ", self.rainbowMaker.numRows(), "rows."
                    print "And it took", self.clock, "seconds."

                    print "(Back)"
                    print "(Exit)"
                    self.rainbowMaker.reset()
                    userInput = raw_input("Choice: ")

                    #Sterolize inputs
                    goodNames = {"Back", "back", "Exit", "exit"}
                    while not userInput in goodNames:

                        print "Input Error!"

                        userInput = raw_input("Try Again: ")

                    if userInput in ("Back", "back"):

                        self.state = "serverRainMakerScreen"

                    else:

                        #We're done
                        self.done = True

                ###################################### DICTIONARY (SERVER) ######################################

                #############################################
                #############################################
                #if we're at the serverDictionaryScreen state (Screen)
                elif state == "serverDictionaryScreen":

                    #Start up the networkServer class (as sub-process in the background)
                    #self.networkServer.start()

                    #What did the user pick? (Crack it!, Back, Exit)
                    print "============="
                    print "serverDictionaryScreen"
                    print

                    #Get the algorithm

                    print "What's the algorithm: "
                    print
                    print "(md5)"
                    print "(sha1)"
                    print "(sha256)"
                    print "(sha512)"
                    print
                    algo = raw_input("Choice: ")

                    #Sterolize inputs
                    goodNames = {"md5", "sha1", "sha256", "sha512"}
                    while not algo in goodNames:

                        print "Input Error!"

                        algo = raw_input("Try Again: ")

                    #Set algorithm of dictionary to user input of 'algo'
                    self.dictionary.setAlgorithm(algo)

                    #Get the file name
                    print
                    fileName = raw_input("What's the file name: ")
                    while not self.dictionary.setFileName(fileName) == "Good":

                        print "File not found..."
                        fileName = raw_input("What's the file name: ")

                    #Get the hash
                    print
                    hash = raw_input("What's the hash we're searching for: ")
                    self.dictionary.setHash(hash)

                    #Get the go-ahead

                    print
                    print "Ready to go?"
                    print
                    print "(Crack)"
                    print
                    print "(Back)"
                    print "(Exit)"
                    userInput = raw_input("Choice: ")

                    #Sterolize inputs
                    goodNames = {"Crack", "crack", "Back", "back", "Exit", "exit"}
                    while not userInput in goodNames:

                        print "Input Error!"

                        userInput = raw_input("Try Again: ")

                    if userInput in ("Crack", "crack"):

                        self.state = "serverDictionarySearchingScreen"

                    elif userInput in ("Back", "back"):

                        self.state = "serverStartScreen"

                    else:

                        #We're done
                        self.done = True

                #############################################
                #############################################
                #if we're at the singleDictionarySearchingScreen state (Screen)
                elif state == "serverDictionarySearchingScreen":

                    #display results and wait for user interaction
                    print "============="
                    print "serverDictionarySearchingScreen"

                    #Start up the networkServer class (as sub-process in the background)
                    self.networkServer.start()

                    self.clock = time()

                    #Have another dictionary (ie server-size) that chunks the data
                    #   So you don't have to send the whole file to every node
                    #dictionary2 = Dictionary.Dictionary()

                    #Give new dictionary (node) info it needs through a string (sent over network)
                    #dictionary2.setVariables(self.dictionary.serverString())

                    #Stuff for those pretty status pictures stuff
                    starCounter = 0
                    whiteL = ""
                    whiteR = "            "

                    isFound = False

                    #While we haven't gotten all through the file or found the key...
                    while not (self.dictionary.isEof() or isFound):

                        #Clear the screen and re-draw
                        os.system('cls' if os.name == 'nt' else 'clear')
                        #Ohhh, pretty status pictures
                        print "Searching--> [" + whiteL + "*" + whiteR + "]"
                        if starCounter > 11:
                            starCounter = 0
                            whiteL = ""
                            whiteR = "            "
                        else:
                            starCounter += 1
                            whiteL = whiteL + " "
                            whiteR = whiteR[:-1]

                        #What's the server saying:
                        rec = self.controllerPipe.recv()

                        #If the server needs a chunk, give one. (this should be the first thing server says)
                        if rec == "nextChunk":

                            #chunk is a Chunk object
                            chunk = self.dictionary.getNextChunk()

                            self.controllerPipe.send("nextChunk")

                            self.controllerPipe.send(chunk)

                        #If the server needs a chunk again
                        elif rec == "chunkAgain":

                            #Get the parameters of the chunk
                            params = self.controllerPipe.recv()

                            #Get the chunk again (again a Chunk object)
                            chunk = self.dictionary.getThisChunk(params)

                            self.controllerPipe.send("chunkAgain")

                            #Send the chunk again
                            self.controllerPipe.send(chunk)

                        #if the server is waiting for nodes to finish
                        elif rec == "waiting":

                            self.controllerPipe.send("waiting")

                            #Placeholder
                            chrisHamm = True

                        #If the server has a key
                        elif rec == "found":

                            self.controllerPipe.send("found")

                            #Get the key
                            key = self.controllerPipe.recv()

                            #This will help for error checking later, though for now not so much
                            #isFound = self.dictionary.isKey(key)

                            self.dictionary.setKey(key)

                    elapsed = (time() - self.clock)
                    self.clock = elapsed

                    #Let the network  class know to be done
                    self.controllerPipe.send("done")

                    #if the key has been found
                    if isFound:

                        self.state = "serverDictionaryFoundScreen"

                    else:

                        self.state = "serverDictionaryNotFoundScreen"

                #############################################
                #############################################
                #if we're at the singleDictionaryFoundScreen state (Screen)
                elif state == "serverDictionaryFoundScreen":

                    self.networkServer.join()
                    #self.networkServer.terminate()

                    #display results and wait for user interaction

                    #What did the user pick? (Crack it!, Back, Exit)
                    print "============="
                    print "serverDictionaryFoundScreen"

                    print "Key is: ", self.dictionary.showKey()
                    print "Wish a", self.dictionary.algorithm, "hash of: ", self.dictionary.getHash()
                    print "And it took", self.clock, "seconds."

                    print "(Back)"
                    print "(Exit)"
                    self.dictionary.reset()
                    userInput = raw_input("Choice: ")

                    #Sterolize inputs
                    goodNames = {"Back", "back", "Exit", "exit"}
                    while not userInput in goodNames:

                        print "Input Error!"

                        userInput = raw_input("Try Again: ")

                    if userInput in ("Back", "back"):

                        self.state = "serverDictionaryScreen"

                    else:

                        #We're done
                        self.done = True

                #############################################
                #############################################
                #if we're at the singleDictionaryNotFoundScreen state (Screen)
                elif state == "serverDictionaryNotFoundScreen":

                    #Start up the networkServer class (as sub-process in the background)
                    self.networkServer.join()
                    #self.networkServer.terminate()

                    #display results and wait for user interaction

                    #What did the user pick? (Crack it!, Back, Exit)
                    print "============="
                    print "serverDictionaryNotFoundScreen"
                    print
                    print "Sorry, we didn't find it."
                    print "Just FYI though, that took", self.clock, "seconds."
                    print
                    print "(Back)"
                    print "(Exit)"
                    self.dictionary.reset()
                    userInput = raw_input("Choice: ")

                    #Sterolize inputs
                    goodNames = {"Back", "back", "Exit", "exit"}
                    while not userInput in goodNames:

                        print "Input Error!"

                        userInput = raw_input("Try Again: ")

                    if userInput in ("Back", "back"):

                        self.state = "serverDictionaryScreen"

                    else:

                        #We're done
                        self.done = True

                #########################################################################################
                ###################################### SINGLE-USER ######################################
                ######################################################################################### vvv

                #############################################
                #############################################
                #if we're at the Single-User start state (Screen)
                elif state == "singleStartScreen":

                    #What did the user pick? (Brute-Force, Rainbow, Dictionary, Back, Exit)
                    print "============="
                    print "Single-User Mode StartScreen"
                    print
                    print "(BruteForce)"
                    print "(RainbowMake)"
                    print "(RainbowUse)"
                    print "(Dictionary)"
                    print
                    print "(Back)"
                    print "(Exit)"
                    userInput = raw_input("Choice: ")

                    #Sterolize inputs
                    goodNames = {"BruteForce", "bruteforce", "Brute", "brute", "RainbowMake", "rainbowmake", "rainmake", "make", "RainbowUse", "rainbowuse", "rainuse", "use", "Dictionary", "dictionary", "dic", "Back", "back", "Exit", "exit"}
                    while not userInput in goodNames:

                        print "Input Error!"

                        userInput = raw_input("Try Again: ")

                    if userInput in ("BruteForce", "bruteforce", "Brute", "brute"):

                        self.state = "singleBruteForceScreen"

                    elif userInput in ("RainbowMake", "rainbowmake", "rainmake", "make"):

                        self.state = "singleRainMakerScreen"

                    elif userInput in ("RainbowUse", "rainbowuse", "rainuse", "use"):

                        self.state = "singleRainUserScreen"

                    elif userInput in ("Dictionary", "dictionary", "dic"):

                        self.state = "singleDictionaryScreen"

                    elif userInput in ("Back", "back"):

                        self.state = "startScreen"

                    else:

                        #We're done
                        self.done = True

                ###################################### BRUTE-FORCE (SINGLE) ######################################

                #############################################
                #############################################
                #if we're at the  singleBruteForceScreen state (Screen)
                elif state == "singleBruteForceScreen":

                    #What did the user pick? (Crack it!, Back, Exit)
                    #userInput = GUI.getInput()

                    if userInput == "crackIt":

                        self.state = "singlerRainMakerScreen"

                        #get info from GUI and pass to Brute_Force class

                    elif userInput == "back":

                        self.state = "singleStartScreen"

                    else:

                        #We're done
                        self.done = True

                #############################################
                #############################################
                #if we're at the singleBruteSearchingScreen state (Screen)
                elif state == "singleBruteSearchingScreen":

                    #display results and wait for user interaction

                    #What did the user pick? (Crack it!, Back, Exit)
                    #userInput = GUI.getInput()

                    if userInput == "back":

                        #GUI.setState("singleBruteForceScreen")
                        self.state = "singlerRainMakerScreen"

                    else:

                        #We're done
                        self.done = True

                #############################################
                #############################################
                #if we're at the singleBruteFoundScreen state (Screen)
                elif state == "singleBruteFoundScreen":

                    #display results and wait for user interaction

                    #What did the user pick? (Crack it!, Back, Exit)
                    #userInput = GUI.getInput()

                    if userInput == "back":

                        #GUI.setState("singleBruteForceScreen")
                        self.state = "singlerRainMakerScreen"

                    else:

                        #We're done
                        self.done = True

                #############################################
                #############################################
                #if we're at the singleBruteNotFoundScreen state (Screen)
                elif state == "singleBruteNotFoundScreen":

                    #display results and wait for user interaction

                    #What did the user pick? (Crack it!, Back, Exit)
                    #userInput = GUI.getInput()

                    if userInput == "back":

                        #GUI.setState("singleBruteForceScreen")
                        self.state = "singlerRainMakerScreen"

                    else:

                        #We're done
                        self.done = True

                ###################################### RAINBOW USER (SINGLE) ######################################

                #############################################
                #############################################
                #if we're at the singleRainUserScreen state (Screen)
                elif state == "singleRainUserScreen":

                    #What did the user pick? (Crack it!, Back, Exit)
                    print "============="
                    print "singleRainUserScreen"
                    print

                    #Get the file name
                    print
                    fileName = raw_input("What's the file name: ")
                    while not self.rainbowUser.setFileName(fileName) == "Good":

                        print "File not found..."
                        fileName = raw_input("What's the file name: ")

                    #Get the hash
                    print
                    hash = raw_input("What's the hash we're searching for: ")
                    self.rainbowUser.setHash(hash)

                    #Get the go-ahead

                    print
                    print "Ready to go?"
                    print
                    print "(Crack)"
                    print
                    print "(Back)"
                    print "(Exit)"
                    userInput = raw_input("Choice: ")

                    #Sterolize inputs
                    goodNames = {"Crack", "crack", "Back", "back", "Exit", "exit"}
                    while not userInput in goodNames:

                        print "Input Error!"

                        userInput = raw_input("Try Again: ")

                    if userInput in ("Crack", "crack"):

                        self.state = "singleRainUserSearchingScreen"

                    elif userInput in ("Back", "back"):

                        self.state = "singleStartScreen"

                    else:

                        #We're done
                        self.done = True

                #############################################
                #############################################
                #if we're at the singleRainUserSearchingScreen state (Screen)
                elif state == "singleRainUserSearchingScreen":

                    #display results and wait for user interaction
                    print "============="
                    print "singleRainUserSearchingScreen"

                    self.clock = time()

                    #Gets and sets variables from file for setup
                    self.rainbowUser.gatherInfo()

                    #Have another dictionary (ie server-size) that chunks the data
                    #   So you don't have to send the whole file to every node
                    rainbowUser2 = RainbowUser()

                    #Give new dictionary (node) info it needs through a string (sent over network)
                    #dictionary2.setVariables(self.dictionary.serverString())

                    #Stuff for those pretty status pictures stuff
                    starCounter = 0
                    whiteL = ""
                    whiteR = "            "

                    #While we haven't gotten all through the file or found the key...
                    while not (self.rainbowUser.isEof() or rainbowUser2.isFound()):

                        #Clear the screen and re-draw
                        os.system('cls' if os.name == 'nt' else 'clear')
                        #Ohhh, pretty status pictures
                        print "Searching--> [" + whiteL + "*" + whiteR + "]"
                        if starCounter > 11:
                            starCounter = 0
                            whiteL = ""
                            whiteR = "            "
                        else:
                            starCounter += 1
                            whiteL = whiteL + " "
                            whiteR = whiteR[:-1]

                        #Serve up the next chunk
                        chunk = self.rainbowUser.getNextChunk()

                        #and process it using the node-side client
                        rainbowUser2.find(chunk)

                    elapsed = (time() - self.clock)
                    self.clock = elapsed

                    #if a(the) node finds a key
                    if rainbowUser2.isFound():

                        #Let the server know what the key is
                        self.rainbowUser.key = rainbowUser2.getKey()
                        self.state = "singleRainUserFoundScreen"

                    else:

                        self.state = "singleRainUserNotFoundScreen"

                #############################################
                #############################################
                #if we're at the singleRainUserFoundScreen state (Screen)
                elif state == "singleRainUserFoundScreen":

                    #display results and wait for user interaction

                    #What did the user pick? (Crack it!, Back, Exit)
                    ###userInput = GUI.getInput()
                    print "============="
                    print "singleRainUserFoundScreen"

                    print "Key is: ", self.rainbowUser.getKey()
                    print "Wish a", self.rainbowUser.algorithm, "hash of: ", self.rainbowUser.getHash()
                    print "And it took", self.clock, "seconds."

                    print "(Back)"
                    print "(Exit)"
                    self.rainbowUser.reset()
                    userInput = raw_input("Choice: ")

                    #Sterolize inputs
                    goodNames = {"Back", "back", "Exit", "exit"}
                    while not userInput in goodNames:

                        print "Input Error!"

                        userInput = raw_input("Try Again: ")

                    if userInput in ("Back", "back"):

                        self.state = "singleStartScreen"

                    else:

                        #We're done
                        self.done = True

                #############################################
                #############################################
                #if we're at the singleRainUserNotFoundScreen state (Screen)
                elif state == "singleRainUserNotFoundScreen":

                    #display results and wait for user interaction

                    #What did the user pick? (Crack it!, Back, Exit)
                    ###userInput = GUI.getInput()
                    print "============="
                    print "singleRainUserNotFoundScreen"
                    print
                    print "Sorry, we didn't find it."
                    print "Just FYI though, that took", self.clock, "seconds."
                    print
                    print "(Back)"
                    print "(Exit)"
                    self.dictionary.reset()
                    userInput = raw_input("Choice: ")

                    #Sterolize inputs
                    goodNames = {"Back", "back", "Exit", "exit"}
                    while not userInput in goodNames:

                        print "Input Error!"

                        userInput = raw_input("Try Again: ")

                    if userInput in ("Back", "back"):

                        self.state = "singleStartScreen"

                    else:

                        #We're done
                        self.done = True

                ###################################### RAINBOW MAKER (SINGLE) ######################################

                #############################################
                #############################################
                #if we're at the singleRainMakerScreen state (Screen)
                elif state == "singleRainMakerScreen":

                    print "============="
                    print "singleRainMakerScreen"
                    print

                    #Get the algorithm
                    print "What's the algorithm: "
                    print "(md5)"
                    print "(sha1)"
                    print "(sha256)"
                    print "(sha512)"
                    print
                    algo = raw_input("Choice: ")

                    #Sterolize inputs
                    goodNames = {"md5", "sha1", "sha256", "sha512"}
                    while not algo in goodNames:

                        print "Input Error!"

                        algo = raw_input("Try Again: ")

                    #Set algorithm of RainbowMaker to user input of 'algo'
                    self.rainbowMaker.setAlgorithm(algo)

                    #Get the Number of chars of key
                    print
                    numChars = raw_input("How many characters will the key be? ")
                    while not self.isInt(numChars):

                        print "Input Error, Not an Integer!"

                        numChars = raw_input("Try Again: ")

                    self.rainbowMaker.setNumChars(numChars)

                    #Get the alphabet to be used
                    print
                    print "What's the alphabet: "
                    print "0-9(d)"
                    print "a-z(a)"
                    print "A-Z(A)"
                    print "a-z&A-Z(m)"
                    print "a-z&A-Z&0-9(M)"
                    print
                    alphabet = raw_input("Choice: ")

                    #Sterolize inputs
                    goodNames = {"d", "a", "A", "m", "M"}
                    while not alphabet in goodNames:

                        print "Input Error!"

                        alphabet = raw_input("Try Again: ")
                    self.rainbowMaker.setAlphabet(alphabet)

                    #Get dimensions
                    print
                    chainLength = raw_input("How long will the chains be? ")
                    while not self.isInt(chainLength):

                        print "Input Error, Not an Integer!"

                        chainLength = raw_input("Try Again: ")

                    print
                    numRows = raw_input("How many rows will there be? ")
                    while not self.isInt(numRows):

                        print "Input Error, Not an Integer!"

                        numRows = raw_input("Try Again: ")

                    self.rainbowMaker.setDimensions(chainLength, numRows)

                    #Get the file name
                    print
                    fileName = raw_input("What's the file name: ")
                    self.rainbowMaker.setFileName(fileName)

                    #Get the go-ahead
                    print
                    print "Ready to go?"
                    print
                    print "(Create)"
                    print
                    print "(Back)"
                    print "(Exit)"
                    userInput = raw_input("Choice: ")

                    #Sterolize inputs
                    goodNames = {"Create", "create", "Back", "back", "Exit", "exit"}
                    while not userInput in goodNames:

                        print "Input Error!"

                        userInput = raw_input("Try Again: ")

                    if userInput in ("Create", "create"):

                        self.state = "singleRainMakerDoingScreen"

                    elif userInput in ("Back", "back"):

                        self.state = "singleStartScreen"

                    else:

                        #We're done
                        self.done = True

                #############################################
                #############################################
                #if we're at the singleRainMakerSearchingScreen state (Screen)
                elif state == "singleRainMakerDoingScreen":

                    #display results and wait for user interaction
                    print "============="
                    print "singleRainMakerDoingScreen"

                    self.clock = time()

                    rainbowMaker2 = RainbowMaker()

                    paramsChunk = self.rainbowMaker.makeParamsChunk()

                    #Get the file ready (put info in first line)
                    self.rainbowMaker.setupFile()

                    #Stuff for those pretty status pictures stuff
                    starCounter = 0
                    whiteL = ""
                    whiteR = "            "

                    #While we haven't gotten all through the file or found the key...
                    while not self.rainbowMaker.isDone():

                        #Clear the screen and re-draw
                        os.system('cls' if os.name == 'nt' else 'clear')
                        #Ohhh, pretty status pictures
                        print "Creating--> [" + whiteL + "*" + whiteR + "]"
                        if starCounter > 11:
                            starCounter = 0
                            whiteL = ""
                            whiteR = "            "
                        else:
                            starCounter += 1
                            whiteL = whiteL + " "
                            whiteR = whiteR[:-1]


                        chunkOfDone = rainbowMaker2.create(paramsChunk)

                        self.rainbowMaker.putChunkInFile(chunkOfDone)

                    elapsed = (time() - self.clock)
                    self.clock = elapsed

                    #If there are 10,000 or less rows, run collision detection
                    if self.rainbowMaker.getHeight() <= 10000:

                        #Clear the screen and re-draw
                        os.system('cls' if os.name == 'nt' else 'clear')

                        print "Collision Detector Running..."
                        print "(This should take less than a minute)"

                        self.colidingClock = time()

                        collisions = self.rainbowMaker.collisionFinder()

                        print "Collision Detector Complete"

                        elapsed = (time() - self.colidingClock)
                        self.colidingClock = elapsed
                        print "And it took", self.colidingClock, "seconds."
                        print

                        if collisions > 0:

                            percent = (float(collisions) / float(self.rainbowMaker.getHeight())) * 100.0

                            print str(collisions) + " Collisions found."
                            print "Out of: " + str(self.rainbowMaker.getHeight()) + " Rows Total (" + str(percent) + "%)"

                            #Get the go-ahead
                            print
                            print "Did you want to run the Collision Fixer?"
                            print
                            print "This will take at lease twice as long as"
                            print " the Collision Detector. It probably won't"
                            print " finish if you have more than 50% collisions."
                            print
                            print "If more than 20% of your lines have collisions:"
                            print " it's probably a problem with how you constructed"
                            print " the table or how small your key-space is. If you"
                            print " must use that keys-space, try shorter chains"
                            print " (thin width) and a bigger file (tall height)"
                            print " to reduce collisions"
                            print
                            print "(Yes)"
                            print "(no)"
                            print

                            userInput = raw_input("Choice: ")

                            #Sterolize inputs
                            goodNames = {"Yes", "yes", "No", "no", "Y", "n"}
                            while not userInput in goodNames:

                                print "Input Error!"

                                userInput = raw_input("Try Again: ")

                            if userInput in ("Yes", "yes", "Y"):

                                self.colidingClock2 = time()

                                while collisions > 0:

                                    #Clear the screen and re-draw
                                    os.system('cls' if os.name == 'nt' else 'clear')
                                    #Ohhh, pretty status pictures
                                    print "Fixing--> [" + whiteL + "*" + whiteR + "]"
                                    print "Collisions Still Detected: " + str(collisions)
                                    if starCounter > 11:
                                        starCounter = 0
                                        whiteL = ""
                                        whiteR = "            "
                                    else:
                                        starCounter += 1
                                        whiteL = whiteL + " "
                                        whiteR = whiteR[:-1]

                                    self.rainbowMaker.collisionFixer()

                                    collisions = self.rainbowMaker.collisionFinder()

                                elapsed = (time() - self.colidingClock2)
                                self.colidingClock2 = elapsed

                    #Done, next screen
                    self.state = "singleRainMakerDoneScreen"

                #############################################
                #############################################
                #if we're at the singleRainMakerDoneScreen state (Screen)
                elif state == "singleRainMakerDoneScreen":

                    #display results and wait for user interaction
                    print "============="
                    print "single RainMaker Done Screen"
                    print

                    print "We just made ", self.rainbowMaker.getFileName()
                    print "With chain length of ", self.rainbowMaker.getLength()
                    print "And ", self.rainbowMaker.numRows(), "rows."
                    print "And it took", self.clock, "seconds."
                    print
                    print "Plus ", self.colidingClock, " seconds for Collision Detection"
                    print "And ", self.colidingClock2, " seconds for Collision Repair"

                    print
                    print "(Back)"
                    print "(Exit)"
                    self.rainbowMaker.reset()
                    userInput = raw_input("Choice: ")

                    #Sterolize inputs
                    goodNames = {"Back", "back", "Exit", "exit"}
                    while not userInput in goodNames:

                        print "Input Error!"

                        userInput = raw_input("Try Again: ")

                    if userInput in ("Back", "back"):

                        self.state = "singleStartScreen"

                    else:

                        #We're done
                        self.done = True

                ###################################### DICTIONARY (SINGLE) ######################################

                #############################################
                #############################################
                #if we're at the singleDictionaryScreen state (Screen)
                elif state == "singleDictionaryScreen":

                    #What did the user pick? (Crack it!, Back, Exit)
                    print "============="
                    print "singleDictionaryScreen"
                    print

                    #Get the algorithm

                    print "What's the algorithm: "
                    print "(md5)"
                    print "(sha1)"
                    print "(sha256)"
                    print "(sha512)"
                    print
                    algo = raw_input("Choice: ")

                    #Sterolize inputs
                    goodNames = {"md5", "sha1", "sha256", "sha512"}
                    while not algo in goodNames:

                        print "Input Error!"

                        algo = raw_input("Try Again: ")

                    #Set algorithm of dictionary to user input of 'algo'
                    self.dictionary.setAlgorithm(algo)

                    #Get the file name
                    print
                    fileName = raw_input("What's the file name: ")
                    while not self.dictionary.setFileName(fileName) == "Good":

                        print "File not found..."
                        fileName = raw_input("What's the file name: ")

                    #Get the hash
                    print
                    hash = raw_input("What's the hash we're searching for: ")
                    self.dictionary.setHash(hash)

                    #Get the go-ahead

                    print
                    print "Ready to go?"
                    print
                    print "(Crack)"
                    print
                    print "(Back)"
                    print "(Exit)"
                    userInput = raw_input("Choice: ")

                    #Sterolize inputs
                    goodNames = {"Crack", "crack", "Back", "back", "Exit", "exit"}
                    while not userInput in goodNames:

                        print "Input Error!"

                        userInput = raw_input("Try Again: ")

                    if userInput in ("Crack", "crack"):

                        self.state = "singleDictionarySearchingScreen"

                    elif userInput in ("Back", "back"):

                        self.state = "singleStartScreen"

                    else:

                        #We're done
                        self.done = True

                #############################################
                #############################################
                #if we're at the singleDictionarySearchingScreen state (Screen)
                elif state == "singleDictionarySearchingScreen":

                    #display results and wait for user interaction
                    print "============="
                    print "singleDictionarySearchingScreen"

                    self.clock = time()

                    #Have another dictionary (ie server-size) that chunks the data
                    #   So you don't have to send the whole file to every node
                    dictionary2 = Dictionary()

                    #Give new dictionary (node) info it needs through a string (sent over network)
                    #dictionary2.setVariables(self.dictionary.serverString())

                    #Stuff for those pretty status pictures stuff
                    starCounter = 0
                    whiteL = ""
                    whiteR = "            "

                    #While we haven't gotten all through the file or found the key...
                    while not (self.dictionary.isEof() or dictionary2.isFound()):

                        #Clear the screen and re-draw
                        os.system('cls' if os.name == 'nt' else 'clear')
                        #Ohhh, pretty status pictures
                        print "Searching--> [" + whiteL + "*" + whiteR + "]"
                        if starCounter > 11:
                            starCounter = 0
                            whiteL = ""
                            whiteR = "            "
                        else:
                            starCounter += 1
                            whiteL = whiteL + " "
                            whiteR = whiteR[:-1]

                        #Serve up the next chunk
                        chunk = self.dictionary.getNextChunk()

                        #and process it using the node-side client
                        dictionary2.find(chunk)

                    elapsed = (time() - self.clock)
                    self.clock = elapsed

                    #if a(the) node finds a key
                    if dictionary2.isFound():

                        #Let the server know what the key is
                        self.dictionary.key = dictionary2.showKey()
                        self.state = "singleDictionaryFoundScreen"

                    else:

                        self.state = "singleDictionaryNotFoundScreen"

                #############################################
                #############################################
                #if we're at the singleDictionaryFoundScreen state (Screen)
                elif state == "singleDictionaryFoundScreen":

                    #display results and wait for user interaction

                    #What did the user pick? (Crack it!, Back, Exit)
                    print "============="
                    print "singleDictionaryFoundScreen"

                    print "Key is: ", self.dictionary.showKey()
                    print "Wish a", self.dictionary.algorithm, "hash of: ", self.dictionary.getHash()
                    print "And it took", self.clock, "seconds."

                    print "(Back)"
                    print "(Exit)"
                    self.dictionary.reset()
                    userInput = raw_input("Choice: ")

                    #Sterolize inputs
                    goodNames = {"Back", "back", "Exit", "exit"}
                    while not userInput in goodNames:

                        print "Input Error!"

                        userInput = raw_input("Try Again: ")

                    if userInput in ("Back", "back"):

                        self.state = "singleDictionaryScreen"

                    else:

                        #We're done
                        self.done = True

                #############################################
                #############################################
                #if we're at the singleDictionaryNotFoundScreen state (Screen)
                elif state == "singleDictionaryNotFoundScreen":

                    #display results and wait for user interaction

                    #What did the user pick? (Crack it!, Back, Exit)
                    print "============="
                    print "singleDictionaryNotFoundScreen"
                    print
                    print "Sorry, we didn't find it."
                    print "Just FYI though, that took", self.clock, "seconds."
                    print
                    print "(Back)"
                    print "(Exit)"
                    self.dictionary.reset()
                    userInput = raw_input("Choice: ")

                    #Sterolize inputs
                    goodNames = {"Back", "back", "Exit", "exit"}
                    while not userInput in goodNames:

                        print "Input Error!"

                        userInput = raw_input("Try Again: ")

                    if userInput in ("Back", "back"):

                        self.state = "singleDictionaryScreen"

                    else:

                        #We're done
                        self.done = True

    #returns true/false if value is int
    def isInt(self, value):

        try:

            int(value)
            return True

        except ValueError:

            return False

Controller()


''''
Two versions of a diagram grouped differently--Latest_Stable_Versions

startScreen

nodeStartScreen
nodeConnectingScreen
nodeConnectedToScreen
nodeDoingStuffScreen

serverStartScreen
serverBruteScreen
serverBruteSearchingScreen
serverBruteFoundScreen
serverBruteNotFoundScreen
serverRainScreen ---deleted, just use server main
serverRainUserScreen
serverRainUserSearchingScreen
serverRainUserFoundScreen
serverRainUserNotFoundScreen
serverRainMakerScreen
serverRainMakerDoingScreen
serverRainMakerDoneScreen
serverDictionaryScreen
serverDictionarySearchingScreen
serverDictionaryFoundScreen
serverDictionaryNotFoundScreen

singleStartScreen
singleBruteScreen
singleBruteSearchingScreen
singleBruteFoundScreen
singleBruteNotFoundScreen
singleRainScreen
singleRainUserScreen
singleRainUserSearchingScreen
singleRainUserFoundScreen
singleRainUserNotFoundScreen
singleRainMakerScreen
singleRainMakerDoingScreen
singleRainMakerDoneScreen
singleDictionaryScreen
singleDictionarySearchingScreen
singleDictionaryFoundScreen
singleDictionaryNotFoundScreen


Note: screen/state is used interchangeably.
choice -> screen (attributes)

-> start
    node -> node start screen (get server's ip adress from user)
        be a node -> connecting... screen
            -> connected to (server) screen (server's ip displayed)
            -> doing stuff screen (server's ip displayed)
    server -> server start screen
        brute force -> server brute screen (get all info from user)
            crack it -> server brute searching... screen (display info to user)
                -> server brute found screen
                -> server brute not found screen
        rainbow tables -> server rain screen
            use -> server rainuser screen (get all info from user)
                crack it -> server rainuser searching... screen (display all info for user)
                    -> server rainbowuser found screen
                    -> server rainbowuser not found screen
            create -> server rainmaker screen (get all info from user)
                create table -> server rainmaker doing... screen
                    ->server rainmaker done screen
        dictionary -> server dictionary screen (get all info from user)
            crack it -> server dictionary searching... screen (display info to user)
                -> server dictionary found screen
                -> server dictionary not found screen
    single-user -> single start screen
        brute force -> single brute screen (get all info from user)
            crack it -> single brute searching... screen (display info to user)
                -> single brute found screen
                -> single brute not found screen
        rainbow tables -> single rain screen
            use -> single rainuser screen (get all info from user)
                crack it -> single rainuser searching... screen (display all info for user)
                    -> single rainbowuser found screen
                    -> single rainbowuser not found screen
            create -> single rainmaker screen (get all info from user)
                create table -> single rainmaker doing... screen
                    ->single rainmaker done screen
        dictionary -> single dictionary screen (get all info from user)
            crack it -> single dictionary searching... screen (display info to user)
                -> single dictionary found screen
                -> single dictionary not found screen
    exit -> exit!


'''''