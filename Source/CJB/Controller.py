#   Controller.py

#   This is the main class that 'controls'
#   the other classes by acting as a go-between
#   with the GUI and the actual worker classes

#   Chris Bugg
#   10/7/14

#   Update - 10/11/14 (CJB)
#               -> Main layout is complete, just needs more actual methods
#               ->  from supporting classes.

#   NOTE: Diagrams of the layout (approximate names) are at bottom of file

#Imports
import GUI
import Brute_Force
import Dictionary
import RainbowMaker
import RainbowUser


#Controller class
class Controller():

    #Class variables
    done = False

    #Constructor
    def __init__(self):

        #Startup GUI as new process
        GUI.GUI()

        #Loop till we're done
        while not self.done:

            #Do stuff with GUI, get state,
            # process, and tell GUI when to
            # move to new screen/state

            #Get current screen from GUI
            state = GUI.getState()

            #Lots of if statements

            #if we're at the start state
            if state == "startScreen":

                #What did the user pick? (Node, Server, Single, Exit)
                userInput = GUI.getInput()

                #If user picks Node, tell GUI to go to Node start screen
                if userInput == "Node":

                    GUI.setState("nodeStartScreen")

                elif userInput == "Server":

                    GUI.setState("serverStartScreen")

                elif userInput == "Single":

                    GUI.setState("singleStartScreen")

                else:

                    #We're done
                    self.Done = True

            ################### NODE ################### vvv

            #if we're at the node start state (Screen)
            elif state == "nodeStartScreen":

                #What did the user pick? (Be a node, Back, Exit)
                userInput = GUI.getInput()

                if userInput == "beNode":

                    GUI.setState("nodeConnectingScreen")

                elif userInput == "back":

                    GUI.setState("startScreen")

                else:

                    #We're done
                    self.Done = True

            #if we're at the node connecting... state (Screen)
            elif state == "nodeConnectingScreen":

                #What did the user pick? (Be a Node, Back, Exit)
                userInput = GUI.getInput()

                #wait for server connection
                #then switch to nodeConnectedToScreen

                if userInput == "back":

                    GUI.setState("startScreen")

                else:

                    #We're done
                    self.Done = True

            #if we're at the node connected state (Screen)
            elif state == "nodeConnectedToScreen":

                #What did the user pick? (Be a Node, Back, Exit)
                userInput = GUI.getInput()

                #wait for job or disconnect
                #then switch to nodeDoingStuffScreen or nodeConnectingScreen depending

                if userInput == "back":

                    GUI.setState("startScreen")

                else:

                    #We're done
                    self.Done = True

            #if we're at the node doing stuff state (Screen)
            elif state == "nodeDoingStuffScreen":

                #What did the user pick? (Be a Node, Back, Exit)
                userInput = GUI.getInput()

                #wait to get done with our stuff
                #then switch to nodeConnectedToScreen or nodeConnectingScreen depending

                if userInput == "back":

                    GUI.setState("startScreen")

                else:

                    #We're done
                    self.Done = True

            ################### SERVER ################### vvv

            #if we're at the Server start state (Screen)
            elif state == "serverStartScreen":

                #What did the user pick? (Brute-Force, Rainbow, Back, Exit)
                userInput = GUI.getInput()

                if userInput == "bruteForce":

                    GUI.setState("serverBruteForceScreen")

                    #get info from GUI and pass to Brute_Force class

                elif userInput == "rainbowMake":

                    GUI.setState("serverRainMakerScreen")

                    #get info from GUI and pass to Rainbow Maker class

                elif userInput == "rainbowUser":

                    GUI.setState("serverRainUserScreen")

                    #get info from GUI and pass to Rainbow User class

                elif userInput == "dictionary":

                    GUI.setState("serverDictionaryScreen")

                    #get info from GUI and pass to Dictionary class

                elif userInput == "back":

                    GUI.setState("startScreen")

                else:

                    #We're done
                    self.Done = True

            #if we're at the serverBruteForceScreen state (Screen)
            elif state == "serverBruteForceScreen":

                #What did the user pick? (Crack it!, Back, Exit)
                userInput = GUI.getInput()

                if userInput == "crackIt":

                    GUI.setState("serverBruteSearchingScreen")

                    #get info from GUI and pass to Brute_Force class

                elif userInput == "back":

                    GUI.setState("serverForceScreen")

                else:

                    #We're done
                    self.Done = True

            #if we're at the serverBruteSearchingScreen state (Screen)
            elif state == "serverBruteSearchingScreen":

                #display results and wait for user interaction

                #What did the user pick? (Crack it!, Back, Exit)
                userInput = GUI.getInput()

                if userInput == "back":

                    GUI.setState("serverBruteForceScreen")

                else:

                    #We're done
                    self.Done = True

            #if we're at the serverBruteFoundScreen state (Screen)
            elif state == "serverBruteFoundScreen":

                #display results and wait for user interaction

                #What did the user pick? (Crack it!, Back, Exit)
                userInput = GUI.getInput()

                if userInput == "back":

                    GUI.setState("serverBruteForceScreen")

                else:

                    #We're done
                    self.Done = True

            #if we're at the serverBruteNotFoundScreen state (Screen)
            elif state == "serverBruteNotFoundScreen":

                #display results and wait for user interaction

                #What did the user pick? (Crack it!, Back, Exit)
                userInput = GUI.getInput()

                if userInput == "back":

                    GUI.setState("serverBruteForceScreen")

                else:

                    #We're done
                    self.Done = True

            #if we're at the serverRainUserScreen state (Screen)
            elif state == "serverRainUserScreen":

                #What did the user pick? (Crack it!, Back, Exit)
                userInput = GUI.getInput()

                if userInput == "crackIt":

                    GUI.setState("serverRainUserSearchingScreen")

                    #get info from GUI and pass to Brute_Force class

                elif userInput == "back":

                    GUI.setState("serverStartScreen")

                else:

                    #We're done
                    self.Done = True

            #if we're at the serverRainUserSearchingScreen state (Screen)
            elif state == "serverRainUserSearchingScreen":

                #display results and wait for user interaction

                #What did the user pick? (Crack it!, Back, Exit)
                userInput = GUI.getInput()

                if userInput == "back":

                    GUI.setState("serverRainUserScreen")

                else:

                    #We're done
                    self.Done = True

            #if we're at the serverRainUserFoundScreen state (Screen)
            elif state == "serverRainUserFoundScreen":

                #display results and wait for user interaction

                #What did the user pick? (Crack it!, Back, Exit)
                userInput = GUI.getInput()

                if userInput == "back":

                    GUI.setState("serverRainUserScreen")

                else:

                    #We're done
                    self.Done = True

            #if we're at the serverRainUserNotFoundScreen state (Screen)
            elif state == "serverRainUserNotFoundScreen":

                #display results and wait for user interaction

                #What did the user pick? (Crack it!, Back, Exit)
                userInput = GUI.getInput()

                if userInput == "back":

                    GUI.setState("serverRainUserScreen")

                else:

                    #We're done
                    self.Done = True

            #if we're at the serverRainMakerScreen state (Screen)
            elif state == "serverRainMakerScreen":

                #What did the user pick? (Crack it!, Back, Exit)
                userInput = GUI.getInput()

                if userInput == "makeIt":

                    GUI.setState("serverRainMakerDoingScreen")

                    #get info from GUI and pass to Brute_Force class

                elif userInput == "back":

                    GUI.setState("serverStartScreen")

                else:

                    #We're done
                    self.Done = True

            #if we're at the serverRainMakerSearchingScreen state (Screen)
            elif state == "serverRainMakerSearchingScreen":

                #display results and wait for user interaction

                #What did the user pick? (Crack it!, Back, Exit)
                userInput = GUI.getInput()

                if userInput == "back":

                    GUI.setState("serverRainMakerScreen")

                else:

                    #We're done
                    self.Done = True

            #if we're at the serverRainMakerDoneScreen state (Screen)
            elif state == "serverRainMakerDoneScreen":

                #display results and wait for user interaction

                #What did the user pick? (Crack it!, Back, Exit)
                userInput = GUI.getInput()

                if userInput == "back":

                    GUI.setState("serverRainMakerScreen")

                else:

                    #We're done
                    self.Done = True

            #if we're at the serverDictionaryScreen state (Screen)
            elif state == "serverDictionaryScreen":

                #What did the user pick? (Crack it!, Back, Exit)
                userInput = GUI.getInput()

                if userInput == "crackIt":

                    GUI.setState("serverDictionarySearchingScreen")

                    #get info from GUI and pass to Brute_Force class

                elif userInput == "back":

                    GUI.setState("serverStartScreen")

                else:

                    #We're done
                    self.Done = True

            #if we're at the serverDictionarySearchingScreen state (Screen)
            elif state == "serverDictionarySearchingScreen":

                #display results and wait for user interaction

                #What did the user pick? (Crack it!, Back, Exit)
                userInput = GUI.getInput()

                if userInput == "back":

                    GUI.setState("serverDictionaryScreen")

                else:

                    #We're done
                    self.Done = True

            #if we're at the serverDictionaryFoundScreen state (Screen)
            elif state == "serverDictionaryFoundScreen":

                #display results and wait for user interaction

                #What did the user pick? (Crack it!, Back, Exit)
                userInput = GUI.getInput()

                if userInput == "back":

                    GUI.setState("serverDictionaryScreen")

                else:

                    #We're done
                    self.Done = True

            #if we're at the serverDictionaryNotFoundScreen state (Screen)
            elif state == "serverDictionaryNotFoundScreen":

                #display results and wait for user interaction

                #What did the user pick? (Crack it!, Back, Exit)
                userInput = GUI.getInput()

                if userInput == "back":

                    GUI.setState("serverDictionaryScreen")

                else:

                    #We're done
                    self.Done = True

            ################### SINGLE-USER ################### vvv

            #if we're at the Single-User start state (Screen)
            elif state == "singleStart":

                #What did the user pick? (Brute-Force, Rainbow, Dictionary, Back, Exit)
                userInput = GUI.getInput()

                if userInput == "bruteForce":

                    GUI.setState("singleBruteForceScreen")

                    #get info from GUI and pass to Brute_Force class

                elif userInput == "rainbowMake":

                    GUI.setState("singleRainMakerScreen")

                    #get info from GUI and pass to Rainbow Maker class

                elif userInput == "rainbowUse":

                    GUI.setState("singleRainUserScreen")

                    #get info from GUI and pass to Rainbow User class

                elif userInput == "dictionary":

                    GUI.setState("singleDictionaryScreen")

                    #get info from GUI and pass to Dictionary class

                elif userInput == "back":

                    GUI.setState("startScreen")

                else:

                    #We're done
                    self.Done = True

            #if we're at the  singleBruteForceScreen state (Screen)
            elif state == "singleBruteForceScreen":

                #What did the user pick? (Crack it!, Back, Exit)
                userInput = GUI.getInput()

                if userInput == "crackIt":

                    GUI.setState("singleBruteSearchingScreen")

                    #get info from GUI and pass to Brute_Force class

                elif userInput == "back":

                    GUI.setState("singleForceScreen")

                else:

                    #We're done
                    self.Done = True

            #if we're at the singleBruteSearchingScreen state (Screen)
            elif state == "singleBruteSearchingScreen":

                #display results and wait for user interaction

                #What did the user pick? (Crack it!, Back, Exit)
                userInput = GUI.getInput()

                if userInput == "back":

                    GUI.setState("singleBruteForceScreen")

                else:

                    #We're done
                    self.Done = True

            #if we're at the singleBruteFoundScreen state (Screen)
            elif state == "singleBruteFoundScreen":

                #display results and wait for user interaction

                #What did the user pick? (Crack it!, Back, Exit)
                userInput = GUI.getInput()

                if userInput == "back":

                    GUI.setState("singleBruteForceScreen")

                else:

                    #We're done
                    self.Done = True

            #if we're at the singleBruteNotFoundScreen state (Screen)
            elif state == "singleBruteNotFoundScreen":

                #display results and wait for user interaction

                #What did the user pick? (Crack it!, Back, Exit)
                userInput = GUI.getInput()

                if userInput == "back":

                    GUI.setState("singleBruteForceScreen")

                else:

                    #We're done
                    self.Done = True

            #if we're at the singleRainUserScreen state (Screen)
            elif state == "singleRainUserScreen":

                #What did the user pick? (Crack it!, Back, Exit)
                userInput = GUI.getInput()

                if userInput == "crackIt":

                    GUI.setState("singleRainUserSearchingScreen")

                    #get info from GUI and pass to Brute_Force class

                elif userInput == "back":

                    GUI.setState("singleStartScreen")

                else:

                    #We're done
                    self.Done = True

            #if we're at the singleRainUserSearchingScreen state (Screen)
            elif state == "singleRainUserSearchingScreen":

                #display results and wait for user interaction

                #What did the user pick? (Crack it!, Back, Exit)
                userInput = GUI.getInput()

                if userInput == "back":

                    GUI.setState("singleRainUserScreen")

                else:

                    #We're done
                    self.Done = True

            #if we're at the singleRainUserFoundScreen state (Screen)
            elif state == "singleRainUserFoundScreen":

                #display results and wait for user interaction

                #What did the user pick? (Crack it!, Back, Exit)
                userInput = GUI.getInput()

                if userInput == "back":

                    GUI.setState("singleRainUserScreen")

                else:

                    #We're done
                    self.Done = True

            #if we're at the singleRainUserNotFoundScreen state (Screen)
            elif state == "singleRainUserNotFoundScreen":

                #display results and wait for user interaction

                #What did the user pick? (Crack it!, Back, Exit)
                userInput = GUI.getInput()

                if userInput == "back":

                    GUI.setState("singleRainUserScreen")

                else:

                    #We're done
                    self.Done = True

            #if we're at the singleRainMakerScreen state (Screen)
            elif state == "singleRainMakerScreen":

                #What did the user pick? (Crack it!, Back, Exit)
                userInput = GUI.getInput()

                if userInput == "makeIt":

                    GUI.setState("singleRainMakerDoingScreen")

                    #get info from GUI and pass to Brute_Force class

                elif userInput == "back":

                    GUI.setState("singleStartScreen")

                else:

                    #We're done
                    self.Done = True

            #if we're at the singleRainMakerSearchingScreen state (Screen)
            elif state == "singleRainMakerSearchingScreen":

                #display results and wait for user interaction

                #What did the user pick? (Crack it!, Back, Exit)
                userInput = GUI.getInput()

                if userInput == "back":

                    GUI.setState("singleRainMakerScreen")

                else:

                    #We're done
                    self.Done = True

            #if we're at the singleRainMakerDoneScreen state (Screen)
            elif state == "singleRainMakerDoneScreen":

                #display results and wait for user interaction

                #What did the user pick? (Crack it!, Back, Exit)
                userInput = GUI.getInput()

                if userInput == "back":

                    GUI.setState("singlerRainMakerScreen")

                else:

                    #We're done
                    self.Done = True

            #if we're at the singleDictionaryScreen state (Screen)
            elif state == "singleDictionaryScreen":

                #What did the user pick? (Crack it!, Back, Exit)
                userInput = GUI.getInput()

                if userInput == "crackIt":

                    GUI.setState("singleDictionarySearchingScreen")

                    #get info from GUI and pass to Brute_Force class

                elif userInput == "back":

                    GUI.setState("singleStartScreen")

                else:

                    #We're done
                    self.Done = True

            #if we're at the singleDictionarySearchingScreen state (Screen)
            elif state == "singleDictionarySearchingScreen":

                #display results and wait for user interaction

                #What did the user pick? (Crack it!, Back, Exit)
                userInput = GUI.getInput()

                if userInput == "back":

                    GUI.setState("singleDictionaryScreen")

                else:

                    #We're done
                    self.Done = True

            #if we're at the singleDictionaryFoundScreen state (Screen)
            elif state == "singleDictionaryFoundScreen":

                #display results and wait for user interaction

                #What did the user pick? (Crack it!, Back, Exit)
                userInput = GUI.getInput()

                if userInput == "back":

                    GUI.setState("singleDictionaryScreen")

                else:

                    #We're done
                    self.Done = True

            #if we're at the singleDictionaryNotFoundScreen state (Screen)
            elif state == "singleDictionaryNotFoundScreen":

                #display results and wait for user interaction

                #What did the user pick? (Crack it!, Back, Exit)
                userInput = GUI.getInput()

                if userInput == "back":

                    GUI.setState("singleDictionaryScreen")

                else:

                    #We're done
                    self.Done = True


''''
Two versions of a diagram grouped differently--CJB

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