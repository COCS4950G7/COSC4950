__author__ = 'chris hamm'
#GUI_DEMO6
#Created: 3/2/2105

try:
    from Tkinter import Tk, RIGHT, TOP, LEFT, BOTTOM, BOTH, Menu, Label, Entry, OptionMenu, StringVar, IntVar
    from ttk import Frame, Button, Style, Radiobutton
    from tkMessageBox import askyesno, showwarning, showinfo  #used for message boxes
    from tkFileDialog import askopenfilename #used for creating an open file dialog
    from NetworkServer_r15a import Server
    from NetworkClient_r15a import Client
    from GUI_Demo6_WindowClass import Window
    from GUI_Demo6_WindowClass import drawableObject
    from multiprocessing import Process
    from functools import partial
except Exception as inst:
    print "============================================================================================="
    print "GUI ERROR: An exception was thrown in importing libraries try block"
    #the exception instance
    print type(inst)
    #srguments stored in .args
    print inst.args
    #_str_ allows args tto be printed directly
    print inst
    print "============================================================================================="


class guiDemo6(Frame):
    def __init__(self,parent):
        Frame.__init__(self,parent)
        self.parent = parent #parent is called root in the main function
        self.outBoundDict = {} #dictionary object that holds the parameters to be sent to server/client
        self.listOfWindows= [] #holds all of the windows that have been made
        self.initGUI() #calls the function to open the main menu

    def initGUI(self):
        mainMenuWindow= Window(self.parent)
        self.listOfWindows.append(mainMenuWindow)
        self.parent.title("Mighty Cracker") #this changes the title of the screen
        mainMenuLabel= drawableObject(mainMenuWindow)
        mainMenuLabel.setObjectType('Label')
        mainMenuLabel.setText("Main Menu")
        mainMenuWindow.addDrawableObjectToList(mainMenuLabel)
        SingleComputerModeButton = drawableObject(mainMenuWindow)
        SingleComputerModeButton.setObjectType('Button')
        SingleComputerModeButton.setName("SingleComputerModeButton")
        SingleComputerModeButton.setCommand(0)
        mainMenuWindow.addCommandToDict(SingleComputerModeButton, self.onExit)
        SingleComputerModeButton.setText("Single Computer Mode")
        mainMenuWindow.addDrawableObjectToList(SingleComputerModeButton)
        NetworkingModeButton= drawableObject(mainMenuWindow)
        NetworkingModeButton.setObjectType('Button')
        NetworkingModeButton.setText("Networking Mode")
        mainMenuWindow.addDrawableObjectToList(NetworkingModeButton)

        mainMenuWindow.drawScreen() #Draws all of the drawable objects to the screen

    def onExit(self):
        for i in range(0, len(self.listOfWindows)):
            print "inside on exit loop"
            self.listOfWindows[i].destroy()
        self.parent.destroy()
        print "parent destroyed"

def main():
    root = Tk()
    root.geometry("1024x768+300+300")
    app = guiDemo6(root)
    root.mainloop()


if __name__ == '__main__':
    main()