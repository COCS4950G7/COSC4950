__author__ = 'Chris Hamm'
#GUI_Demo5
#CReated: 3/2/2015

#TEST VERSION


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


class Window(Frame):
    try:
        #Class variables
        def __init__(self):
            Frame.__init__(self )
            self.drawOnScreenList= [] #list that contains what needs to be draw to the screen, and in what order based on what is first in the list
            self.pack(fill=BOTH, expand=1)


        def drawScreen(self): #function draws objects to the screen

            for index in range(0, len(self.drawOnScreenList)):
                #get object type
                objectType = str(self.drawOnScreenList[index].getObjectType())
                if(objectType is 'Button'):
                    tempName= str(self.drawOnScreenList[index].getName())
                    #if both command and lambda command are None
                    if((self.drawOnScreenList[index].getCommand() is None) and (self.drawOnScreenList[index].getLambdaCommand() is None)):
                        tempName= Button(self, text=str(self.drawOnScreenList[index].getText()) )
                    #elif lambda command is not none but command is none
                    elif((self.drawOnScreenList[index].getCommand() is None) and (self.drawOnScreenList[index].getLambdaCommand() is not None)):
                        tempName= Button(self, text=str(self.drawOnScreenList[index].getText()), command=lambda: self.drawOnScreenList[index].getLambdaCommand())
                    #elif command is not None and lambda is none
                    elif((self.drawOnScreenList[index].getCommand() is not None) and (self.drawOnScreenList[index].getLambdaCommand() is None)):
                        tempName= Button(self, text=str(self.drawOnScreenList[index].getText()), command=self.drawOnScreenList[index].getLambdaCommand())
                    else:
                        raise Exception("drawScreen error: command and lambda command are both not None!")
                    tempName.pack(side=str(self.drawOnScreenList[index].getSide()), padx=int(self.drawOnScreenList[index].getPadx()), pady=int(self.drawOnScreenList[index].getPady()))
                #end of if button
                elif(objectType is 'Label'):
 #                   tempName= str(self.drawOnScreenList[index].getName())
                    tempName= Label(self, text=str(self.drawOnScreenList[index].getText()))
                    tempName.pack(side=str(self.drawOnScreenList[index].getSide()), padx=int(self.drawOnScreenList[index].getPadx()), pady=int(self.drawOnScreenList[index].getPady()))
                #end of if label
                elif(objectType is 'Entry'):
                    tempName= str(self.drawOnScreenList[index].getName())
                    tempName= Entry(self, bd=5, textvariable= self.drawOnScreenList[index].getTextVariable())
                    tempName.pack(side=str(self.drawOnScreenList[index].getSide()), padx=int(self.drawOnScreenList[index].getPadx()), pady=int(self.drawOnScreenList[index].getPady()))
                #end of if Entry
                elif(objectType is 'RadioButton'):
                    tempName= str(self.drawOnScreenList[index].getName())
                    tempName= Radiobutton(self, text=str(self.drawOnScreenList[index].getText()), variable=self.drawOnScreenList[index].getVariable(), value=self.drawOnScreenList[index].getValue() )
                    tempName.pack(side=str(self.drawOnScreenList[index].getSide()), padx=int(self.drawOnScreenList[index].getPadx()), pady=int(self.drawOnScreenList[index].getPady()))
                #end of if Radiobutton
                else:
                    raise Exception("drawOnScreen ERROR: unrecognized objectType: '"+str(objectType)+"'")

        def removeAllFromScreen(self): #unpacks all objects from the screen
            for index in range(0, len(self.drawOnScreenList)):
                self.drawOnScreenList[index].pack_forget()

        def setWindowTitle(self,newTitle):
            self.windowTitle= newTitle

        def getWindowTitle(self):
            return self.windowTitle

        def addDrawableObjectToList(self, inputDrawableObject):
            self.drawOnScreenList.append(inputDrawableObject)

    except Exception as inst:
        print "============================================================================================="
        print "GUI ERROR (WINDOW CLASS): An exception was thrown in Windows Class Master try block"
        #the exception instance
        print type(inst)
        #srguments stored in .args
        print inst.args
        #_str_ allows args tto be printed directly
        print inst
        print "============================================================================================="
#end of windows class


class drawableObject():
    try:
        def __init__(self):
            self.objectType= "Button" #button, label, etc
            self.side= TOP #what side to draw on, default TOP
            self.myPadx=5 #default 5
            self.myPady=5 #default 5
            self.name = "" #objects name
            self.text= "" #default text is blank
            self.command= None #command for when pressed
            self.lambdaCommand= None
            self.variable= None
            self.textVariable= ""
            self.value= ""

        def setObjectType(self,inputType):
            if(inputType is 'Button'):
                self.objectType= "Button"
            elif(inputType is 'Label'):
                self.objectType= "Label"
            elif(inputType is 'Entry'):
                self.objectType= "Entry"
            elif(inputType is 'RadioButton'):
                self.objectType= "RadioButton"
            else:
                raise Exception("ERROR: unknown object type: '"+str(inputType)+"'")

        def getObjectType(self):
            return self.objectType

        def setSide(self,inputSide):
            if(inputSide is 'TOP'):
                self.side= TOP
            elif(inputSide is 'RIGHT'):
                self.side= RIGHT
            elif(inputSide is "LEFT"):
                self.side= LEFT
            elif(inputSide is "BOTTOM"):
                self.side= BOTTOM
            else:
                raise Exception("ERROR: unknown onbject side: '"+str(inputSide)+"'")

        def getSide(self):
            return self.side

        def setPadx(self,input):
            self.myPadx= input

        def getPadx(self):
            return self.myPadx

        def setPady(self,input):
            self.myPady= input

        def getPady(self):
            return self.myPady

        def setName(self,inputName):
            self.name= inputName

        def getName(self):
            return self.name

        def setText(self,inputText):
            self.text= inputText

        def getText(self):
            return self.text

        def setCommand(self,inputCommand):
            self.command= inputCommand

        def getCommand(self):
            return self.command

        def setLambdaCommand(self,inputCommand):
            self.lambdaCommand= inputCommand

        def getLambdaCommand(self):
            return self.lambdaCommand

        def setVariable(self,inputVariable):
            self.variable= inputVariable

        def getVariable(self):
            return self.variable

        def setTextVariable(self,inputVar):
            self.textVariable= inputVar

        def getTextVariable(self):
            return self.textVariable

        def setValue(self,inputValue):
            self.value= inputValue

        def getValue(self):
            return self.value



    except Exception as inst:
        print "============================================================================================="
        print "GUI ERROR (drawable object class): An exception was thrown in drawableObject Class Master try block"
        #the exception instance
        print type(inst)
        #srguments stored in .args
        print inst.args
        #_str_ allows args tto be printed directly
        print inst
        print "============================================================================================="