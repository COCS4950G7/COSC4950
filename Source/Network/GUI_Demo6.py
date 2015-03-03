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
        SingleComputerModeButton.setText("Single Computer Mode")
        SingleComputerModeButton.setLambdaCommand(lambda: self.changeWindow(mainMenuWindow, self.selectCrackingMethodGUI('Single')))
        mainMenuWindow.addDrawableObjectToList(SingleComputerModeButton)
        NetworkingModeButton= drawableObject(mainMenuWindow)
        NetworkingModeButton.setObjectType('Button')
        NetworkingModeButton.setText("Networking Mode")
        NetworkingModeButton.setLambdaCommand(lambda: self.changeWindow(mainMenuWindow, self.selectNetworkModeGUI()))
        mainMenuWindow.addDrawableObjectToList(NetworkingModeButton)
        CloseButton= drawableObject(mainMenuWindow)
        CloseButton.setObjectType('Button')
        CloseButton.setText("Close Program")
        CloseButton.setSide('BOTTOM') #not using the default TOP value, so I must specify what I want
        CloseButton.setLambdaCommand(self.onExit)
        mainMenuWindow.addDrawableObjectToList(CloseButton)

        mainMenuWindow.drawScreen() #Draws all of the drawable objects to the screen

    def selectNetworkModeGUI(self):
        selectNetworkModeWindow= Window(self.parent)
        self.listOfWindows.append(selectNetworkModeWindow)
        self.parent.title("Mighty Cracker")
        selectNetworkModeLabel= drawableObject(selectNetworkModeWindow)
        selectNetworkModeLabel.setObjectType('Label')
        selectNetworkModeLabel.setText("Select Networking Mode for this Node")
        selectNetworkModeWindow.addDrawableObjectToList(selectNetworkModeLabel)
        networkServerModeButton= drawableObject(selectNetworkModeWindow)
        networkServerModeButton.setObjectType('Button')
        networkServerModeButton.setText("Network Server Mode")
        networkServerModeButton.setLambdaCommand(lambda: self.changeWindow( selectNetworkModeWindow, self.selectCrackingMethodGUI('Network')))
        selectNetworkModeWindow.addDrawableObjectToList((networkServerModeButton))
        networkClientModeButton= drawableObject(selectNetworkModeWindow)
        networkClientModeButton.setObjectType('Button')
        networkClientModeButton.setText("Network Client Mode")
        selectNetworkModeWindow.addDrawableObjectToList(networkClientModeButton)
        closeButton= drawableObject(selectNetworkModeWindow)
        closeButton.setObjectType('Button')
        closeButton.setText("Close Program")
        closeButton.setSide('BOTTOM')
        closeButton.setLambdaCommand(self.onExit)
        selectNetworkModeWindow.addDrawableObjectToList(closeButton)
        backToMainMenuButton = drawableObject(selectNetworkModeWindow)
        backToMainMenuButton.setObjectType('Button')
        backToMainMenuButton.setText("Back to Main Menu")
        backToMainMenuButton.setSide('BOTTOM')
        backToMainMenuButton.setLambdaCommand(lambda: self.changeWindow(selectNetworkModeWindow, self.initGUI()))
        selectNetworkModeWindow.addDrawableObjectToList(backToMainMenuButton)

        selectNetworkModeWindow.drawScreen()

    def selectCrackingMethodGUI(self, SorNMode):
        #SorNMode means single or network mode
        if(SorNMode is 'Single'):
            self.SorNMode= SorNMode
        elif(SorNMode is 'Network'):
            self.SorNMode= SorNMode
        else:
            raise Exception("GUI ERROR: invalid SorNMode: '"+str(SorNMode)+"'")
        selectCrackingMethodWindow= Window(self.parent)
        self.listOfWindows.append(selectCrackingMethodWindow)
        self.parent.title("Mighty Cracker")
        selectCrackingMethodLabel= drawableObject(selectCrackingMethodWindow)
        selectCrackingMethodLabel.setObjectType('Label')
        selectCrackingMethodLabel.setText("=========================Select A Cracking Method=========================")
        selectCrackingMethodWindow.addDrawableObjectToList(selectCrackingMethodLabel)
        currentModeLabel= drawableObject(selectCrackingMethodWindow)
        currentModeLabel.setObjectType('Label')
        currentModeLabel.setText("Running in "+str(self.SorNMode)+" Mode")
        selectCrackingMethodWindow.addDrawableObjectToList(currentModeLabel)
        dictionaryCrackingMethodButton= drawableObject(selectCrackingMethodWindow)
        dictionaryCrackingMethodButton.setObjectType('Button')
        dictionaryCrackingMethodButton.setText("Dictionary")
        dictionaryCrackingMethodButton.setLambdaCommand(lambda: self.changeWindow(selectCrackingMethodWindow, self.dictionaryCrackingMethodSettingsGUI(self.SorNMode)))
        selectCrackingMethodWindow.addDrawableObjectToList(dictionaryCrackingMethodButton)
        bruteForceCrackingMethodButton= drawableObject(selectCrackingMethodWindow)
        bruteForceCrackingMethodButton.setObjectType('Button')
        bruteForceCrackingMethodButton.setText("Brute-Force (Default)")
        bruteForceCrackingMethodButton.setLambdaCommand(lambda: self.changeWindow(selectCrackingMethodWindow, self.bruteForceCrackingMethodSettingsGUI(self.SorNMode)))
        selectCrackingMethodWindow.addDrawableObjectToList(bruteForceCrackingMethodButton)
        rainbowTableCrackingMethodButton= drawableObject(selectCrackingMethodWindow)
        rainbowTableCrackingMethodButton.setObjectType('Button')
        rainbowTableCrackingMethodButton.setText("Rainbow Table")
        selectCrackingMethodWindow.addDrawableObjectToList(rainbowTableCrackingMethodButton)
        closeButton= drawableObject(selectCrackingMethodWindow)
        closeButton.setObjectType('Button')
        closeButton.setText("Close Program")
        closeButton.setSide("BOTTOM")
        closeButton.setLambdaCommand(self.onExit)
        selectCrackingMethodWindow.addDrawableObjectToList(closeButton)
        backToMainMenuButton= drawableObject(selectCrackingMethodWindow)
        backToMainMenuButton.setObjectType('Button')
        backToMainMenuButton.setText("Back to Main Menu")
        backToMainMenuButton.setSide("BOTTOM")
        backToMainMenuButton.setLambdaCommand(lambda: self.changeWindow(selectCrackingMethodWindow, self.initGUI()))
        selectCrackingMethodWindow.addDrawableObjectToList(backToMainMenuButton)

        selectCrackingMethodWindow.drawScreen()

    def dictionaryCrackingMethodSettingsGUI(self, SorNMode):
        #SorNMode means single or network mode
        if(SorNMode is 'Single'):
            self.SorNMode= SorNMode
        elif(SorNMode is 'Network'):
            self.SorNMode= SorNMode
        else:
            raise Exception("GUI ERROR: invalid SorNMode: '"+str(SorNMode)+"'")
        dictionaryCrackingMethodSettingsWindow= Window(self.parent)
        self.listOfWindows.append(dictionaryCrackingMethodSettingsWindow)
        self.parent.title("Mighty Cracker")
        dictionaryCrackingMethodSettingsLabel= drawableObject(dictionaryCrackingMethodSettingsWindow)
        dictionaryCrackingMethodSettingsLabel.setObjectType('Label')
        dictionaryCrackingMethodSettingsLabel.setText("=========================Dictionary Cracking Method Settings=========================")
        dictionaryCrackingMethodSettingsWindow.addDrawableObjectToList(dictionaryCrackingMethodSettingsLabel)
        currentMode= drawableObject(dictionaryCrackingMethodSettingsWindow)
        currentMode.setObjectType('Label')
        currentMode.setText("Running in "+str(SorNMode)+" Mode")
        dictionaryCrackingMethodSettingsWindow.addDrawableObjectToList(currentMode)
        selectedDictionaryFileLabel= drawableObject(dictionaryCrackingMethodSettingsWindow)
        selectedDictionaryFileLabel.setObjectType('Label')
        selectedDictionaryFileLabel.setTextVariable("No file has been Selected")
        selectedDictionaryFileLabel.setText("Selected Dictionary File: "+str(selectedDictionaryFileLabel.getTextVariable()))
        dictionaryCrackingMethodSettingsWindow.addDrawableObjectToList(selectedDictionaryFileLabel)
        closeButton= drawableObject(dictionaryCrackingMethodSettingsWindow)
        closeButton.setObjectType('Button')
        closeButton.setText("Close Program")
        closeButton.setSide("BOTTOM")
        closeButton.setLambdaCommand(self.onExit)
        dictionaryCrackingMethodSettingsWindow.addDrawableObjectToList(closeButton)
        backToMainMenuButton= drawableObject(dictionaryCrackingMethodSettingsWindow)
        backToMainMenuButton.setObjectType('Button')
        backToMainMenuButton.setText("Back to Main Menu")
        backToMainMenuButton.setSide("BOTTOM")
        backToMainMenuButton.setLambdaCommand(lambda: self.changeWindow(dictionaryCrackingMethodSettingsWindow, self.initGUI()))
        dictionaryCrackingMethodSettingsWindow.addDrawableObjectToList(backToMainMenuButton)

        dictionaryCrackingMethodSettingsWindow.drawScreen()

    def bruteForceCrackingMethodSettingsGUI(self, SorNMode):
        #SorNMode means single or network mode
        if(SorNMode is 'Single'):
            self.SorNMode= SorNMode
        elif(SorNMode is 'Network'):
            self.SorNMode= SorNMode
        else:
            raise Exception("GUI ERROR: invalid SorNMode: '"+str(SorNMode)+"'")
        bruteForceCrackingMethodSettingsWindow= Window(self.parent)
        self.listOfWindows.append(bruteForceCrackingMethodSettingsWindow)
        self.parent.title("Mighty Cracker")
        bruteForceCrackingMethodSettingsLabel= drawableObject(bruteForceCrackingMethodSettingsWindow)
        bruteForceCrackingMethodSettingsLabel.setObjectType('Label')
        bruteForceCrackingMethodSettingsLabel.setText("=========================Brute-Force Cracking Method Settings=========================")
        bruteForceCrackingMethodSettingsWindow.addDrawableObjectToList(bruteForceCrackingMethodSettingsLabel)
        currentMode= drawableObject(bruteForceCrackingMethodSettingsWindow)
        currentMode.setObjectType('Label')
        currentMode.setText("Running in "+str(SorNMode)+" Mode")
        bruteForceCrackingMethodSettingsWindow.addDrawableObjectToList(currentMode)
        closeButton= drawableObject(bruteForceCrackingMethodSettingsWindow)
        closeButton.setObjectType('Button')
        closeButton.setText("Close Program")
        closeButton.setSide("BOTTOM")
        closeButton.setLambdaCommand(self.onExit)
        bruteForceCrackingMethodSettingsWindow.addDrawableObjectToList(closeButton)
        backToMainMenuButton= drawableObject(bruteForceCrackingMethodSettingsWindow)
        backToMainMenuButton.setObjectType('Button')
        backToMainMenuButton.setText("Back to Main Menu")
        backToMainMenuButton.setSide("BOTTOM")
        backToMainMenuButton.setLambdaCommand(lambda: self.changeWindow(bruteForceCrackingMethodSettingsWindow, self.initGUI()))
        bruteForceCrackingMethodSettingsWindow.addDrawableObjectToList(backToMainMenuButton)

        bruteForceCrackingMethodSettingsWindow.drawScreen()


    def changeWindow(self, windowToBeClosed, functionToStartNewWindow):
        windowToBeClosed.pack_forget()
        functionToStartNewWindow

    def selectFileWindow(self):
        filename= ""
        filename= askopenfilename()
        #TODO adapt this to run with dictionary cracking method settings
        #self.selectedDictionaryFileLabel.config(text=str(filename))
        #self.selectedDictionaryFile= str(self.selectedDictionaryFileLabel.cget("text"))

    def onExit(self):
        for i in range(0, len(self.listOfWindows)):
            self.listOfWindows[i].destroy()
        self.parent.destroy()
        print "parent window has been destroyed"

def main():
    root = Tk()
    root.geometry("1024x768+300+300")
    app = guiDemo6(root)
    root.mainloop()


if __name__ == '__main__':
    main()