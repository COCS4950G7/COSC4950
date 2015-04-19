#   Console_UI.py

#   This is a text-based UI class that connects
#   with the network server and client classes

#   Chris Bugg
#   10/7/14

#TODO:  Implement collision detection

#Imports
import time
import os
from multiprocessing import Process, Event, Manager, freeze_support
import string
import Chunk

from NetworkClient_r15b import Client
from NetworkServer_r15c import Server

class ConsoleUI():

    if __name__ == '__main__':
        freeze_support()

        #Class variables
        settings = dict()
        done = False

        #Initializing variable to a default value
        #serverIP = "192.168.1.3"
        serverIP = "127.0.1.1"

        #Define the shared dictionary and it's values
        manager = Manager()
        dictionary = manager.dict()
        dictionary["key"] = ''
        dictionary["finished chunks"] = 0
        dictionary["total chunks"] = 0
        dictionary["server ip"] = "127.1.1.1"
        #dictionary["current chunk"] = Chunk.Chunk()
        dictionary["current word"] = ""

        #server/client/GUI signals shutdown when they're all done
        shutdown = Event()
        shutdown.clear()

        #Define the various events
        #server signals update when something has occurred (ie: chunk processed)
        update = Event()
        update.clear()

        #client signals if it's connected or not
        is_connected = Event()
        is_connected.clear()

        #client signals if it's doing stuff or not
        is_doing_stuff = Event()
        is_doing_stuff.clear()

        #Shared is a list of shared events
        shared = []
        shared.append(dictionary)
        shared.append(shutdown)
        shared.append(update)
        shared.append(is_connected)
        shared.append(is_doing_stuff)

        #Defining network sub-processes as class variables that are instances of the network objects
        networkServer = Process(target=Server, args=(settings, shared,))
        networkClient = Process(target=Client, args=(serverIP, shared,))

        state = "startScreen"

        #Displayed to the user while searching
        current_search_item = ""

        clock = 0
        #colliding_Clock = 0
        #colliding_Clock2 = 0

    #Constructor
    def __init__(self):

        if not __name__ == '__main__':
            freeze_support()
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
                print "Authors: Chris Hamm, Jon Wright, Nick Baum, Chris Bugg"
                print
                print "Description:"
                print "Our project, Mighty Cracker, is a program designed to crack hashed "
                print "passwords. It is stand-alone, GUI, and can run on Mac 10+, Linux 14+, BSD 10+"
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
                self.dictionary["server ip"] = raw_input("What's the server's IP: ")

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
                while not self.is_connected.is_set():

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
                    #self.update.wait()
                    #self.update.clear()

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

                #While connected and not doing stuff
                while self.is_connected.is_set() and not self.is_doing_stuff.is_set():

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

                #If client has been given the shutdown command, shutdown
                if self.shutdown.is_set():

                    self.state = "nodeStartScreen"
                    time.sleep(2)
                    self.networkClient.terminate()

                #if client is no longer connected, go to connecting screen
                elif not self.is_connected.is_set():

                    self.state = "nodeConnectingScreen"

                #If client is doing stuff, the go to doing stuff screen
                elif self.is_doing_stuff.is_set():

                    self.state = "nodeDoingStuffScreen"

            #############################################
            #############################################
            #if we're at the node connected state (Screen)
            elif state == "nodeDoingStuffScreen":

                #Stuff for those pretty status pictures stuff
                star_counter = 0
                white_l = ""
                white_r = "            "

                #While connected and doing stuff
                while self.is_connected.is_set() and self.is_doing_stuff.is_set() and not self.shutdown.is_set():

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

                #If client has been given the shutdown command, shutdown
                if self.shutdown.is_set():

                    self.state = "nodeStartScreen"
                    time.sleep(2)
                    self.networkClient.terminate()

                #if not connected, go to connecting screen
                elif not self.is_connected.is_set():

                    self.state = "nodeConnectingScreen"

                #if connected but not doing stuff, go to connected screen
                elif not self.is_doing_stuff.is_set():

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
                print "From a File (f)  BROKE BROKE BROKE"
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
                    self.settings['hash'] = temp_hash
                    self.settings['file mode'] = False

                elif single_or_file in ("file", "f", "File"):

                    #Get the file name
                    print
                    hash_file_name = raw_input("What's the hash file name (___.txt): ")
                    while not self.does_file_exist(hash_file_name):

                        print "File not found..."
                        hash_file_name = raw_input("What's the hash file name (___.txt): ")
                    self.settings['input file name'] = hash_file_name + ".txt"

                    #Get the file name
                    print
                    results_file = raw_input("What's file name that we'll put the results (____.txt): ")
                    self.settings['output file name'] = results_file + ".txt"
                    #Hashes from a file?
                    self.settings['file mode'] = True

                self.settings['cracking method'] = "bf"
                self.settings['algorithm'] = algorithm
                self.settings['alphabet'] = alphabet
                self.settings['min key length'] = int(min_key_length)
                self.settings['max key length'] = int(max_key_length)
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

                    self.state = "serverBruteSearchingScreen"

                elif user_input in ("Back", "back", "b"):

                    self.state = "startScreen"

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

                self.clock = time.time()

                self.networkServer.start()

                #Stuff for those pretty status pictures stuff
                star_counter = 0
                white_l = ""
                white_r = "            "

                while not self.shutdown.is_set():

                    #Clear the screen and re-draw
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print "Server IP: ", self.dictionary["server ip"]
                    #Ohhh, pretty status pictures
                    print "Searching--> [" + white_l + "*" + white_r + "]"
                    print "Finished Chunks: ", self.dictionary['finished chunks'], "/", self.dictionary['total chunks']
                    print "Current Word: ", self.dictionary["current word"]
                    if star_counter > 11:
                        star_counter = 0
                        white_l = ""
                        white_r = "            "
                    else:
                        star_counter += 1
                        white_l += " "
                        white_r = white_r[:-1]

                    time.sleep(1)
                    self.update.wait()
                    self.update.clear()

                self.clock = time.time() - self.clock

                if not self.dictionary["key"] == '':

                    self.state = "serverBruteFoundScreen"

                else:

                    self.state = "serverBruteNotFoundScreen"

            #############################################
            #############################################
            #if we're at the serverBruteFoundScreen state (Screen)
            elif state == "serverBruteFoundScreen":

                self.networkServer.terminate()

                print "============="
                print "Start -> Server -> Brute Force -> Found!"
                print

                #If we were using just one hash, not a file
                if not self.settings['file mode']:

                    print "Key is: ", self.dictionary["key"]
                    print "And that took: ", self.clock, "seconds."

                else:

                    print "We just make ", self.settings['input file name']
                    print "Which lists out the hash/key pairs we found."
                    print "And that took: ", self.clock, "seconds."

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

            #############################################
            #############################################
            #if we're at the serverBruteNotFoundScreen state (Screen)
            elif state == "serverBruteNotFoundScreen":

                self.networkServer.terminate()

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

                print "============="
                print "Start -> Server -> Rainbow User"
                print

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
                print "From a File (f)  BROKE BROKE BROKE"
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
                    self.settings['hash'] = temp_hash
                    self.settings['file mode'] = False

                elif single_or_file in ("file", "f", "File"):

                    #Get the file name
                    print
                    hash_file_name = raw_input("What's the hash file name (___.txt): ")
                    while not self.does_file_exist(hash_file_name):

                        print "File not found..."
                        hash_file_name = raw_input("What's the hash file name (___.txt): ")
                    self.settings['input file name'] = hash_file_name + ".txt"

                    #Get the file name
                    print
                    results_file = raw_input("What's file name that we'll put the results (____.txt): ")
                    self.settings['output file name'] = results_file + ".txt"
                    #Hashes from a file?
                    self.settings['file mode'] = True

                self.settings['cracking method'] = "rain"
                self.settings['file name'] = file_name + ".txt"
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

                    self.state = "serverRainUserSearchingScreen"

                elif user_input in ("Back", "back", "b"):

                    self.state = "serverStartScreen"

                else:

                    #We're done
                    self.done = True

            #############################################
            #############################################
            #if we're at the serverRainUserSearchingScreen state (Screen)
            elif state == "serverRainUserSearchingScreen":

                print "============="
                print "Start -> Server -> Rainbow User -> Searching..."

                self.clock = time.time()

                self.networkServer.start()

                #Stuff for those pretty status pictures stuff
                star_counter = 0
                white_l = ""
                white_r = "            "

                #While we haven't gotten all through the file or found the key...
                while not self.shutdown.is_set():

                    #Clear the screen and re-draw
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print "Server IP: ", self.dictionary["server ip"]
                    #Ohhh, pretty status pictures
                    print "Searching--> [" + white_l + "*" + white_r + "]"
                    print "Finished Chunks: ", self.dictionary['finished chunks'], "/", self.dictionary['total chunks']
                    print "Current Word: ", self.dictionary["current word"]
                    if star_counter > 11:
                        star_counter = 0
                        white_l = ""
                        white_r = "            "
                    else:
                        star_counter += 1
                        white_l += " "
                        white_r = white_r[:-1]

                    time.sleep(1)
                    self.update.wait()
                    self.update.clear()

                self.clock = time.time() - self.clock

                if not self.dictionary["key"] == '':

                    self.state = "serverRainUserFoundScreen"

                else:

                    self.state = "serverRainUserNotFoundScreen"

            #############################################
            #############################################
            #if we're at the serverRainUserFoundScreen state (Screen)
            elif state == "serverRainUserFoundScreen":

                self.networkServer.terminate()

                print "============="
                print "Start -> Server -> Rainbow User -> Found!"
                print

                #If we were using just one hash, not a file
                if not self.settings['file mode']:

                    print "Key is: ", self.dictionary["key"]
                    print "And that took: ", self.clock, "seconds."

                else:

                    print "We just make ", self.settings['input file name']
                    print "Which lists out the hash/key pairs we found."
                    print "And that took: ", self.clock, "seconds."

                print "(back)"
                print "(Exit)"

                user_input = raw_input("Choice: ")

                #Sterolize inputs
                good_names = {"Back", "back", "b", "Exit", "exit"}
                while not user_input in good_names:

                    print "Input Error!"

                    user_input = raw_input("Try Again: ")

                if user_input in ("Back", "back", "b"):

                    self.state = "serverStartScreen"

                else:

                    #We're done
                    self.done = True

            #############################################
            #############################################
            #if we're at the serverRainUserNotFoundScreen state (Screen)
            elif state == "serverRainUserNotFoundScreen":

                self.networkServer.terminate()

                print "============="
                print "Start -> Server -> Rainbow User -> Not Found"
                print
                print "Sorry, we didn't find anything."
                print "Just FYI though, that took", self.clock, "seconds."
                print

                print "(back)"
                print "(Exit)"

                user_input = raw_input("Choice: ")

                #Sterolize inputs
                good_names = {"Back", "back", "b", "Exit", "exit"}
                while not user_input in good_names:

                    print "Input Error!"

                    user_input = raw_input("Try Again: ")

                if user_input in ("Back", "back", "b"):

                    self.state = "serverStartScreen"

                else:

                    #We're done
                    self.done = True

            ###################################### RAINBOW MAKER (SERVER) ######################################

            #############################################
            #############################################
            #if we're at the serverRainMakerScreen state (Screen)
            elif state == "serverRainMakerScreen":

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

                #Get the Number of chars of key
                print
                key_length = raw_input("How many characters will the key be? ")
                while not self.is_int(key_length):

                    print "Input Error, Not an Integer!"

                    key_length = raw_input("Try Again: ")

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

                #Get the file name
                print
                file_name = raw_input("What's the file name (___.txt): ")

                self.settings['cracking method'] = "rainmaker"
                self.settings['algorithm'] = algorithm
                self.settings['file name'] = file_name + ".txt"
                self.settings['key length'] = key_length
                self.settings['alphabet'] = alphabet_string
                self.settings['chain length'] = chain_length
                self.settings['num rows'] = num_rows
                self.settings['single'] = "False"

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

                    self.state = "serverRainMakerDoingScreen"

                elif user_input in ("Back", "back", "b"):

                    self.state = "serverStartScreen"

                else:

                    #We're done
                    self.done = True

            #############################################
            #############################################
            #if we're at the serverRainMakerDoingScreen state (Screen)
            elif state == "serverRainMakerDoingScreen":

                print "============="
                print "Start -> Server -> Rainbow Maker -> Creating..."
                print

                self.clock = time.time()

                self.networkServer.start()

                #Stuff for those pretty status pictures stuff
                star_counter = 0
                white_l = ""
                white_r = "            "

                #While we haven't gotten all through the file or found the key...
                while not self.shutdown.is_set():

                    #Clear the screen and re-draw
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print "Server IP: ", self.dictionary["server ip"]
                    #Ohhh, pretty status pictures
                    print "Creating--> [" + white_l + "*" + white_r + "]"
                    print "Finished Chunks: ", self.dictionary['finished chunks'], "/", self.dictionary['total chunks']
                    if star_counter > 11:
                        star_counter = 0
                        white_l = ""
                        white_r = "            "
                    else:
                        star_counter += 1
                        white_l += " "
                        white_r = white_r[:-1]

                    time.sleep(1)
                    self.update.wait()
                    self.update.clear()

                self.clock = time.time() - self.clock

                #Collision Detector has been nullified with placeholder values
                #   till it is implemented in server. You should still be able
                #   to see the functionality, but this means it won't break
                #   the program when run.

                #If there are 10,000 or less rows, run collision detection
                #if self.settings['num rows'] <= 10000:
                if 1 == 2:

                    #Clear the screen and re-draw
                    os.system('cls' if os.name == 'nt' else 'clear')

                    print "Collision Detector Running..."
                    print "(This should take less than a minute)"

                    self.colidingClock = time.time()

                    #collisions = self.rainbowMaker.collisionFinder()
                    collisions = 0

                    print "Collision Detector Complete"

                    elapsed = (time.time() - self.colidingClock)
                    self.colidingClock = elapsed
                    print "And it took", self.colidingClock, "seconds."
                    print

                    if collisions > 0:

                        #percent = (float(collisions) / float(self.rainbowMaker.getHeight())) * 100.0

                        print str(collisions) + " Collisions found."
                        #print "Out of: " + str(self.rainbowMaker.getHeight()) + " Rows Total (" + str(percent) + "%)"

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

                            self.colidingClock2 = time.time()

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
                                    white_l += " "
                                    white_r = white_r[:-1]

                                #self.rainbowMaker.collisionFixer()

                                #collisions = self.rainbowMaker.collisionFinder()

                            elapsed = (time.time() - self.colidingClock2)
                            self.colidingClock2 = elapsed

                #Done, next screen
                self.state = "serverRainMakerDoneScreen"

            #############################################
            #############################################
            #if we're at the serverRainMakerDoneScreen state (Screen)
            elif state == "serverRainMakerDoneScreen":

                self.networkServer.terminate()

                #display results and wait for user interaction
                print "============="
                print "Start -> Server -> Rainbow Maker -> Done!"
                print

                print "We just made ", self.settings['file name']
                print "Using the alphabet ", self.settings['alphabet']
                print "With a chain length of", self.settings['chain length']
                print "And", self.settings['num rows'], "rows."
                print "It utilizes the", self.settings['algorithm'], "algorithm"
                print "With a key length of", self.settings['key length']
                print "And it took", self.clock, "seconds."

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

                    self.state = "serverStartScreen"

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
                print "Start -> Server Mode -> Dictionary"
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
                print "From a File (f)  BROKE BROKE BROKE"
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
                    self.settings['hash'] = temp_hash
                    self.settings['file mode'] = False

                elif single_or_file in ("file", "f", "File"):

                    #Get the file name
                    print
                    hash_file_name = raw_input("What's the hash file name (___.txt): ")
                    while not self.does_file_exist(hash_file_name):

                        print "File not found..."
                        hash_file_name = raw_input("What's the hash file name (___.txt): ")
                    self.settings['input file name'] = hash_file_name + ".txt"

                    #Get the file name
                    print
                    results_file = raw_input("What's file name that we'll put the results (____.txt): ")
                    self.settings['output file name'] = results_file + ".txt"
                    #Hashes from a file?
                    self.settings['file mode'] = True

                self.settings['cracking method'] = "dic"
                self.settings['algorithm'] = algorithm
                self.settings['file name'] = file_name + ".txt"
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

                self.clock = time.time()

                #Start up the networkServer class (as sub-process in the background)
                self.networkServer.start()

                #Stuff for those pretty status pictures stuff
                star_counter = 0
                white_l = ""
                white_r = "            "

                while not self.shutdown.is_set():

                    #Clear the screen and re-draw
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print "Server IP: ", self.dictionary["server ip"]
                    #Ohhh, pretty status pictures
                    print "Searching--> [" + white_l + "*" + white_r + "]"
                    print "Finished Chunks: ", self.dictionary['finished chunks'], "/", self.dictionary['total chunks']
                    print "Current Word: ", self.dictionary["current word"]
                    if star_counter > 11:
                        star_counter = 0
                        white_l = ""
                        white_r = "            "
                    else:
                        star_counter += 1
                        white_l += " "
                        white_r = white_r[:-1]

                    time.sleep(1)
                    self.update.wait()
                    self.update.clear()

                self.clock = time.time() - self.clock

                if not self.dictionary["key"] == '':

                    self.state = "serverDictionaryFoundScreen"

                else:

                    self.state = "serverDictionaryNotFoundScreen"

            #############################################
            #############################################
            #if we're at the singleDictionaryFoundScreen state (Screen)
            elif state == "serverDictionaryFoundScreen":

                self.networkServer.terminate()

                print "============="
                print "Start -> Server -> Dictionary -> Found!"
                print

                #If we were using just one hash, not a file
                if not self.settings['file mode']:

                    print "Key is: ", self.dictionary["key"]
                    print "And that took: ", self.clock, "seconds."

                else:

                    print "We just make ", self.settings['input file name']
                    print "Which lists out the hash/key pairs we found."
                    print "And that took: ", self.clock, "seconds."

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

            #############################################
            #############################################
            #if we're at the singleDictionaryNotFoundScreen state (Screen)
            elif state == "serverDictionaryNotFoundScreen":

                self.networkServer.terminate()

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
                good_names = {"BruteForce", "bruteforce", "Brute", "brute", "bf", "b", "RainbowMake", "rainbowmake",
                              "rainmake", "make", "RainbowUse", "rainbowuse", "rainuse", "use", "Dictionary",
                              "dictionary", "dic", "d", "Back", "back", "Exit", "exit"}
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
                max_key_length = raw_input("What's the maximum key length? ")
                while not self.is_int(max_key_length):

                    print "Input Error, Not an Integer!"

                    max_key_length = raw_input("Try Again: ")

                #Get the hash
                print
                print "Are we searching for a single hash, or from a file of hashes?"
                print
                print "Single Hash (s)"
                print "From a File (f)  BROKE BROKE BROKE"
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
                    self.settings['hash'] = temp_hash
                    self.settings['file mode'] = False

                elif single_or_file in ("file", "f", "File"):

                    #Get the file name
                    print
                    hash_file_name = raw_input("What's the hash file name (___.txt): ")
                    while not self.does_file_exist(hash_file_name):

                        print "File not found..."
                        hash_file_name = raw_input("What's the hash file name (___.txt): ")
                    self.settings['input file name'] = hash_file_name + ".txt"

                    #Get the file name
                    print
                    results_file = raw_input("What's file name that we'll put the results (____.txt): ")
                    self.settings['output file name'] = results_file + ".txt"
                    #Hashes from a file?
                    self.settings['file mode'] = True

                self.settings['cracking method'] = "bf"
                self.settings['algorithm'] = algorithm
                self.settings['alphabet'] = alphabet
                self.settings['min key length'] = int(min_key_length)
                self.settings['max key length'] = int(max_key_length)
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

                self.clock = time.time()

                self.networkServer.start()

                #Stuff for those pretty status pictures stuff
                star_counter = 0
                white_l = ""
                white_r = "            "

                while not self.shutdown.is_set():

                    #Clear the screen and re-draw
                    os.system('cls' if os.name == 'nt' else 'clear')
                    #Ohhh, pretty status pictures
                    print "Searching--> [" + white_l + "*" + white_r + "]"
                    print "Finished Chunks: ", self.dictionary['finished chunks'], "/", self.dictionary['total chunks']
                    print "Current Prefix: ", self.dictionary["current word"]
                    if star_counter > 11:
                        star_counter = 0
                        white_l = ""
                        white_r = "            "
                    else:
                        star_counter += 1
                        white_l += " "
                        white_r = white_r[:-1]

                    time.sleep(1)
                    self.update.wait()
                    self.update.clear()

                self.clock = time.time() - self.clock

                if not self.dictionary["key"] == '':

                    self.state = "singleBruteFoundScreen"

                else:

                    self.state = "singleBruteNotFoundScreen"

            #############################################
            #############################################
            #if we're at the singleBruteFoundScreen state (Screen)
            elif state == "singleBruteFoundScreen":

                self.networkServer.terminate()

                print "============="
                print "Start -> Single-User Mode -> Brute Force -> Found!"
                print

                #If we were using just one hash, not a file
                if not self.settings['file mode']:

                    print "Key is: ", self.dictionary["key"]
                    print "And that took: ", self.clock, "seconds."

                else:

                    print "We just make ", self.settings['input file name']
                    print "Which lists out the hash/key pairs we found."
                    print "And that took: ", self.clock, "seconds."

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

                self.networkServer.terminate()

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
                file_name = raw_input("What's the file name (___.txt): ")
                while not self.does_file_exist(file_name):

                    print "File not found..."
                    file_name = raw_input("What's the file name (___.txt): ")

                #Get the hash
                print
                print "Are we searching for a single hash, or from a file of hashes?"
                print
                print "Single Hash (s)"
                print "From a File (f)  BROKE BROKE BROKE"
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
                    self.settings['hash'] = temp_hash
                    self.settings['file mode'] = False

                elif single_or_file in ("file", "f", "File"):

                    #Get the file name
                    print
                    hash_file_name = raw_input("What's the hash file name (___.txt): ")
                    while not self.does_file_exist(hash_file_name):

                        print "File not found..."
                        hash_file_name = raw_input("What's the hash file name (___.txt): ")
                    self.settings['input file name'] = hash_file_name + ".txt"

                    #Get the file name
                    print
                    results_file = raw_input("What's file name that we'll put the results (____.txt): ")
                    self.settings['output file name'] = results_file + ".txt"
                    #Hashes from a file?
                    self.settings['file mode'] = True

                self.settings['cracking method'] = "rain"
                self.settings['file name'] = file_name + ".txt"
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

                self.clock = time.time()

                self.networkServer.start()

                #Stuff for those pretty status pictures stuff
                star_counter = 0
                white_l = ""
                white_r = "            "

                #While we haven't gotten all through the file or found the key...
                while not self.shutdown.is_set():

                    #Clear the screen and re-draw
                    os.system('cls' if os.name == 'nt' else 'clear')
                    #Ohhh, pretty status pictures
                    print "Searching--> [" + white_l + "*" + white_r + "]"
                    print "Finished Chunks: ", self.dictionary['finished chunks'], "/", self.dictionary['total chunks']
                    print "Current Word: ", self.dictionary["current word"]
                    if star_counter > 11:
                        star_counter = 0
                        white_l = ""
                        white_r = "            "
                    else:
                        star_counter += 1
                        white_l += " "
                        white_r = white_r[:-1]

                    time.sleep(1)
                    self.update.wait()
                    self.update.clear()

                self.clock = time.time() - self.clock

                if not self.dictionary["key"] == '':

                    self.state = "singleRainUserFoundScreen"

                else:

                    self.state = "singleRainUserNotFoundScreen"

            #############################################
            #############################################
            #if we're at the singleRainUserFoundScreen state (Screen)
            elif state == "singleRainUserFoundScreen":

                self.networkServer.terminate()

                #What did the user pick? (Crack it!, Back, Exit)
                print "============="
                print "Start -> Single-User Mode -> Rainbow User -> Found!"
                print

                #If we were using just one hash, not a file
                if not self.settings['file mode']:

                    print "Key is: ", self.dictionary["key"]
                    print "And that took: ", self.clock, "seconds."

                else:

                    print "We just make ", self.settings['input file name']
                    print "Which lists out the hash/key pairs we found."
                    print "And that took: ", self.clock, "seconds."

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
            #if we're at the singleRainUserNotFoundScreen state (Screen)
            elif state == "singleRainUserNotFoundScreen":

                self.networkServer.terminate()

                #What did the user pick? (Crack it!, Back, Exit)
                print "============="
                print "Start -> Single-User Mode -> Rainbow User -> Not Found"
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

                #Get the Number of chars of key
                print
                key_length = raw_input("How many characters will the key be? ")
                while not self.is_int(key_length):

                    print "Input Error, Not an Integer!"

                    key_length = raw_input("Try Again: ")

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

                alphabet_string = self.convert_to_string(alphabet)

                #Get dimensions
                print
                print "Longer chains reduce table size, but make using the table take longer."
                chain_length = raw_input("How long will the chains be? (50000?) ")
                while not self.is_int(chain_length):

                    print "Input Error, Not an Integer!"

                    chain_length = raw_input("Try Again: ")

                if int(chain_length) >= 1000000:

                    print
                    print "If the table width (length of chains) is at least 1,000,000"
                    print " the 'finished chunks' count should be multiplied by the average "
                    print " number of CPU cores per client."

                print
                print "More rows increases the size of the file and the table."
                num_rows = raw_input("How many rows will there be? (50000?) ")
                while not self.is_int(num_rows):

                    print "Input Error, Not an Integer!"

                    num_rows = raw_input("Try Again: ")

                if (int(chain_length) * int(num_rows)) < 1000000:

                    print
                    print "The total dimensions of the table (width*height) will be set to at"
                    print " least 1,000,000. Your set width won't change, but rows will be added."

                #Get the file name
                print
                file_name = raw_input("What's the file name (___.txt): ")

                self.settings['cracking method'] = "rainmaker"
                self.settings['algorithm'] = algorithm
                self.settings['file name'] = file_name + ".txt"
                self.settings['key length'] = key_length
                self.settings['alphabet'] = alphabet_string
                self.settings['chain length'] = int(chain_length)
                self.settings['num rows'] = int(num_rows)
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

                self.clock = time.time()

                self.networkServer.start()

                #Stuff for those pretty status pictures stuff
                star_counter = 0
                white_l = ""
                white_r = "            "

                #While we haven't gotten all through the file or found the key...
                while not self.shutdown.is_set():

                    #Clear the screen and re-draw
                    os.system('cls' if os.name == 'nt' else 'clear')
                    #Ohhh, pretty status pictures
                    print "Creating--> [" + white_l + "*" + white_r + "]"
                    print "Finished Chunks: ", self.dictionary['finished chunks'], "/", self.dictionary['total chunks']
                    if star_counter > 11:
                        star_counter = 0
                        white_l = ""
                        white_r = "            "
                    else:
                        star_counter += 1
                        white_l += " "
                        white_r = white_r[:-1]

                    time.sleep(1)
                    self.update.wait()
                    self.update.clear()

                self.clock = time.time() - self.clock

                #Collision Detector has been nullified with placeholder values
                #   till it is implemented in server. You should still be able
                #   to see the functionality, but this means it won't break
                #   the program when run.

                #If there are 10,000 or less rows, run collision detection
                #if self.settings['num rows'] <= 10000:
                if 1 == 2:

                    #Clear the screen and re-draw
                    os.system('cls' if os.name == 'nt' else 'clear')

                    print "Collision Detector Running..."
                    print "(This should take less than a minute)"

                    self.colidingClock = time.time()

                    #collisions = self.rainbowMaker.collisionFinder()
                    collisions = 0

                    print "Collision Detector Complete"

                    elapsed = (time.time() - self.colidingClock)
                    self.colidingClock = elapsed
                    print "And it took", self.colidingClock, "seconds."
                    print

                    if collisions > 0:

                        #percent = (float(collisions) / float(self.rainbowMaker.getHeight())) * 100.0

                        print str(collisions) + " Collisions found."
                        #print "Out of: " + str(self.rainbowMaker.getHeight()) + " Rows Total (" + str(percent) + "%)"

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

                            self.colidingClock2 = time.time()

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
                                    white_l += " "
                                    white_r = white_r[:-1]

                                #self.rainbowMaker.collisionFixer()

                                #collisions = self.rainbowMaker.collisionFinder()

                            elapsed = (time.time() - self.colidingClock2)
                            self.colidingClock2 = elapsed

                self.networkServer.terminate()

                time.sleep(2)

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

                print "We just made ", self.settings['file name']
                print "Using the alphabet ", self.settings['alphabet']
                print "With a chain length of", self.settings['chain length']
                print "And", self.settings['num rows'], "rows."
                print "It utilizes the", self.settings['algorithm'], "algorithm"
                print "With a key length of", self.settings['key length']
                print "And it took", self.clock, "seconds."

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
                print "From a File (f)  BROKE BROKE BROKE"
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
                    self.settings['hash'] = temp_hash
                    self.settings['file mode'] = False

                elif single_or_file in ("file", "f", "File"):

                    #Get the file name
                    print
                    hash_file_name = raw_input("What's the hash file name (___.txt): ")
                    while not self.does_file_exist(hash_file_name):

                        print "File not found..."
                        hash_file_name = raw_input("What's the hash file name (___.txt): ")
                    self.settings['input file name'] = hash_file_name + ".txt"

                    #Get the file name
                    print
                    results_file = raw_input("What's file name that we'll put the results (____.txt): ")
                    self.settings['output file name'] = results_file + ".txt"
                    #Hashes from a file?
                    self.settings['file mode'] = True

                self.settings['cracking method'] = "dic"
                self.settings['algorithm'] = algorithm
                self.settings['file name'] = file_name + ".txt"
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

                self.clock = time.time()

                self.networkServer.start()

                #Stuff for those pretty status pictures stuff
                star_counter = 0
                white_l = ""
                white_r = "            "

                while not self.shutdown.is_set():

                    #Clear the screen and re-draw
                    os.system('cls' if os.name == 'nt' else 'clear')
                    #Ohhh, pretty status pictures
                    print "Searching--> [" + white_l + "*" + white_r + "]"
                    print "Finished Chunks: ", self.dictionary['finished chunks'], "/", self.dictionary['total chunks']
                    print "Current Word: ", self.dictionary["current word"]
                    if star_counter > 11:
                        star_counter = 0
                        white_l = ""
                        white_r = "            "
                    else:
                        star_counter += 1
                        white_l += " "
                        white_r = white_r[:-1]

                    time.sleep(1)
                    self.update.wait()
                    self.update.clear()

                self.clock = time.time() - self.clock

                if not self.dictionary["key"] == '':

                    self.state = "singleDictionaryFoundScreen"

                else:

                    self.state = "singleDictionaryNotFoundScreen"

            #############################################
            #############################################
            #if we're at the singleDictionaryFoundScreen state (Screen)
            elif state == "singleDictionaryFoundScreen":

                self.networkServer.terminate()

                #What did the user pick? (Crack it!, Back, Exit)
                print "============="
                print "Start -> Single-User Mode -> Dictionary -> Found!"
                print

                #If we were using just one hash, not a file
                if not self.settings['file mode']:

                    print "Key is: ", self.dictionary["key"]
                    print "And that took: ", self.clock, "seconds."

                else:

                    print "We just made ", self.settings['output file name']
                    print "Which lists out the hash/key pairs we found."
                    print "And that took: ", self.clock, "seconds."

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

            #############################################
            #############################################
            #if we're at the singleDictionaryNotFoundScreen state (Screen)
            elif state == "singleDictionaryNotFoundScreen":

                self.networkServer.terminate()

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

        #temp_file = str(file_name) + ".txt"

        #Checks for file not found and returns code to caller class
        try:
            temp_file = open(file_name + ".txt", "r")
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
        punctuation = string.punctuation

        alphabet_string = ""

        for choice in choices_list:

            if choice == "a":

                alphabet_string += lower_alphabet

            elif choice == "A":

                alphabet_string += upper_alphabet

            elif choice == "p":

                alphabet_string += punctuation

            elif choice == "d":

                alphabet_string += digits

        return alphabet_string


ConsoleUI()