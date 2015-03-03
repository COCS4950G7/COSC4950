__author__ = 'Chris Hamm'
#GUI_Demo3
#TODO thought, have a event trigger a wake up in GUI, to indicate that something changed in the status (maybe)
#TODO condense the unpack methods into one function that adapts based on which screen you where using
    #TODO an unpacking manager
#TODO have global master set of predefined buttons and labals
#reference www.pyton-course.eu/tkinter_entry_widgets.php for more sophisticated gui layouts

try: #importing libraries try block
    from Tkinter import Tk, RIGHT, TOP, LEFT, BOTTOM, BOTH, Menu, Label, Entry, OptionMenu, StringVar, IntVar
    from ttk import Frame, Button, Style, Radiobutton
    from tkMessageBox import askyesno, showwarning, showinfo  #used for message boxes
    from tkFileDialog import askopenfilename #used for creating an open file dialog
    from NetworkServer_r15a import Server
    from NetworkClient_r15a import Client
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

class guiDemo3(Frame):

    def __init__(self,parent):
        Frame.__init__(self,parent)
        self.parent = parent
        self.dict = {} #temporary
        self.initUI() #start up the main menu

    def initUI(self):
        try:
            self.parent.title("Mighty Cracker")
            self.style = Style()
            self.style.theme_use("default")

            self.pack(fill=BOTH, expand=1)

            #load buttons and labels
            self.closeButton= Button(self, text="Close Program", command=self.confirmExit)
            self.closeButton.pack(side=BOTTOM, padx=5, pady=5)
            self.mainMenuLabel= Label(self, text="Main Menu")
            self.mainMenuLabel.pack(side=TOP,padx=5, pady=5)
            self.singleModeButton= Button(self, text="Single Computer Mode", command=self.unpackInitUI_LoadSingleComputerMode)
            self.singleModeButton.pack(side=TOP, padx=5, pady=5)
            self.networkModeButton= Button(self, text="Networking Mode", command=self.unpackInitUI_LoadNetworkMode)
            self.networkModeButton.pack(side=TOP, padx=5, pady=5)

        except Exception as inst:
            print "============================================================================================="
            print "GUI ERROR: An exception was thrown in initUI definition Try block"
            #the exception instance
            print type(inst)
            #srguments stored in .args
            print inst.args
            #_str_ allows args tto be printed directly
            print inst
            print "============================================================================================="
    #end of initUI////////////////////////////

    def unpackInitUI_LoadSingleComputerMode(self):
        self.closeButton.pack_forget()
        self.mainMenuLabel.pack_forget()
        self.singleModeButton.pack_forget()
        self.networkModeButton.pack_forget()
        self.singleModeUI()

    def unpackInitUI_LoadNetworkMode(self):
        self.closeButton.pack_forget()
        self.mainMenuLabel.pack_forget()
        self.singleModeButton.pack_forget()
        self.networkModeButton.pack_forget()
        self.networkModeUI()

    def unpackSingleModeUI_LoadInitUI(self):
        self.closeButton.pack_forget()
        self.returnToInitUIButton.pack_forget()
        self.singleModeLabel.pack_forget()
        self.selectCrackingMethodLabel.pack_forget()
        self.dictionaryCrackingMethodButton.pack_forget()
        self.bruteForceCrackingMethodButton.pack_forget()
        self.rainbowTableCrackingMethodButton.pack_forget()
        self.initUI()

    def unpackSingleModeUI_LoadSingleDictionaryUI(self):
        self.closeButton.pack_forget()
        self.returnToInitUIButton.pack_forget()
        self.singleModeLabel.pack_forget()
        self.selectCrackingMethodLabel.pack_forget()
        self.dictionaryCrackingMethodButton.pack_forget()
        self.bruteForceCrackingMethodButton.pack_forget()
        self.rainbowTableCrackingMethodButton.pack_forget()
        self.dictionaryCrackingMethodUI(0)

    def unpackSingleModeUI_LoadSingleBruteForceUI(self):
        self.closeButton.pack_forget()
        self.returnToInitUIButton.pack_forget()
        self.singleModeLabel.pack_forget()
        self.selectCrackingMethodLabel.pack_forget()
        self.dictionaryCrackingMethodButton.pack_forget()
        self.bruteForceCrackingMethodButton.pack_forget()
        self.rainbowTableCrackingMethodButton.pack_forget()
        self.bruteForceCrackingMethodUI(0)

    def unpackSingleModeUI_LoadSingleRainbowTableUI(self):
        self.closeButton.pack_forget()
        self.returnToInitUIButton.pack_forget()
        self.singleModeLabel.pack_forget()
        self.selectCrackingMethodLabel.pack_forget()
        self.dictionaryCrackingMethodButton.pack_forget()
        self.bruteForceCrackingMethodButton.pack_forget()
        self.rainbowTableCrackingMethodButton.pack_forget()
        self.rainbowTableCrackingMethodUI(0)

    def singleModeUI(self):
        try:
            self.parent.title("Mighty Cracker")
            self.style = Style()
            self.style.theme_use("default")

            self.pack(fill=BOTH, expand=1)

            #load buttons and labels
            self.closeButton= Button(self, text="Close Program", command=self.confirmExit)
            self.closeButton.pack(side=BOTTOM, padx=5, pady=5)
            self.returnToInitUIButton= Button(self, text="Return to Main Menu", command=self.unpackSingleModeUI_LoadInitUI)
            self.returnToInitUIButton.pack(side=BOTTOM, padx=5, pady=5)
            self.singleModeLabel= Label(self, text="Single Computer Mode")
            self.singleModeLabel.pack(side=TOP, padx=5, pady=5)
            self.selectCrackingMethodLabel= Label(self, text="Select Your Cracking Method")
            self.selectCrackingMethodLabel.pack(side=TOP, padx=5, pady=5)
            self.dictionaryCrackingMethodButton= Button(self, text="Dictionary", command=self.unpackSingleModeUI_LoadSingleDictionaryUI)
            self.dictionaryCrackingMethodButton.pack(side=TOP, padx=5, pady=5)
            self.bruteForceCrackingMethodButton= Button(self, text="Brute-Force (default)", command=self.unpackSingleModeUI_LoadSingleBruteForceUI)
            self.bruteForceCrackingMethodButton.pack(side=TOP, padx=5, pady=5)
            self.rainbowTableCrackingMethodButton= Button(self, text="Rainbow Table", command=self.unpackSingleModeUI_LoadSingleRainbowTableUI)
            self.rainbowTableCrackingMethodButton.pack(side=TOP, padx=5, pady=5)

        except Exception as inst:
            print "============================================================================================="
            print "GUI ERROR: An exception was thrown in singleModeUI definition Try block"
            #the exception instance
            print type(inst)
            #srguments stored in .args
            print inst.args
            #_str_ allows args tto be printed directly
            print inst
            print "============================================================================================="
    #End of single mode

    def unpackNetworkModeUI_LoadInitUI(self):
        self.closeButton.pack_forget()
        self.returnToInitUIButton.pack_forget()
        self.networkModeLabel.pack_forget()
        self.selectNetworkModuleLabel.pack_forget()
        self.serverModuleButton.pack_forget()
        self.clientModuleButton.pack_forget()
        self.initUI()

    def networkModeUI(self):
        try:
            self.parent.title("Mighty Cracker")
            self.style = Style()
            self.style.theme_use("default")

            self.pack(fill=BOTH, expand=1)

            #load buttons and labels
            self.closeButton= Button(self, text="Close Program", command=self.confirmExit)
            self.closeButton.pack(side=BOTTOM, padx=5, pady=5)
            self.returnToInitUIButton= Button(self, text="Return to Main Menu", command=self.unpackNetworkModeUI_LoadInitUI)
            self.returnToInitUIButton.pack(side=BOTTOM, padx=5, pady=5)
            self.networkModeLabel= Label(self, text="Network Mode: Server/Client Selection Screen")
            self.networkModeLabel.pack(side=TOP, padx=5, pady=5)
            self.selectNetworkModuleLabel= Label(self, text="Select Server or Client")
            self.selectNetworkModuleLabel.pack(side=TOP, padx=5, pady=5)
            self.serverModuleButton= Button(self, text="I am the Server", command= self.unpackNetworkModeUI_LoadNetworkServerUI)
            self.serverModuleButton.pack(side=TOP, padx=5, pady=5)
            self.clientModuleButton= Button(self, text="I am a Client", command= self.unpackNetworkModeUI_LoadNetworkClientUI)
            self.clientModuleButton.pack(side=TOP, padx=5, pady=5)

        except Exception as inst:
            print "============================================================================================="
            print "GUI ERROR: An exception was thrown in networkModeUI definition Try block"
            #the exception instance
            print type(inst)
            #srguments stored in .args
            print inst.args
            #_str_ allows args tto be printed directly
            print inst
            print "============================================================================================="
    #end of networkModeUI

    def unpackNetworkModeUI_LoadNetworkServerUI(self):
        self.closeButton.pack_forget()
        self.returnToInitUIButton.pack_forget()
        self.networkModeLabel.pack_forget()
        self.selectNetworkModuleLabel.pack_forget()
        self.serverModuleButton.pack_forget()
        self.clientModuleButton.pack_forget()
        self.networkServerUI()

    def unpackNetworkModeUI_LoadNetworkClientUI(self):
        self.closeButton.pack_forget()
        self.returnToInitUIButton.pack_forget()
        self.networkModeLabel.pack_forget()
        self.selectNetworkModuleLabel.pack_forget()
        self.serverModuleButton.pack_forget()
        self.clientModuleButton.pack_forget()
        self.networkClientUI()

    def unpackNetworkClientUI_LoadInitUI(self):
        self.closeButton.pack_forget()
        self.returnToInitUIButton.pack_forget()
        self.networkClientLabel.pack_forget()
        self.insertServerIPLabel.pack_forget()
        self.insertServerIPTextfield.pack_forget()
        self.startClientButton.pack_forget()
        self.initUI()

    def networkClientUI(self):
        try:
            self.parent.title("Mighty Cracker")
            self.style = Style()
            self.style.theme_use("default")

            self.pack(fill=BOTH, expand=1)

            #load buttons and labels
            self.closeButton= Button(self, text="Close Program", command=self.confirmExit)
            self.closeButton.pack(side=BOTTOM, padx=5, pady=5)
            self.returnToInitUIButton= Button(self, text="Return to Main Menu", command=self.unpackNetworkClientUI_LoadInitUI)
            self.returnToInitUIButton.pack(side=BOTTOM, padx=5, pady=5)
            self.networkClientLabel= Label(self, text="Network Client")
            self.networkClientLabel.pack(side=TOP, padx=5, pady=5)
            self.insertServerIPLabel= Label(self, text="Enter in the Server's IP:")
            self.insertServerIPLabel.pack(side=TOP, padx=5, pady=5)
            self.insertServerIPTextfield= Entry(self, bd=5)
            self.insertServerIPTextfield.pack(side=TOP, padx=5, pady=5)
            #TODO allow right click for pasting into box
            self.startClientButton= Button(self, text="Start Client", command=lambda: self.startClient(str(self.insertServerIPTextfield.get())))
            self.startClientButton.pack(side=TOP, padx=5, pady=5)
        except Exception as inst:
            print "============================================================================================="
            print "GUI ERROR: An exception was thrown in networkClientUI definition Try block"
            #the exception instance
            print type(inst)
            #srguments stored in .args
            print inst.args
            #_str_ allows args tto be printed directly
            print inst
            print "============================================================================================="
    #end of networkclient UI

    def startClient(self,inputIP):
        try:
            if(len(inputIP) < 1):
                showwarning("Network Client Start Warning: NO IP","No IP address has been entered!")
            else:
                self.networkClient= Process(target=Client, args=(inputIP,))
                self.networkClient.start()
                self.networkClientStatusUI()
        except Exception as inst:
            print "============================================================================================="
            print "GUI ERROR: An exception was thrown in startClient definition Try block"
            #the exception instance
            print type(inst)
            #srguments stored in .args
            print inst.args
            #_str_ allows args tto be printed directly
            print inst
            print "============================================================================================="

    def networkClientStatusUI(self):
        self.networkClientStatusWindow= Tk()
        self.networkClientStatusWindow.geometry("640x480")
        self.networkClientStatusWindow.title("Network Client Status Window")
        self.networkClientStatusWindow.style = Style()
        self.networkClientStatusWindow.style.theme_use("default")
        self.networkClientStatusWindow.pack(fill=BOTH, expand=1)
        #TODO throws an attribute error on 'pack', thus nothing is drawn to the screen, fix this
        self.CloseButton= Button(self, text="Close Status Window", command=lambda: closeStatusWindow())
        self.CloseButton.pack(side=BOTTOM, padx=5, pady=5)

        def closeStatusWindow(self):
            self.networkClientStatusWindow.destroy()


    def unpackNetworkServerUI_LoadInitUI(self):
        self.closeButton.pack_forget()
        self.returnToInitUIButton.pack_forget()
        self.networkServerLabel.pack_forget()
        self.selectCrackingMethodLabel.pack_forget()
        self.dictionaryCrackingMethodButton.pack_forget()
        self.bruteForceCrackingMethodButton.pack_forget()
        self.rainbowTableCrackingMethodButton.pack_forget()
        self.initUI()

    def networkServerUI(self):
        try:
            self.parent.title("Mighty Cracker")
            self.style = Style()
            self.style.theme_use("default")

            self.pack(fill=BOTH, expand=1)

            #load buttons and labels
            self.closeButton= Button(self, text="Close Program", command=self.confirmExit)
            self.closeButton.pack(side=BOTTOM, padx=5, pady=5)
            self.returnToInitUIButton= Button(self, text="Return to Main Menu", command=self.unpackNetworkServerUI_LoadInitUI)
            self.returnToInitUIButton.pack(side=BOTTOM, padx=5, pady=5)
            self.networkServerLabel= Label(self, text="Network Server")
            self.networkServerLabel.pack(side=TOP, padx=5,  pady=5)
            self.selectCrackingMethodLabel= Label(self, text="Select Your Cracking Method")
            self.selectCrackingMethodLabel.pack(side=TOP, padx=5, pady=5)
            self.dictionaryCrackingMethodButton= Button(self, text="Dictionary", command=self.unpackNetworkServerUI_LoadNetworkDictionaryUI)
            self.dictionaryCrackingMethodButton.pack(side=TOP, padx=5, pady=5)
            self.bruteForceCrackingMethodButton= Button(self, text="Brute-Force (default)", command=self.unpackNetwrokServerUI_LoadNetworkBruteForceUI)
            self.bruteForceCrackingMethodButton.pack(side=TOP, padx=5, pady=5)
            self.rainbowTableCrackingMethodButton= Button(self, text="Rainbow Table", command=self.unpackNetworkServerUI_LoadNetworkRainbowTableUI)
            self.rainbowTableCrackingMethodButton.pack(side=TOP, padx=5, pady=5)
        except Exception as inst:
            print "============================================================================================="
            print "GUI ERROR: An exception was thrown in networkServerUI definition Try block"
            #the exception instance
            print type(inst)
            #srguments stored in .args
            print inst.args
            #_str_ allows args tto be printed directly
            print inst
            print "============================================================================================="
    #end of networkServerUI

    def unpackNetworkServerUI_LoadNetworkDictionaryUI(self):
        self.closeButton.pack_forget()
        self.returnToInitUIButton.pack_forget()
        self.networkServerLabel.pack_forget()
        self.selectCrackingMethodLabel.pack_forget()
        self.dictionaryCrackingMethodButton.pack_forget()
        self.bruteForceCrackingMethodButton.pack_forget()
        self.rainbowTableCrackingMethodButton.pack_forget()
        self.dictionaryCrackingMethodUI(1)

    def unpackNetwrokServerUI_LoadNetworkBruteForceUI(self):
        self.closeButton.pack_forget()
        self.returnToInitUIButton.pack_forget()
        self.networkServerLabel.pack_forget()
        self.selectCrackingMethodLabel.pack_forget()
        self.dictionaryCrackingMethodButton.pack_forget()
        self.bruteForceCrackingMethodButton.pack_forget()
        self.rainbowTableCrackingMethodButton.pack_forget()
        self.bruteForceCrackingMethodUI(1)

    def unpackNetworkServerUI_LoadNetworkRainbowTableUI(self):
        self.closeButton.pack_forget()
        self.returnToInitUIButton.pack_forget()
        self.networkServerLabel.pack_forget()
        self.selectCrackingMethodLabel.pack_forget()
        self.dictionaryCrackingMethodButton.pack_forget()
        self.bruteForceCrackingMethodButton.pack_forget()
        self.rainbowTableCrackingMethodButton.pack_forget()
        self.rainbowTableCrackingMethodUI(1)

    def unpackDictionaryCrackingMethodUI_LoadInitUI(self):
        self.closeButton.pack_forget()
        self.returnToInitUIButton.pack_forget()
        self.dictionaryCrackingMethodLabel.pack_forget()
        self.currentModeLabel.pack_forget()
        self.dictionaryFileLocationLabel.pack_forget()
        self.selectedDictionaryFileLabel.pack_forget()
        self.selectDictionaryFileButton.pack_forget()
        self.inputHashTextFieldLabel.pack_forget()
        self.inputHashTextField.pack_forget()
        self.selectAlgorithmLabel.pack_forget()
        self.md5RadioButton.pack_forget()
        self.sha1RadioButton.pack_forget()
        self.sha224RadioButton.pack_forget()
        self.sha256RadioButton.pack_forget()
        self.sha512RadioButton.pack_forget()
        self.startDictionaryCrackButton.pack_forget()
        self.initUI()

    def dictionaryCrackingMethodUI(self,mode):
        #mode is either 1 (network) or 0 (single)
        currentMode= "ERROR: Mode not selected" #initialize variable
        self.selectedDictionaryFile= ""
        selectedAlgorithm= "MD5" #set to md5 as the default
        inputHash= StringVar()
        inputHash.set("")
        try:
            if(mode == 0):
                currentMode= "Single"
            elif(mode == 1):
                currentMode= "Network"
            else:
                raise Exception("ERROR: Invalid mode parameter: '"+str(mode)+"'")

            self.parent.title("Mighty Cracker")
            self.style = Style()
            self.style.theme_use("default")

            self.pack(fill=BOTH, expand=1)

            #load buttons and labels
            self.closeButton= Button(self, text="Close Program", command=self.confirmExit)
            self.closeButton.pack(side=BOTTOM, padx=5, pady=5)
            self.returnToInitUIButton= Button(self, text="Return to Main Menu", command=self.unpackDictionaryCrackingMethodUI_LoadInitUI)
            self.returnToInitUIButton.pack(side=BOTTOM, padx=5, pady=5)
            self.dictionaryCrackingMethodLabel= Label(self, text="Dictionary Cracking Method")
            self.dictionaryCrackingMethodLabel.pack(side=TOP, padx=5, pady=5)
            self.currentModeLabel = Label(self,text="Current Mode: "+str(currentMode))
            self.currentModeLabel.pack(side=TOP, padx=5, pady=5)
            self.dictionaryFileLocationLabel= Label(self, text="Dictionary File to be used:")
            self.dictionaryFileLocationLabel.pack(side=TOP, padx=5, pady=5)
            self.selectedDictionaryFileLabel= Label(self, text=str(self.selectedDictionaryFile))
            self.selectedDictionaryFileLabel.pack(side=TOP, padx=5, pady=5)
            self.selectDictionaryFileButton= Button(self, text="Select Dictionary File", textvariable= str(self.selectedDictionaryFile), command=self.selectFileWindow) #
            self.selectDictionaryFileButton.pack(side=TOP, padx=5, pady=5)
            #TODO modify the dictionary file so that when a file is selected, that filepath is passed onto server
            #TODO check for dictionary file existance before handling (and file extensions for windows)
            #TODO insert option to crack a file of hashes (pass file to the server/single)
            #TODO check for file existance before handling (and file extensions for windows)
            self.inputHashTextFieldLabel= Label(self, text="The hash to be cracked:")
            self.inputHashTextFieldLabel.pack(side=TOP, padx=5, pady=5)
            self.inputHashTextField= Entry(self, bd=5, textvariable= inputHash)
            self.inputHashTextField.pack(side=TOP, padx=5, pady=5)
            self.selectAlgorithmLabel = Label(self, text="Select the Cracking Algorithm:")
            self.selectAlgorithmLabel.pack(side=TOP, padx=5, pady=5)
            self.md5RadioButton=  Radiobutton(self, text="MD5 (default)", variable= selectedAlgorithm, value="MD5" )
            self.md5RadioButton.pack(side=LEFT, padx=5, pady=5)
            self.sha1RadioButton= Radiobutton(self, text="SHA 1", variable= selectedAlgorithm, value="SHA 1")
            self.sha1RadioButton.pack(side=LEFT, padx=5, pady=5)
            self.sha224RadioButton= Radiobutton(self, text="SHA 224", variable= selectedAlgorithm, value="SHA 224")
            self.sha224RadioButton.pack(side=LEFT, padx=5, pady=5)
            self.sha256RadioButton= Radiobutton(self, text="SHA 256", variable= selectedAlgorithm, value="SHA 256")
            self.sha256RadioButton.pack(side=LEFT, padx=5, pady=5)
            self.sha512RadioButton= Radiobutton(self, text="SHA 512", variable= selectedAlgorithm, value="SHA 512")
            self.sha512RadioButton.pack(side=LEFT, padx=5, pady=5)
            #TODO display result in a noneditable text view
            if(currentMode is 'Single'):
                self.dict = {'cracking method': "dic", 'file name': str(self.selectedDictionaryFile), 'algorithm': selectedAlgorithm, 'hash': str(inputHash.get()), 'single':"True"}
                self.startDictionaryCrackButton= Button(self, text="Start Dictionary Crack (Single Mode)", command=lambda: self.startNetworkServer(self.dict))
                self.startDictionaryCrackButton.pack(side=BOTTOM, padx=5, pady=5)
            elif(currentMode is 'Network'):
                print "GUI DEBUG: Inside elif(currentMode is 'Network)"
                if(len(str(self.inputHashTextField)) < 1):
                    showwarning("Empty hash text field", "The hash text field is empty")
                else:
                    print "GUI DEBUG: '"+str(self.inputHashTextField.get())+"'"
                    self.dict = {'cracking method': "dic", 'file name': str(self.selectedDictionaryFile), 'algorithm': selectedAlgorithm, 'hash': str(inputHash.get())}
                    self.startDictionaryCrackButton= Button(self, text="Start Dictionary Crack (Network Mode)", command=lambda: self.startNetworkServer(self.dict))
                    self.startDictionaryCrackButton.pack(side=BOTTOM, padx=5, pady=5)

            else:
                raise Exception("GUI ERROR: Invalid currentMode in startDictionaryCrackButton: '"+str(currentMode)+"'")

        except Exception as inst:
            print "============================================================================================="
            print "GUI ERROR: An exception was thrown in dictionaryCrackingMethodUI definition Try block"
            #the exception instance
            print type(inst)
            #srguments stored in .args
            print inst.args
            #_str_ allows args tto be printed directly
            print inst
            print "============================================================================================="
    #end of dictionary cracking methodUI

    def setDictHash(self,newHash):
        print "GUI DEBUG: hash is: '"+str(newHash)+"'"
        self.dict['hash']= str(newHash)

    def startNetworkServer(self, crackingMethod):
        print "GUI DEBUG: hash is: '"+str(crackingMethod['hash'])+"'"
        self.networkServer= Process(target=Server, args=(crackingMethod,))
        self.networkServer.start()
        #TODO idea: create a server is running window, with the stats

    def unpackBruteForceCrackingMethodUI_LoadInitUI(self):
        self.closeButton.pack_forget()
        self.returnToInitUIButton.pack_forget()
        self.inputHashTextFieldLabel.pack_forget()
        self.inputHashTextField.pack_forget()
        self.bruteForceCrackingMethodLabel.pack_forget()
        self.currentModeLabel.pack_forget()
        self.startBruteForceCrackButton.pack_forget()
        self.algorithmSelectionLabel.pack_forget()
        self.algorithmOptionMenu.pack_forget()
        self.alphabetSelectionLabel.pack_forget()
        self.alphabetOptionMenu.pack_forget()
        self.minKeyLengthLabel.pack_forget()
        self.minKeyLengthTextField.pack_forget()
        self.maxKeyLengthLabel.pack_forget()
        self.maxKeyLengthTextField.pack_forget()
        self.outputHashTextFieldLabel.pack_forget()
        self.outputHashTextField.pack_forget()
        self.initUI()

    def bruteForceCrackingMethodUI(self, mode):
        #mode is either 1 (network) or 0 (single)
        currentMode= None
        selectedAlgorithm= StringVar()
        selectedAlgorithm.set("MD5")
        selectedAlphabet= StringVar()
        selectedAlphabet.set("All")
        minKeyLength= IntVar()
        minKeyLength.set(5)
        maxKeyLength= IntVar()
        maxKeyLength.set(15)
        inputHash= StringVar()
        inputHash.set("")
        try:
            if(mode==0):
                currentMode= "Single"
            elif(mode ==1):
                currentMode= "Network"
            else:
                raise Exception("ERROR: Invalid mode parameter: '"+str(mode)+"'")

            self.parent.title("Mighty Cracker")
            self.style = Style()
            self.style.theme_use("default")

            self.pack(fill=BOTH, expand=1)

            #load buttons and labels
            self.closeButton= Button(self, text="Close Program", command=self.confirmExit)
            self.closeButton.pack(side=BOTTOM, padx=5, pady=5)
            self.returnToInitUIButton= Button(self, text="Return to Main Menu", command=self.unpackBruteForceCrackingMethodUI_LoadInitUI)
            self.returnToInitUIButton.pack(side=BOTTOM, padx=5, pady=5)
            self.bruteForceCrackingMethodLabel = Label(self, text="Brute-Force Cracking Method")
            self.bruteForceCrackingMethodLabel.pack(side=TOP, padx=5, pady=5)
            self.currentModeLabel= Label(self, text="Current Mode: "+str(currentMode))
            self.currentModeLabel.pack(side=TOP, padx=5, pady=5)
            self.algorithmSelectionLabel= Label(self, text="Select which algorithm you want to use:")
            self.algorithmSelectionLabel.pack(side=TOP, padx=5, pady=5)
            self.algorithmOptionMenu= OptionMenu(self, selectedAlgorithm, "MD5", "SHA 1", "SHA 224", "SHA 256", "SHA 512")
            self.algorithmOptionMenu.pack(side=TOP, padx=5, pady=5)
            self.alphabetSelectionLabel= Label(self, text="Select which alphabet you want to use:")
            self.alphabetSelectionLabel.pack(side=TOP, padx=5, pady=5)
            self.alphabetOptionMenu= OptionMenu(self, selectedAlphabet, "All", "ASCII_Uppercase", "ASCII_Lowercase", "Digits", "Special_Symbols")
            self.alphabetOptionMenu.pack(side=TOP, padx=5, pady=5)
            self.minKeyLengthLabel= Label(self, text="Select the minimum key length: (Default is 5)")
            self.minKeyLengthLabel.pack(side=TOP, padx=5, pady=5)
            self.minKeyLengthTextField= Entry(self, bd=5, textvariable= minKeyLength)
            self.minKeyLengthTextField.pack(side=TOP, padx=5, pady=5)
            self.maxKeyLengthLabel= Label(self, text="Select the maximum key length:  (Default is 15)")
            self.maxKeyLengthLabel.pack(side=TOP, padx=5, pady=5)
            self.maxKeyLengthTextField= Entry(self, bd=5, textvariable= maxKeyLength)
            self.maxKeyLengthTextField.pack(side=TOP, padx=5, pady=5)
            #TODO add support for combination of alphabets
            #TODO insert option to hash a file of hashes (pass the file to server/single)
            #TODO check for file existance before handling (and file extensions for windows)
            self.inputHashTextFieldLabel= Label(self, text="The hash to be cracked:")
            self.inputHashTextFieldLabel.pack(side=TOP, padx=5, pady=5)
            self.inputHashTextField= Entry(self, bd=5, textvariable= inputHash)
            self.inputHashTextField.pack(side=TOP, padx=5, pady=5)
            #TODO display results is a copiable textview

            if(currentMode is 'Single'):
                self.dict = {'cracking method': "bf", 'hash': str(inputHash.get()), 'algorithm':str(selectedAlgorithm.get()),
                             'alphabet':str(selectedAlphabet.get()), 'min key length':int(minKeyLength.get()), 'max key length':int(maxKeyLength.get()), 'single':"True"}
                self.startBruteForceCrackButton= Button(self, text="Start Brute-Force Crack (Single Mode)", command=lambda: self.startNetworkServer(self.dict))
                self.startBruteForceCrackButton.pack(side=BOTTOM, padx=5, pady=5)

            elif(currentMode is 'Network'):
               # print "GUI DEBUG: Inside elif(currentMode is 'Network)"
                #if(len(str(inputHash.get())) < 1):
                 #   showwarning("Empty hash text field", "The hash text field is empty")
                #else:
                print "GUI DEBUG: '"+str(self.inputHashTextField.get())+"'"
                self.dict = {'cracking method': "bf", 'hash': str(inputHash.get()), 'algorithm':str(selectedAlgorithm.get()),
                             'alphabet':str(selectedAlphabet.get()), 'min key length':int(minKeyLength.get()), 'max key length':int(maxKeyLength.get())}
                self.startBruteForceCrackButton= Button(self, text="Start Brute-Force Crack (Network Mode)", command=lambda: self.startNetworkServer(self.dict))
                self.startBruteForceCrackButton.pack(side=BOTTOM, padx=5, pady=5)
            else:
                raise Exception("ERROR: Invalid mode parameter in Brute-Force CrackingUI: '"+str(mode)+"'")

            #This will display the results, could set to show up after the program is run.
            self.outputHashTextFieldLabel= Label(self, text="Results")
            self.outputHashTextFieldLabel.pack(side=TOP, padx=5, pady=5)
            self.outputHashTextField= Entry(self, bd=5)
            self.outputHashTextField.insert(0, "Test")
            self.outputHashTextField.pack(side=TOP,padx=5, pady=5)

        except Exception as inst:
            print "============================================================================================="
            print "GUI ERROR: An exception was thrown in bruteForceCrackingMethodUI definition Try block"
            #the exception instance
            print type(inst)
            #srguments stored in .args
            print inst.args
            #_str_ allows args tto be printed directly
            print inst
            print "============================================================================================="
    #end of brute force cracking UI

    def unpackRainbowTableCrackingMethodUI_LoadInitUI(self):
        self.closeButton.pack_forget()
        self.returnToInitUIButton.pack_forget()
        self.rainbowTableCrackingMethodLabel.pack_forget()
        self.currentModeLabel.pack_forget()
        self.initUI()

    def rainbowTableCrackingMethodUI(self, mode):
        #mode is either 1 (network) or 0 (single)
        currentMode= None
        try:
            if(mode == 0):
                currentMode = "Single"
            elif(mode == 1):
                currentMode = "Network"
            else:
               raise Exception("ERROR: Invalid mode parameter: '"+str(mode)+"'")

            self.parent.title("Mighty Cracker")
            self.style = Style()
            self.style.theme_use("default")

            self.pack(fill=BOTH, expand=1)

            #load buttons and labels
            self.closeButton= Button(self, text="Close Program", command=self.confirmExit)
            self.closeButton.pack(side=BOTTOM, padx=5, pady=5)
            self.returnToInitUIButton= Button(self, text="Return to Main Menu", command=self.unpackRainbowTableCrackingMethodUI_LoadInitUI)
            self.returnToInitUIButton.pack(side=BOTTOM, padx=5, pady=5)
            self.rainbowTableCrackingMethodLabel= Label(self, text="Rainbow Table Cracking Method")
            self.rainbowTableCrackingMethodLabel.pack(side=TOP, padx=5, pady=5)
            self.currentModeLabel= Label(self,text="Current Mode: "+str(currentMode))
            self.currentModeLabel.pack(side=TOP, padx=5, pady=5)
            #TODO insert Rainbow table settings here

        except Exception as inst:
            print "============================================================================================="
            print "GUI ERROR: An exception was thrown in rainbowTableCrackingMethodUI definition Try block"
            #the exception instance
            print type(inst)
            #srguments stored in .args
            print inst.args
            #_str_ allows args tto be printed directly
            print inst
            print "============================================================================================="
    #end of rainbow table cracking UI

    def selectFileWindow(self):
        filename= ""
        filename= askopenfilename()
        #remove the file extension
       # modifiedFileName= self.removeFileNameExtension(filename)
        print "Modified fileName= '"+str(filename)+"'"
        self.selectedDictionaryFileLabel.config(text=str(filename))
        self.selectedDictionaryFile= str(self.selectedDictionaryFileLabel.cget("text"))

    '''
    def removeFileNameExtension(self, inputFileName):
        outboundFileName= ""
        lastForwardSlashPos=0
        for i in range(0, len(inputFileName)):
            if(inputFileName[i] == "."):
                break
            elif(inputFileName[i] == "/"):
                lastForwardSlashPos= i
                outboundFileName+= inputFileName[i]
            else:
                outboundFileName+= inputFileName[i]
        print "FileName after extension is removed: '"+str(outboundFileName)+"'"
        pathlessFileName= self.removeAbsoluteFilePath(outboundFileName, lastForwardSlashPos)
        print "FileName after absolute filepath was removed: '"+str(pathlessFileName)+"'"
        return pathlessFileName

    def removeAbsoluteFilePath(self, inboundFilePath, lastForwardSlashPos):
        relativeFilePath= ""
        for i in range(lastForwardSlashPos+1, len(inboundFilePath)):
            if(inboundFilePath[i] is not None):
                relativeFilePath+= inboundFilePath[i]
            else:
                break
        return relativeFilePath
    '''

    def confirmExit(self):
        result= askyesno('Exit Confirmation', 'Are you sure you want to quit this application? \n (WARNING: All server, client, and single computer processes will be terminated!!)')
        if result == True:
            self.onExit()
        #if no is selected, then the window just closes

    def onExit(self):
       # self.networkServer.join()
        try:
            self.networkServer.terminate()
        except Exception as inst:
            print "============================================================================================="
            print "GUI ERROR: An exception was thrown in onExit terminate networkserver process Try block"
            #the exception instance
            print type(inst)
            #srguments stored in .args
            print inst.args
            #_str_ allows args tto be printed directly
            print inst
            print "============================================================================================="
        #self.networkClient.join()
        try:
            self.networkClient.terminate()
        except Exception as inst:
            print "============================================================================================="
            print "GUI ERROR: An exception was thrown in onExit terminate networkclient process Try block"
            #the exception instance
            print type(inst)
            #srguments stored in .args
            print inst.args
            #_str_ allows args tto be printed directly
            print inst
            print "============================================================================================="

        self.parent.destroy()
        #self.quit()

def main():
    root = Tk()
    root.geometry("1024x768+300+300")
    app = guiDemo3(root)
    root.mainloop()

if __name__ == '__main__':
    main()