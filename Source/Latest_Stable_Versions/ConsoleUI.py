#   Console_UI.py

#   This is a text-based UI class that connects
#   with the network server and client classes

#   Chris Bugg
#   10/7/14

#   What should work:
#   - Single -> Dictionary
#            -> Brute Force
#            ->
#            ->
#   - Server -> Dictionary
#            -> Brute Force
#            ->
#            ->
#   - Node Mode


#Imports
import time
import os
from multiprocessing import Process, Value, Array
import string

from Dictionary import Dictionary
from Brute_Force import Brute_Force
from NetworkClient import Client
from NetworkServer import Server
from RainbowMaker import RainbowMaker
from RainbowUser import RainbowUser


class ConsoleUI():

    #Class variables
    settings = dict()
    done = False
    rainbow_Maker = RainbowMaker()
    rainbow_User = RainbowUser()
    dictionary = Dictionary()
    brute_force = Brute_Force()

    #Initializing variable to a default value
    serverIP = "127.0.1.1"

    #Magical shared variables with server

    #Create a list of size __ with "0" as the elements (empty list)
    list_of_shared_variables = [0] * 5

    magic_is_done = Value('b', False)
    list_of_shared_variables[0] = magic_is_done

    magic_is_found = Value('b', False)
    list_of_shared_variables[1] = magic_is_found

    magic_key = Array('c', 128)
    list_of_shared_variables[2] = magic_key

    magic_is_connected = Value('b', False)
    list_of_shared_variables[3] = magic_is_connected

    magic_doing_stuff = Value('b', False)
    list_of_shared_variables[4] = magic_doing_stuff

    #Defining network sub-processes as class variables that are instances of the network objects
    networkServer = Process(target=Server, args=(settings, list_of_shared_variables,))
    networkClient = Process(target=Client, args=(serverIP,))

    #tempGUI Variables
    state = "startScreen"

    clock = 0
    colliding_Clock = 0
    colliding_Clock2 = 0

    #Constructor
    def __init__(self):

        if not __name__ == '__main__':

            return

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
                user_input = raw_input("Choice: ")

                #Sterolize inputs
                good_names = {"Node", "node", "n", "Server", "server", "ser", "Single", "single", "sin", "About",
                              "about", "Exit", "exit", "a"}
                while not user_input in good_names:

                    print "Input Error!"

                    user_input = raw_input("Try Again: ")

                #If user picks Node, tell GUI to go to Node start screen
                if user_input in ("Node", "node", "n"):

                    self.state = "nodeStartScreen"

                elif user_input in ("Server", "server", "ser"):

                    self.state = "serverStartScreen"

                elif user_input in ("single", "Single", "sin"):

                    self.state = "singleStartScreen"

                elif user_input in "a":

                    self.aLane = True

                    self.state = "serverStartScreen"

                elif user_input in ("About", "about"):

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
                user_input = raw_input("Choice: ")

                #Sterolize inputs
                good_names = {"back", "Back", "Exit", "exit"}
                while not user_input in good_names:

                    print "Input Error!"

                    user_input = raw_input("Try Again: ")

                if user_input in ("Back", "back"):

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
                user_input = raw_input("Choice: ")

                #Sterolize inputs
                good_names = {"Node", "node", "n", "back", "Back", "b", "Exit", "exit"}
                while not user_input in good_names:

                    print "Input Error!"

                    user_input = raw_input("Try Again: ")

                if user_input in ("Node", "node", "n"):

                    self.state = "nodeConnectingScreen"

                elif user_input in ("Back", "back", "b"):

                    self.state = "startScreen"

                else:

                    #We're done
                    self.done = True

            #############################################
            #############################################
            #if we're at the node connecting... state (Screen)
            elif state == "nodeConnectingScreen":

                self.networkClient.start()

                print "============="
                print "Start -> Node -> Connecting..."
                print

                #Stuff for those pretty status pictures stuff
                star_counter = 0
                white_l = ""
                white_r = "            "

                #While not connected, print a "connecting" bar
                while not self.list_of_shared_variables[3].value:

                    #Clear the screen and re-draw
                    os.system('cls' if os.name == 'nt' else 'clear')
                    #Ohhh, pretty status pictures
                    print "Connecting--> [" + white_l + "*" + white_r + "]"
                    if star_counter > 11:
                        star_counter = 0
                        white_l = ""
                        white_r = "            "
                    else:
                        star_counter += 1
                        white_l += " "
                        white_r = white_r[:-1]

                    time.sleep(1)

                #Got connected, so switch screens
                self.state = "nodeConnectedToScreen"

            #############################################
            #############################################
            #if we're at the node connected state (Screen)
            elif state == "nodeConnectedToScreen":

                #Stuff for those pretty status pictures stuff
                star_counter = 0
                white_l = ""
                white_r = "            "

                #While not connected, print a "connecting" bar
                while self.list_of_shared_variables[3].value and not self.list_of_shared_variables[4].value:

                    #Clear the screen and re-draw
                    os.system('cls' if os.name == 'nt' else 'clear')
                    #Ohhh, pretty status pictures
                    print "Connected--> [" + white_l + "*" + white_r + "]"
                    if star_counter > 11:
                        star_counter = 0
                        white_l = ""
                        white_r = "            "
                    else:
                        star_counter += 1
                        white_l += " "
                        white_r = white_r[:-1]

                    time.sleep(1)

                if not self.list_of_shared_variables[3].value:

                    self.state = "nodeConnectingScreen"

                elif self.list_of_shared_variables[4].value:

                    self.state = "nodeDoingStuffScreen"

            #############################################
            #############################################
            #if we're at the node connected state (Screen)
            elif state == "nodeDoingStuffScreen":

                #Stuff for those pretty status pictures stuff
                star_counter = 0
                white_l = ""
                white_r = "            "

                #While not connected, print a "connecting" bar
                while self.list_of_shared_variables[3].value and self.list_of_shared_variables[4].value:

                    #Clear the screen and re-draw
                    os.system('cls' if os.name == 'nt' else 'clear')
                    #Ohhh, pretty status pictures
                    print "Working--> [" + white_l + "*" + white_r + "]"
                    if star_counter > 11:
                        star_counter = 0
                        white_l = ""
                        white_r = "            "
                    else:
                        star_counter += 1
                        white_l += " "
                        white_r = white_r[:-1]

                    time.sleep(1)

                if not self.list_of_shared_variables[3].value:

                    self.state = "nodeConnectingScreen"

                elif not self.list_of_shared_variables[4].value:

                    self.state = "nodeConnectedScreen"

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
                if self.aLane:

                    user_input = "d"
                    print "Choice: d"

                else:

                    user_input = raw_input("Choice: ")

                #Sterolize inputs
                good_names = {"bruteForce", "brute", "bf", "b", "rainbowMake", "make", "rainbowUser", "use",
                              "dictionary", "dic", "d", "back", "Back", "b" "Exit", "exit"}
                while not user_input in good_names:

                    print "Input Error!"

                    user_input = raw_input("Try Again: ")

                if user_input in ("bruteForce", "brute", "bf", "b"):

                    self.state = "serverBruteForceScreen"

                elif user_input in ("rainbowMake", "make"):

                    self.state = "serverRainMakerScreen"

                elif user_input in ("rainbowUser", "use"):

                    self.state = "serverRainUserScreen"

                elif user_input in ("dictionary", "dic", "d"):

                    self.state = "serverDictionaryScreen"

                elif user_input in ("back", "Back", "b"):

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
                print "============="
                print "Start -> Server Mode -> Brute Force"
                print

                #Get the algorithm
                print "What's the algorithm: "
                print "(md5)"
                print "(sha1)"
                print "(sha256)"
                print "(sha512)"
                print
                algorithm = raw_input("Choice: ")

                #Sterolize inputs
                good_names = {"md5", "sha1", "sha256", "sha512"}
                while not algorithm in good_names:

                    print "Input Error!"

                    algorithm = raw_input("Try Again: ")

                #Get the alphabet to be used
                print
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
                while not self.is_valid_alphabet(alphabet):

                    print "Input Error!"

                    alphabet = raw_input("Try Again: ")

                alphabet = self.convert_to_string(alphabet)

                #Get min key length
                print
                min_key_length = raw_input("What's the minimum key length? ")
                while not self.is_int(min_key_length):

                    print "Input Error, Not an Integer!"

                    min_key_length = raw_input("Try Again: ")

                #Get max key length
                print
                max_key_length = raw_input("What's the maximum key length?")
                while not self.is_int(max_key_length):

                    print "Input Error, Not an Integer!"

                    max_key_length = raw_input("Try Again: ")

                #Get the hash
                print
                print "Are we searching for a single hash, or from a file of hashes?"
                print
                print "Single Hash (s)"
                print "From a File (f)"
                print
                single_or_file = raw_input("Choice: ")

                #Sterolize inputs
                good_names = {"single", "s", "file", "f", "Single", "File"}
                while not single_or_file in good_names:

                    print "Input Error!"

                    single_or_file = raw_input("Try Again: ")

                if single_or_file in ("single", "s", "Single"):

                    #Get the hash
                    print
                    temp_hash = raw_input("What's the hash we're searching for: ")

                elif single_or_file in ("file", "f", "File"):

                    #Get the file name
                    print
                    hash_file_name = raw_input("What's the hash file name (___.txt): ")
                    while not self.does_file_exist(hash_file_name):

                        print "File not found..."
                        hash_file_name = raw_input("What's the hash file name (___.txt): ")

                self.settings['algorithm'] = algorithm
                self.settings['hash'] = temp_hash
                self.settings['alphabet'] = alphabet
                self.settings['min key length'] = min_key_length
                self.settings['max key length'] = max_key_length
                #In the form of: "single" or "server" or "client"
                self.settings['single'] = "False"

                #Get the go-ahead
                print
                print "Ready to go?"
                print
                print "Crack That Hash! (c)"
                print
                print "Go Back (back)"
                print "(Exit)"
                user_input = raw_input("Choice: ")

                #Sterolize inputs
                good_names = {"Crack", "crack", "c", "Back", "back", "b", "Exit", "exit"}
                while not user_input in good_names:

                    print "Input Error!"

                    user_input = raw_input("Try Again: ")

                if user_input in ("Crack", "crack", "c"):

                    self.state = "serverDictionarySearchingScreen"

                elif user_input in ("Back", "back", "b"):

                    self.state = "startStartScreen"

                else:

                    #We're done
                    self.done = True

            #############################################
            #############################################
            #if we're at the serverBruteSearchingScreen state (Screen)
            elif state == "serverBruteSearchingScreen":

                #display results and wait for user interaction
                print "============="
                print "Start -> Server Mode -> Brute Force -> Searching..."

                self.networkServer.start()

                #Stuff for those pretty status pictures stuff
                star_counter = 0
                white_l = ""
                white_r = "            "

                while not self.list_of_shared_variables[0].value:

                    #Clear the screen and re-draw
                    os.system('cls' if os.name == 'nt' else 'clear')
                    #Ohhh, pretty status pictures
                    print "Searching--> [" + white_l + "*" + white_r + "]"
                    if star_counter > 11:
                        star_counter = 0
                        white_l = ""
                        white_r = "            "
                    else:
                        star_counter += 1
                        white_l += " "
                        white_r = white_r[:-1]

                    time.sleep(1)

                if self.list_of_shared_variables[1].value:

                    self.state = "serverBruteFoundScreen"

                else:

                    self.state = "serverBruteNotFoundScreen"

            #############################################
            #############################################
            #if we're at the serverBruteFoundScreen state (Screen)
            elif state == "serverBruteFoundScreen":

                print "============="
                print "Start -> Server -> Brute Force -> Found!"
                print "Key is: ", self.list_of_shared_variables[2].value
                print "Go Back (back)"
                print "(Exit)"
                user_input = raw_input("Choice: ")

                #Sterolize inputs
                good_names = {"Back", "back", "b", "Exit", "exit"}
                while not user_input in good_names:

                    print "Input Error!"

                    user_input = raw_input("Try Again: ")

                if user_input in ("Back", "back", "b"):

                    self.state = "serverBruteForceScreen"

                else:

                    #We're done
                    self.done = True


            #############################################
            #############################################
            #if we're at the serverBruteNotFoundScreen state (Screen)
            elif state == "serverBruteNotFoundScreen":

                print "============="
                print "Start -> Server -> Brute Force -> Not Found"
                print
                print "Sorry, we didn't find it."
                print "Just FYI though, that took", self.clock, "seconds."
                print
                print "Go Back (back)"
                print "(Exit)"
                user_input = raw_input("Choice: ")

                #Sterolize inputs
                good_names = {"Back", "back", "b", "Exit", "exit"}
                while not user_input in good_names:

                    print "Input Error!"

                    user_input = raw_input("Try Again: ")

                if user_input in ("Back", "back", "b"):

                    self.state = "serverBruteForceScreen"

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
                user_input = raw_input("Choice: ")

                if user_input == "crackIt":

                    ###GUI.setState("serverRainUserSearchingScreen")
                    self.state = "serverRainUserSearchingScreen"

                    #get info from GUI and pass to Brute_Force class

                elif user_input == "back":

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
                user_input = raw_input("Choice: ")

                if user_input == "back":

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
                user_input = raw_input("Choice: ")

                if user_input == "back":

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
                user_input = raw_input("Choice: ")

                if user_input == "back":

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
                algorithm = raw_input("Choice: ")

                #Sterolize inputs
                good_names = {"md5", "sha1", "sha256", "sha512"}
                while not algorithm in good_names:

                    print "Input Error!"

                    algorithm = raw_input("Try Again: ")

                #Set algorithm of RainbowMaker to user input of 'algorithm'
                self.rainbow_Maker.setAlgorithm(algorithm)

                #Get the Number of chars of key
                print
                num_chars = raw_input("How many characters will the key be? ")
                while not self.is_int(num_chars):

                    print "Input Error, Not an Integer!"

                    num_chars = raw_input("Try Again: ")

                self.rainbow_Maker.setNumChars(num_chars)

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
                good_names = {"d", "a", "A", "m", "M"}
                while not alphabet in good_names:

                    print "Input Error!"

                    alphabet = raw_input("Try Again: ")
                self.rainbow_Maker.setAlphabet(alphabet)

                #Get dimensions
                print
                chain_length = raw_input("How long will the chains be? ")
                while not self.is_int(chain_length):

                    print "Input Error, Not an Integer!"

                    chain_length = raw_input("Try Again: ")

                print
                num_rows = raw_input("How many rows will there be? ")
                while not self.is_int(num_rows):

                    print "Input Error, Not an Integer!"

                    num_rows = raw_input("Try Again: ")

                self.rainbow_Maker.setDimensions(chain_length, num_rows)

                #Get the file name
                print
                file_name = raw_input("What's the file name: ")
                self.rainbow_Maker.setFileName(file_name)

                #Get the go-ahead
                print
                print "Ready to go?"
                print
                print "(Create)"
                print
                print "(Back)"
                print "(Exit)"
                user_input = raw_input("Choice: ")

                #Sterolize inputs
                good_names = {"Create", "create", "Back", "back", "Exit", "exit"}
                while not user_input in good_names:

                    print "Input Error!"

                    user_input = raw_input("Try Again: ")

                if user_input in ("Create", "create"):

                    self.state = "serverRainMakerSearchingScreen"

                elif user_input in ("Back", "back"):

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

                #self.clock = time()


                #rainbowMaker2 = RainbowMaker()

                #Give new rainbowMaker (node) info it needs through a string (sent over network)
                #rainbowMaker2.setVariables(self.rainbowMaker.serverString())
                #paramsChunk = self.rainbow_Maker.makeParamsChunk()

                #Get the file ready (put info in first line)
                #self.rainbow_Maker.setupFile()

                #Stuff for those pretty status pictures stuff
                #star_counter = 0
                #white_l = ""
                #white_r = "            "
                '''
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
                '''
                #elapsed = (time() - self.clock)
                #self.clock = elapsed

                #Let the network  class know to be done
                #self.controllerPipe.send("done")

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

                print "We just made ", self.rainbow_Maker.getFileName()
                print "With chain length of ", self.rainbow_Maker.getLength()
                print "And ", self.rainbow_Maker.numRows(), "rows."
                print "And it took", self.clock, "seconds."

                print "(Back)"
                print "(Exit)"
                self.rainbow_Maker.reset()
                user_input = raw_input("Choice: ")

                #Sterolize inputs
                good_names = {"Back", "back", "Exit", "exit"}
                while not user_input in good_names:

                    print "Input Error!"

                    user_input = raw_input("Try Again: ")

                if user_input in ("Back", "back"):

                    self.state = "serverRainMakerScreen"

                else:

                    #We're done
                    self.done = True

            ###################################### DICTIONARY (SERVER) ######################################

            #############################################
            #############################################
            #if we're at the serverDictionaryScreen state (Screen)
            elif state == "serverDictionaryScreen":

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
                algorithm = raw_input("Choice: ")

                #Sterolize inputs
                good_names = {"md5", "sha1", "sha256", "sha512"}
                while not algorithm in good_names:

                    print "Input Error!"

                    algorithm = raw_input("Try Again: ")

                #Get the file name
                print
                file_name = raw_input("What's the file name (___.txt): ")
                while not self.does_file_exist(file_name):

                    print "File not found..."
                    file_name = raw_input("What's the file name (___.txt): ")

                #Get the hash
                print
                print "Are we searching for a single hash, or from a file of hashes?"
                print
                print "Single Hash (s)"
                print "From a File (f)"
                print
                single_or_file = raw_input("Choice: ")

                #Sterolize inputs
                good_names = {"single", "s", "file", "f", "Single", "File"}
                while not single_or_file in good_names:

                    print "Input Error!"

                    single_or_file = raw_input("Try Again: ")

                if single_or_file in ("single", "s", "Single"):

                    #Get the hash
                    print
                    temp_hash = raw_input("What's the hash we're searching for: ")

                elif single_or_file in ("file", "f", "File"):

                    #Get the file name
                    print
                    hash_file_name = raw_input("What's the hash file name (___.txt): ")
                    while not self.does_file_exist(hash_file_name):

                        print "File not found..."
                        hash_file_name = raw_input("What's the hash file name (___.txt): ")

                    #Get the file name
                    print
                    results_file = raw_input("What's file name that we'll put the results (____.txt): ")

                self.settings['algorithm'] = algorithm
                self.settings['file name'] = file_name
                self.settings['hash'] = temp_hash
                #In the form of: "single" or "server" or "client"
                self.settings['single'] = "False"

                #Get the go-ahead
                print
                print "Ready to go?"
                print
                print "Crack That Hash! (c)"
                print
                print "Go Back (back)"
                print "(Exit)"
                user_input = raw_input("Choice: ")

                #Sterolize inputs
                good_names = {"Crack", "crack", "c", "Back", "back", "b", "Exit", "exit"}
                while not user_input in good_names:

                    print "Input Error!"

                    user_input = raw_input("Try Again: ")

                if user_input in ("Crack", "crack", "c"):

                    self.state = "serverDictionarySearchingScreen"

                elif user_input in ("Back", "back", "b"):

                    self.state = "startStartScreen"

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

                #Stuff for those pretty status pictures stuff
                star_counter = 0
                white_l = ""
                white_r = "            "

                while not self.list_of_shared_variables[0].value:

                    #Clear the screen and re-draw
                    os.system('cls' if os.name == 'nt' else 'clear')
                    #Ohhh, pretty status pictures
                    print "Searching--> [" + white_l + "*" + white_r + "]"
                    if star_counter > 11:
                        star_counter = 0
                        white_l = ""
                        white_r = "            "
                    else:
                        star_counter += 1
                        white_l += " "
                        white_r = white_r[:-1]

                    time.sleep(1)

                if self.list_of_shared_variables[1].value:

                    self.state = "serverDictionaryFoundScreen"

                else:

                    self.state = "serverDictionaryNotFoundScreen"

            #############################################
            #############################################
            #if we're at the singleDictionaryFoundScreen state (Screen)
            elif state == "serverDictionaryFoundScreen":

                self.networkServer.join()

                print "============="
                print "Start -> Server -> Dictionary -> Found!"
                print "Key is: ", self.list_of_shared_variables[2].value
                print "Go Back (back)"
                print "(Exit)"
                user_input = raw_input("Choice: ")

                #Sterolize inputs
                good_names = {"Back", "back", "b", "Exit", "exit"}
                while not user_input in good_names:

                    print "Input Error!"

                    user_input = raw_input("Try Again: ")

                if user_input in ("Back", "back", "b"):

                    self.state = "serverDictionaryScreen"

                else:

                    #We're done
                    self.done = True

            #############################################
            #############################################
            #if we're at the singleDictionaryNotFoundScreen state (Screen)
            elif state == "serverDictionaryNotFoundScreen":

                print "============="
                print "Start -> Server -> Dictionary -> Not Found"
                print
                print "Sorry, we didn't find it."
                print "Just FYI though, that took", self.clock, "seconds."
                print
                print "Go Back (back)"
                print "(Exit)"
                user_input = raw_input("Choice: ")

                #Sterolize inputs
                good_names = {"Back", "back", "b", "Exit", "exit"}
                while not user_input in good_names:

                    print "Input Error!"

                    user_input = raw_input("Try Again: ")

                if user_input in ("Back", "back", "b"):

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
                user_input = raw_input("Choice: ")

                #Sterolize inputs
                good_names = {"BruteForce", "bruteforce", "Brute", "brute", "bf", "b", "RainbowMake", "rainbowmake", "rainmake", "make", "RainbowUse", "rainbowuse", "rainuse", "use", "Dictionary", "dictionary", "dic", "d", "Back", "back", "Exit", "exit"}
                while not user_input in good_names:

                    print "Input Error!"

                    user_input = raw_input("Try Again: ")

                if user_input in ("BruteForce", "bruteforce", "Brute", "brute", "bf", "b"):

                    self.state = "singleBruteForceScreen"

                elif user_input in ("RainbowMake", "rainbowmake", "rainmake", "make"):

                    self.state = "singleRainMakerScreen"

                elif user_input in ("RainbowUse", "rainbowuse", "rainuse", "use"):

                    self.state = "singleRainUserScreen"

                elif user_input in ("Dictionary", "dictionary", "dic", "d"):

                    self.state = "singleDictionaryScreen"

                elif user_input in ("Back", "back"):

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
                algorithm = raw_input("Choice: ")

                #Sterolize inputs
                good_names = {"md5", "sha1", "sha256", "sha512"}
                while not algorithm in good_names:

                    print "Input Error!"

                    algorithm = raw_input("Try Again: ")

                #Get the alphabet to be used
                print
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
                while not self.is_valid_alphabet(alphabet):

                    print "Input Error!"

                    alphabet = raw_input("Try Again: ")

                alphabet = self.convert_to_string(alphabet)

                #Get min key length
                print
                min_key_length = raw_input("What's the minimum key length? ")
                while not self.is_int(min_key_length):

                    print "Input Error, Not an Integer!"

                    min_key_length = raw_input("Try Again: ")

                #Get max key length
                print
                max_key_length = raw_input("What's the maximum key length?")
                while not self.is_int(max_key_length):

                    print "Input Error, Not an Integer!"

                    max_key_length = raw_input("Try Again: ")

                #Get the hash
                print
                print "Are we searching for a single hash, or from a file of hashes?"
                print
                print "Single Hash (s)"
                print "From a File (f)"
                print
                single_or_file = raw_input("Choice: ")

                #Sterolize inputs
                good_names = {"single", "s", "file", "f", "Single", "File"}
                while not single_or_file in good_names:

                    print "Input Error!"

                    single_or_file = raw_input("Try Again: ")

                if single_or_file in ("single", "s", "Single"):

                    #Get the hash
                    print
                    temp_hash = raw_input("What's the hash we're searching for: ")

                elif single_or_file in ("file", "f", "File"):

                    #Get the file name
                    print
                    hash_file_name = raw_input("What's the hash file name (___.txt): ")
                    while not self.does_file_exist(hash_file_name):

                        print "File not found..."
                        hash_file_name = raw_input("What's the hash file name (___.txt): ")

                self.settings['algorithm'] = algorithm
                self.settings['hash'] = temp_hash
                self.settings['alphabet'] = alphabet
                self.settings['min key length'] = min_key_length
                self.settings['max key length'] = max_key_length
                #In the form of: "single" or "server" or "client"
                self.settings['single'] = "True"

                #Get the go-ahead
                print
                print "Ready to go?"
                print
                print "Crack That Hash! (c)"
                print
                print "Go Back (back)"
                print "(Exit)"
                user_input = raw_input("Choice: ")

                #Sterolize inputs
                good_names = {"Crack", "crack", "c", "Back", "back", "b", "Exit", "exit"}
                while not user_input in good_names:

                    print "Input Error!"

                    user_input = raw_input("Try Again: ")

                if user_input in ("Crack", "crack", "c"):

                    self.state = "singleBruteSearchingScreen"

                elif user_input in ("Back", "back", "b"):

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

                self.networkServer.start()

                #Stuff for those pretty status pictures stuff
                star_counter = 0
                white_l = ""
                white_r = "            "

                while not self.list_of_shared_variables[0].value:

                    #Clear the screen and re-draw
                    os.system('cls' if os.name == 'nt' else 'clear')
                    #Ohhh, pretty status pictures
                    print "Searching--> [" + white_l + "*" + white_r + "]"
                    if star_counter > 11:
                        star_counter = 0
                        white_l = ""
                        white_r = "            "
                    else:
                        star_counter += 1
                        white_l += " "
                        white_r = white_r[:-1]

                    time.sleep(1)

                if self.list_of_shared_variables[1].value:

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
                print "Key is: ", self.list_of_shared_variables[2].value
                print "And it took", self.clock, "seconds."

                print "Go Back (back)"
                print "(Exit)"

                user_input = raw_input("Choice: ")

                #Sterolize inputs
                good_names = {"Back", "back", "b", "Exit", "exit"}
                while not user_input in good_names:

                    print "Input Error!"

                    user_input = raw_input("Try Again: ")

                if user_input in ("Back", "back", "b"):

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

                user_input = raw_input("Choice: ")

                #Sterolize inputs
                good_names = {"Back", "back", "b", "Exit", "exit"}
                while not user_input in good_names:

                    print "Input Error!"

                    user_input = raw_input("Try Again: ")

                if user_input in ("Back", "back", "b"):

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
                file_name = raw_input("What's the file name: ")
                while not self.rainbowUser.setFileName(file_name) == "Good":

                    print "File not found..."
                    file_name = raw_input("What's the file name: ")

                #Get the hash
                print
                temp_hash = raw_input("What's the hash we're searching for: ")
                self.rainbowUser.setHash(temp_hash)

                #Get the go-ahead

                print
                print "Ready to go?"
                print
                print "Crack That Hash! (c)"
                print
                print "Go Back (back)"
                print "(Exit)"
                user_input = raw_input("Choice: ")

                #Sterolize inputs
                good_names = {"Crack", "crack", "c", "Back", "back", "b", "Exit", "exit"}
                while not user_input in good_names:

                    print "Input Error!"

                    user_input = raw_input("Try Again: ")

                if user_input in ("Crack", "crack", "c"):

                    self.state = "singleRainUserSearchingScreen"

                elif user_input in ("Back", "back", "b"):

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

                #self.clock = time()

                #Gets and sets variables from file for setup
                self.rainbowUser.gatherInfo()

                #Have another dictionary (ie server-size) that chunks the data
                #   So you don't have to send the whole file to every node
                rainbowUser2 = RainbowUser()

                #Give new dictionary (node) info it needs through a string (sent over network)
                #dictionary2.setVariables(self.dictionary.serverString())

                #Stuff for those pretty status pictures stuff
                star_counter = 0
                white_l = ""
                white_r = "            "

                #While we haven't gotten all through the file or found the key...
                while not (self.rainbowUser.isEof() or rainbowUser2.isFound()):

                    #Clear the screen and re-draw
                    os.system('cls' if os.name == 'nt' else 'clear')
                    #Ohhh, pretty status pictures
                    print "Searching--> [" + white_l + "*" + white_r + "]"
                    if star_counter > 11:
                        star_counter = 0
                        white_l = ""
                        white_r = "            "
                    else:
                        star_counter += 1
                        white_l = white_l + " "
                        white_r = white_r[:-1]

                    #Serve up the next chunk
                    chunk = self.rainbowUser.getNextChunk()

                    #and process it using the node-side client
                    rainbowUser2.find(chunk)

                #elapsed = (time() - self.clock)
                #self.clock = elapsed

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
                user_input = raw_input("Choice: ")

                #Sterolize inputs
                good_names = {"Back", "back", "b", "Exit", "exit"}
                while not user_input in good_names:

                    print "Input Error!"

                    user_input = raw_input("Try Again: ")

                if user_input in ("Back", "back", "b"):

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
                user_input = raw_input("Choice: ")

                #Sterolize inputs
                good_names = {"Back", "back", "b", "Exit", "exit"}
                while not user_input in good_names:

                    print "Input Error!"

                    user_input = raw_input("Try Again: ")

                if user_input in ("Back", "back", "b"):

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
                algorithm = raw_input("Choice: ")

                #Sterolize inputs
                good_names = {"md5", "sha1", "sha256", "sha512"}
                while not algorithm in good_names:

                    print "Input Error!"

                    algorithm = raw_input("Try Again: ")

                #Set algorithm of RainbowMaker to user input of 'algorithm'
                #self.rainbowMaker.setAlgorithm(algorithm)

                #Get the Number of chars of key
                print
                key_length = raw_input("How many characters will the key be? ")
                while not self.is_int(key_length):

                    print "Input Error, Not an Integer!"

                    key_length = raw_input("Try Again: ")

                #self.rainbowMaker.setNumChars(numChars)

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
                while not self.is_valid_alphabet(alphabet):

                    print "Input Error!"

                    alphabet = raw_input("Try Again: ")

                alphabet_string = self.convert_to_string(alphabet)

                #Get dimensions
                print
                chain_length = raw_input("How long will the chains be? ")
                while not self.is_int(chain_length):

                    print "Input Error, Not an Integer!"

                    chain_length = raw_input("Try Again: ")

                print
                num_rows = raw_input("How many rows will there be? ")
                while not self.is_int(num_rows):

                    print "Input Error, Not an Integer!"

                    num_rows = raw_input("Try Again: ")

                #self.rainbowMaker.setDimensions(chain_length, num_rows)

                #Get the file name
                print
                file_name = raw_input("What's the file name: ")
                #self.rainbowMaker.setFileName(file_name)

                self.settings['algorithm'] = algorithm
                self.settings['file name'] = file_name
                self.settings['key length'] = key_length
                self.settings['alphabet'] = alphabet
                self.settings['chain length'] = chain_length
                self.settings['num rows'] = num_rows
                #In the form of: "single" or "server" or "client"
                self.settings['single'] = "True"

                #Get the go-ahead
                print
                print "Ready to go?"
                print
                print "Create the Table! (c)"
                print
                print "Go Back (back)"
                print "(Exit)"
                user_input = raw_input("Choice: ")

                #Sterolize inputs
                good_names = {"Create", "create", "c", "Back", "back", "b", "Exit", "exit"}
                while not user_input in good_names:

                    print "Input Error!"

                    user_input = raw_input("Try Again: ")

                if user_input in ("Create", "create", "c"):

                    self.state = "singleRainMakerDoingScreen"

                elif user_input in ("Back", "back", "b"):

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

                #self.clock = time()

                rainbowMaker2 = RainbowMaker()

                paramsChunk = self.rainbowMaker.makeParamsChunk()

                #Get the file ready (put info in first line)
                self.rainbowMaker.setupFile()

                #Stuff for those pretty status pictures stuff
                star_counter = 0
                white_l = ""
                white_r = "            "

                #While we haven't gotten all through the file or found the key...
                while not self.rainbowMaker.isDone():

                    #Clear the screen and re-draw
                    os.system('cls' if os.name == 'nt' else 'clear')
                    #Ohhh, pretty status pictures
                    print "Creating--> [" + white_l + "*" + white_r + "]"
                    if star_counter > 11:
                        star_counter = 0
                        white_l = ""
                        white_r = "            "
                    else:
                        star_counter += 1
                        white_l = white_l + " "
                        white_r = white_r[:-1]


                    chunkOfDone = rainbowMaker2.create(paramsChunk)

                    self.rainbowMaker.putChunkInFile(chunkOfDone)

                #elapsed = (time() - self.clock)
                #self.clock = elapsed

                #If there are 10,000 or less rows, run collision detection
                if self.rainbowMaker.getHeight() <= 10000:

                    #Clear the screen and re-draw
                    os.system('cls' if os.name == 'nt' else 'clear')

                    print "Collision Detector Running..."
                    print "(This should take less than a minute)"

                    #self.colidingClock = time()

                    collisions = self.rainbowMaker.collisionFinder()

                    print "Collision Detector Complete"

                    #elapsed = (time() - self.colidingClock)
                    #self.colidingClock = elapsed
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

                        user_input = raw_input("Choice: ")

                        #Sterolize inputs
                        good_names = {"Yes", "yes", "No", "no", "Y", "n"}
                        while not user_input in good_names:

                            print "Input Error!"

                            user_input = raw_input("Try Again: ")

                        if user_input in ("Yes", "yes", "Y"):

                            #self.colidingClock2 = time()

                            while collisions > 0:

                                #Clear the screen and re-draw
                                os.system('cls' if os.name == 'nt' else 'clear')
                                #Ohhh, pretty status pictures
                                print "Fixing--> [" + white_l + "*" + white_r + "]"
                                print "Collisions Still Detected: " + str(collisions)
                                if star_counter > 11:
                                    star_counter = 0
                                    white_l = ""
                                    white_r = "            "
                                else:
                                    star_counter += 1
                                    white_l = white_l + " "
                                    white_r = white_r[:-1]

                                self.rainbowMaker.collisionFixer()

                                collisions = self.rainbowMaker.collisionFinder()

                           # elapsed = (time() - self.colidingClock2)
                            #self.colidingClock2 = elapsed

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
                user_input = raw_input("Choice: ")

                #Sterolize inputs
                good_names = {"Back", "back", "b", "Exit", "exit"}
                while not user_input in good_names:

                    print "Input Error!"

                    user_input = raw_input("Try Again: ")

                if user_input in ("Back", "back", "b"):

                    self.state = "singleStartScreen"

                else:

                    #We're done
                    self.done = True

            ###################################### DICTIONARY (SINGLE) ######################################

            #############################################
            #############################################
            #if we're at the singleDictionaryScreen state (Screen)
            elif state == "singleDictionaryScreen":

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
                algorithm = raw_input("Choice: ")

                #Sterolize inputs
                good_names = {"md5", "sha1", "sha256", "sha512"}
                while not algorithm in good_names:

                    print "Input Error!"

                    algorithm = raw_input("Try Again: ")

                #Get the file name
                print
                file_name = raw_input("What's the file name (___.txt): ")
                while not self.does_file_exist(file_name):

                    print "File not found..."
                    file_name = raw_input("What's the file name (___.txt): ")

                #Get the hash
                print
                print "Are we searching for a single hash, or from a file of hashes?"
                print
                print "Single Hash (s)"
                print "From a File (f)"
                print
                single_or_file = raw_input("Choice: ")

                #Sterolize inputs
                good_names = {"single", "s", "file", "f", "Single", "File"}
                while not single_or_file in good_names:

                    print "Input Error!"

                    single_or_file = raw_input("Try Again: ")

                if single_or_file in ("single", "s", "Single"):

                    #Get the hash
                    print
                    temp_hash = raw_input("What's the hash we're searching for: ")

                elif single_or_file in ("file", "f", "File"):

                    #Get the file name
                    print
                    hash_file_name = raw_input("What's the hash file name (___.txt): ")
                    while not self.does_file_exist(hash_file_name):

                        print "File not found..."
                        hash_file_name = raw_input("What's the hash file name (___.txt): ")

                    #Get the file name
                    print
                    results_file = raw_input("What's file name that we'll put the results (____.txt): ")

                self.settings['algorithm'] = algorithm
                self.settings['file name'] = file_name
                self.settings['hash'] = temp_hash
                #In the form of: "single" or "server" or "client"
                self.settings['single'] = "True"

                #Get the go-ahead
                print
                print "Ready to go?"
                print
                print "Crack That Hash! (c)"
                print
                print "Go Back (back)"
                print "(Exit)"
                user_input = raw_input("Choice: ")

                #Sterolize inputs
                good_names = {"Crack", "crack", "c", "Back", "back", "b", "Exit", "exit"}
                while not user_input in good_names:

                    print "Input Error!"

                    user_input = raw_input("Try Again: ")

                if user_input in ("Crack", "crack", "c"):

                    self.state = "singleDictionarySearchingScreen"

                elif user_input in ("Back", "back", "b"):

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

                self.networkServer.start()

                #Stuff for those pretty status pictures stuff
                star_counter = 0
                white_l = ""
                white_r = "            "

                while not self.list_of_shared_variables[0].value:

                    #Clear the screen and re-draw
                    os.system('cls' if os.name == 'nt' else 'clear')
                    #Ohhh, pretty status pictures
                    print "Searching--> [" + white_l + "*" + white_r + "]"
                    if star_counter > 11:
                        star_counter = 0
                        white_l = ""
                        white_r = "            "
                    else:
                        star_counter += 1
                        white_l += " "
                        white_r = white_r[:-1]

                    time.sleep(1)

                if self.list_of_shared_variables[1].value:

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
                print "Key is: ", self.list_of_shared_variables[2].value
                print "Go Back (back)"
                print "(Exit)"
                user_input = raw_input("Choice: ")

                #Sterolize inputs
                good_names = {"Back", "back", "b", "Exit", "exit"}
                while not user_input in good_names:

                    print "Input Error!"

                    user_input = raw_input("Try Again: ")

                if user_input in ("Back", "back", "b"):

                    self.state = "singleDictionaryScreen"

                else:

                    #We're done
                    self.done = True

            #############################################
            #############################################
            #if we're at the singleDictionaryNotFoundScreen state (Screen)
            elif state == "singleDictionaryNotFoundScreen":

                print "============="
                print "Start -> Single-User Mode -> Dictionary -> Not Found"
                print
                print "Sorry, we didn't find anything."
                print "Just FYI though, that took", self.clock, "seconds."
                print
                print "Go Back (back)"
                print "(Exit)"
                user_input = raw_input("Choice: ")

                #Sterolize inputs
                good_names = {"Back", "back", "b", "Exit", "exit"}
                while not user_input in good_names:

                    print "Input Error!"

                    user_input = raw_input("Try Again: ")

                if user_input in ("Back", "back", "b"):

                    self.state = "singleDictionaryScreen"

                else:

                    #We're done
                    self.done = True

    #returns true/false if value is int
    @staticmethod
    def is_int(value):

        try:

            int(value)
            return True

        except ValueError:

            return False

    #Checks to see if file exists
    @staticmethod
    def does_file_exist(file_name):

        temp_file = str(file_name) + ".txt"

        #Checks for file not found and returns code to caller class
        try:
            temp_file = open(file_name, "r")
            temp_file.close()
            return True

        except (OSError, IOError):
            return False

    #Figure out if an alphabet choice is valid or not
    @staticmethod
    def is_valid_alphabet(alphabet_choice):

        choices_list = list(alphabet_choice)

        for choice in choices_list:

            good_choices = {"a", "A", "p", "d"}

            if not choice in good_choices:

                return False

        return True

    #Convert an alphabet choice to an alphabet string
    @staticmethod
    def convert_to_string(alphabet_choice):

        choices_list = list(alphabet_choice)

        lower_alphabet = "abcdefghijklmnopqrstuvwxyz_"
        upper_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ_"
        digits = "0123456789_"
        punctuation = string.punctuation + " "

        lower_alphabet_list = list(lower_alphabet)
        upper_alphabet_list = list(upper_alphabet)
        digits_list = list(digits)
        punctuation_list = list(punctuation)

        alphabet_string = ""

        for choice in choices_list:

            if choice == "a":

                alphabet_string += lower_alphabet_list

            elif choice == "A":

                alphabet_string += upper_alphabet_list

            elif choice == "p":

                alphabet_string += punctuation_list

            elif choice == "d":

                alphabet_string += digits_list

        return alphabet_string

ConsoleUI()