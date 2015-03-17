__author__ = 'chris hamm'
#GUI_WX_Demo4

import wx
import hashlib
import sys
from multiprocessing import Process, Event
from NetworkServer_r15b import Server
from NetworkClient_r15a import Client
from HashGenerator_RevHamm import hashGenerator


class PanelOne(wx.Panel):           #========================Main Menu=====================
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)

        vbox= wx.BoxSizer(wx.VERTICAL)

        hbox1= wx.BoxSizer(wx.HORIZONTAL)
        screenHeader= wx.StaticText(self, label="Mighty Cracker")
        hbox1.Add(screenHeader)
        vbox.Add(hbox1, flag=wx.TOP|wx.CENTER, border=10)

        vbox.Add((-1, 25)) #add extra space between header and the first button

        hbox2= wx.BoxSizer(wx.HORIZONTAL)
        SingleModeButton= wx.Button(self, label="Single Mode")
        hbox2.Add(SingleModeButton)
        vbox.Add(hbox2, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox3= wx.BoxSizer(wx.HORIZONTAL)
        NetworkModeButton= wx.Button(self, label="Network Mode")
        hbox3.Add(NetworkModeButton)
        vbox.Add(hbox3, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox4= wx.BoxSizer(wx.HORIZONTAL)
        aboutUsButton= wx.Button(self, label="About Us")
        hbox4.Add(aboutUsButton)
        vbox.Add(hbox4, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox5= wx.BoxSizer(wx.HORIZONTAL)
        CloseButton= wx.Button(self, label="Close")
        hbox5.Add(CloseButton)
        vbox.Add(hbox5, flag=wx.CENTER, border=10)

        self.SetSizer(vbox)

        #Bind the buttons to events
        SingleModeButton.Bind(wx.EVT_BUTTON,  parent.onSingleModeButtonClick)
        NetworkModeButton.Bind(wx.EVT_BUTTON, parent.switchFromPanel1ToPanel6)
        aboutUsButton.Bind(wx.EVT_BUTTON, parent.switchFromPanel1ToPanel13)
        CloseButton.Bind(wx.EVT_BUTTON, parent.OnClose)



class PanelTwo(wx.Panel):             #====================Select Cracking Method=============================
    def __init__(self,parent):
        wx.Panel.__init__(self, parent=parent)

        vbox= wx.BoxSizer(wx.VERTICAL)

        hbox1= wx.BoxSizer(wx.HORIZONTAL)
        screenHeader= wx.StaticText(self, label="Select Cracking Method")
        hbox1.Add(screenHeader)
        vbox.Add(hbox1, flag=wx.TOP|wx.CENTER, border=10)

        vbox.Add((-1,25)) #spacer for adding space between header and the buttons

        hbox2= wx.BoxSizer(wx.HORIZONTAL)
        self.currentMode= wx.StaticText(self, label="Current Mode: Not yet Specified")
        hbox2.Add(self.currentMode)
        vbox.Add(hbox2, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox3= wx.BoxSizer(wx.HORIZONTAL)
        DictionaryMethodButton= wx.Button(self, label="Dictionary")
        hbox3.Add(DictionaryMethodButton)
        vbox.Add(hbox3, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox4= wx.BoxSizer(wx.HORIZONTAL)
        BruteForceMethodButton= wx.Button(self, label="Brute Force")
        hbox4.Add(BruteForceMethodButton)
        vbox.Add(hbox4, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox5= wx.BoxSizer(wx.HORIZONTAL)
        RainbowTableMethodButton= wx.Button(self, label="Rainbow Table")
        hbox5.Add(RainbowTableMethodButton)
        vbox.Add(hbox5, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox6= wx.BoxSizer(wx.HORIZONTAL)
        BackToMainMenuButton= wx.Button(self, label="Back To Main Menu")
        hbox6.Add(BackToMainMenuButton)
        vbox.Add(hbox6, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox7= wx.BoxSizer(wx.HORIZONTAL)
        CloseButton= wx.Button(self, label="Close")
        hbox7.Add(CloseButton)
        vbox.Add(hbox7, flag=wx.CENTER, border=10)

        self.SetSizer(vbox)

        #Bind the buttons to events
        DictionaryMethodButton.Bind(wx.EVT_BUTTON, parent.switchFromPanel2ToPanel3)
        BruteForceMethodButton.Bind(wx.EVT_BUTTON, parent.switchFromPanel2ToPanel4)
        RainbowTableMethodButton.Bind(wx.EVT_BUTTON, parent.switchFromPanel2ToPanel5)
        BackToMainMenuButton.Bind(wx.EVT_BUTTON, parent.switchFromPanel2ToPanel1)
        CloseButton.Bind(wx.EVT_BUTTON, parent.OnClose)

class PanelThree(wx.Panel):         #========================Dictionary Cracking Method Settings=================
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        listOfAlgorithms= ['MD5', 'SHA1', 'SHA224', 'SHA256', 'SHA512']

        vbox= wx.BoxSizer(wx.VERTICAL)

        hbox1= wx.BoxSizer(wx.HORIZONTAL)
        screenHeader= wx.StaticText(self, label="Dictionary Cracking Method Settings")
        hbox1.Add(screenHeader)
        vbox.Add(hbox1, flag=wx.TOP|wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox2= wx.BoxSizer(wx.HORIZONTAL)
        self.currentMode= wx.StaticText(self, label="Current Mode: Not Specified")
        hbox2.Add(self.currentMode)
        vbox.Add(hbox2, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox3= wx.BoxSizer(wx.HORIZONTAL)
        selectAlgorithmHeader= wx.StaticText(self, label="Select Algorithm: ")
        hbox3.Add(selectAlgorithmHeader)
        self.selectedAlgorithm= wx.ComboBox(self, choices= listOfAlgorithms, style=wx.CB_READONLY)
        hbox3.Add(self.selectedAlgorithm, flag=wx.LEFT, border=5)
        vbox.Add(hbox3, flag=wx.ALIGN_CENTER|wx.RIGHT, border=10)

        vbox.Add((-1,10))

        hbox4= wx.BoxSizer(wx.HORIZONTAL)
        self.inputHashHeader= wx.StaticText(self, label="Hash to be Cracked: No Hash has been input")
        hbox4.Add(self.inputHashHeader)
        vbox.Add(hbox4, flag=wx.CENTER, border=10)

        vbox.Add(((-1,10)))

        hbox5=wx.BoxSizer(wx.HORIZONTAL)
        inputHashButton= wx.Button(self, label="Set Hash To Be Cracked")
        hbox5.Add(inputHashButton)
        generateHashButton= wx.Button(self, label="Generate Hash Code")
        hbox5.Add(generateHashButton, flag=wx.LEFT, border=5)
        vbox.Add(hbox5, flag=wx.ALIGN_CENTER|wx.RIGHT, border=10)

        vbox.Add((-1,10))

        hbox6= wx.BoxSizer(wx.HORIZONTAL)
        self.inputDictFileHeader= wx.StaticText(self, label="Selected Dictionary File: No Dictionary File Selected")
        hbox6.Add(self.inputDictFileHeader)
        vbox.Add(hbox6, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox7= wx.BoxSizer(wx.HORIZONTAL)
        setDictFileButton= wx.Button(self, label="Select Dictionary File")
        hbox7.Add(setDictFileButton)
        vbox.Add(hbox7, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox8= wx.BoxSizer(wx.HORIZONTAL)
        self.StartConnectButton= wx.Button(self, label="Start/Connect Button")
        hbox8.Add(self.StartConnectButton)
        vbox.Add(hbox8, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox9= wx.BoxSizer(wx.HORIZONTAL)
        BackToMainMenuButton= wx.Button(self, label="Back To Main Menu")
        hbox9.Add(BackToMainMenuButton)
        CloseButton= wx.Button(self, label="Close")
        hbox9.Add(CloseButton, flag=wx.LEFT, border=5)
        vbox.Add(hbox9, flag=wx.ALIGN_CENTER|wx.RIGHT, border=10)

        self.SetSizer(vbox)

        #Bind the buttons to events
        inputHashButton.Bind(wx.EVT_BUTTON, parent.setDictionaryHashToBeCracked)
        generateHashButton.Bind(wx.EVT_BUTTON, parent.generateHashDialogDic)
        setDictFileButton.Bind(wx.EVT_BUTTON, parent.selectDictFile)
        self.StartConnectButton.Bind(wx.EVT_BUTTON, parent.startDictionaryCrack)
        BackToMainMenuButton.Bind(wx.EVT_BUTTON, parent.switchFromPanel3ToPanel1)
        CloseButton.Bind(wx.EVT_BUTTON, parent.OnClose)

class PanelFour(wx.Panel):            #==================Brute Force Cracking method Settings==================
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        listOfAlgorithms= ['MD5', 'SHA1', 'SHA224', 'SHA256', 'SHA512']
        listOfAlphabets= ['All', 'ASCII_Uppercase', 'ASCII_Lowercase', 'Digits', 'Special_Symbols']
        #TODO if large number is insered, the button covers it up

        vbox= wx.BoxSizer(wx.VERTICAL)

        hbox1= wx.BoxSizer(wx.HORIZONTAL)
        screenHeader= wx.StaticText(self, label="Brute Force Cracking Method Settings")
        hbox1.Add(screenHeader)
        vbox.Add(hbox1, flag=wx.TOP|wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox2= wx.BoxSizer(wx.HORIZONTAL)
        self.currentMode= wx.StaticText(self, label="Current Mode: Not Specified")
        hbox2.Add(self.currentMode)
        vbox.Add(hbox2, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox3= wx.BoxSizer(wx.HORIZONTAL)
        self.selectedAlgorithmHeader= wx.StaticText(self, label="Select Algorithm:")
        hbox3.Add(self.selectedAlgorithmHeader)
        self.selectedAlgorithm= wx.ComboBox(self, choices=listOfAlgorithms)
        hbox3.Add(self.selectedAlgorithm, flag=wx.LEFT, border=5)
        vbox.Add(hbox3, flag=wx.ALIGN_CENTER|wx.RIGHT, border=10)

        vbox.Add((-1,10))

        hbox4= wx.BoxSizer(wx.HORIZONTAL)
        self.inputHashHeader= wx.StaticText(self, label="Hash To Be Cracked: No Hash has been Input")
        hbox4.Add(self.inputHashHeader)
        vbox.Add(hbox4, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox5= wx.BoxSizer(wx.HORIZONTAL)
        inputHashButton= wx.Button(self, label="Set Hash To Be Cracked")
        hbox5.Add(inputHashButton)
        generateHashButton= wx.Button(self, label="Generate Hash Code")
        hbox5.Add(generateHashButton, flag=wx.LEFT, border=5)
        vbox.Add(hbox5, flag=wx.ALIGN_CENTER|wx.RIGHT, border=10)

        vbox.Add((-1,10))

        hbox6= wx.BoxSizer(wx.HORIZONTAL)
        self.minKeyLengthHeader= wx.StaticText(self, label="Min Key Length: 5")
        hbox6.Add(self.minKeyLengthHeader)
        changeMinKeyLengthButton= wx.Button(self, label="Set Min Key Length")
        hbox6.Add(changeMinKeyLengthButton, flag=wx.LEFT, border=5)
        vbox.Add(hbox6, flag=wx.ALIGN_CENTER|wx.RIGHT, border=10)

        vbox.Add((-1,10))

        hbox7= wx.BoxSizer(wx.HORIZONTAL)
        self.maxKeyLengthHeader= wx.StaticText(self, label="Max Key Length: 15")
        hbox7.Add(self.maxKeyLengthHeader)
        changeMaxKeyLengthButton= wx.Button(self, label="Set Max Key Length")
        hbox7.Add(changeMaxKeyLengthButton, flag=wx.LEFT, border=5)
        vbox.Add(hbox7, flag=wx.ALIGN_CENTER|wx.RIGHT, border=10)

        vbox.Add((-1,10))

        hbox8= wx.BoxSizer(wx.HORIZONTAL)
        self.selectedAlphabetHeader= wx.StaticText(self, label="Selected Alphabet: ")
        hbox8.Add(self.selectedAlphabetHeader)
        self.selectedAlphabet= wx.ComboBox(self, choices=listOfAlphabets)
        hbox8.Add(self.selectedAlphabet, flag=wx.LEFT, border=5)
        vbox.Add(hbox8, flag=wx.ALIGN_CENTER|wx.RIGHT, border=10)


        vbox.Add((-1,10))

        hbox9= wx.BoxSizer(wx.HORIZONTAL)
        self.StartConnectButton= wx.Button(self, label="Start/Connect Button")
        hbox9.Add(self.StartConnectButton)
        vbox.Add(hbox9, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox10= wx.BoxSizer(wx.HORIZONTAL)
        BackToMainMenuButton= wx.Button(self, label="Back To Main Menu")
        hbox10.Add(BackToMainMenuButton)
        CloseButton= wx.Button(self, label="Close")
        hbox10.Add(CloseButton, flag=wx.LEFT, border=5)
        vbox.Add(hbox10, flag=wx.ALIGN_CENTER|wx.RIGHT, border=10)

        self.SetSizer(vbox)

        #Bind the buttons to events
        inputHashButton.Bind(wx.EVT_BUTTON, parent.setBruteForceHashToBeCracked)
        generateHashButton.Bind(wx.EVT_BUTTON, parent.generateHashDialogBF)
        changeMinKeyLengthButton.Bind(wx.EVT_BUTTON, parent.setBFMinKeyLength)
        changeMaxKeyLengthButton.Bind(wx.EVT_BUTTON, parent.setBFMaxKeyLength)
        self.StartConnectButton.Bind(wx.EVT_BUTTON, parent.startBruteForceCrack)
        BackToMainMenuButton.Bind(wx.EVT_BUTTON, parent.switchFromPanel4ToPanel1)
        CloseButton.Bind(wx.EVT_BUTTON, parent.OnClose)

class PanelFive(wx.Panel):                 #====================Rainbow Table Mode Select=========================
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)

        vbox= wx.BoxSizer(wx.VERTICAL)

        hbox1= wx.BoxSizer(wx.HORIZONTAL)
        screenHeader= wx.StaticText(self, label="Rainbow Table Mode Select")
        hbox1.Add(screenHeader)
        vbox.Add(hbox1, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox2= wx.BoxSizer(wx.HORIZONTAL)
        self.currentMode= wx.StaticText(self, label="Current Mode: Not Specified")
        hbox2.Add(self.currentMode)
        vbox.Add(hbox2, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox3= wx.BoxSizer(wx.HORIZONTAL)
        crackRainbowTableButton= wx.Button(self, label="Crack Using Rainbow Table")
        hbox3.Add(crackRainbowTableButton)
        vbox.Add(hbox3, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox4= wx.BoxSizer(wx.HORIZONTAL)
        makeRainbowTableButton= wx.Button(self, label="Rainbow Table Maker")
        hbox4.Add(makeRainbowTableButton)
        vbox.Add(hbox4, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox5= wx.BoxSizer(wx.HORIZONTAL)
        BackToMainMenuButton= wx.Button(self, label="Back To Main Menu")
        hbox5.Add(BackToMainMenuButton)
        CloseButton= wx.Button(self, label="Close")
        hbox5.Add(CloseButton, flag=wx.LEFT, border=5)
        vbox.Add(hbox5, flag=wx.ALIGN_CENTER|wx.RIGHT, border=10)

        self.SetSizer(vbox)

        #Bind the buttons to events
        crackRainbowTableButton.Bind(wx.EVT_BUTTON, parent.switchFromPanel5ToPanel11)
        makeRainbowTableButton.Bind(wx.EVT_BUTTON, parent.switchFromPanel5ToPanel12)
        BackToMainMenuButton.Bind(wx.EVT_BUTTON, parent.switchFromPanel5ToPanel1)
        CloseButton.Bind(wx.EVT_BUTTON, parent.OnClose)

class PanelSix(wx.Panel):                  #====================Select Node Type Screen============================
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)

        vbox= wx.BoxSizer(wx.VERTICAL)

        hbox1= wx.BoxSizer(wx.HORIZONTAL)
        screenHeader= wx.StaticText(self, label="Select Node Type")
        hbox1.Add(screenHeader)
        vbox.Add(hbox1, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox2=wx.BoxSizer(wx.HORIZONTAL)
        NetworkServerButton= wx.Button(self, label="Network Server")
        hbox2.Add(NetworkServerButton)
        vbox.Add(hbox2, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox3=wx.BoxSizer(wx.HORIZONTAL)
        NetworkClientButton= wx.Button(self, label="Network Client")
        hbox3.Add(NetworkClientButton)
        vbox.Add(hbox3, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox4=wx.BoxSizer(wx.HORIZONTAL)
        BackToMainMenuButton= wx.Button(self, label="Back To Main Menu")
        hbox4.Add(BackToMainMenuButton)
        CloseButton= wx.Button(self, label="Close")
        hbox4.Add(CloseButton, flag=wx.LEFT, border=5)
        vbox.Add(hbox4, flag=wx.ALIGN_CENTER|wx.RIGHT, border=10)

        self.SetSizer(vbox)

        #Bind the buttons to events
        NetworkServerButton.Bind(wx.EVT_BUTTON, parent.onNetworkModeButtonClick)
        NetworkClientButton.Bind(wx.EVT_BUTTON, parent.switchFromPanel6ToPanel7)
        BackToMainMenuButton.Bind(wx.EVT_BUTTON, parent.switchFromPanel6ToPanel1)
        CloseButton.Bind(wx.EVT_BUTTON, parent.OnClose)

class PanelSeven(wx.Panel):          #=============================Network Client Main Screen=======================
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)

        vbox= wx.BoxSizer(wx.VERTICAL)

        hbox1= wx.BoxSizer(wx.HORIZONTAL)
        screenHeader= wx.StaticText(self, label="Network Client Main Screen")
        hbox1.Add(screenHeader)
        vbox.Add(hbox1, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox2=wx.BoxSizer(wx.HORIZONTAL)
        self.serverIPAddress= wx.StaticText(self, label="Server's IP Address: No IP Address Has been Input Yet")
        hbox2.Add(self.serverIPAddress)
        vbox.Add(hbox2, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox3=wx.BoxSizer(wx.HORIZONTAL)
        InputServerIPButton= wx.Button(self, label="Input the Server IP")
        hbox3.Add(InputServerIPButton)
        vbox.Add(hbox3, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox4=wx.BoxSizer(wx.HORIZONTAL)
        ConnectToServerButton= wx.Button(self, label="Connect To The Server")
        hbox4.Add(ConnectToServerButton)
        vbox.Add(hbox4, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox5=wx.BoxSizer(wx.HORIZONTAL)
        BackToMainMenuButton= wx.Button(self, label="Back To Main Menu")
        hbox5.Add(BackToMainMenuButton)
        CloseButton= wx.Button(self, label="Close")
        hbox5.Add(CloseButton, flag=wx.LEFT, border=5)
        vbox.Add(hbox5, flag=wx.ALIGN_CENTER|wx.RIGHT, border=10)

        self.SetSizer(vbox)

        #Bind the buttons to events
        InputServerIPButton.Bind(wx.EVT_BUTTON, parent.getIPFromUser)
        ConnectToServerButton.Bind(wx.EVT_BUTTON, parent.connectToServer)
        BackToMainMenuButton.Bind(wx.EVT_BUTTON, parent.switchFromPanel7ToPanel1)
        CloseButton.Bind(wx.EVT_BUTTON, parent.OnClose)

class PanelEight(wx.Panel):       #========================Network Client Status Screen===========================
    def __init__(self,parent):
        wx.Panel.__init__(self, parent)

        vbox= wx.BoxSizer(wx.VERTICAL)

        hbox1=wx.BoxSizer(wx.HORIZONTAL)
        screenHeader= wx.StaticText(self, label="Network Client Status Screen")
        hbox1.Add(screenHeader)
        vbox.Add(hbox1, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox2=wx.BoxSizer(wx.HORIZONTAL)
        self.clientIPAddress= wx.StaticText(self, label="Client IP Address: Not Specified")
        hbox2.Add(self.clientIPAddress)
        self.connectedToIP= wx.StaticText(self, label="Connected To: Not Connected to any Server")
        hbox2.Add(self.connectedToIP, flag=wx.LEFT, border=5)
        vbox.Add(hbox2, flag=wx.ALIGN_CENTER|wx.RIGHT, border=10)

        vbox.Add((-1,10))

        hbox3=wx.BoxSizer(wx.HORIZONTAL)
        self.currentStatus= wx.StaticText(self, label="Current Status: Running")
        hbox3.Add(self.currentStatus)
        vbox.Add(hbox3, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox4=wx.BoxSizer(wx.HORIZONTAL)
        disconnectClientButton= wx.Button(self, label="Disconnect From Server")
        hbox4.Add(disconnectClientButton)
        vbox.Add(hbox4, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox5=wx.BoxSizer(wx.HORIZONTAL)
        CloseButton= wx.Button(self, label="Close")
        hbox5.Add(CloseButton)
        vbox.Add(hbox5, flag=wx.CENTER, border=10)

        self.SetSizer(vbox)

        #Bind the buttons to events
        disconnectClientButton.Bind(wx.EVT_BUTTON, parent.disconnectClient)
        CloseButton.Bind(wx.EVT_BUTTON, parent.OnClose)

class PanelNine(wx.Panel):                     #================Network Server Status Screen======================
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        vbox= wx.BoxSizer(wx.VERTICAL)

        hbox1= wx.BoxSizer(wx.HORIZONTAL)
        screenHeader= wx.StaticText(self, label="Network Server Status Screen")
        hbox1.Add(screenHeader)
        vbox.Add(hbox1, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox2=wx.BoxSizer(wx.HORIZONTAL)
        self.currentCrackingMode= wx.StaticText(self, label="Cracking Mode: Not Specified")
        hbox2.Add(self.currentCrackingMode)
        vbox.Add(hbox2, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox3=wx.BoxSizer(wx.HORIZONTAL)
        self.serverIPAddress= wx.StaticText(self, label="Server IP Address: Not Set Yet")
        hbox3.Add(self.serverIPAddress)
        vbox.Add(hbox3, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox4=wx.BoxSizer(wx.HORIZONTAL)
        self.currentStatus= wx.StaticText(self, label="Current Status: Running")
        hbox4.Add(self.currentStatus)
        vbox.Add(hbox4, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox5=wx.BoxSizer(wx.HORIZONTAL)
        forceQuitServerButton= wx.Button(self, label="Close the server")
        hbox5.Add(forceQuitServerButton)
        CloseButton= wx.Button(self, label="Close")
        hbox5.Add(CloseButton, flag=wx.LEFT, border=5)
        vbox.Add(hbox5, flag=wx.ALIGN_CENTER|wx.RIGHT, border=10)

        self.SetSizer(vbox)

        #Bind the buttons to events
        forceQuitServerButton.Bind(wx.EVT_BUTTON, parent.forceCloseServer)
        CloseButton.Bind(wx.EVT_BUTTON, parent.OnClose)

class PanelTen(wx.Panel):                          #====================Single Mode Status Screen==================
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        vbox= wx.BoxSizer(wx.VERTICAL)

        hbox1= wx.BoxSizer(wx.HORIZONTAL)
        screenHeader= wx.StaticText(self, label="Single Mode Status Screen")
        hbox1.Add(screenHeader)
        vbox.Add(hbox1, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox2=wx.BoxSizer(wx.HORIZONTAL)
        self.currentCrackingMode= wx.StaticText(self, label="Cracking Mode: Not Specified")
        hbox2.Add(self.currentCrackingMode)
        vbox.Add(hbox2, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox3= wx.BoxSizer(wx.HORIZONTAL)
        self.currentStatus= wx.StaticText(self, label="Current Status: Running")
        hbox3.Add(self.currentStatus)
        vbox.Add(hbox3, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox4= wx.BoxSizer(wx.HORIZONTAL)
        quitSearchButton= wx.Button(self, label="Quit Searching")
        hbox4.Add(quitSearchButton)
        CloseButton= wx.Button(self, label="Close")
        hbox4.Add(CloseButton, flag=wx.LEFT, border=5)
        vbox.Add(hbox4, flag=wx.ALIGN_CENTER|wx.RIGHT, border=10)

        self.SetSizer(vbox)

        #Bind the buttons to events
        quitSearchButton.Bind(wx.EVT_BUTTON, parent.ShowNotFinishedMessage1)
        CloseButton.Bind(wx.EVT_BUTTON, parent.OnClose)

class PanelEleven(wx.Panel):     #======================Rainbow Table Cracking Method Settings=========================
    def __init__ (self, parent):
        wx.Panel.__init__(self,parent)

        listOfAlgorithms= ['MD5', 'SHA1', 'SHA224', 'SHA256', 'SHA512']

        vbox= wx.BoxSizer(wx.VERTICAL)

        hbox1=wx.BoxSizer(wx.HORIZONTAL)
        screenHeader= wx.StaticText(self, label="Rainbow Table Cracking Method Settings")
        hbox1.Add(screenHeader)
        vbox.Add(hbox1, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox2=wx.BoxSizer(wx.HORIZONTAL)
        self.currentMode= wx.StaticText(self, label="Current Mode: Not Specified")
        hbox2.Add(self.currentMode)
        vbox.Add(hbox2, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox9=wx.BoxSizer(wx.HORIZONTAL)
        selectedAlgorithmHeader= wx.StaticText(self, label="Selected Algorithm: ")
        hbox9.Add(selectedAlgorithmHeader)
        self.selectedAlgorithm= wx.ComboBox(self, choices=listOfAlgorithms)
        hbox9.Add(self.selectedAlgorithm, flag=wx.LEFT, border=5)
        vbox.Add(hbox9, flag=wx.ALIGN_CENTER|wx.RIGHT, border=10)

        vbox.Add((-1,10))

        hbox3=wx.BoxSizer(wx.HORIZONTAL)
        self.selectedFileHeader= wx.StaticText(self, label="Selected Rainbow Table File: No File has been Selected")
        hbox3.Add(self.selectedFileHeader)
        vbox.Add(hbox3, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox4=wx.BoxSizer(wx.HORIZONTAL)
        selectFileButton= wx.Button(self, label="Select File")
        hbox4.Add(selectFileButton)
        vbox.Add(hbox4, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox5= wx.BoxSizer(wx.HORIZONTAL)
        self.hashToBeCrackedHeader= wx.StaticText(self, label="Hash to be cracked: No Hash has been entered")
        hbox5.Add(self.hashToBeCrackedHeader)
        vbox.Add(hbox5, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox6=wx.BoxSizer(wx.HORIZONTAL)
        setHashCodeButton= wx.Button(self, label="Set Hash To Be Cracked")
        hbox6.Add(setHashCodeButton)
        generateHashButton= wx.Button(self, label="Generate Hash Code")
        hbox6.Add(generateHashButton, flag=wx.LEFT, border=5)
        vbox.Add(hbox6, flag=wx.ALIGN_CENTER|wx.RIGHT, border=10)

        vbox.Add((-1,10))

        hbox7=wx.BoxSizer(wx.HORIZONTAL)
        self.StartConnectButton= wx.Button(self, label="Start/Connect Button")
        hbox7.Add(self.StartConnectButton)
        vbox.Add(hbox7, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox8=wx.BoxSizer(wx.HORIZONTAL)
        quitSearchButton= wx.Button(self, label="Quit Searching")
        hbox8.Add(quitSearchButton)
        CloseButton= wx.Button(self, label="Close")
        hbox8.Add(CloseButton, flag=wx.LEFT, border=5)
        vbox.Add(hbox8, flag=wx.ALIGN_CENTER|wx.RIGHT, border=10)

        self.SetSizer(vbox)

        #bind the buttons to events
        selectFileButton.Bind(wx.EVT_BUTTON, parent.selectRUFileSelect)
        setHashCodeButton.Bind(wx.EVT_BUTTON, parent.setRUHashToBeCracked)
        generateHashButton.Bind(wx.EVT_BUTTON, parent.generateHashDialogRT)
        self.StartConnectButton.Bind(wx.EVT_BUTTON, parent.startRainbowTableCrack)
        quitSearchButton.Bind(wx.EVT_BUTTON, parent.switchFromPanel11ToPanel1)
        CloseButton.Bind(wx.EVT_BUTTON, parent.OnClose)

class PanelTwelve(wx.Panel):              #=========================Rainbow Table Maker===========================
    def __init__ (self,parent):
        wx.Panel.__init__(self, parent)

        listOfAlgorithms= ['MD5', 'SHA1', 'SHA224', 'SHA256', 'SHA512']
        listOfAlphabets= ['All', 'ASCII_Uppercase', 'ASCII_Lowercase', 'Digits', 'Special_Symbols']

        vbox= wx.BoxSizer(wx.VERTICAL)

        hbox1=wx.BoxSizer(wx.HORIZONTAL)
        screenHeader= wx.StaticText(self, label="Rainbow Table Maker")
        hbox1.Add(screenHeader)
        vbox.Add(hbox1, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox2=wx.BoxSizer(wx.HORIZONTAL)
        self.currentMode= wx.StaticText(self, label="Current Mode: Not Specified")
        hbox2.Add(self.currentMode)
        vbox.Add(hbox2, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox3=wx.BoxSizer(wx.HORIZONTAL)
        self.selectedAlgorithmHeader= wx.StaticText(self, label="Select Algorithm: ")
        hbox3.Add(self.selectedAlgorithmHeader)
        self.selectedAlgorithm= wx.ComboBox(self, choices=listOfAlgorithms, style=wx.CB_READONLY)
        hbox3.Add(self.selectedAlgorithm, flag=wx.LEFT, border=5)
        vbox.Add(hbox3, flag=wx.ALIGN_CENTER|wx.RIGHT, border=10)

        vbox.Add((-1,10))

        hbox4=wx.BoxSizer(wx.HORIZONTAL)
        self.keyLengthHeader= wx.StaticText(self, label="Key Length: 10")
        hbox4.Add(self.keyLengthHeader)
        changeKeyLengthButton= wx.Button(self, label="Set Key Length")
        hbox4.Add(changeKeyLengthButton, flag=wx.LEFT, border=5)
        vbox.Add(hbox4, flag=wx.ALIGN_CENTER|wx.RIGHT, border=10)

        vbox.Add((-1,10))

        hbox5=wx.BoxSizer(wx.HORIZONTAL)
        selectAlphabetHeader= wx.StaticText(self, label="Select Alphabet")
        hbox5.Add(selectAlphabetHeader)
        self.selectedAlphabet= wx.ComboBox(self, choices=listOfAlphabets, style=wx.CB_READONLY)
        hbox5.Add(self.selectedAlphabet, flag=wx.LEFT, border=5)
        vbox.Add(hbox5, flag=wx.ALIGN_CENTER|wx.RIGHT, border=10)

        vbox.Add((-1,10))

        hbox6=wx.BoxSizer(wx.HORIZONTAL)
        self.chainLengthHeader= wx.StaticText(self, label="Table Chain Length: 1000")
        hbox6.Add(self.chainLengthHeader)
        changeChainLengthButton= wx.Button(self, label="Set Table Chain Length")
        hbox6.Add(changeChainLengthButton, flag=wx.LEFT, border=5)
        vbox.Add(hbox6, flag=wx.ALIGN_CENTER|wx.RIGHT, border=10)

        vbox.Add((-1,10))

        hbox7=wx.BoxSizer(wx.HORIZONTAL)
        self.numOfRowsHeader= wx.StaticText(self, label="Number of Rows: 10000")
        hbox7.Add(self.numOfRowsHeader)
        setNumOfRowsButton= wx.Button(self, label="Set Number Of Rows")
        hbox7.Add(setNumOfRowsButton, flag=wx.LEFT, border=5)
        vbox.Add(hbox7, flag=wx.ALIGN_CENTER|wx.RIGHT, border=10)

        vbox.Add((-1,10))

        hbox8=wx.BoxSizer(wx.HORIZONTAL)
        self.fileNameHeader= wx.StaticText(self, label="Save Rainbow Table File As: myRainbowTable.txt")
        hbox8.Add(self.fileNameHeader)
        vbox.Add(hbox8, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox9=wx.BoxSizer(wx.HORIZONTAL)
        changeFileNameButton= wx.Button(self, label="Change Saved File Name")
        hbox9.Add(changeFileNameButton)
        vbox.Add(hbox9, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox10=wx.BoxSizer(wx.HORIZONTAL)
        self.startConnectButton= wx.Button(self, label="Start/Connect Button")
        hbox10.Add(self.startConnectButton)
        vbox.Add(hbox10, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox11=wx.BoxSizer(wx.HORIZONTAL)
        backToMainMenuButton= wx.Button(self, label="Back to Main Menu")
        hbox11.Add(backToMainMenuButton)
        CloseButton= wx.Button(self, label="Close")
        hbox11.Add(CloseButton, flag=wx.LEFT, border=5)
        vbox.Add(hbox11, flag=wx.ALIGN_CENTER|wx.RIGHT, border=10)

        self.SetSizer(vbox)

        #bind the buttons to events
        changeKeyLengthButton.Bind(wx.EVT_BUTTON, parent.setRMKeyLength)
        changeChainLengthButton.Bind(wx.EVT_BUTTON, parent.setRMChainLength)
        setNumOfRowsButton.Bind(wx.EVT_BUTTON, parent.setRMNumOfRows)
        changeFileNameButton.Bind(wx.EVT_BUTTON, parent.setRMFileName)
        self.startConnectButton.Bind(wx.EVT_BUTTON, parent.startRainbowTableCreationSession)
        backToMainMenuButton.Bind(wx.EVT_BUTTON, parent.switchFromPanel12ToPanel1)
        CloseButton.Bind(wx.EVT_BUTTON, parent.OnClose)

class PanelThirteen(wx.Panel):              #====================About Us Page===================================
    def __init__(self,parent):
        wx.Panel.__init__(self,parent)

        vbox= wx.BoxSizer(wx.VERTICAL)

        hbox1= wx.BoxSizer(wx.HORIZONTAL)
        aboutUsHeader= wx.StaticText(self, label="About Us", style=wx.ALIGN_CENTER_HORIZONTAL)
        hbox1.Add(aboutUsHeader)
        vbox.Add(hbox1, flag=wx.CENTER|wx.TOP, border=10)

        vbox.Add((-1,10)) #add an extra spacer to give more room between the aboutUsHeader and the TextCtrl

        hbox2= wx.BoxSizer(wx.HORIZONTAL)
        textBox= wx.TextCtrl(self, style=wx.TE_MULTILINE|wx.CB_READONLY|wx.HSCROLL)
        hbox2.Add(textBox, proportion=1, flag=wx.EXPAND)
        vbox.Add(hbox2, proportion=1, flag=wx.LEFT|wx.RIGHT|wx.EXPAND, border=10)

        vbox.Add((-1, 25)) #add extra space between the textctrl and the buttons

        hbox3= wx.BoxSizer(wx.HORIZONTAL)
        backToMainMenuButton= wx.Button(self, label="Back To Main Menu")
        hbox3.Add(backToMainMenuButton)
        closeButton= wx.Button(self, label="Close")
        hbox3.Add(closeButton, flag=wx.LEFT|wx.BOTTOM, border=5)
        vbox.Add(hbox3, flag=wx.ALIGN_RIGHT|wx.RIGHT, border=10)

        self.SetSizer(vbox)

        #link the buttons up to events
        backToMainMenuButton.Bind(wx.EVT_BUTTON, parent.switchFromPanel13ToPanel1)
        closeButton.Bind(wx.EVT_BUTTON, parent.OnClose)

'''
        #define buttons and widgets
        aboutUsHeader= wx.StaticText(self, label="About Us", style=wx.ALIGN_CENTER_HORIZONTAL)
        aboutUsTextBody1= wx.StaticText(self, label="Authors: Chris Hamm, John Wright, Nick Baum, and Chris Bugg.", style=wx.ALIGN_CENTER_HORIZONTAL)
        aboutUsTextBody2= wx.StaticText(self, label=" ", style=wx.ALIGN_CENTER_HORIZONTAL)
        aboutUsTextBody3= wx.StaticText(self, label="Description: ", style=wx.ALIGN_CENTER_HORIZONTAL)
        aboutUsTextBody4= wx.StaticText(self, label=" ", style=wx.ALIGN_CENTER_HORIZONTAL)
        aboutUsTextBody5= wx.StaticText(self, label="Our project, Mighty Cracker, is a program designed to crack hashed", style=wx.ALIGN_CENTER_HORIZONTAL)
        aboutUsTextBody6= wx.StaticText(self, label="passwords. It is stand-alone, GUI, and can run on Mac 10+, Linux 14+,", style=wx.ALIGN_CENTER_HORIZONTAL)
        aboutUsTextBody7= wx.StaticText(self, label="and Windows 7+. It uses the power of multiprocessing to fully utilize", style=wx.ALIGN_CENTER_HORIZONTAL)
        aboutUsTextBody8= wx.StaticText(self, label="every computer available, and can utilize a LAN to distribute the", style=wx.ALIGN_CENTER_HORIZONTAL)
        aboutUsTextBody9= wx.StaticText(self, label="workload over up to 90 computers (nodes). For now, the algorithms", style=wx.ALIGN_CENTER_HORIZONTAL)
        aboutUsTextBody10= wx.StaticText(self, label="that it can utilize are: sha 224,sha 256, sha 512, sha 1, and md5,", style=wx.ALIGN_CENTER_HORIZONTAL)
        aboutUsTextBody11= wx.StaticText(self, label="which cover a fair amount of the common hashing algorithms used.", style=wx.ALIGN_CENTER_HORIZONTAL)
        aboutUsTextBody12= wx.StaticText(self, label=" ", style=wx.ALIGN_CENTER_HORIZONTAL)
        aboutUsTextBody13= wx.StaticText(self, label="We've implemented three common attack methods to find an original password.", style=wx.ALIGN_CENTER_HORIZONTAL)
        aboutUsTextBody14= wx.StaticText(self, label=" Dictionary takes a list of passwords, hashes them, and compares the", style=wx.ALIGN_CENTER_HORIZONTAL)
        aboutUsTextBody15= wx.StaticText(self, label="     hashes to the original (user inputted) hash to find a match.", style=wx.ALIGN_CENTER_HORIZONTAL)
        aboutUsTextBody16= wx.StaticText(self, label=" Brute Force will iterate through any combination (up to 16 ", style=wx.ALIGN_CENTER_HORIZONTAL)
        aboutUsTextBody17= wx.StaticText(self, label="     characters) of letters, numbers, and symbols to brute-force", style=wx.ALIGN_CENTER_HORIZONTAL)
        aboutUsTextBody18= wx.StaticText(self, label="     the password, returning an original if found.",style= wx.ALIGN_CENTER_HORIZONTAL)
        aboutUsTextBody19= wx.StaticText(self, label=" Rainbow Tables are pre-computed arrays of hashes, organized to to", style= wx.ALIGN_CENTER_HORIZONTAL)
        aboutUsTextBody20= wx.StaticText(self, label="     provide a time-cost trade-off. The creator creates tables to", style=wx.ALIGN_CENTER_HORIZONTAL)
        aboutUsTextBody21= wx.StaticText(self, label="     be used at a later time, and the user uses created tables.", style=wx.ALIGN_CENTER_HORIZONTAL)
        aboutUsTextBody22= wx.StaticText(self, label="     This gives one a huge advantage if you know what the password", style=wx.ALIGN_CENTER_HORIZONTAL)
        aboutUsTextBody23= wx.StaticText(self, label="     will consist of ahead of time.", style=wx.ALIGN_CENTER_HORIZONTAL)
        aboutUsTextBody24= wx.StaticText(self, label=" ", style=wx.ALIGN_CENTER_HORIZONTAL)
        aboutUsTextBody25= wx.StaticText(self, label="These three methods can all be used on either a single computer", style=wx.ALIGN_CENTER_HORIZONTAL)
        aboutUsTextBody26= wx.StaticText(self, label="(single-user mode) or on a network of computers (similar to", style=wx.ALIGN_CENTER_HORIZONTAL)
        aboutUsTextBody27= wx.StaticText(self, label="a Beowulf cluster). When using on headless systems, the program", style=wx.ALIGN_CENTER_HORIZONTAL)
        aboutUsTextBody28= wx.StaticText(self, label="can run in terminal (text-only) mode with a -c command.", style=wx.ALIGN_CENTER_HORIZONTAL)
        aboutUsTextBody29= wx.StaticText(self, label=" ", style=wx.ALIGN_CENTER_HORIZONTAL)
        aboutUsTextBody30= wx.StaticText(self, label="Of the distributed, multi-process, simple GUI approach this program", style=wx.ALIGN_CENTER_HORIZONTAL)
        aboutUsTextBody31= wx.StaticText(self, label="takes, it is potentially more powerful and more user-friendly than", style=wx.ALIGN_CENTER_HORIZONTAL)
        aboutUsTextBody32= wx.StaticText(self, label="most other hash cracking software out there today, making it more", style=wx.ALIGN_CENTER_HORIZONTAL)
        aboutUsTextBody33= wx.StaticText(self, label="accessible for more people. Simply open the executable and crack ", style=wx.ALIGN_CENTER_HORIZONTAL)
        aboutUsTextBody34= wx.StaticText(self, label="passwords.", style=wx.ALIGN_CENTER_HORIZONTAL)
        aboutUsTextBody35= wx.StaticText(self, label=" ", style=wx.ALIGN_CENTER_HORIZONTAL)
        aboutUsTextBody36= wx.StaticText(self, label="In the future we'd like to add on the ability to crack the LMT-family", style=wx.ALIGN_CENTER_HORIZONTAL)
        aboutUsTextBody37= wx.StaticText(self, label="of hashes (Windows) as well as add in GPU support for additional power.", style=wx.ALIGN_CENTER_HORIZONTAL)
        aboutUsTextBody38= wx.StaticText(self, label=" ", style=wx.ALIGN_CENTER_HORIZONTAL)
        backToMainMenuButton= wx.Button(self, label="Back To Main Menu", style=wx.ALIGN_CENTER_HORIZONTAL)
        CloseButton= wx.Button(self, label="Close", style=wx.ALIGN_CENTER_HORIZONTAL)
'''
'''
        #add buttons to the grid
        gsizer.AddMany([(aboutUsHeader, 0, wx.ALIGN_CENTER, 9),
            (aboutUsTextBody1, 0, wx.ALIGN_CENTER, 9),
            (aboutUsTextBody2, 0, wx.ALIGN_CENTER, 9),
            (aboutUsTextBody3, 0, wx.ALIGN_CENTER, 9),
            (aboutUsTextBody4, 0, wx.ALIGN_CENTER, 9),
            (aboutUsTextBody5, 0, wx.ALIGN_CENTER, 9),
            (aboutUsTextBody6, 0, wx.ALIGN_CENTER, 9),
            (aboutUsTextBody7, 0, wx.ALIGN_CENTER, 9),
            (aboutUsTextBody8, 0, wx.ALIGN_CENTER, 9),
            (aboutUsTextBody9, 0, wx.ALIGN_CENTER, 9),
            (aboutUsTextBody10, 0, wx.ALIGN_CENTER, 9),
            (aboutUsTextBody11, 0, wx.ALIGN_CENTER, 9),
            (aboutUsTextBody12, 0, wx.ALIGN_CENTER, 9),
            (aboutUsTextBody13, 0, wx.ALIGN_CENTER, 9),
            (aboutUsTextBody14, 0, wx.ALIGN_CENTER, 9),
            (aboutUsTextBody15, 0, wx.ALIGN_CENTER, 9),
            (aboutUsTextBody16, 0, wx.ALIGN_CENTER, 9),
            (aboutUsTextBody17, 0, wx.ALIGN_CENTER, 9),
            (aboutUsTextBody18, 0, wx.ALIGN_CENTER, 9),
            (aboutUsTextBody19, 0, wx.ALIGN_CENTER, 9),
            (aboutUsTextBody20, 0, wx.ALIGN_CENTER, 9),
            (aboutUsTextBody21, 0, wx.ALIGN_CENTER, 9),
            (aboutUsTextBody22, 0, wx.ALIGN_CENTER, 9),
            (aboutUsTextBody23, 0, wx.ALIGN_CENTER, 9),
            (aboutUsTextBody24, 0, wx.ALIGN_CENTER, 9),
            (aboutUsTextBody25, 0, wx.ALIGN_CENTER, 9),
            (aboutUsTextBody26, 0, wx.ALIGN_CENTER, 9),
            (aboutUsTextBody27, 0, wx.ALIGN_CENTER, 9),
            (aboutUsTextBody28, 0, wx.ALIGN_CENTER, 9),
            (aboutUsTextBody29, 0, wx.ALIGN_CENTER, 9),
            (aboutUsTextBody30, 0, wx.ALIGN_CENTER, 9),
            (aboutUsTextBody31, 0, wx.ALIGN_CENTER, 9),
            (aboutUsTextBody32, 0, wx.ALIGN_CENTER, 9),
            (aboutUsTextBody33, 0, wx.ALIGN_CENTER, 9),
            (aboutUsTextBody34, 0, wx.ALIGN_CENTER, 9),
            (aboutUsTextBody35, 0, wx.ALIGN_CENTER, 9),
            (aboutUsTextBody36, 0, wx.ALIGN_CENTER, 9),
            (aboutUsTextBody37, 0, wx.ALIGN_CENTER, 9),
            (aboutUsTextBody38, 0, wx.ALIGN_CENTER, 9),
            (backToMainMenuButton, 0, wx.ALIGN_CENTER, 9),
            (CloseButton, 0, wx.ALIGN_CENTER, 9)])
        #TODO text and buttons are still offscreen in linux
'''

class myFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "Mighty Cracker", size=(1024, 768))

        self.panel_one= PanelOne(self)
        self.panel_two= PanelTwo(self)
        self.panel_three= PanelThree(self)
        self.panel_four= PanelFour(self)
        self.panel_five= PanelFive(self)
        self.panel_six= PanelSix(self)
        self.panel_seven= PanelSeven(self)
        self.panel_eight= PanelEight(self)
        self.panel_nine= PanelNine(self)
        self.panel_ten= PanelTen(self)
        self.panel_eleven= PanelEleven(self)
        self.panel_twelve= PanelTwelve(self)
        self.panel_thirteen= PanelThirteen(self)
        self.panel_two.Hide()
        self.panel_three.Hide()
        self.panel_four.Hide()
        self.panel_five.Hide()
        self.panel_six.Hide()
        self.panel_seven.Hide()
        self.panel_eight.Hide()
        self.panel_nine.Hide()
        self.panel_ten.Hide()
        self.panel_eleven.Hide()
        self.panel_twelve.Hide()
        self.panel_thirteen.Hide()

        self.sizer= wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.panel_one, 1, wx.EXPAND)
        self.sizer.Add(self.panel_two, 1, wx.EXPAND)
        self.sizer.Add(self.panel_three, 1, wx.EXPAND)
        self.sizer.Add(self.panel_four, 1, wx.EXPAND)
        self.sizer.Add(self.panel_five, 1, wx.EXPAND)
        self.sizer.Add(self.panel_six, 1, wx.EXPAND)
        self.sizer.Add(self.panel_seven, 1, wx.EXPAND)
        self.sizer.Add(self.panel_eight, 1, wx.EXPAND)
        self.sizer.Add(self.panel_nine, 1, wx.EXPAND)
        self.sizer.Add(self.panel_ten, 1, wx.EXPAND)
        self.sizer.Add(self.panel_eleven, 1, wx.EXPAND)
        self.sizer.Add(self.panel_twelve, 1, wx.EXPAND)
        self.sizer.Add(self.panel_thirteen, 1, wx.EXPAND)
        self.SetSizer(self.sizer)

        #update is an event intended to be set by server to let the UI know that the shared dictionary has been updated
        self.update = Event()
        self.update.clear()

        #shutdown is linked the the server/client shared shutdown command. setting this should should down server and client.
        self.shutdown = Event()
        self.shutdown.clear()


    #---------switch from Panel 1
    def switchFromPanel1ToPanel2(self):
        self.SetTitle("Mighty Cracker: Select Cracking Method")
        self.panel_one.Hide()
        self.panel_two.Show()
        self.Layout()

    def switchFromPanel1ToPanel6(self, event):
        self.SetTitle("Mighty Cracker: Choose Node Type")
        self.panel_one.Hide()
        self.panel_six.Show()
        self.Layout()

    def switchFromPanel1ToPanel13(self, event):
        self.SetTitle("Mighty Cracker: About Us")
        self.panel_one.Hide()
        self.panel_thirteen.Show()
        self.Layout()
    #---------end of switch from panel 1

    #--------switch from panel 2
    def switchFromPanel2ToPanel1(self, event):
        self.SetTitle("Mighty Cracker")
        self.panel_two.Hide()
        self.panel_one.Show()
        self.Layout()

    def switchFromPanel2ToPanel3(self, event):
        self.SetTitle("Mighty Cracker: Dictionary Cracking Method Settings")
        tempCurrentMode= self.panel_two.currentMode.GetLabelText()
        self.panel_three.currentMode.SetLabel(tempCurrentMode)
        self.panel_two.Hide()
        self.panel_three.Show()
        self.Layout()

    def switchFromPanel2ToPanel4(self, event):
        self.SetTitle("Mighty Cracker: Brute Force Cracking Method Settings")
        tempCurrentMode= self.panel_two.currentMode.GetLabelText()
        self.panel_four.currentMode.SetLabel(tempCurrentMode)
        self.panel_two.Hide()
        self.panel_four.Show()
        self.Layout()

    def switchFromPanel2ToPanel5(self, event):
        self.SetTitle("Mighty Cracker: Rainbow Table Cracking Method Settings")
        tempCurrentMode= self.panel_two.currentMode.GetLabelText()
        self.panel_five.currentMode.SetLabel(tempCurrentMode)
        self.panel_two.Hide()
        self.panel_five.Show()
        self.Layout()
    #--------end of switch from panel 2

    #--------switch from panel 3
    def switchFromPanel3ToPanel1(self, event):
        self.SetTitle("Mighty Cracker")
        self.panel_three.Hide()
        self.panel_one.Show()
        self.Layout()

    def switchFromPanel3ToPanel9(self):
        self.SetTitle("Mighty Cracker: Network Server Status Screen")
        self.panel_nine.currentCrackingMode.SetLabel("Cracking Mode: Dictionary")
        tempIP= self.get_ip()
        self.panel_nine.serverIPAddress.SetLabel("Server IP Address: "+str(tempIP))
        self.panel_three.Hide()
        self.panel_nine.Show()
        self.Layout()

    def switchFromPanel3ToPanel10(self):
        self.SetTitle("Mighty Cracker: Single Mode Status Screen")
        self.panel_ten.currentCrackingMode.SetLabel("Cracking Mode: Dictionary")
        self.panel_three.Hide()
        self.panel_ten.Show()
        self.Layout()
    #----------end switch from panel 3

    #--------switch from panel 4
    def switchFromPanel4ToPanel1(self, event):
        self.SetTitle("Mighty Cracker")
        self.panel_four.Hide()
        self.panel_one.Show()
        self.Layout()

    def switchFromPanel4ToPanel9(self):
        self.SetTitle("Mighty Cracker: Network Server Status Screen")
        self.panel_nine.currentCrackingMode.SetLabel("Cracking Mode: Brute-Force")
        tempIP= self.get_ip()
        self.panel_nine.serverIPAddress.SetLabel("Server IP Address: "+str(tempIP))
        self.panel_four.Hide()
        self.panel_nine.Show()
        self.Layout()

    def switchFromPanel4ToPanel10(self):
        self.SetTitle("Mighty Cracker: Single Mode Status Screen")
        self.panel_ten.currentCrackingMode.SetLabel("Cracking Mode: Brute-Force")
        self.panel_four.Hide()
        self.panel_ten.Show()
        self.Layout()
    #---------end switch from panel 4

    #----------switch from panel 5
    def switchFromPanel5ToPanel1(self, event):
        self.SetTitle("Mighty Cracker")
        self.panel_five.Hide()
        self.panel_one.Show()
        self.Layout()

    def switchFromPanel5ToPanel11(self, event):
        self.SetTitle("Mighty Cracker: Rainbow Table Cracking Method")
        tempCurrentMode= self.panel_five.currentMode.GetLabelText()
        self.panel_eleven.currentMode.SetLabel(tempCurrentMode)
        self.panel_five.Hide()
        self.panel_eleven.Show()
        self.Layout()

    def switchFromPanel5ToPanel12(self, event):
        self.SetTitle("Mighty Cracker: Rainbow Table Maker")
        tempCurrentMode= self.panel_five.currentMode.GetLabelText()
        self.panel_twelve.currentMode.SetLabel(tempCurrentMode)
        self.panel_five.Hide()
        self.panel_twelve.Show()
        self.Layout()
    #---------end of switch from panel 5

    #------------switch from panel 6
    def switchFromPanel6ToPanel1(self, event):
        self.SetTitle("Mighty Cracker")
        self.panel_six.Hide()
        self.panel_one.Show()
        self.Layout()

    def switchFromPanel6ToPanel2(self):
        self.SetTitle("Mighty Cracker: Select Cracking Method")
        self.panel_six.Hide()
        self.panel_two.Show()
        self.Layout()

    def switchFromPanel6ToPanel7(self, event):
        self.SetTitle("Mighty Cracker: Network Client")
        self.panel_six.Hide()
        self.panel_seven.Show()
        self.Layout()
    #-----------end of switch from panel 6

    #------------switch from panel 7
    def switchFromPanel7ToPanel1(self, event):
        self.SetTitle("Mighty Cracker")
        self.panel_seven.Hide()
        self.panel_one.Show()
        self.Layout()

    def switchFromPanel7ToPanel8(self):
        self.SetTitle("Mighty Cracker: Client Status")
        tempIP= self.get_ip()
        self.panel_eight.clientIPAddress.SetLabel("Client IP Address: "+str(tempIP))
        self.panel_seven.Hide()
        self.panel_eight.Show()
        self.Layout()
    #--------------end of switch from panel 7

    #---------switch from panel 8
    def switchFromPanel8ToPanel1(self):
        self.SetTitle("Mighty Cracker")
        self.panel_eight.Hide()
        self.panel_one.Show()
        self.Layout()
    #---------end of switch from panel 8

    #---------switch from panel 9
    def switchFromPanel9ToPanel1(self):
        self.SetTitle("Mighty Cracker")
        self.panel_nine.Hide()
        self.panel_one.Show()
        self.Layout()
    #-----------end of switch from panel 9

    #-----------switch from panel 10
    def switchFromPanel10ToPanel1(self):
        self.SetTitle("Mighty Cracker")
        self.panel_ten.Hide()
        self.panel_one.Show()
        self.Layout()
    #------------end of switch from panel 10

    #----------switch from panel 11
    def switchFromPanel11ToPanel1(self, event):
        self.SetTitle("Mighty Cracker")
        self.panel_eleven.Hide()
        self.panel_one.Show()
        self.Layout()

    def switchFromPanel11ToPanel9(self):
        self.SetTitle("Mighty Cracker: Network Server Status Screen")
        self.panel_nine.currentCrackingMode.SetLabel("Cracking Mode: Rainbow Table")
        tempIP= self.get_ip()
        self.panel_nine.serverIPAddress.SetLabel("Server IP Address: "+str(tempIP))
        self.panel_eleven.Hide()
        self.panel_nine.Show()
        self.Layout()

    def switchFromPanel11ToPanel10(self):
        self.SetTitle("Mighty Cracker: Single Mode Status Screen")
        self.panel_ten.currentCrackingMode.SetLabel("Cracking Mode: Rainbow Table")
        self.panel_eleven.Hide()
        self.panel_ten.Show()
        self.Layout()
    #-----------end of switch from panel 11

    #------------switch from panel 12
    def switchFromPanel12ToPanel1(self, event):
        self.SetTitle("Mighty Cracker")
        self.panel_twelve.Hide()
        self.panel_one.Show()
        self.Layout()

    def switchFromPanel12ToPanel9(self):
        self.SetTitle("Mighty Cracker: Network Server Status Screen")
        self.panel_nine.currentCrackingMode.SetLabel("Cracking Mode: Rainbow Table Maker")
        tempIP= self.get_ip()
        self.panel_nine.serverIPAddress.SetLabel("Server IP Address: "+str(tempIP))
        self.panel_twelve.Hide()
        self.panel_nine.Show()
        self.Layout()

    def switchFromPanel12ToPanel10(self):
        self.SetTitle("Mighty Cracker: Single Mode Status Screen")
        self.panel_ten.currentCrackingMode.SetLabel("Cracking Mode: Rainbow Table Maker")
        self.panel_twelve.Hide()
        self.panel_ten.Show()
        self.Layout()
    #-------------end of switch from panel 12

    #--------------switch from panel 13
    def switchFromPanel13ToPanel1(self, event):
        self.SetTitle("Mighty Cracker")
        self.panel_thirteen.Hide()
        self.panel_one.Show()
        self.Layout()
    #------------end of switch from panel 13


    #defined functions
    def ShowNotFinishedMessage1(self, event):
        dial= wx.MessageDialog(None, 'This function has not been completed yet', 'Notice:', wx.OK)
        dial.ShowModal()

    def getIPFromUser(self, event):
        dial = wx.TextEntryDialog(self, "What is the Server's IP Address?", "Input IP Address", "", style=wx.OK)
        dial.ShowModal()
        self.panel_seven.serverIPAddress.SetLabel("Server's IP Address: "+ str(dial.GetValue()))
        dial.Destroy()

    def setDictionaryHashToBeCracked(self, event):
        dial = wx.TextEntryDialog(self, "Input the Hash To Be Cracked", "Input Hash", "", style=wx.OK)
        dial.ShowModal()
        self.panel_three.inputHashHeader.SetLabel("Hash To Be Cracked: "+str(dial.GetValue()))
        dial.Destroy()

    def setBruteForceHashToBeCracked(self, event):
        dial = wx.TextEntryDialog(self, "Input the Hash To Be Cracked", "Input Hash", "", style=wx.OK)
        dial.ShowModal()
        self.panel_four.inputHashHeader.SetLabel("Hash To Be Cracked: "+str(dial.GetValue()))
        dial.Destroy()

    def selectDictFile(self, event):
        dial= wx.FileDialog(self, message="Choose a Dictionary File", defaultFile="",
                             style=wx.OPEN|wx.MULTIPLE|wx.CHANGE_DIR)
        if(dial.ShowModal() == wx.ID_OK):
            paths = dial.GetPath()
            self.panel_three.inputDictFileHeader.SetLabel("Selected Dictionary File: "+ str(paths))
        dial.Destroy()

    def OnClose(self, event):
        dial = wx.MessageBox('Are you sure you want to quit?', 'Exit?', wx.YES_NO|wx.NO_DEFAULT, self)
        if dial == wx.YES:
            self.shutdown.set()
            self.Close()

    def disconnectClient(self, event):
        dial= wx.MessageBox('Are you sure you want to disconnect from the server? Disconnecting before the search is finished could cause errors',
                            'Disconnect from Server?', wx.YES_NO|wx.NO_DEFAULT, self)
        if dial == wx.YES:
            self.NetworkClient.terminate()
            self.switchFromPanel8ToPanel1()

    def forceCloseServer(self, event):
        dial= wx.MessageBox('Are you sure you want to close the server? Closing the server will forcifully disconnect all clients.',
                            'Close the Server?', wx.YES_NO|wx.NO_DEFAULT, self)
        if(dial == wx.YES):
            self.NetworkServer.terminate()
            self.shutdown.set()
            self.switchFromPanel9ToPanel1()

    def setCurrentMode(self, inputText):
        self.CurrentMode= inputText

    def generateHashDialogDic(self, event):
        dial= wx.TextEntryDialog(self, "Input Key To Be Hashed", "Input Key To Be Hashed","", style=wx.OK)
        dial.ShowModal()
        inputKey= str(dial.GetValue())
        inputAlgorithm= self.panel_three.selectedAlgorithm.GetValue()
        generatedHash= str(hashlib.new(str(inputAlgorithm), inputKey).hexdigest())
        self.panel_three.inputHashHeader.SetLabel("Hash To Be Cracked: "+str(generatedHash))
        dial.Destroy()

    def generateHashDialogBF(self, event):
        dial= wx.TextEntryDialog(self, "Input Key To Be Hashed", "Input Key To Be Hashed","", style=wx.OK)
        dial.ShowModal()
        inputKey= str(dial.GetValue())
        inputAlgorithm= self.panel_four.selectedAlgorithm.GetValue()
        generatedHash= str(hashlib.new(str(inputAlgorithm), inputKey).hexdigest())
        self.panel_four.inputHashHeader.SetLabel("Hash To Be Cracked: "+str(generatedHash))
        dial.Destroy()

    def generateHashDialogRT(self, event):
        dial= wx.TextEntryDialog(self, "Input Key To Be Hashed", "Input Key To Be Hashed","", style=wx.OK)
        dial.ShowModal()
        inputKey= str(dial.GetValue())
        inputAlgorithm= self.panel_eleven.selectedAlgorithm.GetValue()
        generatedHash= str(hashlib.new(str(inputAlgorithm), inputKey).hexdigest())
        self.panel_eleven.hashToBeCrackedHeader.SetLabel("Hash To Be Cracked: "+str(generatedHash))
        dial.Destroy()

    def setBFMinKeyLength(self, event):
        dial = wx.TextEntryDialog(self, "Input the Min Key Length", "Input Min Key Length", "", style=wx.OK)
        dial.ShowModal()
        input= str(dial.GetValue())
        foundInvalidChar= False
        for i in range(0, len(input)):
            if input[i].isalpha():
                foundInvalidChar= True
        if(foundInvalidChar==True):
            dial2= wx.MessageDialog(None, "Illegal Alpha Character detected.\n"
                                          "Min Key Length Value was not set.", "Invalid Input", wx.OK)
            dial2.ShowModal()
        else:
            self.panel_four.minKeyLengthHeader.SetLabel("Min Key Length: "+str(input))
        dial.Destroy()

    def setBFMaxKeyLength(self, event):
        dial= wx.TextEntryDialog(self, "Input the Max Key Length", "Input Max Key Length","", style=wx.OK)
        dial.ShowModal()
        input= str(dial.GetValue())
        foundInvalidChar= False
        for i in range(0, len(input)):
            if input[i].isalpha():
                foundInvalidChar= True
        if(foundInvalidChar == True):
            dial2 = wx.MessageDialog(None, "Illegal Alpha Character detected.\n"
                                           "Max Key Length Value was not set.", "Invalid Input", wx.OK)
            dial2.ShowModal()
        else:
            self.panel_four.maxKeyLengthHeader.SetLabel("Max Key Length: "+str(input))
        dial.Destroy()

    def setRMKeyLength(self, event):
        dial= wx.TextEntryDialog(self, "Input New Key Length", "Input the new Key Length", "", style=wx.OK)
        dial.ShowModal()
        input = str(dial.GetValue())
        foundInvalidChar= False
        for i in range(0, len(input)):
            if input[i].isalpha():
                foundInvalidChar= True
        if(foundInvalidChar == True):
            dial2= wx.MessageDialog(None, "Illegal Alpha Character detected.\n"
                                          "Key Length was not set.", "Invalid Input", wx.OK)
            dial2.ShowModal()
        else:
            self.panel_twelve.keyLengthHeader.SetLabel("Key Length: "+str(input))
        dial.Destroy()

    def setRMChainLength(self, event):
        dial= wx.TextEntryDialog(self, "Input New Chain Length", "Input the new Chain Length", "", style=wx.OK)
        dial.ShowModal()
        input = str(dial.GetValue())
        foundInvalidChar= False
        for i in range(0, len(input)):
            if input[i].isalpha():
                foundInvalidChar= True
        if(foundInvalidChar == True):
            dial2= wx.MessageDialog(None, "Illegal Alpha Character detected.\n"
                                          "Chain Length was not set.", "Invalid Input", wx.OK)
            dial2.ShowModal()
        else:
            self.panel_twelve.chainLengthHeader.SetLabel("Table Chain Length: "+str(input))
        dial.Destroy()

    def setRMNumOfRows(self, event):
        dial= wx.TextEntryDialog(self, "Input New Number of Rows", "Input the new Number of Rows", "", style=wx.OK)
        dial.ShowModal()
        input = str(dial.GetValue())
        foundInvalidChar= False
        for i in range(0, len(input)):
            if input[i].isalpha():
                foundInvalidChar= True
        if(foundInvalidChar == True):
            dial2= wx.MessageDialog(None, "Illegal Alpha Character detected.\n"
                                          "Number of Rows was not set.", "Invalid Input", wx.OK)
            dial2.ShowModal()
        else:
            self.panel_twelve.numOfRowsHeader.SetLabel("Number of Rows: "+str(input))
        dial.Destroy()

    def setRMFileName(self,event):
        dial= wx.TextEntryDialog(self, "Input the name for this rainbow table file\n"
                                       "(The file extension will automatically be added)", "Enter in the new name", "", style=wx.OK)
        dial.ShowModal()
        #TODO add check to make sure there is no file extension in the input box
        #TODO ===================================check for illegal file name characters======================================
            #TODO illegal for windows CMD: /, \(backslash), ?, *, :, |, ", . (other than for file extension), <, >,
            #TODO illegal for OSX: /, :,
            #TODO illegal for Linux: /, .(as the first character), \0 (null terminator),
            #TODO special cases for Linux: \(backslash), ?,  *, |, <, >,
        #TODO =================================end of illegal file name characters==================================
        if((self.checkForValidFileNameLength(dial.GetValue()) is True) and (self.checkForIllegalFileNameChar(dial.GetValue()) is False)):
                self.panel_twelve.fileNameHeader.SetLabel("Save Rainbow Table File As: "+str(dial.GetValue())+".txt")
        else:
            dial2= wx.MessageDialog(None, "Illegal File Name Length. \n"
                                          "The new filename was not set.", "File Name is longer than 255 characters", wx.OK)
            dial2.ShowModal()
        dial.Destroy()

    def checkForValidFileNameLength(self, inputString):
        if(len(inputString) > 255):
            return False
        else:
            return True

    def selectRUFileSelect(self, event):
        import os
        fileDial= wx.FileDialog(None, "Select a rainbow table file", os.getcwd(), "", "All files (*.*)|*.*", wx.OPEN)
        if(fileDial.ShowModal() == wx.ID_OK):
            input= str(fileDial.GetPath())
            self.panel_eleven.selectedFileHeader.SetLabel("Selected Rainbow Table File: "+str(input))
        fileDial.Destroy()

    def setRUHashToBeCracked(self, event):
        dial= wx.TextEntryDialog(self, "Insert the Hash Code to be cracked", "Insert the Hash Code to be cracked", "", style=wx.OK)
        dial.ShowModal()
        self.panel_eleven.hashToBeCrackedHeader.SetLabel("Hash to be cracked: "+str(dial.GetValue()))
        dial.Destroy()

    def onSingleModeButtonClick(self, e):
        self.panel_two.currentMode.SetLabel("Current Mode: Single Mode")
        self.panel_three.StartConnectButton.SetLabel("Start Dictionary Crack")
        self.panel_four.StartConnectButton.SetLabel("Start Brute Force Crack")
        self.panel_eleven.StartConnectButton.SetLabel("Start Rainbow Crack")
        self.panel_twelve.startConnectButton.SetLabel("Make Rainbow Table")
        self.switchFromPanel1ToPanel2()

    def onNetworkModeButtonClick(self, e):
        self.panel_two.currentMode.SetLabel("Current Mode: Network Mode")
        self.panel_three.StartConnectButton.SetLabel("Start Hosting Dictionary Crack")
        self.panel_four.StartConnectButton.SetLabel("Start Hosting Brute Force Crack")
        self.panel_eleven.StartConnectButton.SetLabel("Start Hosting Rainbow Crack")
        self.panel_twelve.startConnectButton.SetLabel("Start Hosting a Rainbow Table Creation Session")
        self.switchFromPanel6ToPanel2()

    def connectToServer(self, event):
        tempServerIP= self.panel_seven.serverIPAddress.GetLabel()
        #TODO need error checking to make sure that the server ip has been entered
        #remove the prefix to th eip address
        serverIP=""
        for i in range(21, len(tempServerIP)):
            serverIP+= tempServerIP[i]
        print "GUI DEBUG: started Network Client"
        print "GUI DEBUG: server IP: '"+str(serverIP)+"'"
        self.NetworkClient= Process(target=Client, args=(serverIP,))
        self.NetworkClient.start()
        self.panel_eight.connectedToIP.SetLabel("Connected To: "+str(serverIP))
        self.switchFromPanel7ToPanel8()

    def startDictionaryCrack(self, event):
        crackingMethodSetting= "dic"
        tempAlgorithmSetting= str(self.panel_three.selectedAlgorithm.GetValue())
        algorithmSetting= tempAlgorithmSetting
        tempHashSetting= str(self.panel_three.inputHashHeader.GetLabel())
        hashSetting= ""
        for i in range(19, len(tempHashSetting)):
            hashSetting+= tempHashSetting[i]
        tempFileName= str(self.panel_three.inputDictFileHeader.GetLabel())
        FileName= ""
        for i in range(26, len(tempFileName)):
            FileName+= tempFileName[i]
        tempSingleSetting= str(self.panel_three.currentMode.GetLabel())
        tempSingleSetting2=""
        for i in range(14, len(tempSingleSetting)):
            tempSingleSetting2+= tempSingleSetting[i]
        singleSetting=""
        if(self.compareString(tempSingleSetting2, "Single Mode",0,0,len(tempSingleSetting2), len("Single Mode"))==True):
            singleSetting="True"
        else:
            singleSetting="False"
        crackingSettings= {"cracking method":crackingMethodSetting, "algorithm": algorithmSetting, "hash":hashSetting, "file name":FileName, "single": singleSetting}


        #shared variable array
        #[0]shared dictionary, [1]shutdown, [2]update
        listOfSharedVariables= []
        listOfSharedVariables.append(crackingSettings)
        listOfSharedVariables.append(self.shutdown)
        listOfSharedVariables.append(self.update)
        print "GUI DEBUG: Starting up Server Process"
        self.NetworkServer= Process(target=Server, args=(crackingSettings,listOfSharedVariables,))
        #print "GUI DEBUG: before process is started"
        self.NetworkServer.start()
        #print "GUI DEBUG: after process has started"
        if(singleSetting is 'False'):
            self.switchFromPanel3ToPanel9()
        else:
            self.switchFromPanel3ToPanel10()


    def startBruteForceCrack(self, event):
        crackingMethodSetting= "bf"
        tempAlgorithmSetting= str(self.panel_four.selectedAlgorithm.GetValue())
        algorithmSetting= tempAlgorithmSetting
        tempHashSetting= str(self.panel_four.inputHashHeader.GetLabel())
        hashSetting=""
        for i in range(19, len(tempHashSetting)):
            hashSetting+= tempHashSetting[i]
        tempMinKeyLength= str(self.panel_four.minKeyLengthHeader.GetLabel())
        minKeyLengthSetting=""
        for i in range(15, len(tempMinKeyLength)):
            minKeyLengthSetting+= tempMinKeyLength[i]
        finalMinKeyLengthSetting= int(minKeyLengthSetting)
        tempMaxKeyLength= str(self.panel_four.maxKeyLengthHeader.GetLabel())
        maxKeyLengthSetting=""
        for i in range(15, len(tempMaxKeyLength)):
            maxKeyLengthSetting+= tempMaxKeyLength[i]
        finalMaxKeyLengthSetting= int(maxKeyLengthSetting)
        tempAlphabetSetting= str(self.panel_four.selectedAlphabet.GetValue())
        alphabetSetting= tempAlphabetSetting
        tempSingleSetting= str(self.panel_four.currentMode.GetLabel())
        tempSingleSetting2=""
        for i in range(14, len(tempSingleSetting)):
            tempSingleSetting2+= tempSingleSetting[i]
        singleSetting=""
        if(self.compareString(tempSingleSetting2, "Single Mode",0,0,len(tempSingleSetting2), len("Single Mode"))==True):
            singleSetting="True"
        else:
            singleSetting="False"
        crackingSettings= {"cracking method":crackingMethodSetting, "algorithm":algorithmSetting, "hash":hashSetting, "min key length":finalMinKeyLengthSetting,
                           "max key length":finalMaxKeyLengthSetting, "alphabet":alphabetSetting, "single":singleSetting}

        #shared variable array
        #[0]shared dictionary, [1]shutdown, [2]update
        listOfSharedVariables= []
        listOfSharedVariables.append(crackingSettings)
        listOfSharedVariables.append(self.shutdown)
        listOfSharedVariables.append(self.update)
        self.NetworkServer= Process(target=Server, args=(crackingSettings,listOfSharedVariables,))
        self.NetworkServer.start()
        if(singleSetting is 'False'):
            self.switchFromPanel4ToPanel9()
        else:
            self.switchFromPanel4ToPanel10()

    def startRainbowTableCrack(self, event):
        crackingMethod= "rain"
        tempFileName= self.panel_eleven.selectedFileHeader.GetLabelText()
        #remove extra heading in from of the file path
        fileName= ""
        for i in range(28, len(tempFileName)):
            fileName+= str(tempFileName[i])
        tempHashToBeCracked= self.panel_eleven.hashToBeCrackedHeader.GetLabelText()
        #remove extra heading from the front of the hash code
        hashToBeCracked= ""
        for i in range(19, len(tempHashToBeCracked)):
            hashToBeCracked+= str(tempHashToBeCracked[i])
        tempSingleSetting= self.panel_eleven.currentMode.GetLabelText()
        #remove extra heading from current Mode
        tempSingleSetting2= ""
        for i in range (13, len(tempSingleSetting)):
            tempSingleSetting2+= str(tempSingleSetting[i])
        singleSetting = ""
        if(self.compareString(tempSingleSetting2, "Single Mode",0,0,len(tempSingleSetting2), len("Single Mode"))==True):
            singleSetting="True"
        else:
            singleSetting="False"
        crackingSettings= {"cracking method":crackingMethod, "file name":fileName, "hash":hashToBeCracked, "single":singleSetting}

        #shared variable array
        #[0]shared dictionary, [1]shutdown, [2]update
        listOfSharedVariables= []
        listOfSharedVariables.append(crackingSettings)
        listOfSharedVariables.append(self.shutdown)
        listOfSharedVariables.append(self.update)
        self.NetworkServer= Process(target=Server, args=(crackingSettings,listOfSharedVariables,))
        self.NetworkServer.start()
        if(singleSetting is 'False'):
            self.switchFromPanel11ToPanel9()
        else:
            self.switchFromPanel11ToPanel10()

    def startRainbowTableCreationSession(self, event):
        crackingMethod= "rainmaker"
        tempAlgorithmSetting= str(self.panel_twelve.selectedAlgorithm.GetValue())
        algorithmSetting= tempAlgorithmSetting
        tempKeyLengthSetting= self.panel_twelve.keyLengthHeader.GetLabelText()
        #remove extra header from string
        tempKeyLengthSetting2= ""
        for i in range(11, len(tempKeyLengthSetting)):
            tempKeyLengthSetting2+= tempKeyLengthSetting[i]
        keyLengthSetting= int(tempKeyLengthSetting2)
        tempAlphabetSettings= str(self.panel_twelve.selectedAlphabet.GetValue())
        alphabetSetting= tempAlphabetSettings
        tempChainLengthSetting= str(self.panel_twelve.chainLengthHeader.GetLabelText())
        #remove extra header info from the strings
        tempChainLengthSetting2= ""
        for i in range(19, len(tempChainLengthSetting)):
            tempChainLengthSetting2 += tempChainLengthSetting[i]
        chainLengthSetting= int(tempChainLengthSetting2)
        tempNumberOfRows= self.panel_twelve.numOfRowsHeader.GetLabelText()
        #remove extra stuff from string
        tempNumberOfRows2= ""
        for i in range(15, len(tempNumberOfRows)):
            tempNumberOfRows2+= tempNumberOfRows[i]
        numberOfRowsSetting= int(tempNumberOfRows2)
        tempFileName= str(self.panel_twelve.fileNameHeader.GetLabelText())
        #remove extra heading text from string
        fileNameSetting= ""
        for i in range(28, len(tempFileName)):
            fileNameSetting+= tempFileName[i]
        tempSingleSetting= self.panel_twelve.currentMode.GetLabelText()
        #remove extra heading from current Mode
        tempSingleSetting2= ""
        for i in range (14, len(tempSingleSetting)):
            tempSingleSetting2+= str(tempSingleSetting[i])
        singleSetting = ""
        if(self.compareString(tempSingleSetting2, "Single Mode",0,0,len(tempSingleSetting2), len("Single Mode"))==True):
            singleSetting="True"
        else:
            singleSetting="False"
        crackingSettings = {"cracking method":crackingMethod, "algorithm":algorithmSetting, "key length":keyLengthSetting,
                            "alphabet":alphabetSetting, "chain length":chainLengthSetting, "num rows":numberOfRowsSetting,
                            "file name":fileNameSetting, "single":singleSetting}

        #shared variable array
        #[0]shared dictionary, [1]shutdown, [2]update
        listOfSharedVariables= []
        listOfSharedVariables.append(crackingSettings)
        listOfSharedVariables.append(self.shutdown)
        listOfSharedVariables.append(self.update)
        self.NetworkServer= Process(target=Server, args=(crackingSettings,listOfSharedVariables,))
        self.NetworkServer.start()
        if(singleSetting is 'False'):
            self.switchFromPanel12ToPanel9()
        else:
            self.switchFromPanel12ToPanel10()

    def get_ip(self):
        import platform
        import socket
            #detect the OS
        try:  # getOS try block
            if platform.system() == "Windows":  # Detecting Windows
                self.IP= socket.gethostbyname(socket.gethostname())
                return self.IP
            elif platform.system() == "Linux":  # Detecting Linux
                import fcntl
                import struct
                import os

                def get_interface_ip(ifname):
                    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915,
                                                        struct.pack('256s', ifname[:15]))[20:24])

                #end of def
                def get_lan_ip():
                    ip = socket.gethostbyname(socket.gethostname())
                    if ip.startswith("127.") and os.name != "nt":
                        interfaces = ["eth0", "eth1", "eth2", "wlan0", "wlan1", "wifi0", "ath0", "ath1", "ppp0"]
                        for ifname in interfaces:
                            try:
                                ip = get_interface_ip(ifname)
                                print "IP address was retrieved from the " + str(ifname) + " interface."
                                break
                            except IOError:
                                pass
                    return ip
                #end of def
                self.IP= get_lan_ip()
                return self.IP
            elif platform.system() == "Darwin":  # Detecting OSX
                self.IP = socket.gethostbyname(socket.gethostname())
                return self.IP
            else:                           # Detecting an OS that is not listed
                self.IP = socket.gethostbyname(socket.gethostname())
                return self.IP

        except Exception as inst:
            print "========================================================================================"
            print "ERROR: An exception was thrown in getOS try block"
            print type(inst)  # the exception instance
            print inst.args  # arguments stored in .args
            print inst  # _str_ allows args tto be printed directly
            print "========================================================================================"
        #end of detect the OS


    def compareString(self,inboundStringA, inboundStringB, startA, startB, endA, endB):
        try:
            posA = startA
            posB = startB
            if((endA-startA) != (endB-startB)):
                return False
            for x in range(startA,endA):
                tempCharA= inboundStringA[posA]
                tempCharB= inboundStringB[posB]
                if(tempCharA != tempCharB):
                    return False
                posA+= 1
                posB+= 1
            return True
        except Exception as inst:
            print "========================================================================\n"
            print "Exception thrown in compareString Function: " +str(inst)+"\n"
            print "========================================================================\n"
            return False


if __name__ == '__main__':
    app= wx.App(0)
    frame= myFrame()
    frame.Show()
    app.MainLoop()
