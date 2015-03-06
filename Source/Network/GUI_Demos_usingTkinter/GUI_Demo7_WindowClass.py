__author__ = 'chris hamm'
#GUI_Demo7_WindowClass
#created: 3/3/2015

#Uses a more sophistaicated version of the drawable objects system. window still contain list of drawable objects
#drawable objects are broken into more subcategories
#shared variable groups are groups of drawable objects that share a common variable

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
    def __init__(self):
        Frame.__init__(self)
        self.drawOnScreenList= []
        self.pack(fill=BOTH, expand=1)

    def drawScreen(self):
        for i in range(0, len(self.drawOnScreenList)):
            objectType= str(self.drawOnScreenList[i].getObjectType())
            if(objectType is 'Button'):
                tempName= Button(self, text=str(self.drawOnScreenList[i].getText()), command=self.drawOnScreenList[i].getLambdaCommand())
                tempName.pack(side= self.drawOnScreenList[i].getSide(), padx= self.drawOnScreenList[i].getPadx(), pady= self.drawOnScreenList[i].getPady())
            #end of if button
            elif(objectType is 'Label'):
                tempName= Label(self, text=str(self.drawOnScreenList[i].getText()), textvariable= self.drawOnScreenList[i].getTextVariable())
                tempName.pack(side=str(self.drawOnScreenList[i].getSide()), padx=int(self.drawOnScreenList[i].getPadx()), pady=int(self.drawOnScreenList[i].getPady()))
            #end of if label
            elif(objectType is 'Entry'):
                tempName= Entry(self, bd=5)#TODO link this to the shared variable group
                tempName.pack(side=str(self.drawOnScreenList[i].getSide()), padx=int(self.drawOnScreenList[i].getPadx()), pady=int(self.drawOnScreenList[i].getPady()))
            #end of if Entry

    def setWindowTitle(self,newTitle):
            self.windowTitle= newTitle

    def getWindowTitle(self):
        return self.windowTitle

    def addDrawableObjectToList(self, inputDrawableObject):
        self.drawOnScreenList.append(inputDrawableObject)


#end of window class

class sharedVariableGroup():

    def __init__(self):
        self.listOfGroupedDrawableObjects= []
        self.localStringVar= StringVar()
        self.localStringVar.set("StringVar not set")
        self.localIntVar= IntVar()
        self.localIntVar.set(0)
        self.localTextVariable= None

    def addDrawableObjectToGroup(self, inputDrawableObject):
        self.listOfGroupedDrawableObjects.append(inputDrawableObject)

    def setLocalStringVar(self, inputString):
        self.localStringVar.set(inputString)

    def updateLocalStringVar(self, inputString):
        self.localStringVar.config(textvariable=inputString)

    def getLocalStringVar(self):
        return self.localStringVar.get()

    def setLocalIntVar(self, inputInt):
        self.localIntVar.set(inputInt)

    def getLocalIntVar(self):
        return self.localIntVar.get()

    def setLocalTextVariable(self, inputText):
        self.localTextVariable= inputText

    def getLocalTextVariable(self):
        return self.localTextVariable


#end of sharedVariableGroup

class drawableObject():

    def __init__(self):
        self.objectType= "Button" #button, label, etc
        self.side= TOP #what side to draw on, default TOP
        self.myPadx=5 #default 5
        self.myPady=5 #default 5
        self.name = "" #objects name,
        self.text= "" #default text is blank
        self.lambdaCommand= None
        self.textVariable= None

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

    def setLambdaCommand(self,inputCommand):
        self.lambdaCommand= inputCommand

    def getLambdaCommand(self):
        return self.lambdaCommand

    def setTextVariable(self,inputVariable):
        self.textVariable= inputVariable

    def getTextVariable(self):
        return self.textVariable


#end of drawable object class