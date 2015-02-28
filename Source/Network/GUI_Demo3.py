__author__ = 'Chris Hamm'
#GUI_Demo3
#TODO thought, have a event trigger a wake up in GUI, to indicate that something changed in the status
#TODO condense the unpack methods into one function that adapts based on which screen you where using
#TODO reference www.pyton-course.eu/tkinter_entry_widgets.php for more sophisticated gui layouts

try: #importing libraries try block
    from Tkinter import Tk, RIGHT, TOP, LEFT, BOTTOM, BOTH, Menu, Label, Entry
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
            self.startClientButton= Button(self, text="Start Client", command=lambda:self.startClient(str(self.insertServerIPTextfield.get())))
            #TODO pass values in by a dictionary, see server_r15a to dictionary chunk manager for reference
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

    def startClient(self,inputIP):
        try:
            if(len(inputIP) < 1):
                showwarning("Network Client Start Warning: NO IP","No IP address has been entered!")
            else:
                #print "GUI BEDUG: '"+str(inputIP)+"'"
                import socket
                try:
                    socket.inet_aton(inputIP) #if sucsessful, then it is legal
                    self.networkClient= Process(target=Client, args=(inputIP,))
                    self.networkClient.start()
                except socket.error:
                    showwarning("Invalid IP Address", "The IP address you entered is not valid.")
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
        selectedDictionaryFile= "No Dictionary file has been selected"
        selectedAlgorithm= "MD5" #set to md5 as the default
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
            if(currentMode is 'Single'):
                self.startDictionaryCrackButton= Button(self, text="Start Dictionary Crack (Single Mode)")
                self.startDictionaryCrackButton.pack(side=BOTTOM, padx=5, pady=5)
                 #TODO create call method to start the dictionary crack
            elif(currentMode is 'Network'):
                dict = {'cracking method': "dictionary", 'file name': "dic"}
                self.startDictionaryCrackButton= Button(self, text="Start Dictionary Crack (Network Mode)", command=lambda: self.startNetworkServer(dict))
                self.startDictionaryCrackButton.pack(side=BOTTOM, padx=5, pady=5)

            else:
                raise Exception("GUI ERROR: Invalid currentMode in startDictionaryCrackButton: '"+str(currentMode)+"'")


            self.dictionaryCrackingMethodLabel= Label(self, text="Dictionary Cracking Method")
            self.dictionaryCrackingMethodLabel.pack(side=TOP, padx=5, pady=5)
            self.currentModeLabel = Label(self,text="Current Mode: "+str(currentMode))
            self.currentModeLabel.pack(side=TOP, padx=5, pady=5)
            self.dictionaryFileLocationLabel= Label(self, text="Dictionary File to be used:")
            self.dictionaryFileLocationLabel.pack(side=TOP, padx=5, pady=5)
            self.selectedDictionaryFileLabel= Label(self, text=str(selectedDictionaryFile))
            self.selectedDictionaryFileLabel.pack(side=TOP, padx=5, pady=5)
            self.selectDictionaryFileButton= Button(self, text="Select Dictionary File", command=self.selectFileWindow)
            self.selectDictionaryFileButton.pack(side=TOP, padx=5, pady=5)
            #TODO check for dictionary file existance before handling (and file extensions for windows)
            #TODO insert option to crack a file of hashes (pass file to the server/single)
            #TODO check for file existance before handling (and file extensions for windows)
            self.inputHashTextFieldLabel= Label(self, text="The hash to be cracked:")
            self.inputHashTextFieldLabel.pack(side=TOP, padx=5, pady=5)
            self.inputHashTextField= Entry(self, bd=5)
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

    def startNetworkServer(self, crackingMethod):
        self.networkServer= Process(target=Server, args=(crackingMethod,))
        self.networkServer.start()

    def unpackBruteForceCrackingMethodUI_LoadInitUI(self):
        self.closeButton.pack_forget()
        self.returnToInitUIButton.pack_forget()
        self.inputHashTextFieldLabel.pack_forget()
        self.inputHashTextField.pack_forget()
        self.bruteForceCrackingMethodLabel.pack_forget()
        self.currentModeLabel.pack_forget()
        self.startBruteForceCrackButton.pack_forget()
        self.initUI()

    def bruteForceCrackingMethodUI(self, mode):
        #mode is either 1 (network) or 0 (single)
        currentMode= None
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
            if(currentMode is 'Single'):
                self.startBruteForceCrackButton= Button(self, text="Start Brute-Force Crack (Single Mode)")
                self.startBruteForceCrackButton.pack(side=BOTTOM, padx=5, pady=5)
                #TODO create call method to start the brute force crack
            elif(currentMode is 'Network'):
                self.startBruteForceCrackButton= Button(self, text="Start Brute-Force Crack (Network Mode)")
                self.startBruteForceCrackButton.pack(side=BOTTOM, padx=5, pady=5)
                #TODO create call method to start the network brute force crack
            else:
                raise Exception ("GUI ERROR: Invalid currentMode in startBruteForceCrackButton: '"+str(currentMode)+"'")
            self.bruteForceCrackingMethodLabel = Label(self, text="Brute-Force Cracking Method")
            self.bruteForceCrackingMethodLabel.pack(side=TOP, padx=5, pady=5)
            self.currentModeLabel= Label(self, text="Current Mode: "+str(currentMode))
            self.currentModeLabel.pack(side=TOP, padx=5, pady=5)
            #TODO insert option to hash a file of hashes (pass the file to server/single)
            #TODO check for file existance before handling (and file extensions for windows)
            self.inputHashTextFieldLabel= Label(self, text="The hash to be cracked:")
            self.inputHashTextFieldLabel.pack(side=TOP, padx=5, pady=5)
            self.inputHashTextField= Entry(self, bd=5)
            self.inputHashTextField.pack(side=TOP, padx=5, pady=5)
            #TODO display results is a copiable textview

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

    def selectFileWindow(self):
        filename= ""
        filename= askopenfilename()
        self.selectedDictionaryFileLabel.config(text=str(filename))


    def confirmExit(self):
        result= askyesno('Exit Confirmation', 'Are you sure you want to quit this application? \n (WARNING: All server, client, and single computer processes will be terminated!!)')
        if result == True:
            self.onExit()
        #if no is selected, then the window just closes

    def onExit(self):
        self.quit()

def main():
    root = Tk()
    root.geometry("640x480+300+300")
    app = guiDemo3(root)
    root.mainloop()

if __name__ == '__main__':
    main()