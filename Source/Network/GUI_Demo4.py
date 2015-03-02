__author__ = 'chris Hamm'
#GUI_Demo4
#Created: 2/28/2015

#Designed to replace GUI_Demo3

#USES WINDOW OBJECTS!!!!

try:
    from Tkinter import Tk, RIGHT, TOP, LEFT, BOTTOM, BOTH, Menu, Label, Entry, OptionMenu, StringVar, IntVar
    from ttk import Frame, Button, Style, Radiobutton
    from tkMessageBox import askyesno, showwarning, showinfo  #used for message boxes
    from tkFileDialog import askopenfilename #used for creating an open file dialog
    from NetworkServer_r15a import Server
    from NetworkClient_r15a import Client
    from GUI_Demo4_WindowClass import Window
    from GUI_Demo4_WindowClass import drawableObject
    from multiprocessing import Process
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
            self.listOfWindows= []
            self.initGUI()


        def initGUI(self):
            mainMenuWindow= Window()
            self.listOfWindows.append(mainMenuWindow)
            self.parent.title("Mighty Cracker")
            #Window.setWindowTitle("Mighty Cracker")
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
            CloseButton.setSide('BOTTOM')
            CloseButton.setCommand(self.onExit())
            #NOTE: COMMENT OUT THE LINE BELOW TO REMOVE THE CLOSE BUTTON
            mainMenuWindow.addDrawableObjectToList(CloseButton)
            #NOTE: COMMENT OUT THE ABOVE LINE TO REMOVE THE CLOSE BUTTON
            mainMenuWindow.drawScreen()

        def onExit(self):
            for i in range(0, len(self.listOfWindows)):
                self.listOfWindows[i].destroy()
            self.parent.destroy()


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