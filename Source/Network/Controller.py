#   Controller.py

#   This is the main class that 'controls'
#   the other classes by acting as a go-between
#   with the GUI and the actual worker classes

#   Chris Bugg
#   10/7/14

#   Update - 10/11/14 (Latest Stable Versions)
#               -> Main layout is complete, just needs more actual methods
#               ->  from supporting classes.

#   NOTE: Diagrams of the layout (approximate names) are at bottom of file

#   Update - 10/30/14 (Latest Stable Versions)
#               -> Works in Console-only mode with Dictionary class (single-user only)
#                   -> use "-c" argument to activate console-only mode
#               -> More friendly UI, W/TIMER, AND STATUS BAR!!!!!

#   ############################ W I P ###########################

# HEY!!!! CLIENT NEEDS TO START VIA THE CONTROLLER!
#BUT CONTROLLER STARTS SERVER AUTOMATICALLY
#CLIENT FAILS TO EVEN LAUNCH!!!!!!!!!!!!!!!!!




#Imports
from time import time
import sys
import os
from multiprocessing import Process, Pipe, Lock

#import GUI
#import RainbowMaker
import Dictionary
#import Brute_Force
import NetworkClient_rBugg
import NetworkServer_r7A
import Chunk




#Controller class
#from Source.Dictionary import Dictionary
#from Source.Rainbow import RainbowUser


