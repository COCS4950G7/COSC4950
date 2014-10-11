__author__ = 'ChrisBugg'
#   Controller.py

#   This is the main class that 'controls'
#   the other classes by acting as a go-between
#   with the GUI and the actual worker classes

#   Chris Bugg
#   10/7/14

#Imports
import GUI


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

            #if we're at the becomeNode state (Screen)
            elif state == "nodeConnectingScreen":

                #What did the user pick? (Be a Node, Back, Exit)
                userInput = GUI.getInput()

                #wait for server connection
                #then switch to nodeConnectedToScreen

                if userInput == "back":

                    GUI.setState("start")

                else:

                    #We're done
                    self.Done = True

            #if we're at the Server start state (Screen)
            elif state == "serverStart":

                #What did the user pick? (Brute-Force, Rainbow, Back, Exit)
                userInput = GUI.getInput()

                if userInput == "bruteForce":

                    GUI.setState("serverBruteForce")

                    #get info from GUI and pass to Brute_Force class

                elif userInput == "rainbowCreate":

                    GUI.setState("serverRainbowCreate")

                    #get info from GUI and pass to Rainbow Maker class

                elif userInput == "rainbowUse":

                    GUI.setState("serverRainbowUse")

                    #get info from GUI and pass to Rainbow User class

                elif userInput == "dictionary":

                    GUI.setState("serverDictionary")

                    #get info from GUI and pass to Dictionary class

                elif userInput == "back":

                    GUI.setState("start")

                else:

                    #We're done
                    self.Done = True

            #if we're at the serverBruteForce state (Screen)
            elif state == "serverBruteForce":

                #What did the user pick? (Crack it!, Back, Exit)
                userInput = GUI.getInput()

                if userInput == "crackIt":

                    GUI.setState("serverBruteSearching")

                    #get info from GUI and pass to Brute_Force class

                elif userInput == "back":

                    GUI.setState("serverStart")

                else:

                    #We're done
                    self.Done = True

            #if we're at the Single-User start state (Screen)
            elif state == "singleStart":

                #What did the user pick? (Brute-Force, Rainbow, Dictionary, Back, Exit)
                userInput = GUI.getInput()

                if userInput == "bruteForce":

                    GUI.setState("singleBruteForce")

                    #get info from GUI and pass to Brute_Force class

                elif userInput == "rainbowCreate":

                    GUI.setState("singleRainbowCreate")

                    #get info from GUI and pass to Rainbow Maker class

                elif userInput == "rainbowUse":

                    GUI.setState("singleRainbowUse")

                    #get info from GUI and pass to Rainbow User class

                elif userInput == "dictionary":

                    GUI.setState("singleDictionary")

                    #get info from GUI and pass to Dictionary class

                elif userInput == "back":

                    GUI.setState("start")

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
serverRainScreen
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