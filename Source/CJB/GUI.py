#   GUI.py

#   This is the class that controls and displays
#   the GUI, taking information from the Controller
#   and giving info back

#   Chris Bugg
#   10/7/14

#   Updated - 10/11/14 (CJB)
#               -> Added Tkinter example and stand-alone ability (if uncommented)

#Inputs
#import Tkinter

#GUI class
class GUI():

    #Class Variables
    state = ""
    done = False
    currentInput = ""

    #Contructor
    def __init__(self):
        done = True

        """""
        #Uncomment for Tkinter GUI example

        myContainer1 = Tkinter.Frame()
        myContainer1.pack()

        button1 = Tkinter.Button(myContainer1)
        button1["text"]="Hello, World!"
        button1["background"] = "green"
        button1.pack()

        myContainer1.mainloop()
        """""




    #Returns what the user picked as a string for controller class
    def getInput(self):

        return self.currentInput

    #Returns current screen state (where we are in the program) as a string
    def getState(self):

        return self.state

    #Sets the screen state to go to
    def setState(self, futureState):

        self.state = futureState

#Uncomment for Stand-alone running
#GUI()