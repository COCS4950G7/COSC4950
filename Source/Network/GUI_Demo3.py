__author__ = 'Chris Hamm'
#GUI_Demo3

try: #importing libraries try block
    from Tkinter import Tk, RIGHT, TOP, LEFT, BOTTOM, BOTH, Menu, Label, Entry
    from ttk import Frame, Button, Style, Radiobutton
    from NetworkServer_r15 import Server
    from NetworkClient_r15 import Client
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
            self.closeButton= Button(self, text="Close Program", command=self.onExit)
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
            self.closeButton= Button(self, text="Close Program", command=self.onExit)
            self.closeButton.pack(side=BOTTOM, padx=5, pady=5)
            self.returnToInitUIButton= Button(self, text="Return to Main Menu", command=self.unpackSingleModeUI_LoadInitUI)
            self.returnToInitUIButton.pack(side=BOTTOM, padx=5, pady=5)
            self.singleModeLabel= Label(self, text="Single Computer Mode")
            self.singleModeLabel.pack(side=TOP, padx=5, pady=5)
            self.selectCrackingMethodLabel= Label(self, text="Select Your Cracking Method")
            self.selectCrackingMethodLabel.pack(side=TOP, padx=5, pady=5)
            self.dictionaryCrackingMethodButton= Button(self, text="Dictionary", command=self.unpackSingleModeUI_LoadSingleDictionaryUI)
            self.dictionaryCrackingMethodButton.pack(side=TOP, padx=5, pady=5)
            self.bruteForceCrackingMethodButton= Button(self, text="Brute-Force", command=self.unpackSingleModeUI_LoadSingleBruteForceUI)
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
            self.closeButton= Button(self, text="Close Program", command=self.onExit)
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
            self.closeButton= Button(self, text="Close Program", command=self.onExit)
            self.closeButton.pack(side=BOTTOM, padx=5, pady=5)
            self.returnToInitUIButton= Button(self, text="Return to Main Menu", command=self.unpackNetworkClientUI_LoadInitUI)
            self.returnToInitUIButton.pack(side=BOTTOM, padx=5, pady=5)
            self.networkClientLabel= Label(self, text="Network Client")
            self.networkClientLabel.pack(side=TOP, padx=5, pady=5)
            self.insertServerIPLabel= Label(self, text="Enter in the Server's IP:")
            self.insertServerIPLabel.pack(side=TOP, padx=5, pady=5)
            self.insertServerIPTextfield= Entry(self, bd=5)
            self.insertServerIPTextfield.pack(side=TOP, padx=5, pady=5)
            self.startClientButton= Button(self, text="Start Client", command=self.startClient(str(self.insertServerIPTextfield)))
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
            self.networkClient= Process(target=Client, args=(inputIP,))
            self.networkClient.start()
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
            self.closeButton= Button(self, text="Close Program", command=self.onExit)
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
        self.selectAlgorithmLabel.pack_forget()
        self.md5RadioButton.pack_forget()
        self.sha1RadioButton.pack_forget()
        self.initUI()

    def dictionaryCrackingMethodUI(self,mode):
        #mode is either 1 (network) or 0 (single)
        currentMode= None #initialize variable
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
            self.closeButton= Button(self, text="Close Program", command=self.onExit)
            self.closeButton.pack(side=BOTTOM, padx=5, pady=5)
            self.returnToInitUIButton= Button(self, text="Return to Main Menu", command=self.unpackDictionaryCrackingMethodUI_LoadInitUI)
            self.returnToInitUIButton.pack(side=BOTTOM, padx=5, pady=5)
            self.dictionaryCrackingMethodLabel= Label(self, text="Dictionary Cracking Method")
            self.dictionaryCrackingMethodLabel.pack(side=TOP, padx=5, pady=5)
            self.currentModeLabel = Label(self,text="Current Mode: "+str(currentMode))
            self.currentModeLabel.pack(side=TOP, padx=5, pady=5)
            self.selectAlgorithmLabel = Label(self, text="Select the Cracking Algorithm:")
            self.selectAlgorithmLabel.pack(side=TOP, padx=5, pady=5)
            self.md5RadioButton=  Radiobutton(self, text="MD5 (default)", variable= selectedAlgorithm, value="MD5" )
            self.md5RadioButton.pack(side=LEFT, padx=5, pady=5)
            self.sha1RadioButton= Radiobutton(self, text="SHA1", variable= selectedAlgorithm, value="SHA1")
            self.sha1RadioButton.pack(side=LEFT, padx=5, pady=5)
            #TODO insert dictionary settings here

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

    def unpackBruteForceCrackingMethodUI_LoadInitUI(self):
        self.closeButton.pack_forget()
        self.returnToInitUIButton.pack_forget()
        self.bruteForceCrackingMethodLabel.pack_forget()
        self.currentModeLabel.pack_forget()
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
            self.closeButton= Button(self, text="Close Program", command=self.onExit)
            self.closeButton.pack(side=BOTTOM, padx=5, pady=5)
            self.returnToInitUIButton= Button(self, text="Return to Main Menu", command=self.unpackBruteForceCrackingMethodUI_LoadInitUI)
            self.returnToInitUIButton.pack(side=BOTTOM, padx=5, pady=5)
            self.bruteForceCrackingMethodLabel = Label(self, text="Brute-Force Cracking Method")
            self.bruteForceCrackingMethodLabel.pack(side=TOP, padx=5, pady=5)
            self.currentModeLabel= Label(self, text="Current Mode: "+str(currentMode))
            self.currentModeLabel.pack(side=TOP, padx=5, pady=5)
            #TODO insert brute force settings here

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
            self.closeButton= Button(self, text="Close Program", command=self.onExit)
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

    def onExit(self):
        self.quit()

def main():
    root = Tk()
    root.geometry("640x480+300+300")
    app = guiDemo3(root)
    root.mainloop()

if __name__ == '__main__':
    main()