__author__ = 'chris Hamm'
#GUI_Demo4
#Created: 3/1/2015

#Designed to replace GUI_Demo3 (Not ready to do this yet)

#USES WINDOW OBJECTS!!!!

#USES DRAWABLE OBJECTS which are stored in the window objects. When a drawable object is added to the drawOnScreenList, it is then drawn by the drawScreen function within the window.

try:
    from Tkinter import Tk, RIGHT, TOP, LEFT, BOTTOM, BOTH, Menu, Label, Entry, OptionMenu, StringVar, IntVar
    from ttk import Frame, Button, Style, Radiobutton
    from tkMessageBox import askyesno, showwarning, showinfo  #used for message boxes
    from tkFileDialog import askopenfilename #used for creating an open file dialog
    from NetworkServer_r15a import Server
    from NetworkClient_r15a import Client
    from Source.Network.Obsolete.GUI_Demos_usingTkinter.GUI_Demo4_WindowClass import Window
    from Source.Network.Obsolete.GUI_Demos_usingTkinter.GUI_Demo4_WindowClass import drawableObject
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


class guiDemo4(Frame):
    try:
        def __init__(self,parent):
            Frame.__init__(self,parent)
            self.parent = parent
            self.outBoundDict = {} #dictionary object that holds the parameters to be sent to server/client
            self.listOfWindows= [] #holds all of the windows that have been made
            self.initGUI() #calls the function to open the main menu


        def initGUI(self):
            mainMenuWindow= Window()
            self.listOfWindows.append(mainMenuWindow)
            self.parent.title("Mighty Cracker") #this changes the title of the screen
            mainMenuLabel= drawableObject()
            mainMenuLabel.setObjectType('Label')
            mainMenuLabel.setText("Main Menu")
            mainMenuWindow.addDrawableObjectToList(mainMenuLabel)
            SingleComputerModeButton = drawableObject()
            SingleComputerModeButton.setObjectType('Button')
            SingleComputerModeButton.setText("Single Computer Mode")
            mainMenuWindow.addDrawableObjectToList(SingleComputerModeButton)
            NetworkingModeButton= drawableObject()
            NetworkingModeButton.setObjectType('Button')
            NetworkingModeButton.setText("Networking Mode")
            mainMenuWindow.addDrawableObjectToList(NetworkingModeButton)

            CloseButton= drawableObject()
            CloseButton.setObjectType('Button')
            CloseButton.setText("Close Program")
            CloseButton.setSide('BOTTOM') #not using the default TOP value, so I must specify what I want
            #CloseButtonLambdaCommand= partial(drawableObject, buttonCalls= self.onExit())
            CloseButton.setLambdaCommand(self.onExit)

            #NOTE: COMMENT OUT THE LINE BELOW TO REMOVE THE CLOSE BUTTON
            mainMenuWindow.addDrawableObjectToList(CloseButton)
            #NOTE: COMMENT OUT THE ABOVE LINE TO REMOVE THE CLOSE BUTTON
            mainMenuWindow.drawScreen() #Draws all of the drawable objects to the screen

        def onExit(self):
            for i in range(0, len(self.listOfWindows)):
                print "inside on exit loop"
                self.listOfWindows[i].destroy()
            self.parent.destroy()
            print "parent destroyed"


    except Exception as inst:
        print "============================================================================================="
        print "GUI ERROR: An exception was thrown in guiDemo4 Master try block"
        #the exception instance
        print type(inst)
        #srguments stored in .args
        print inst.args
        #_str_ allows args tto be printed directly
        print inst
        print "============================================================================================="

def main():
    root = Tk()
    root.geometry("1024x768+300+300")
    app = guiDemo4(root)
    root.mainloop()


if __name__ == '__main__':
    main()