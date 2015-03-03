__author__ = 'chris hamm'
#GUI_DEMO6_WINDOWCLASS
#created: 3/2/2015

#SAME ******* ERROR, keyerror '' on return self.parentWindow.get


try:
    from Tkinter import Tk, RIGHT, TOP, LEFT, BOTTOM, BOTH, Menu, Label, Entry, OptionMenu, StringVar, IntVar
    from ttk import Frame, Button, Style, Radiobutton
    from tkMessageBox import askyesno, showwarning, showinfo  #used for message boxes
    from tkFileDialog import askopenfilename #used for creating an open file dialog
   # from functools import partial

except Exception as inst:
    print "============================================================================================="
    print "GUI ERROR (WINDOW CLASS): An exception was thrown in importing libraries try block"
    #the exception instance
    print type(inst)
    #srguments stored in .args
    print inst.args
    #_str_ allows args to be printed directly
    print inst
    print "============================================================================================="


class Window(Frame):
    try:
        #Class variables
        def __init__(self, superParent):
            Frame.__init__(self , superParent) #superParent is the parent of guidemo6, aka root
            self.superParent= superParent
            self.drawOnScreenList= [] #list that contains what needs to be draw to the screen, and in what order based on what is first in the list
            self.dictOfCommands= {} #dictionary of commands
            self.pack(fill=BOTH, expand=1)

        def drawScreen(self): #function draws objects to the screen

            for index in range(0, len(self.drawOnScreenList)):
                #get object type
                objectType = str(self.drawOnScreenList[index].getObjectType())
                if(objectType is 'Button'):
                    #if both command and lambda command are None
                    if((self.drawOnScreenList[index].getCommand() is None) and (self.drawOnScreenList[index].getLambdaCommand() is None)):
                        tempName= Button(self, text=str(self.drawOnScreenList[index].getText()) )
                    #elif lambda command is not none but command is none
                    elif((self.drawOnScreenList[index].getCommand() is None) and (self.drawOnScreenList[index].getLambdaCommand() is not None)):
                        tempName= Button(self, text=str(self.drawOnScreenList[index].getText()), command=self.drawOnScreenList[index].getLambdaCommand())
                    #elif command is not None and lambda is none
                    elif((self.drawOnScreenList[index].getCommand() is not None) and (self.drawOnScreenList[index].getLambdaCommand() is None)):
                        tempName= Button(self, text=str(self.drawOnScreenList[index].getText()), command=self.drawOnScreenList[index].getCommand( ))
                    else:
                        raise Exception("drawScreen error: command and lambda command are both not None!")
                    tempName.pack(side=str(self.drawOnScreenList[index].getSide()), padx=int(self.drawOnScreenList[index].getPadx()), pady=int(self.drawOnScreenList[index].getPady()))
                #end of if button
                elif(objectType is 'Label'):
                    tempName= Label(self, text=str(self.drawOnScreenList[index].getText()))
                    tempName.pack(side=str(self.drawOnScreenList[index].getSide()), padx=int(self.drawOnScreenList[index].getPadx()), pady=int(self.drawOnScreenList[index].getPady()))
                #end of if label
                elif(objectType is 'Entry'):
                    tempName= Entry(self, bd=5, textvariable= self.drawOnScreenList[index].getTextVariable())
                    tempName.pack(side=str(self.drawOnScreenList[index].getSide()), padx=int(self.drawOnScreenList[index].getPadx()), pady=int(self.drawOnScreenList[index].getPady()))
                #end of if Entry
                elif(objectType is 'RadioButton'):
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

        def addCommandToDict(self, inputDrawableObject, inputCommand):
            self.dictOfCommands[inputDrawableObject.getName()]= inputCommand

        def getCommandFromDict(self, inputDrawableObjectName):
            return self.dictOfCommands[inputDrawableObjectName]

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
        def __init__(self, parentWindow):
            self.parentWindow= parentWindow
            self.objectType= "Button" #button, label, etc
            self.side= TOP #what side to draw on, default TOP
            self.myPadx=5 #default 5
            self.myPady=5 #default 5
            self.name = "" #objects name, used for dictOfCommands key
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