class Controller():

    #Class variables
    done = False
    #rainbowMaker = RainbowMaker.RainbowMaker()
    #rainbowUser = RainbowUser.RainbowUser()
    dictionary = Dictionary.Dictionary()
    #brute_force = Brute_Force.Brute_Force()

    #lock = Lock()
    controllerPipe, networkPipe = Pipe()

    #Defining network sub-processes as class variables that are instances of the network objects
    networkServer = 0
    #networkServer = Process(target=NetworkServer.NetworkServer(networkPipe))
    #networkClient = 0
    #networkClient = Process(target=NetworkClient.NetworkClient(networkPipe))
    networkClient = Process(target=NetworkClient_rBugg.NetworkClient, args=(networkPipe,))

    #Initializing variable to a default value
    serverIP = "127.1.1.1"

    #tempGUI Variables
    state = "startScreen"
    #userInput = ""

    #Constructor
    def __init__(self):

        args = sys.argv

        clock = 0

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

                ################### NODE ################### vvv

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

                            #Exit our loop and go to next screen
                            done = True

                        #If the server says we're connected (or still connected)
                        elif rec == "connected":

                            #Clear the screen and re-draw
                            os.system('cls' if os.name == 'nt' else 'clear')
                            print "============="
                            print "nodeConnectedToScreen"

                        #If the server says we're doing stuff
                        elif rec == "doingStuff":

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
                                self.dictionary.find2(chunk)

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

                    self.networkClient.join()
                    #self.networkClient.terminate()

                    #Go back to the nodeStart screen since we're done here
                    self.state = "nodeStartScreen"

                    '''
                    print "(back)"
                    print "(Exit)"
                    userInput = raw_input("Choice: ")

                    #wait for job or disconnect
                    #then switch to nodeDoingStuffScreen or nodeConnectingScreen depending

                    if userInput == "back":

                        ###GUI.setState("nodeStartScreen")
                        self.state = "nodeStartScreen"

                    else:

                        #We're done
                        self.done = True
                    '''
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

                ################### SERVER ################### vvv

                #if we're at the Server start state (Screen)
                elif state == "serverStartScreen":

                    #What did the user pick? (Brute-Force, Rainbow, Back, Exit)
                    ###userInput = GUI.getInput()
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
                    goodNames = {"bruteForce", "rainbowMake", "rainbowUser", "dictionary", "back", "Back", "Exit", "exit"}
                    while not userInput in goodNames:

                        print "Input Error!"

                    if userInput == "bruteForce":

                        ###GUI.setState("serverBruteForceScreen")
                        self.state = "serverBruteForceScreen"

                        #get info from GUI and pass to Brute_Force class

                    elif userInput == "rainbowMake":

                        ###GUI.setState("serverRainMakerScreen")
                        self.state = "serverRainMakerScreen"

                        #get info from GUI and pass to Rainbow Maker class

                    elif userInput == "rainbowUser":

                        ###GUI.setState("serverRainUserScreen")
                        self.state = "serverRainUserScreen"

                        #get info from GUI and pass to Rainbow User class

                    elif userInput == "dictionary":

                        ###GUI.setState("serverDictionaryScreen")
                        self.state = "serverDictionaryScreen"

                        #get info from GUI and pass to Dictionary class

                    elif userInput == "back":

                        ###GUI.setState("startScreen")
                        self.state = "startScreen"

                    else:

                        #We're done
                        self.done = True

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

                #if we're at the serverRainMakerScreen state (Screen)
                elif state == "serverRainMakerScreen":

                    #What did the user pick? (Crack it!, Back, Exit)
                    ###userInput = GUI.getInput()
                    print "============="
                    print "serverRainMakerScreen"
                    print "(makeIt)"
                    print "(back)"
                    print "(Exit)"
                    userInput = raw_input("Choice: ")

                    if userInput == "makeIt":

                        ###GUI.setState("serverRainMakerSearchingScreen")
                        self.state = "serverRainMakerSearchingScreen"

                        #get info from GUI and pass to Brute_Force class

                    elif userInput == "back":

                        ###GUI.setState("serverStartScreen")
                        self.state = "serverStartScreen"

                    else:

                        #We're done
                        self.done = True

                #if we're at the serverRainMakerSearchingScreen state (Screen)
                elif state == "serverRainMakerSearchingScreen":

                    #display results and wait for user interaction

                    #What did the user pick? (Crack it!, Back, Exit)
                    ###userInput = GUI.getInput()
                    print "============="
                    print "serverRainMakerSearchingScreen"
                    print "(back)"
                    print "(Exit)"
                    userInput = raw_input("Choice: ")

                    if userInput == "back":

                        ###GUI.setState("serverRainMakerScreen")
                        self.state = "serverRainMakerScreen"

                    else:

                        #We're done
                        self.done = True

                #if we're at the serverRainMakerDoneScreen state (Screen)
                elif state == "serverRainMakerDoneScreen":

                    #display results and wait for user interaction

                    #What did the user pick? (Crack it!, Back, Exit)
                    ###userInput = GUI.getInput()
                    print "============="
                    print "serverRainMakerDoneScreen"
                    print "(back)"
                    print "(Exit)"
                    userInput = raw_input("Choice: ")

                    if userInput == "back":

                        ###GUI.setState("serverRainMakerScreen")
                        self.state = "serverRainMakerScreen"

                    else:

                        #We're done
                        self.done = True

                 #if we're at the serverDictionaryScreen state (Screen)
                elif state == "serverDictionaryScreen":

                    #Start up the networkServer class (as sub-process in the background)
                    self.networkServer = Process(target=NetworkServer.NetworkServer(self.networkPipe))
                    self.networkServer.start()

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

                #if we're at the singleDictionarySearchingScreen state (Screen)
                elif state == "serverDictionarySearchingScreen":

                    #display results and wait for user interaction
                    print "============="
                    print "serverDictionarySearchingScreen"

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
                            chunk = self.dictionary.getNextChunk2()

                            self.controllerPipe.send(chunk)

                        #If the server needs a chunk again
                        elif rec == "chunkAgain":

                            #Get the parameters of the chunk
                            params = self.controllerPipe.recv()

                            #Get the chunk again (again a Chunk object)
                            chunk = self.dictionary.getThisChunk2(params)

                            #Send the chunk again
                            self.controllerPipe.send(chunk)

                        #if the server is waiting for nodes to finish
                        elif rec == "waiting":

                            #Placeholder
                            chrisHamm = True

                        #If the server has a key
                        elif rec == "found":

                            #Get the key
                            key = self.controllerPipe.recv()

                            #This will help for error checking later, though for now not so much
                            isFound = self.dictionary.isKey2(key)

                    elapsed = (time() - self.clock)
                    self.clock = elapsed

                    #Let the network  class know to be done
                    self.controllerPipe.send("done")

                    #if the key has been found
                    if isFound:

                        self.state = "serverDictionaryFoundScreen"

                    else:

                        self.state = "serverDictionaryNotFoundScreen"

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

                ################### SINGLE-USER ################### vvv

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

                #if we're at the singleRainUserScreen state (Screen)
                elif state == "singleRainUserScreen":

                    #What did the user pick? (Crack it!, Back, Exit)
                    ###userInput = GUI.getInput()
                    print "============="
                    print "singleRainUserScreen"
                    print "(crackIt)"
                    print "(back)"
                    print "(Exit)"
                    userInput = raw_input("Choice: ")

                    if userInput == "crackIt":

                        ###GUI.setState("singleRainUserSearchingScreen")
                        self.state = "singleRainUserSearchingScreen"

                        #get info from GUI and pass to Brute_Force class


                    elif userInput == "back":

                        ###GUI.setState("singleStartScreen")
                        self.state = "singleStartScreen"

                    else:

                        #We're done
                        self.done = True

                #if we're at the singleRainUserSearchingScreen state (Screen)
                elif state == "singleRainUserSearchingScreen":

                    #display results and wait for user interaction

                    #What did the user pick? (Crack it!, Back, Exit)
                    ###userInput = GUI.getInput()
                    print "============="
                    print "singleRainUserSearchingScreen"
                    print "(back)"
                    print "(Exit)"
                    userInput = raw_input("Choice: ")

                    if userInput == "back":

                        ###GUI.setState("singleRainUserScreen")
                        self.state = "singleRainUserScreen"

                    else:

                        #We're done
                        self.done = True

                #if we're at the singleRainUserFoundScreen state (Screen)
                elif state == "singleRainUserFoundScreen":

                    #display results and wait for user interaction

                    #What did the user pick? (Crack it!, Back, Exit)
                    ###userInput = GUI.getInput()
                    print "============="
                    print "singleRainUserFoundScreen"
                    print "(back)"
                    print "(Exit)"
                    userInput = raw_input("Choice: ")

                    if userInput == "back":

                        ###GUI.setState("singleRainUserScreen")
                        self.state = "singleRainUserScreen"

                    else:

                        #We're done
                        self.done = True

                #if we're at the singleRainUserNotFoundScreen state (Screen)
                elif state == "singleRainUserNotFoundScreen":

                    #display results and wait for user interaction

                    #What did the user pick? (Crack it!, Back, Exit)
                    ###userInput = GUI.getInput()
                    print "============="
                    print "singleRainUserNotFoundScreen"
                    print "(back)"
                    print "(Exit)"
                    userInput = raw_input("Choice: ")

                    if userInput == "back":

                        self.state = "singleRainUserScreen"

                    else:

                        #We're done
                        self.done = True

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
                    print
                    alphabet = raw_input("Choice: ")

                    #Sterolize inputs
                    goodNames = {"d", "a", "A", "m"}
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

                #if we're at the singleRainMakerSearchingScreen state (Screen)
                elif state == "singleRainMakerDoingScreen":

                    #display results and wait for user interaction
                    print "============="
                    print "singleRainMakerDoingScreen"

                    self.clock = time()

                    #Have one ranbowMaker (ie server-size) that chunks the data
                    #   So you don't have to send the whole file to every node
                    rainbowMaker2 = RainbowMaker.RainbowMaker()

                    #Give new rainbowMaker (node) info it needs through a string (sent over network)
                    rainbowMaker2.setVariables(self.rainbowMaker.serverString())

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

                        #Serve up the next chunk from the server-side dictionary class
                        #chunkList = self.rainbowMaker.getNextChunk()

                        #Size of chunks (number of rows to create) you want the nodes (node in this case) to do
                        #IE: number of total rows user picked divided into __ different chunks
                        #chunkSize = self.rainbowMaker.numRows()/100

                        #and process it using the node-side client
                        chunkOfDone = rainbowMaker2.create()

                        #Then give the result back to the server
                        self.rainbowMaker.giveChunk(chunkOfDone)

                    elapsed = (time() - self.clock)
                    self.clock = elapsed

                    #Done, next screen
                    self.state = "singleRainMakerDoneScreen"

                #if we're at the singleRainMakerDoneScreen state (Screen)
                elif state == "singleRainMakerDoneScreen":

                    #display results and wait for user interaction

                    #What did the user pick? (Crack it!, Back, Exit)
                    ###userInput = GUI.getInput()
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

                        self.state = "singleRainMakerScreen"

                    else:

                        #We're done
                        self.done = True

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

                #if we're at the singleDictionarySearchingScreen state (Screen)
                elif state == "singleDictionarySearchingScreen":

                    #display results and wait for user interaction
                    print "============="
                    print "singleDictionarySearchingScreen"

                    self.clock = time()

                    #Have another dictionary (ie server-size) that chunks the data
                    #   So you don't have to send the whole file to every node
                    dictionary2 = Dictionary.Dictionary()

                    #Give new dictionary (node) info it needs through a string (sent over network)
                    dictionary2.setVariables(self.dictionary.serverString())

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

                        #Serve up the next chunk from the server-side dictionary class
                        chunkList = self.dictionary.getNextChunk()

                        #and process it using the node-side client
                        dictionary2.find(chunkList)

                    elapsed = (time() - self.clock)
                    self.clock = elapsed

                    #if a(the) node finds a key
                    if dictionary2.isFound():

                        #Let the server know what the key is
                        self.dictionary.key = dictionary2.showKey()
                        self.state = "singleDictionaryFoundScreen"

                    else:

                        self.state = "singleDictionaryNotFoundScreen"

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
Two versions of a diagram grouped differently--Latest Stable Versions

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