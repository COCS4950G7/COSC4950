__author__ = 'ChrisBugg'
#   GUI.py

#   This is the class that controls and displays
#   the GUI, taking information from the Controller
#   and giving info back

#   Chris Bugg
#   10/7/14


#Inputs

#GUI class
class GUI():

    #Class Variables
    state = ""
    done = False
    currentInput = ""

    #Contructor
    def __init__(self):

        done = True

    #Returns what the user picked as a string for controller class
    def getInput(self):

        return self.currentInput

    #Returns current screen state (where we are in the program) as a string
    def getState(self):

        return self.state

    #Sets the screen state to go to
    def setState(self, futureState):

        self.state = futureState

