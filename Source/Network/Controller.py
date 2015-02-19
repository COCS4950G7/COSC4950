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
import string

#import GUI

from Chunk import Chunk
from Dictionary import Dictionary
from Brute_Force import Brute_Force
from NetworkClient_r13A import NetworkClient
from NetworkServer_r13A import NetworkServer
from RainbowMaker import RainbowMaker
from RainbowUser import RainbowUser


class Controller():

    #Class variables
    done = False
    rainbowMaker = RainbowMaker()
    rainbowUser = RainbowUser()
    dictionary = Dictionary()
    brute_force = Brute_Force()

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

    #Fast Lane
    aLane = False

    #Constructor
    def __init__(self):

        if not __name__ == '__main__':

            return

        args = sys.argv

        #If we didn't get the argument "-c" in command-line
        #if not args.pop() == "-c":

            #x=2 #Placeholder
            #run in standard GUI mode
            #GUI.GUI()

        #if we did get the argument "-c" in command-line
        #else:

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

                print "###################################################"
                print "#################  MIGHTY CRACKER #################"
                print "###################################################"
                print "         Brought to you by: *************"

                print "A general-purpose, hash cracking utility."

                #What did the user pick? (Node, Server, Single, Exit)
                print "============="
                print "Start"
                print
                print "Become A Node (n)"
                print "Run in Server Mode (ser)"
                print "Run in Single-User Mode (sin)"
                print
                print "About Page (about)"
                print
                print "(Exit)"
                userInput = raw_input("Choice: ")

                #Sterolize inputs
                goodNames = {"Node", "node", "n", "Server", "server", "ser", "Single", "single", "sin", "About", "about", "Exit", "exit", "a"}
                while not userInput in goodNames:

                    print "Input Error!"

                    userInput = raw_input("Try Again: ")

                #If user picks Node, tell GUI to go to Node start screen
                if userInput in ("Node", "node", "n"):

                    self.state = "nodeStartScreen"

                elif userInput in ("Server", "server", "ser"):

                    self.state = "serverStartScreen"

                elif userInput in ("single", "Single", "sin"):

                    self.state = "singleStartScreen"

                elif userInput in ("a"):

                    self.aLane = True

                    self.state = "serverStartScreen"

                elif userInput in ("About", "about"):

                    self.state = "aboutScreen"

                else:

                    #We're done
                    self.done = True

            #############################################
            #############################################
            #if we're at the node start state (Screen)
            elif state == "aboutScreen":

                #What did the user pick? (Be a node, Back, Exit)
                print "============="
                print "Start -> About"

                print
                print "Authors: Chris Hamm, John Wright, Nick Baum, Chris Bugg"
                print
                print "Description:"
                print "Our project, Mighty Cracker, is a program designed to crack hashed "
                print "passwords. It is stand-alone, GUI, and can run on Mac 10+, Linux 14+,"
                print "and Windows 7+. It uses the power of multiprocessing to fully utilize"
                print "every computer available, and can utilize a LAN to distribute the"
                print "workload over up to 90 computers (nodes). For now, the algorithms"
                print "that it can utilize are: sha 224,sha 256, sha 512, sha 1, and md5,"
                print "which cover a fair amount of the common hashing algorithms used."
                print
                print "We've implemented three common attack methods to find an original password."
                print " Dictionary takes a list of passwords, hashes them, and compares the "
                print "     hashes to the original (user inputted) hash to find a match."
                print " Brute Force will iterate through any combination (up to 16 "
                print "     characters) of letters, numbers, and symbols to brute-force"
                print "     the password, returning an original if found."
                print " Rainbow Tables are pre-computed arrays of hashes, organized to to"
                print "     provide a time-cost trade-off. The creator creates tables to"
                print "     be used at a later time, and the user uses created tables."
                print "     This gives one a huge advantage if you know what the password"
                print "     will consist of ahead of time."
                print
                print "These three methods can all be used on either a single computer"
                print "(single-user mode) or on a network of computers (similar to"
                print "a Beowulf cluster). When using on headless systems, the program"
                print "can run in terminal (text-only) mode with a -c command."
                print
                print "of the distributed, multi-process, simple GUI approach this program"
                print "takes, it is potentially more powerful and more user-friendly than"
                print "most other hash cracking software out there today, making it more"
                print "accessible for more people. Simply open the executable and crack "
                print "passwords."
                print
                print "In the future we'd like to add on the ability to crack the LMT-family"
                print "of hashes (Windows) as well as add in GPU support for additional power."
                print

                print
                print "Done?"

                print "Go Back (back)"
                print "(Exit)"
                userInput = raw_input("Choice: ")

                #Sterolize inputs
                goodNames = {"back", "Back", "Exit", "exit"}
                while not userInput in goodNames:

                    print "Input Error!"

                    userInput = raw_input("Try Again: ")

                if userInput in ("Back", "back"):

                    self.state = "startScreen"

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
                print "Start -> Node"
                print

                #Get the server's IP:
                self.serverIP = raw_input("What's the server's IP: ")

                print "Ready to Become a Node?"
                print
                print "Node (n)"
                print "Go Back (back)"
                print "(Exit)"
                userInput = raw_input("Choice: ")

                #Sterolize inputs
                goodNames = {"Node", "node", "n", "back", "Back", "b", "Exit", "exit"}
                while not userInput in goodNames:

                    print "Input Error!"

                    userInput = raw_input("Try Again: ")

                if userInput in ("Node", "node", "n"):

                    self.state = "nodeConnectingScreen"

                elif userInput in ("Back", "back", "b"):

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
                print "Start -> Node -> Connecting..."
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
                self.controllerPipe.send("requestNextChunk")

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
                        print "Start -> Node -> Connected..."

                    #If the server says we're doing stuff
                    elif rec == "doingStuff":

                        self.controllerPipe.send("doingStuff")

                        #Clear the screen and re-draw
                        os.system('cls' if os.name == 'nt' else 'clear')
                        print "============="
                        print "Start -> Node -> Working..."

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
                                self.controllerPipe.send("foundSolution")

                                #send the key we found to networkClient
                                self.controllerPipe.send(key)

                                #stop searching and get done
                                done = True

                            else:

                                #if it didn't find anything (but is done)
                                #get next command (which might be chunk or done or something else)
                                self.controllerPipe.send("requestNextChunk")

                        elif paramsList[0] == "rainbowmaker":
                            print "BROKE"
                            #This line will be unreponsive during creation
                            chunkOfDone = self.rainbowMaker.create(chunk)

                            #Tell the server we're done, and here's a chunk
                            self.controllerPipe.send("doneChunk")

                            #Send the server the chunk of done
                            self.controllerPipe.send(chunkOfDone)

                            #Ask the server for another chunk
                            self.controllerPipe.send("requestNextChunk")

                self.networkClient.join()
                #self.networkClient.terminate()

                #Go back to the nodeStart screen since we're done here
                self.state = "nodeStartScreen"


            ####################################################################################
            ###################################### SERVER ######################################
            #################################################################################### vvv

            #############################################
            #############################################
            #if we're at the Server start state (Screen)
            elif state == "serverStartScreen":

                #What did the user pick? (Brute-Force, Rainbow, Back, Exit)
                print "============="
                print "Start -> Server"
                print
                print "Brute Force Attack (b)"
                print "Rainbow Table Maker (make)"
                print "Rainbow Table Attack (use)"
                print "Dictionary Attack (d)"
                print
                print "Go Back (back)"
                print "(Exit)"
                #userInput = raw_input("Choice: ")
                if self.aLane == True:

                    userInput = "d"
                    print "Choice: d"

                else:

                    userInput = raw_input("Choice: ")

                #Sterolize inputs
                goodNames = {"bruteForce", "brute", "bf", "b", "rainbowMake", "make", "rainbowUser", "use", "dictionary", "dic", "d", "back", "Back", "b" "Exit", "exit"}
                while not userInput in goodNames:

                    print "Input Error!"

                    userInput = raw_input("Try Again: ")

                if userInput in ("bruteForce", "brute", "bf", "b"):

                    self.state = "serverBruteForceScreen"

                elif userInput in ("rainbowMake", "make"):

                    self.state = "serverRainMakerScreen"

                elif userInput in ("rainbowUser", "use"):

                    self.state = "serverRainUserScreen"

                elif userInput in ("dictionary", "dic", "d"):

                    self.state = "serverDictionaryScreen"

                elif userInput in ("back", "Back", "b"):

                    self.state = "startScreen"

                else:

                    #We're done
                    self.done = True

            ###################################### BRUTE-FORCE (SERVER) ######################################

            #############################################
            #############################################
            #if we're at the serverBruteForceScreen state (Screen)
            elif state == "Start -> Server -> Brute Force":
                print "BROKE"

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
            elif state == "Start -> Server -> Brute Force -> Searching...":
                print "BROKE"

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
            elif state == "Start -> Server -> Brute Force -> Found":
                print "BROKE"

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
            elif state == "Start -> Server -> Brute Force -> Not Found":
                print "BROKE"

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
                print "BROKE"
                #What did the user pick? (Crack it!, Back, Exit)
                ###userInput = GUI.getInput()
                print "============="
                print "Start -> Server -> Rainbow User"
                print
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
                print "BROKE"
                #display results and wait for user interaction

                #What did the user pick? (Crack it!, Back, Exit)
                ###userInput = GUI.getInput()
                print "============="
                print "Start -> Server -> Rainbow User -> Searching..."
                print
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
                print "BROKE"
                #display results and wait for user interaction

                #What did the user pick? (Crack it!, Back, Exit)
                ###userInput = GUI.getInput()
                print "============="
                print "Start -> Server -> Rainbow User -> Found!"
                print
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
                print "BROKE"
                #display results and wait for user interaction

                #What did the user pick? (Crack it!, Back, Exit)
                ###userInput = GUI.getInput()
                print "============="
                print "Start -> Server -> Rainbow User -> Not Found"
                print
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
                print "BROKE"
                print "============="
                print "Start -> Server -> Rainbow Maker"
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
                print "BROKE"
                #display results and wait for user interaction
                print "============="
                print "Start -> Server -> Rainbow Maker -> Searching..."
                print

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
                print "BROKE"
                #display results and wait for user interaction
                print "============="
                print "Start -> Server -> Rainbow Maker -> Done!"
                print

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
                print "Start -> Server -> Dictionary"
                print

                #Get the algorithm

                print "What's the algorithm: "
                print
                print "(md5)"
                print "(sha1)"
                print "(sha256)"
                print "(sha512)"
                print
                #algo = raw_input("Choice: ")
                if self.aLane == True:

                    algo = "md5"
                    print "Choice: md5"

                else:

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
                #fileName = raw_input("What's the file name (___.txt): ")
                if self.aLane == True:

                    fileName = "dic"
                    print "What's the file name (___.txt): dic"


                else:

                    fileName = raw_input("What's the file name (___.txt): ")

                while not self.dictionary.setFileName(fileName) == "Good":

                    print "File not found..."
                    fileName = raw_input("What's the file name (___.txt): ")

                #Get the hash
                print
                print "Are we searching for a single hash, or from a file of hashes?"
                print
                print "Single Hash (s)"
                print "From a File (f)"
                print
                #userInput = raw_input("Choice: ")
                if self.aLane == True:

                    userInput = "s"
                    print "Choice: s"

                else:

                    userInput = raw_input("Choice: ")

                #Sterolize inputs
                goodNames = {"single", "s", "file", "f", "Single", "File"}
                while not userInput in goodNames:

                    print "Input Error!"

                    userInput = raw_input("Try Again: ")

                if userInput in ("single", "s", "Single"):

                    #Get the hash
                    print
                    #hash = raw_input("What's the hash we're searching for: ")
                    if self.aLane == True:

                        hash = "b6e01cfff96a2233919e4f3c54b01130"
                        print "What's the hash we're searching for: b6e01cfff96a2233919e4f3c54b01130"

                    else:

                        hash = raw_input("What's the hash we're searching for: ")

                    self.dictionary.setHash(hash)
                    self.dictionary.singleHash = True

                elif userInput in ("file", "f", "File"):

                    #Get the file name
                    print
                    fileName = raw_input("What's the hash file name: ")
                    while not self.dictionary.setHashFileName(fileName) == "Good":

                        print "File not found..."
                        fileName = raw_input("What's the hash file name: ")

                    #Get the file name
                    print
                    fileName = raw_input("What's file name that we'll put the results: ")
                    self.dictionary.setDoneFileName(fileName)

                    self.dictionary.singleHash = False

                #Get the go-ahead

                print
                print "Ready to go?"
                print
                print "Crack That Hash! (c)"
                print
                print "Go Back (back)"
                print "(Exit)"
                userInput = raw_input("Choice: ")

                #Sterolize inputs
                goodNames = {"Crack", "crack", "c", "Back", "back", "b", "Exit", "exit"}
                while not userInput in goodNames:

                    print "Input Error!"

                    userInput = raw_input("Try Again: ")

                if userInput in ("Crack", "crack", "c"):

                    self.state = "serverDictionarySearchingScreen"

                elif userInput in ("Back", "back", "b"):

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
                print "Start -> Server -> Dictionary -> Searching..."
                print

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

                isEof = False

                ################ Single Hash #########################
                if self.dictionary.singleHash == True:

                    #While we haven't gotten all through the file or found the key...
                    while not (isEof or isFound):

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

                            if not self.dictionary.isEof():

                                #chunk is a Chunk object
                                chunk = self.dictionary.getNextChunk()

                                self.controllerPipe.send("nextChunk")

                                self.controllerPipe.send(chunk)

                            else:

                                isEof = True

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
                        elif rec == "done":

                            self.controllerPipe.send("done")

                            #Get the key
                            key = self.controllerPipe.recv()

                            #This will help for error checking later, though for now not so much
                            #isFound = self.dictionary.isKey(key)

                            self.dictionary.setKey(key)

                            isFound = True #added in by chris hamm

                    elapsed = (time() - self.clock)
                    self.clock = elapsed

                    #Let the network  class know to be done
                    self.controllerPipe.send("done")

                    #if the key has been found
                    if isFound:

                        self.state = "serverDictionaryFoundScreen"

                    else:

                        self.state = "serverDictionaryNotFoundScreen"

            #################### Hash File #####################
                else:

                    #While we haven't gotten all through the file or found the key...
                    while not (isEof or isFound):

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

                            if not self.dictionary.isEof():

                                #chunk is a Chunk object
                                chunk = self.dictionary.getNextChunk()

                                self.controllerPipe.send("nextChunk")

                                self.controllerPipe.send(chunk)

                            else:

                                isEof = True

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
                print "Start -> Server -> Dictionary -> Found!"

                print "Key is: ", self.dictionary.showKey()
                print "Wish a", self.dictionary.algorithm, "hash of: ", self.dictionary.getHash()
                print "And it took", self.clock, "seconds."

                print "Go Back (back)"
                print "(Exit)"
                self.dictionary.reset()
                userInput = raw_input("Choice: ")

                #Sterolize inputs
                goodNames = {"Back", "back", "b", "Exit", "exit"}
                while not userInput in goodNames:

                    print "Input Error!"

                    userInput = raw_input("Try Again: ")

                if userInput in ("Back", "back", "b"):

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
                print "Start -> Server -> Dictionary -> Not Found"
                print
                print "Sorry, we didn't find it."
                print "Just FYI though, that took", self.clock, "seconds."
                print
                print "Go Back (back)"
                print "(Exit)"
                self.dictionary.reset()
                userInput = raw_input("Choice: ")

                #Sterolize inputs
                goodNames = {"Back", "back", "b", "Exit", "exit"}
                while not userInput in goodNames:

                    print "Input Error!"

                    userInput = raw_input("Try Again: ")

                if userInput in ("Back", "back", "b"):

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
                print "Start -> Single-User Mode"
                print
                print "Brute Force Attack (b)"
                print "Rainbow Table Maker (make)"
                print "Rainbow Table Attack (use)"
                print "Dictionary Attack (d)"
                print
                print "Go Back (back)"
                print "(Exit)"
                userInput = raw_input("Choice: ")

                #Sterolize inputs
                goodNames = {"BruteForce", "bruteforce", "Brute", "brute", "bf", "b", "RainbowMake", "rainbowmake", "rainmake", "make", "RainbowUse", "rainbowuse", "rainuse", "use", "Dictionary", "dictionary", "dic", "d", "Back", "back", "Exit", "exit"}
                while not userInput in goodNames:

                    print "Input Error!"

                    userInput = raw_input("Try Again: ")

                if userInput in ("BruteForce", "bruteforce", "Brute", "brute", "bf", "b"):

                    self.state = "singleBruteForceScreen"

                elif userInput in ("RainbowMake", "rainbowmake", "rainmake", "make"):

                    self.state = "singleRainMakerScreen"

                elif userInput in ("RainbowUse", "rainbowuse", "rainuse", "use"):

                    self.state = "singleRainUserScreen"

                elif userInput in ("Dictionary", "dictionary", "dic", "d"):

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

                print "============="
                print "Start -> Single-User Mode -> Brute Force"
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
                #self.brute_force.setAlgorithm(algo)


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
                #self.brute_force.setAlphabet(alphabet)


                #Get the min and max Number of chars of key

                print
                minKeyLength = raw_input("What's the minimum key length? ")
                while not self.isInt(minKeyLength):

                    print "Input Error, Not an Integer!"

                    minKeyLength = raw_input("Try Again: ")
                print
                maxKeyLength = raw_input("What's the maximum key length? ")
                while not self.isInt(maxKeyLength):

                    print "Input Error, Not an Integer!"

                    maxKeyLength = raw_input("Try Again: ")
                #self.brute_force.setNumChars(numChars)


                #Get the hash

                print
                hash = raw_input("What's the hash we're searching for: ")
                #self.brute_force.setHash(hash)

                #Sets variables in Brute Force class?
                self.brute_force.from_controller(alphabet, algo, hash, minKeyLength, maxKeyLength)

                #Get the go-ahead

                print
                print "Ready to go?"
                print
                print "Crack That Hash! (c)"
                print
                print "Go Back (back)"
                print "(Exit)"
                userInput = raw_input("Choice: ")

                #Sterolize inputs
                goodNames = {"Crack", "crack", "c", "Back", "back", "b", "Exit", "exit"}
                while not userInput in goodNames:

                    print "Input Error!"

                    userInput = raw_input("Try Again: ")

                if userInput in ("Crack", "crack", "c"):

                    self.state = "singleBruteSearchingScreen"

                elif userInput in ("Back", "back", "b"):

                    self.state = "singleStartScreen"

                else:

                    #We're done
                    self.done = True

            #############################################
            #############################################
            #if we're at the singleBruteSearchingScreen state (Screen)
            elif state == "singleBruteSearchingScreen":

                print "============="
                print "Start -> Single-User Mode -> Brute Force -> Searching..."

                self.clock = time()

                #Splitting the work up to simulate network functionality.
                #self.brute_force will be our server instance and
                #brute_force2 will be our node (client) instance
                brute_force2 = Brute_Force()

                #Stuff for those pretty status pictures stuff
                starCounter = 0
                whiteL = ""
                whiteR = "            "

                #While we haven't exhausted our search space or found an answer:
                while not(self.brute_force.isDone() or brute_force2.isFound()):

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
                    chunk = self.brute_force.get_chunk()

                    #and process it using the node-side instance
                    brute_force2.run_chunk(chunk)

                elapsed = (time() - self.clock)
                self.clock = elapsed

                #if a(the) node finds a key
                if brute_force2.isFound():

                    #Let the server know what the key is
                    self.brute_force.key = brute_force2.getKey()
                    self.state = "singleBruteFoundScreen"

                else:

                    self.state = "singleBruteNotFoundScreen"

            #############################################
            #############################################
            #if we're at the singleBruteFoundScreen state (Screen)
            elif state == "singleBruteFoundScreen":

                #display results and wait for user interaction

                print "============="
                print "Start -> Single-User Mode -> Brute Force -> Found!"
                print
                print "Key is: ", self.brute_force.getKey()
                print "Wish a", self.brute_force.algorithm, "hash of: ", self.brute_force.origHash
                print "And it took", self.clock, "seconds."

                print "Go Back (back)"
                print "(Exit)"

                userInput = raw_input("Choice: ")

                #Sterolize inputs
                goodNames = {"Back", "back", "b", "Exit", "exit"}
                while not userInput in goodNames:

                    print "Input Error!"

                    userInput = raw_input("Try Again: ")

                #Reset the variables
                self.brute_force.reset()

                if userInput in ("Back", "back", "b"):

                    self.state = "singleStartScreen"

                else:

                    #We're done
                    self.done = True

            #############################################
            #############################################
            #if we're at the singleBruteNotFoundScreen state (Screen)
            elif state == "singleBruteNotFoundScreen":

                #display results and wait for user interaction

                print "============="
                print "Start -> Single-User Mode -> Brute Force -> Not Found"
                print
                print "Sorry, we didn't find anything."
                print "Just FYI though, that took", self.clock, "seconds."
                print
                print "Go Back (back)"
                print "(Exit)"

                userInput = raw_input("Choice: ")

                #Sterolize inputs
                goodNames = {"Back", "back", "b", "Exit", "exit"}
                while not userInput in goodNames:

                    print "Input Error!"

                    userInput = raw_input("Try Again: ")

                #Reset the variables
                self.brute_force.reset()

                if userInput in ("Back", "back", "b"):

                    self.state = "singleStartScreen"

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
                print "Start -> Single-User Mode -> Rainbow User"
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
                print "Crack That Hash! (c)"
                print
                print "Go Back (back)"
                print "(Exit)"
                userInput = raw_input("Choice: ")

                #Sterolize inputs
                goodNames = {"Crack", "crack", "c", "Back", "back", "b", "Exit", "exit"}
                while not userInput in goodNames:

                    print "Input Error!"

                    userInput = raw_input("Try Again: ")

                if userInput in ("Crack", "crack", "c"):

                    self.state = "singleRainUserSearchingScreen"

                elif userInput in ("Back", "back", "b"):

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
                print "Start -> Single-User Mode -> Rainbow User -> Searching..."

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
                print "Start -> Single-User Mode -> Rainbow User -> Found!"
                print
                print "Key is: ", self.rainbowUser.getKey()
                print "Wish a", self.rainbowUser.algorithm, "hash of: ", self.rainbowUser.getHash()
                print "And it took", self.clock, "seconds."

                print "Go Back (back)"
                print "(Exit)"
                self.rainbowUser.reset()
                userInput = raw_input("Choice: ")

                #Sterolize inputs
                goodNames = {"Back", "back", "b", "Exit", "exit"}
                while not userInput in goodNames:

                    print "Input Error!"

                    userInput = raw_input("Try Again: ")

                if userInput in ("Back", "back", "b"):

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
                print "Start -> Single-User Mode -> Rainbow User -> Not Found"
                print
                print "Sorry, we didn't find it."
                print "Just FYI though, that took", self.clock, "seconds."
                print
                print "Go Back (back)"
                print "(Exit)"
                self.dictionary.reset()
                userInput = raw_input("Choice: ")

                #Sterolize inputs
                goodNames = {"Back", "back", "b", "Exit", "exit"}
                while not userInput in goodNames:

                    print "Input Error!"

                    userInput = raw_input("Try Again: ")

                if userInput in ("Back", "back", "b"):

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
                print "Start -> Single-User Mode -> Rainbow Maker"
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
                #print "What's the alphabet: "
                print "Choose your alphabet: "
                print "0-9(d)"
                print "a-z(a)"
                print "A-Z(A)"
                print "!-~(p)"
                print
                print "Add letters together to add"
                print " multiple alphabets together."
                print "IE: dap = 0-9 & a-z & !-~"
                print

                alphabet = raw_input("Choice: ")

                #Sterolize inputs
                while not self.rainbowMaker.setAlphabet(alphabet):

                    print "Input Error!"

                    alphabet = raw_input("Try Again: ")

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
                print "Create the Table! (c)"
                print
                print "Go Back (back)"
                print "(Exit)"
                userInput = raw_input("Choice: ")

                #Sterolize inputs
                goodNames = {"Create", "create", "c", "Back", "back", "b", "Exit", "exit"}
                while not userInput in goodNames:

                    print "Input Error!"

                    userInput = raw_input("Try Again: ")

                if userInput in ("Create", "create", "c"):

                    self.state = "singleRainMakerDoingScreen"

                elif userInput in ("Back", "back", "b"):

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
                print "Start -> Single-User Mode -> Rainbow Maker -> Working..."

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
                print "Start -> Single-User Mode -> Rainbow Maker -> Done!"
                print

                print "We just made ", self.rainbowMaker.getFileName()
                print "Using the alphabet ", ''.join(self.rainbowMaker.alphabet)
                print "With chain length of ", self.rainbowMaker.getLength()
                print "And ", self.rainbowMaker.numRows(), "rows."
                print "And it took", self.clock, "seconds."
                print
                print "Plus ", self.colidingClock, " seconds for Collision Detection"
                print "And ", self.colidingClock2, " seconds for Collision Repair"

                print
                print "Go Back (back)"
                print "(Exit)"
                self.rainbowMaker.reset()
                userInput = raw_input("Choice: ")

                #Sterolize inputs
                goodNames = {"Back", "back", "b", "Exit", "exit"}
                while not userInput in goodNames:

                    print "Input Error!"

                    userInput = raw_input("Try Again: ")

                if userInput in ("Back", "back", "b"):

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
                print "Start -> Single-User Mode -> Dictionary"
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
                fileName = raw_input("What's the file name (___.txt): ")
                while not self.dictionary.setFileName(fileName) == "Good":

                    print "File not found..."
                    fileName = raw_input("What's the file name (___.txt): ")

                #Get the hash
                print
                print "Are we searching for a single hash, or from a file of hashes?"
                print
                print "Single Hash (s)"
                print "From a File (f)"
                print
                userInput = raw_input("Choice: ")

                #Sterolize inputs
                goodNames = {"single", "s", "file", "f", "Single", "File"}
                while not userInput in goodNames:

                    print "Input Error!"

                    userInput = raw_input("Try Again: ")

                if userInput in ("single", "s", "Single"):

                    #Get the hash
                    print
                    hash = raw_input("What's the hash we're searching for: ")
                    self.dictionary.setHash(hash)
                    self.dictionary.singleHash = True

                elif userInput in ("file", "f", "File"):

                    #Get the file name
                    print
                    fileName = raw_input("What's the hash file name: ")
                    while not self.dictionary.setHashFileName(fileName) == "Good":

                        print "File not found..."
                        fileName = raw_input("What's the hash file name: ")

                    #Get the file name
                    print
                    fileName = raw_input("What's file name that we'll put the results: ")
                    self.dictionary.setDoneFileName(fileName)

                    self.dictionary.singleHash = False

                #Get the go-ahead

                print
                print "Ready to go?"
                print
                print "Crack That Hash! (c)"
                print
                print "Go Back (back)"
                print "(Exit)"
                userInput = raw_input("Choice: ")

                #Sterolize inputs
                goodNames = {"Crack", "crack", "c", "Back", "back", "b", "Exit", "exit"}
                while not userInput in goodNames:

                    print "Input Error!"

                    userInput = raw_input("Try Again: ")

                if userInput in ("Crack", "crack", "c"):

                    self.state = "singleDictionarySearchingScreen"

                elif userInput in ("Back", "back", "b"):

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
                print "Start -> Single-User Mode -> Dictionary -> Searching..."

                self.clock = time()

                #Have another dictionary (ie server-size) that chunks the data
                #   So you don't have to send the whole file to every node
                dictionary2 = Dictionary()

                dictionary2.singleHash = self.dictionary.singleHash

                #Stuff for those pretty status pictures stuff
                starCounter = 0
                whiteL = ""
                whiteR = "            "

                #### Single Hash #########################
                if self.dictionary.singleHash == True:

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
                        self.dictionary.hash = dictionary2.hash
                        self.state = "singleDictionaryFoundScreen"

                    else:

                        self.state = "singleDictionaryNotFoundScreen"


                #### Hash File #####################
                else:

                    doneList = []

                    #While we haven't gotten all through the file or found the key...
                    while not self.dictionary.isEof():

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
                        doneList += dictionary2.find(chunk)

                        dictionary2.doneList = []

                    elapsed = (time() - self.clock)
                    self.clock = elapsed

                    #if a(the) node finds a key
                    if dictionary2.isFound():

                        #Let the server know what the key is
                        self.dictionary.key = dictionary2.showKey()
                        self.dictionary.hash = dictionary2.hash
                        self.dictionary.makeDoneFile(doneList)
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
                print "Start -> Single-User Mode -> Dictionary -> Found!"

                if self.dictionary.singleHash == True:
                    print "Key is: ", self.dictionary.showKey()
                    print "Wish a", self.dictionary.algorithm, "hash of: ", self.dictionary.getHash()

                else:
                    print "Your File, (", self.dictionary.doneFileName, ") of hash/key pairs is ready."
                print "And it took", self.clock, "seconds."

                print "Go Back (back)"
                print "(Exit)"
                self.dictionary.reset()
                userInput = raw_input("Choice: ")

                #Sterolize inputs
                goodNames = {"Back", "back", "b", "Exit", "exit"}
                while not userInput in goodNames:

                    print "Input Error!"

                    userInput = raw_input("Try Again: ")

                if userInput in ("Back", "back", "b"):

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
                print "Start -> Single-User Mode -> Dictionary -> Not Found"
                print
                print "Sorry, we didn't find anything."
                print "Just FYI though, that took", self.clock, "seconds."
                print
                print "Go Back (back)"
                print "(Exit)"
                self.dictionary.reset()
                userInput = raw_input("Choice: ")

                #Sterolize inputs
                goodNames = {"Back", "back", "b", "Exit", "exit"}
                while not userInput in goodNames:

                    print "Input Error!"

                    userInput = raw_input("Try Again: ")

                if userInput in ("Back", "back", "b"):

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