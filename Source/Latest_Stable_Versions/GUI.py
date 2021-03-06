__author__ = 'chris hamm'
#GUI_WX_Demo4

#IMPORTANT!!!!!!!
#NOTICE: USE GUI DEMO 4 for true functionality!!!! This version of gui is broken on the server side!!!!!
#=======================================
#Main Section Header
#=======================================
#---------------------------------------
#Sub Section Header
#---------------------------------------
#.......................................
#Secondary Sub Section Header
#.......................................
import wx
import string
import hashlib
from multiprocessing import Process, Event, Manager, current_process
from NetworkServer import Server
from NetworkClient import Client

#=====================================================================================================================
#               Defining the GUI Display Panels
#                   The Gui Display Panels are the different "screen" that the user sees
#=====================================================================================================================
#--------------------------------------------------------------
#           Main Menu Panel
#               This is The Panel that the application always starts on
#               Able to navigate to these Panels from this screen:
#                   -Select Cracking Method Panel (via Single Mode button)
#                   -Select Node Type Screen (via Network Mode button)
#                   -About Us Page Panel (via About Us button)
#--------------------------------------------------------------
class PanelOne(wx.Panel):           #========================Main Menu Panel=====================
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        vbox= wx.BoxSizer(wx.VERTICAL)

        hbox6= wx.BoxSizer(wx.HORIZONTAL)
        logo= wx.StaticBitmap(self, -1, wx.Bitmap("Mighty_cracker_logo_r2.png", wx.BITMAP_TYPE_ANY))
        hbox6.Add(logo)
        vbox.Add(hbox6, flag=wx.CENTER, border=10)

        vbox.Add((-1,25))

        hbox2= wx.BoxSizer(wx.HORIZONTAL)
        self.SingleModeButton= wx.Button(self, label="Single Mode")
        hbox2.Add(self.SingleModeButton)
        vbox.Add(hbox2, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox3= wx.BoxSizer(wx.HORIZONTAL)
        self.NetworkModeButton= wx.Button(self, label="Network Mode")
        hbox3.Add(self.NetworkModeButton)
        vbox.Add(hbox3, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox4= wx.BoxSizer(wx.HORIZONTAL)
        self.aboutUsButton= wx.Button(self, label="About Us")
        hbox4.Add(self.aboutUsButton)
        vbox.Add(hbox4, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox5= wx.BoxSizer(wx.HORIZONTAL)
        self.CloseButton= wx.Button(self, label="Close")
        hbox5.Add(self.CloseButton)
        vbox.Add(hbox5, flag=wx.CENTER, border=10)

        self.SetSizer(vbox)

        #add tooltip
        self.SingleModeButton.SetToolTip(wx.ToolTip('For if you are using only one computer.'))
        self.NetworkModeButton.SetToolTip(wx.ToolTip('For when you are using a network of more than one computer.'))
        self.aboutUsButton.SetToolTip(wx.ToolTip('About the creators of this software and the purpose of this software.'))
        self.CloseButton.SetToolTip(wx.ToolTip('Close this Program.'))

        #Bind the buttons to events
        self.SingleModeButton.Bind(wx.EVT_BUTTON,  parent.onSingleModeButtonClick)
        self.NetworkModeButton.Bind(wx.EVT_BUTTON, parent.switchFromPanel1ToPanel6)
        self.aboutUsButton.Bind(wx.EVT_BUTTON, parent.switchFromPanel1ToPanel13)
        self.CloseButton.Bind(wx.EVT_BUTTON, parent.OnClose)

#------------------------------------------------------------
#           Select Cracking Method Panel
#               This panel lets the user select which cracking method they wish to use
#               Able to navigate to these panels from this panel:
#                   -Main Menu Panel (via Back To Main Menu button)
#                   -Dictionary Cracking Method Settings Screen (via Dictionary button)
#                   -Brute-Force Cracking Method Settings Screen (via Brute-Force button)
#                   -Rainbow Table Mode Select Screen (via Rainbow Table button)
#------------------------------------------------------------
class PanelTwo(wx.Panel):             #====================Select Cracking Method Panel=============================
    def __init__(self,parent):
        wx.Panel.__init__(self, parent=parent)
        vbox= wx.BoxSizer(wx.VERTICAL)

        hbox1= wx.BoxSizer(wx.HORIZONTAL)
        screenHeader= wx.StaticText(self, label="Select Cracking Method")
        screenHeader.SetFont(parent.titleFont)
        screenHeader.SetForegroundColour((255,255,255)) 
        hbox1.Add(screenHeader)
        vbox.Add(hbox1, flag=wx.TOP|wx.CENTER, border=10)

        vbox.Add((-1,25)) #spacer for adding space between header and the buttons

        hbox2= wx.BoxSizer(wx.HORIZONTAL)
        self.currentMode= wx.StaticText(self, label="Current Mode: Not yet Specified")
        self.currentMode.SetFont(parent.textFont)
        self.currentMode.SetForegroundColour((255,255,255)) 
        hbox2.Add(self.currentMode)
        vbox.Add(hbox2, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox3= wx.BoxSizer(wx.HORIZONTAL)
        self.DictionaryMethodButton= wx.Button(self, label="Dictionary")
        hbox3.Add(self.DictionaryMethodButton)
        vbox.Add(hbox3, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox4= wx.BoxSizer(wx.HORIZONTAL)
        self.BruteForceMethodButton= wx.Button(self, label="Brute Force")
        hbox4.Add(self.BruteForceMethodButton)
        vbox.Add(hbox4, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox5= wx.BoxSizer(wx.HORIZONTAL)
        self.RainbowTableMethodButton= wx.Button(self, label="Rainbow Table")
        hbox5.Add(self.RainbowTableMethodButton)
        vbox.Add(hbox5, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox6= wx.BoxSizer(wx.HORIZONTAL)
        self.BackToMainMenuButton= wx.Button(self, label="Back To Main Menu")
        hbox6.Add(self.BackToMainMenuButton)
        vbox.Add(hbox6, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox7= wx.BoxSizer(wx.HORIZONTAL)
        self.CloseButton= wx.Button(self, label="Close")
        hbox7.Add(self.CloseButton)
        vbox.Add(hbox7, flag=wx.CENTER, border=10)

        self.SetSizer(vbox)

        #add tooltip
        self.DictionaryMethodButton.SetToolTip(wx.ToolTip('Crack a hash code using a dictionary file for a reference.'))
        self.BruteForceMethodButton.SetToolTip(wx.ToolTip('Crack a hash code by trying every possible combination.'))
        self.RainbowTableMethodButton.SetToolTip(wx.ToolTip('Crack a hash code using a rainbow table as a reference.'))
        self.BackToMainMenuButton.SetToolTip(wx.ToolTip('Go back to the main menu'))
        self.CloseButton.SetToolTip(wx.ToolTip('Close the program'))

        #Bind the buttons to events
        self.DictionaryMethodButton.Bind(wx.EVT_BUTTON, parent.switchFromPanel2ToPanel3)
        self.BruteForceMethodButton.Bind(wx.EVT_BUTTON, parent.switchFromPanel2ToPanel4)
        self.RainbowTableMethodButton.Bind(wx.EVT_BUTTON, parent.switchFromPanel2ToPanel5)
        self.BackToMainMenuButton.Bind(wx.EVT_BUTTON, parent.switchFromPanel2ToPanel1)
        self.CloseButton.Bind(wx.EVT_BUTTON, parent.OnClose)

#---------------------------------------------------------------
#           Dictionary Cracking Method Settings Panel
#               This Panel allows the user to configure the dictionary search settings
#               Able to navigate to these panels from this panel:
#                   -Main Menu Panel (via Back To Main Menu button)
#                   -Single Mode Status Screen (if in Single Mode via Start/Connect button or Run Quick Sample Test button)
#                   -Network Mode Status Screen (if in Network Server Mode via Start/Connect button or Run Quick Sample Test button)
#---------------------------------------------------------------
class PanelThree(wx.Panel):         #========================Dictionary Cracking Method Settings Panel=================
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        listOfAlgorithms= ['MD5', 'SHA1', 'SHA224', 'SHA256', 'SHA384', 'SHA512']
        listOfHashingModes= ['Individual Hash Code','File of Hash Codes']
        vbox= wx.BoxSizer(wx.VERTICAL)

        hbox1= wx.BoxSizer(wx.HORIZONTAL)
        screenHeader= wx.StaticText(self, label="Dictionary Cracking Method Settings")
        screenHeader.SetFont(parent.titleFont)
        screenHeader.SetForegroundColour((255,255,255))
        hbox1.Add(screenHeader)
        vbox.Add(hbox1, flag=wx.TOP|wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox2= wx.BoxSizer(wx.HORIZONTAL)
        self.currentMode= wx.StaticText(self, label="Current Mode: Not Specified")
        self.currentMode.SetFont(parent.textFont)
        self.currentMode.SetForegroundColour((255,255,255))
        hbox2.Add(self.currentMode)
        vbox.Add(hbox2, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox3= wx.BoxSizer(wx.HORIZONTAL)
        self.selectAlgorithmHeader= wx.StaticText(self, label="Select Algorithm: ")
        self.selectAlgorithmHeader.SetFont(parent.textFont)
        self.selectAlgorithmHeader.SetForegroundColour((255,255,255))
        hbox3.Add(self.selectAlgorithmHeader)
        self.selectedAlgorithm= wx.ComboBox(self, choices= listOfAlgorithms, style=wx.CB_READONLY)
        hbox3.Add(self.selectedAlgorithm, flag=wx.LEFT, border=5)
        vbox.Add(hbox3, flag=wx.ALIGN_CENTER|wx.RIGHT, border=10)

        vbox.Add((-1,10))

        hbox10=wx.BoxSizer(wx.HORIZONTAL)
        hashTypeHeader= wx.StaticText(self, label="Select Hashing Mode: ")
        hashTypeHeader.SetFont(parent.textFont)
        hashTypeHeader.SetForegroundColour((255,255,255))
        hbox10.Add(hashTypeHeader)
        self.selectedHashingMode= wx.ComboBox(self, choices= listOfHashingModes, style=wx.CB_READONLY)
        hbox10.Add(self.selectedHashingMode, flag=wx.LEFT, border=5)
        vbox.Add(hbox10, flag=wx.ALIGN_CENTER|wx.RIGHT, border=10)

        vbox.Add((-1,10))

        hbox4= wx.BoxSizer(wx.HORIZONTAL)
        self.inputHashHeader= wx.StaticText(self, label="Hash to be Cracked: No Hash has been input")
        self.inputHashHeader.SetFont(parent.textFont)
        self.inputHashHeader.SetForegroundColour((255,255,255))
        hbox4.Add(self.inputHashHeader)
        vbox.Add(hbox4, flag=wx.CENTER, border=10)

        vbox.Add(((-1,10)))

        hbox5=wx.BoxSizer(wx.HORIZONTAL)
        self.inputHashButton= wx.Button(self, label="Set Hash To Be Cracked")
        hbox5.Add(self.inputHashButton)
        self.generateHashButton= wx.Button(self, label="Generate Hash Code")
        hbox5.Add(self.generateHashButton, flag=wx.LEFT, border=5)
        vbox.Add(hbox5, flag=wx.ALIGN_CENTER|wx.RIGHT, border=10)

        vbox.Add((-1,10))

        hbox6= wx.BoxSizer(wx.HORIZONTAL)
        self.inputDictFileHeader= wx.StaticText(self, label="Selected Dictionary File: No Dictionary File Selected")
        self.inputDictFileHeader.SetFont(parent.textFont)
        self.inputDictFileHeader.SetForegroundColour((255,255,255))
        hbox6.Add(self.inputDictFileHeader)
        vbox.Add(hbox6, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox7= wx.BoxSizer(wx.HORIZONTAL)
        self.setDictFileButton= wx.Button(self, label="Select Dictionary File")
        hbox7.Add(self.setDictFileButton)
        vbox.Add(hbox7, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox8= wx.BoxSizer(wx.HORIZONTAL)
        self.StartConnectButton= wx.Button(self, label="Start/Connect Button")
        hbox8.Add(self.StartConnectButton)
        vbox.Add(hbox8, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox11= wx.BoxSizer(wx.HORIZONTAL)
        self.resetToDefaultsButton= wx.Button(self, label="Reset Settings Back To Default")
        hbox11.Add(self.resetToDefaultsButton)
        vbox.Add(hbox11, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox12= wx.BoxSizer(wx.HORIZONTAL)
        self.startQuickSampleTestButton= wx.Button(self, label="Run Quick Sample Test")
        hbox12.Add(self.startQuickSampleTestButton)
        vbox.Add(hbox12, flag=wx.CENTER, border=10)

        #DEFAULT SETTINGS-------------
        #leave current mode the same
        #set selected algorithm to MD5
        #set selected hashing mode to individual hash code
        #set hash to be cracked to: no hash has been input
        #set selected dictionary file to: no dictionary file has been selected.

        vbox.Add((-1,10))

        hbox9= wx.BoxSizer(wx.HORIZONTAL)
        self.BackToMainMenuButton= wx.Button(self, label="Back To Main Menu")
        hbox9.Add(self.BackToMainMenuButton)
        self.CloseButton= wx.Button(self, label="Close")
        hbox9.Add(self.CloseButton, flag=wx.LEFT, border=5)
        vbox.Add(hbox9, flag=wx.ALIGN_CENTER|wx.RIGHT, border=10)

        self.SetSizer(vbox)

        #add tooltips
        self.selectAlgorithmHeader.SetToolTip(wx.ToolTip('The selected algorithm will be used to hash the entries in the \n'
                                                         'dictionary file, which will then be compared to the hash that \n'
                                                         'needs to be cracked'))
        self.selectedAlgorithm.SetToolTip(wx.ToolTip('The selected algorithm will be used to hash the entries in the \n'
                                                         'dictionary file, which will then be compared to the hash that \n'
                                                         'needs to be cracked'))
        self.inputHashButton.SetToolTip(wx.ToolTip('Enter in or paste in the hash code that needs to be cracked.'))
        self.generateHashButton.SetToolTip(wx.ToolTip('Input a key and the hash will be generated for you using the \n'
                                                      'selected algorithm (above).'))
        self.setDictFileButton.SetToolTip(wx.ToolTip('Select which file will be used as the dictionary file.\n'
                                                     '(.txt files only)'))
        self.StartConnectButton.SetToolTip(wx.ToolTip('Start cracking the hash code.\n'
                                                      'If server, Start hosting a dictionary cracking session.'))
        self.selectedHashingMode.SetToolTip(wx.ToolTip('Choose whether to crack a single hash code or a file of hash codes.'))
        self.resetToDefaultsButton.SetToolTip(wx.ToolTip('Resets all of the dictionary cracking settings back their default settings.'))
        self.startQuickSampleTestButton.SetToolTip(wx.ToolTip('Run a quick test using predefined settings. (Key: Popcorn,\n'
                                                              'Algorithm: MD5, Hashing Mode: Individual Hash Code, File: dic.txt'))
        self.BackToMainMenuButton.SetToolTip(wx.ToolTip('Go back to the main menu'))
        self.CloseButton.SetToolTip(wx.ToolTip('Close the program'))

        #Bind the buttons to events
        self.inputHashButton.Bind(wx.EVT_BUTTON, parent.setDictionaryHashToBeCracked)
        self.generateHashButton.Bind(wx.EVT_BUTTON, parent.generateHashDialogDic)
        self.setDictFileButton.Bind(wx.EVT_BUTTON, parent.selectDictFile)
        self.StartConnectButton.Bind(wx.EVT_BUTTON, parent.validateDictionaryInputs)
        self.resetToDefaultsButton.Bind(wx.EVT_BUTTON, parent.resetDictionarySettingsToDefault)
        self.startQuickSampleTestButton.Bind(wx.EVT_BUTTON, parent.configureDictionaryQuickTest)
        self.BackToMainMenuButton.Bind(wx.EVT_BUTTON, parent.switchFromPanel3ToPanel1)
        self.CloseButton.Bind(wx.EVT_BUTTON, parent.OnClose)

#-------------------------------------------------------------
#           Brute-Force Cracking Method Settings Panel
#               This Panel allows the user to configure the brute-force search settings
#               Able to navigate to these panels from this panel:
#                   -Main Menu Panel (via Back To Main Menu button)
#                   -Single Mode Status Screen (if in Single Mode via Start/Connect button or Run Quick Sample Test button)
#                   -Network Mode Status Screen (if in Network Server Mode via Start/Connect button or Run Quick Sample Test button)
#-------------------------------------------------------------
class PanelFour(wx.Panel):            #==================Brute Force Cracking method Settings Panel==================
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        listOfAlgorithms= ['MD5', 'SHA1', 'SHA224', 'SHA256', 'SHA384', 'SHA512']
        listOfAlphabets= ["All","Letters and Digits","Letters and Punctuation","Letters Only","Uppercase Letters","Lowercase Letters",
                          "Digits"]
        vbox= wx.BoxSizer(wx.VERTICAL)

        hbox1= wx.BoxSizer(wx.HORIZONTAL)
        screenHeader= wx.StaticText(self, label="Brute Force Cracking Method Settings")
        screenHeader.SetFont(parent.titleFont)
        screenHeader.SetForegroundColour((255,255,255))
        hbox1.Add(screenHeader)
        vbox.Add(hbox1, flag=wx.TOP|wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox2= wx.BoxSizer(wx.HORIZONTAL)
        self.currentMode= wx.StaticText(self, label="Current Mode: Not Specified")
        self.currentMode.SetFont(parent.textFont)
        self.currentMode.SetForegroundColour((255,255,255))
        hbox2.Add(self.currentMode)
        vbox.Add(hbox2, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox3= wx.BoxSizer(wx.HORIZONTAL)
        self.selectedAlgorithmHeader= wx.StaticText(self, label="Select Algorithm:")
        self.selectedAlgorithmHeader.SetFont(parent.textFont)
        self.selectedAlgorithmHeader.SetForegroundColour((255,255,255))
        hbox3.Add(self.selectedAlgorithmHeader)
        self.selectedAlgorithm= wx.ComboBox(self, choices=listOfAlgorithms, style=wx.CB_READONLY)
        hbox3.Add(self.selectedAlgorithm, flag=wx.LEFT, border=5)
        vbox.Add(hbox3, flag=wx.ALIGN_CENTER|wx.RIGHT, border=10)

        vbox.Add((-1,10))

        hbox4= wx.BoxSizer(wx.HORIZONTAL)
        self.inputHashHeader= wx.StaticText(self, label="Hash To Be Cracked: No Hash has been Input")
        self.inputHashHeader.SetFont(parent.textFont)
        self.inputHashHeader.SetForegroundColour((255,255,255))
        hbox4.Add(self.inputHashHeader)
        vbox.Add(hbox4, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox5= wx.BoxSizer(wx.HORIZONTAL)
        self.inputHashButton= wx.Button(self, label="Set Hash To Be Cracked")
        hbox5.Add(self.inputHashButton)
        self.generateHashButton= wx.Button(self, label="Generate Hash Code")
        hbox5.Add(self.generateHashButton, flag=wx.LEFT, border=5)
        vbox.Add(hbox5, flag=wx.ALIGN_CENTER|wx.RIGHT, border=10)

        vbox.Add((-1,10))

        hbox6= wx.BoxSizer(wx.HORIZONTAL)
        self.minKeyLengthHeader= wx.StaticText(self, label="Min Key Length: 5")
        self.minKeyLengthHeader.SetFont(parent.textFont)
        self.minKeyLengthHeader.SetForegroundColour((255,255,255))
        hbox6.Add(self.minKeyLengthHeader)
        self.changeMinKeyLengthButton= wx.Button(self, label="Set Min Key Length")
        hbox6.Add(self.changeMinKeyLengthButton, flag=wx.LEFT, border=25)
        vbox.Add(hbox6, flag=wx.ALIGN_CENTER|wx.RIGHT, border=10)

        vbox.Add((-1,10))

        hbox7= wx.BoxSizer(wx.HORIZONTAL)
        self.maxKeyLengthHeader= wx.StaticText(self, label="Max Key Length: 15")
        self.maxKeyLengthHeader.SetFont(parent.textFont)
        self.maxKeyLengthHeader.SetForegroundColour((255,255,255)) 
        hbox7.Add(self.maxKeyLengthHeader)
        self.changeMaxKeyLengthButton= wx.Button(self, label="Set Max Key Length")
        hbox7.Add(self.changeMaxKeyLengthButton, flag=wx.LEFT, border=25)
        vbox.Add(hbox7, flag=wx.ALIGN_CENTER|wx.RIGHT, border=10)

        vbox.Add((-1,10))

        hbox8= wx.BoxSizer(wx.HORIZONTAL)
        self.selectedAlphabetHeader= wx.StaticText(self, label="Selected Alphabet: ")
        self.selectedAlphabetHeader.SetFont(parent.textFont)
        self.selectedAlphabetHeader.SetForegroundColour((255,255,255)) 
        hbox8.Add(self.selectedAlphabetHeader)
        self.selectedAlphabet= wx.ComboBox(self, choices=listOfAlphabets, style=wx.CB_READONLY)
        hbox8.Add(self.selectedAlphabet, flag=wx.LEFT, border=5)
        vbox.Add(hbox8, flag=wx.ALIGN_CENTER|wx.RIGHT, border=10)

        vbox.Add((-1,10))

        hbox9= wx.BoxSizer(wx.HORIZONTAL)
        self.StartConnectButton= wx.Button(self, label="Start/Connect Button")
        hbox9.Add(self.StartConnectButton)
        vbox.Add(hbox9, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox11= wx.BoxSizer(wx.HORIZONTAL)
        self.resetBackToDefaultValues= wx.Button(self, label="Reset Settings Back To Default")
        hbox11.Add(self.resetBackToDefaultValues)
        vbox.Add(hbox11, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox12= wx.BoxSizer(wx.HORIZONTAL)
        self.startBruteForceQuickTestButton= wx.Button(self, label="Run Quick Sample Test")
        hbox12.Add(self.startBruteForceQuickTestButton)
        vbox.Add(hbox12, flag=wx.CENTER, border=10)
        #DEFAULTS SETTINGS-----------------
        #change selected algorithm back to MD5
        #change inputhash header to say no hash has been input
        #set min key length to 5
        #set max key length to 15
        #changed selected alphabet to all

        vbox.Add((-1,10))

        hbox10= wx.BoxSizer(wx.HORIZONTAL)
        self.BackToMainMenuButton= wx.Button(self, label="Back To Main Menu")
        hbox10.Add(self.BackToMainMenuButton)
        self.CloseButton= wx.Button(self, label="Close")
        hbox10.Add(self.CloseButton, flag=wx.LEFT, border=5)
        vbox.Add(hbox10, flag=wx.ALIGN_CENTER|wx.RIGHT, border=10)

        self.SetSizer(vbox)

        #tooltips
        self.selectedAlgorithm.SetToolTip(wx.ToolTip('The selected algorithm will be used to hash the generated entries \n'
                                                            ', which will then be compared to the hash that \n'
                                                         'needs to be cracked to see if they match'))
        self.inputHashButton.SetToolTip(wx.ToolTip('Enter in or paste in the hash code that needs to be cracked.'))
        self.generateHashButton.SetToolTip(wx.ToolTip('Input a key and the hash will be generated for you using the \n'
                                                      'selected algorithm (above).'))
        self.changeMinKeyLengthButton.SetToolTip(wx.ToolTip('Sets what the minimum amount of characters that will be in the key.'))
        self.changeMaxKeyLengthButton.SetToolTip(wx.ToolTip('Sets what the maximum amount of characters that will be in the key.'))
        self.selectedAlphabet.SetToolTip(wx.ToolTip('Sets which characters could be in the key. (The fewer possible characters, \n'
                                                    'the faster the cracking process goes)'))
        self.StartConnectButton.SetToolTip(wx.ToolTip('Start cracking the hash code. \n'
                                                      'If server, start hosting a brute force cracking session.'))
        self.resetBackToDefaultValues.SetToolTip(wx.ToolTip('Resets all of the Brute-Force Cracking Settings back to their default values.'))
        self.startBruteForceQuickTestButton.SetToolTip(wx.ToolTip('Run quick test using predefined settings. (Key: aaaff, \n'
                                                                  'Algorithm: MD5, Min Key Length: 4, Max Key Length: 6, Alphabet: Lowercase Letters)'))
        self.BackToMainMenuButton.SetToolTip(wx.ToolTip('Go back to main menu'))
        self.CloseButton.SetToolTip(wx.ToolTip('Close the program'))

        #Bind the buttons to events
        self.inputHashButton.Bind(wx.EVT_BUTTON, parent.setBruteForceHashToBeCracked)
        self.generateHashButton.Bind(wx.EVT_BUTTON, parent.generateHashDialogBF)
        self.changeMinKeyLengthButton.Bind(wx.EVT_BUTTON, parent.setBFMinKeyLength)
        self.changeMaxKeyLengthButton.Bind(wx.EVT_BUTTON, parent.setBFMaxKeyLength)
        self.StartConnectButton.Bind(wx.EVT_BUTTON, parent.validateBruteForceInputs)
        self.resetBackToDefaultValues.Bind(wx.EVT_BUTTON, parent.resetBruteForceSettingsToDefault)
        self.startBruteForceQuickTestButton.Bind(wx.EVT_BUTTON, parent.configureBruteForceQuickTest)
        self.BackToMainMenuButton.Bind(wx.EVT_BUTTON, parent.switchFromPanel4ToPanel1)
        self.CloseButton.Bind(wx.EVT_BUTTON, parent.OnClose)

#-------------------------------------------------------------------
#           Rainbow Table Mode Select
#               This Panel allows the user to specify which specific mode of rainbow table the user wishes to use
#               Able to navigate to these panels from this panel:
#                   -Main Menu Panel (via Back to Main Menu button)
#                   -Rainbow Table Cracking Method Settings Screen (via Crack Using Rainbow Table button)
#                   -Rainbow Table Maker Settings Screen (via Rainbow Table Maker button)
#-------------------------------------------------------------------
class PanelFive(wx.Panel):                 #====================Rainbow Table Mode Select=========================
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        vbox= wx.BoxSizer(wx.VERTICAL)
        hbox1= wx.BoxSizer(wx.HORIZONTAL)
        screenHeader= wx.StaticText(self, label="Rainbow Table Mode Select")
        screenHeader.SetFont(parent.titleFont)
        screenHeader.SetForegroundColour((255,255,255)) 
        hbox1.Add(screenHeader)
        vbox.Add(hbox1, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox2= wx.BoxSizer(wx.HORIZONTAL)
        self.currentMode= wx.StaticText(self, label="Current Mode: Not Specified")
        self.currentMode.SetFont(parent.textFont)
        self.currentMode.SetForegroundColour((255,255,255)) 
        hbox2.Add(self.currentMode)
        vbox.Add(hbox2, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox3= wx.BoxSizer(wx.HORIZONTAL)
        self.crackRainbowTableButton= wx.Button(self, label="Crack Using Rainbow Table")
        hbox3.Add(self.crackRainbowTableButton)
        vbox.Add(hbox3, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox4= wx.BoxSizer(wx.HORIZONTAL)
        self.makeRainbowTableButton= wx.Button(self, label="Rainbow Table Maker")
        hbox4.Add(self.makeRainbowTableButton)
        vbox.Add(hbox4, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox5= wx.BoxSizer(wx.HORIZONTAL)
        self.BackToMainMenuButton= wx.Button(self, label="Back To Main Menu")
        hbox5.Add(self.BackToMainMenuButton)
        self.CloseButton= wx.Button(self, label="Close")
        hbox5.Add(self.CloseButton, flag=wx.LEFT, border=5)
        vbox.Add(hbox5, flag=wx.ALIGN_CENTER|wx.RIGHT, border=10)

        self.SetSizer(vbox)

        #tooltips
        self.crackRainbowTableButton.SetToolTip(wx.ToolTip('Crack a hash code by using a rainbow table.'))
        self.makeRainbowTableButton.SetToolTip(wx.ToolTip('Create a rainbow table to be used with the rainbow table cracking method (above).'))
        self.BackToMainMenuButton.SetToolTip(wx.ToolTip('Go back to main menu'))
        self.CloseButton.SetToolTip(wx.ToolTip('Close the program'))

        #Bind the buttons to events
        self.crackRainbowTableButton.Bind(wx.EVT_BUTTON, parent.switchFromPanel5ToPanel11)
        self.makeRainbowTableButton.Bind(wx.EVT_BUTTON, parent.switchFromPanel5ToPanel12)
        self.BackToMainMenuButton.Bind(wx.EVT_BUTTON, parent.switchFromPanel5ToPanel1)
        self.CloseButton.Bind(wx.EVT_BUTTON, parent.OnClose)

#------------------------------------------------------------
#           Select Node Type Screen Panel
#               This Panel allows the user to specify whether to run in Network Server mode or Network Client mode
#               Able to navigate to these panels from this panel:
#                   -Main Menu Panel (via Back To Main Menu button)
#                   -Select Cracking Method Screen (via Network Server button)
#                   -Network Client Main Screen Panel (via Network Client button)
#------------------------------------------------------------
class PanelSix(wx.Panel):                  #====================Select Node Type Screen============================
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        vbox= wx.BoxSizer(wx.VERTICAL)

        hbox1= wx.BoxSizer(wx.HORIZONTAL)
        screenHeader= wx.StaticText(self, label="Select Node Type")
        screenHeader.SetFont(parent.titleFont)
        screenHeader.SetForegroundColour((255,255,255)) 
        hbox1.Add(screenHeader)
        vbox.Add(hbox1, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox2=wx.BoxSizer(wx.HORIZONTAL)
        self.NetworkServerButton= wx.Button(self, label="Network Server")
        hbox2.Add(self.NetworkServerButton)
        vbox.Add(hbox2, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox3=wx.BoxSizer(wx.HORIZONTAL)
        self.NetworkClientButton= wx.Button(self, label="Network Client")
        hbox3.Add(self.NetworkClientButton)
        vbox.Add(hbox3, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox4=wx.BoxSizer(wx.HORIZONTAL)
        self.BackToMainMenuButton= wx.Button(self, label="Back To Main Menu")
        hbox4.Add(self.BackToMainMenuButton)
        self.CloseButton= wx.Button(self, label="Close")
        hbox4.Add(self.CloseButton, flag=wx.LEFT, border=5)
        vbox.Add(hbox4, flag=wx.ALIGN_CENTER|wx.RIGHT, border=10)

        self.SetSizer(vbox)

        #Tooltips
        self.NetworkServerButton.SetToolTip(wx.ToolTip('Host a cracking session.'))
        self.NetworkClientButton.SetToolTip(wx.ToolTip('Participate in a hosts cracking session'))
        self.BackToMainMenuButton.SetToolTip(wx.ToolTip('Go back to main menu'))
        self.CloseButton.SetToolTip(wx.ToolTip('Close the program'))

        #Bind the buttons to events
        self.NetworkServerButton.Bind(wx.EVT_BUTTON, parent.onNetworkModeButtonClick)
        self.NetworkClientButton.Bind(wx.EVT_BUTTON, parent.switchFromPanel6ToPanel7)
        self.BackToMainMenuButton.Bind(wx.EVT_BUTTON, parent.switchFromPanel6ToPanel1)
        self.CloseButton.Bind(wx.EVT_BUTTON, parent.OnClose)

#------------------------------------------------------------
#           Network Client Main Screen Panel
#               This Panel lets the user input the Network Server's IP address and then connect to the server
#               Able to navigate to these panels from this panel:
#                   -Main Menu Panel (via Back to Main Menu button)
#                   -Network Client Status Screen (via Connect to Server button)
#------------------------------------------------------------
class PanelSeven(wx.Panel):          #=============================Network Client Main Screen=======================
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        vbox= wx.BoxSizer(wx.VERTICAL)

        hbox1= wx.BoxSizer(wx.HORIZONTAL)
        screenHeader= wx.StaticText(self, label="Network Client Main Screen")
        screenHeader.SetFont(parent.titleFont)
        screenHeader.SetForegroundColour((255,255,255)) 
        hbox1.Add(screenHeader)
        vbox.Add(hbox1, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox2=wx.BoxSizer(wx.HORIZONTAL)
        self.serverIPAddress= wx.StaticText(self, label="Server's IP Address: No IP Address Has been Input Yet")
        self.serverIPAddress.SetFont(parent.textFont)
        self.serverIPAddress.SetForegroundColour((255,255,255)) 
        hbox2.Add(self.serverIPAddress)
        vbox.Add(hbox2, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox3=wx.BoxSizer(wx.HORIZONTAL)
        self.InputServerIPButton= wx.Button(self, label="Input the Server IP")
        hbox3.Add(self.InputServerIPButton)
        vbox.Add(hbox3, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox4=wx.BoxSizer(wx.HORIZONTAL)
        self.ConnectToServerButton= wx.Button(self, label="Connect To The Server")
        hbox4.Add(self.ConnectToServerButton)
        vbox.Add(hbox4, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox5=wx.BoxSizer(wx.HORIZONTAL)
        self.BackToMainMenuButton= wx.Button(self, label="Back To Main Menu")
        hbox5.Add(self.BackToMainMenuButton)
        self.CloseButton= wx.Button(self, label="Close")
        hbox5.Add(self.CloseButton, flag=wx.LEFT, border=5)
        vbox.Add(hbox5, flag=wx.ALIGN_CENTER|wx.RIGHT, border=10)

        self.SetSizer(vbox)

        #ToolTips
        self.InputServerIPButton.SetToolTip(wx.ToolTip('Input the IP address of the server you are connecting to'))
        self.ConnectToServerButton.SetToolTip(wx.ToolTip('Connect to the server'))
        self.BackToMainMenuButton.SetToolTip(wx.ToolTip('Go back to main menu'))
        self.CloseButton.SetToolTip(wx.ToolTip('Close the program'))

        #Bind the buttons to events
        self.InputServerIPButton.Bind(wx.EVT_BUTTON, parent.getIPFromUser)
        self.ConnectToServerButton.Bind(wx.EVT_BUTTON, parent.validateNetworkClientInput)
        self.BackToMainMenuButton.Bind(wx.EVT_BUTTON, parent.switchFromPanel7ToPanel1)
        self.CloseButton.Bind(wx.EVT_BUTTON, parent.OnClose)

#----------------------------------------------------------------
#           Network Client Status Screen
#               This Panel displays the status of the search to the client while a search is being conducted
#               Able to navigate to these panels from this panel:
#                   -Main Menu Panel (via Disconnect From Server button)
#----------------------------------------------------------------
class PanelEight(wx.Panel):       #========================Network Client Status Screen===========================
    def __init__(self,parent):
        wx.Panel.__init__(self, parent)
        vbox= wx.BoxSizer(wx.VERTICAL)

        hbox1=wx.BoxSizer(wx.HORIZONTAL)
        screenHeader= wx.StaticText(self, label="Network Client Status Screen")
        screenHeader.SetFont(parent.titleFont)
        screenHeader.SetForegroundColour((255,255,255)) 
        hbox1.Add(screenHeader)
        vbox.Add(hbox1, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox2=wx.BoxSizer(wx.HORIZONTAL)
        self.clientIPAddress= wx.StaticText(self, label="Client IP Address: Not Specified")
        self.clientIPAddress.SetFont(parent.textFont)
        self.clientIPAddress.SetForegroundColour((255,255,255))
        hbox2.Add(self.clientIPAddress)
        self.connectedToIP= wx.StaticText(self, label="Connected To: Not Connected to any Server")
        self.connectedToIP.SetFont(parent.textFont)
        self.connectedToIP.SetForegroundColour((255,255,255)) 
        hbox2.Add(self.connectedToIP, flag=wx.LEFT, border=5)
        vbox.Add(hbox2, flag=wx.ALIGN_CENTER|wx.RIGHT, border=10)

        vbox.Add((-1,10))

        hbox3=wx.BoxSizer(wx.HORIZONTAL)
        self.currentStatus= wx.StaticText(self, label="Current Status: Running")
        self.currentStatus.SetFont(parent.textFont)
        self.currentStatus.SetForegroundColour((255,255,255)) 
        hbox3.Add(self.currentStatus)
        vbox.Add(hbox3, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox6= wx.BoxSizer(wx.HORIZONTAL)
        activityGuageHeader= wx.StaticText(self, label="Activity Gauge:")
        activityGuageHeader.SetFont(parent.textFont)
        activityGuageHeader.SetForegroundColour((255,255,255))
        hbox6.Add(activityGuageHeader)
        self.activityGauge= wx.Gauge(self, range=100, size=(250,15), style=wx.GA_HORIZONTAL)
        self.activityGauge.Pulse() #set to indeterminate mode
        hbox6.Add(self.activityGauge, flag=wx.LEFT, border=5)
        vbox.Add(hbox6, flag=wx.ALIGN_CENTER|wx.RIGHT, border=10)

        vbox.Add((-1,10))

        hbox7= wx.BoxSizer(wx.HORIZONTAL)
        self.solutionHeader= wx.StaticText(self, label="Solution: Not Finished Searching Yet")
        self.solutionHeader.SetFont(parent.textFont)
        self.solutionHeader.SetForegroundColour((255,255,255))
        hbox7.Add(self.solutionHeader)
        vbox.Add(hbox7, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox4=wx.BoxSizer(wx.HORIZONTAL)
        self.disconnectClientButton= wx.Button(self, label="Disconnect From Server")
        hbox4.Add(self.disconnectClientButton)
        vbox.Add(hbox4, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox5=wx.BoxSizer(wx.HORIZONTAL)
        self.CloseButton= wx.Button(self, label="Close")
        hbox5.Add(self.CloseButton)
        vbox.Add(hbox5, flag=wx.CENTER, border=10)

        self.SetSizer(vbox)

        #timer
        self.timer= wx.Timer()

        #ToolTips
        self.disconnectClientButton.SetToolTip(wx.ToolTip('Disconnect from the server'))
        self.CloseButton.SetToolTip(wx.ToolTip('Close the program'))

        #Bind the buttons to events
        self.timer.Bind(wx.EVT_TIMER, parent.updateNetworkClientTimer, self.timer)
        self.disconnectClientButton.Bind(wx.EVT_BUTTON, parent.disconnectClient)
        self.CloseButton.Bind(wx.EVT_BUTTON, parent.OnClose)

#---------------------------------------------------------------
#           Network Server Status Screen
#               This Panel displays the current status of the current search that is being conducted
#               Able to navigate to these panels from this panel:
#                   -Main Menu Panel (via Close the Server button)
#---------------------------------------------------------------
class PanelNine(wx.Panel):
#...............................................................
#           Initialization Function for Panel 9
#               This function is automatically called when a new instance of panel 9 is made
#               Creates a screen header that says 'Network Server Status Screen'
#                   Sets the screen header text to use the title font and sets the text color to white
#               Creates a text field that says 'cracking mode: not specified'
#                   Sets the cracking mode text to use the text font and sets the text color white
#               Creates a text field that says 'Server IP Address Not Set Yet'
#                   Sets the server ip text to use text font and sets the text color to white
#               Creates a text field that says 'Current Status: Running'
#                   Sets the current status text to use text font and sets the text color to white
#               Creates a text field that says 'Hash being cracked not specified'
#                   Sets the hash being cracked text to use the text font and sets the text color to white
#               Creates a text field that says 'activity gauge:" and a gauge
#                   Sets the activity gauge text to use the text font and sets its text color to white
#                   Sets the activity gauge to pulse (only works on windows)
#               Creates a text field that says 'Progress:'
#                   Sets the progress text to use the text font and sets the text color to white
#               Creates a text field that say 'Number of completed chunks ' and 'total number of chunks'
#                   Sets both text fields to use the text font and set the font color to white
#               Creates a text field to say 'Solution: Serach not finished yet'
#                   Sets the solution text to use the text font and sets the text to white
#               Creates a button that says 'close the server' and a button that says 'close'
#               Creates tooltips for the buttons and labels
#               Creates a timer object
#               Binds the buttons to their corresponding functions
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        vbox= wx.BoxSizer(wx.VERTICAL)

        hbox1= wx.BoxSizer(wx.HORIZONTAL)
        screenHeader= wx.StaticText(self, label="Network Server Status Screen")
        screenHeader.SetFont(parent.titleFont)
        screenHeader.SetForegroundColour((255,255,255)) 
        hbox1.Add(screenHeader)
        vbox.Add(hbox1, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox2=wx.BoxSizer(wx.HORIZONTAL)
        self.currentCrackingMode= wx.StaticText(self, label="Cracking Mode: Not Specified")
        self.currentCrackingMode.SetFont(parent.textFont)
        self.currentCrackingMode.SetForegroundColour((255,255,255)) 
        hbox2.Add(self.currentCrackingMode)
        vbox.Add(hbox2, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox3=wx.BoxSizer(wx.HORIZONTAL)
        self.serverIPAddress= wx.StaticText(self, label="Server IP Address: Not Set Yet")
        self.serverIPAddress.SetFont(parent.textFont)
        self.serverIPAddress.SetForegroundColour((255,255,255)) 
        hbox3.Add(self.serverIPAddress)
        vbox.Add(hbox3, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox4=wx.BoxSizer(wx.HORIZONTAL)
        self.currentStatus= wx.StaticText(self, label="Current Status: Running")
        self.currentStatus.SetFont(parent.textFont)
        self.currentStatus.SetForegroundColour((255,255,255)) 
        hbox4.Add(self.currentStatus)
        vbox.Add(hbox4, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox10= wx.BoxSizer(wx.HORIZONTAL)
        self.crackingThisHashHeader= wx.StaticText(self, label="Hash Being Cracked: Not Specified")
        self.crackingThisHashHeader.SetFont(parent.textFont)
        self.crackingThisHashHeader.SetForegroundColour((255,255,255)) 
        hbox10.Add(self.crackingThisHashHeader)
        vbox.Add(hbox10, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox6= wx.BoxSizer(wx.HORIZONTAL)
        activityGaugeHeader= wx.StaticText(self, label="Activity Gauge:")
        activityGaugeHeader.SetFont(parent.textFont)
        activityGaugeHeader.SetForegroundColour((255,255,255))
        hbox6.Add(activityGaugeHeader)
        self.activityGauge = wx.Gauge(self, range=100, size=(250,15), style=wx.GA_HORIZONTAL )
        self.activityGauge.Pulse() #switch gauge to indeterminate mode
        hbox6.Add(self.activityGauge, flag=wx.LEFT, border=5)
        vbox.Add(hbox6, flag=wx.ALIGN_CENTER|wx.RIGHT, border=10)

        vbox.Add((-1,10))

        hbox7= wx.BoxSizer(wx.HORIZONTAL)
        progressBarHeader= wx.StaticText(self, label="Progress:")
        progressBarHeader.SetFont(parent.textFont)
        progressBarHeader.SetForegroundColour((255,255,255))
        hbox7.Add(progressBarHeader)
        self.progressBar= wx.Gauge(self, range=100, size=(250,15), style=wx.GA_HORIZONTAL )
        self.progressBar.SetValue(0) #set value to start at zero
        hbox7.Add(self.progressBar, flag=wx.LEFT, border=5)
        vbox.Add(hbox7, flag=wx.ALIGN_CENTER|wx.RIGHT, border=10)

        vbox.Add((-1,10))

        hbox8= wx.BoxSizer(wx.HORIZONTAL)
        self.numCompletedChunksHeader= wx.StaticText(self, label="Number of Completed Chunks: Calculating") #change in the update timer section
        self.numCompletedChunksHeader.SetFont(parent.textFont)
        self.numCompletedChunksHeader.SetForegroundColour((255,255,255))
        hbox8.Add(self.numCompletedChunksHeader)
        self.numTotalChunksHeader= wx.StaticText(self, label="Total Number of Chunks: Calculating") #change in the update timer function
        self.numTotalChunksHeader.SetFont(parent.textFont)
        self.numTotalChunksHeader.SetForegroundColour((255,255,255))
        hbox8.Add(self.numTotalChunksHeader, flag=wx.LEFT, border=25)
        vbox.Add(hbox8, flag=wx.ALIGN_CENTER|wx.RIGHT, border=10)

        vbox.Add((-1,10))

        hbox9= wx.BoxSizer(wx.HORIZONTAL)
        self.SolutionHeader= wx.StaticText(self, label="Solution: Search Not Finished Yet")
        self.SolutionHeader.SetFont(parent.textFont)
        self.SolutionHeader.SetForegroundColour((255,255,255))
        hbox9.Add(self.SolutionHeader)
        vbox.Add(hbox9, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox5=wx.BoxSizer(wx.HORIZONTAL)
        self.forceQuitServerButton= wx.Button(self, label="Close the server")
        hbox5.Add(self.forceQuitServerButton)
        self.CloseButton= wx.Button(self, label="Close")
        hbox5.Add(self.CloseButton, flag=wx.LEFT, border=5)
        vbox.Add(hbox5, flag=wx.ALIGN_CENTER|wx.RIGHT, border=10)

        self.SetSizer(vbox)

        #ToolTips
        self.activityGauge.SetToolTip(wx.ToolTip('Indicates that the program is still running'))
        self.progressBar.SetToolTip(wx.ToolTip('Shows how far the search is overall'))
        self.forceQuitServerButton.SetToolTip(wx.ToolTip('Forcefully stop the server'))
        self.CloseButton.SetToolTip(wx.ToolTip('Close the program'))

        #create timer
        self.timer= wx.Timer()

        #Bind the buttons to events
        self.timer.Bind(wx.EVT_TIMER, parent.updateNetworkServerTimer, self.timer)
        self.forceQuitServerButton.Bind(wx.EVT_BUTTON, parent.forceCloseServer)
        self.CloseButton.Bind(wx.EVT_BUTTON, parent.OnClose)

#-------------------------------------------------------------
#           Single Mode Status Screen
#               This Panel displays the status of the current search being conducted to a user that is running in Single Mode
#               Able to navigate to these panels from this panel:
#                   -Main Menu Panel (via Back To Main Menu button)
#-------------------------------------------------------------
class PanelTen(wx.Panel):
#............................................................
#           Initialization Function for Panel 10
#               This function is automatically called when a new instance of panel 10 is made
#               Creates a screen header that says 'single mode status screen'
#                   Sets the screen header to use the title font and sets the text color to white
#               Creates a text field that says 'cracking mode not specified'
#                   Sets the cracking mode text to use the text font and sets the text color to white
#               Creates a text field that says ' current status: starting up'
#                   Sets the current status text to use the text font and sets the text color to white
#               Creates a text field that says 'hash being cracked: not specified'
#                   Sets the hash being cracked text to use the text font and sets the text color to white
#               Creates a text field that says 'activity gauge' and gauge
#                   Sets the label text to use the text font and sets the text color to white
#               Creates a text field that says 'progress' and a gauge
#                   Sets the label text to use the text font and sets the text color to white
#               Creates a text field that says 'number of completed chunks: calculating and a text field that says
#                   'Total number of chunks : calculating'
#                   Sets the text to use the text font and sets the text color to white
#               Creates a text field that says ' solution : search not finished yet'
#                   Sets the solution text to use the text font and sets the text color to white
#               Creates a button that says 'back to main menu' and a button that says 'close'
#               Creates tooltips for the buttons and some of the labels
#               Binds the buttons to their corresponding functions
#...............................................................
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        vbox= wx.BoxSizer(wx.VERTICAL)

        hbox1= wx.BoxSizer(wx.HORIZONTAL)
        screenHeader= wx.StaticText(self, label="Single Mode Status Screen")
        screenHeader.SetFont(parent.titleFont)
        screenHeader.SetForegroundColour((255,255,255))
        hbox1.Add(screenHeader)
        vbox.Add(hbox1, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox2=wx.BoxSizer(wx.HORIZONTAL)
        self.currentCrackingMode= wx.StaticText(self, label="Cracking Mode: Not Specified")
        self.currentCrackingMode.SetFont(parent.textFont)
        self.currentCrackingMode.SetForegroundColour((255,255,255))
        hbox2.Add(self.currentCrackingMode)
        vbox.Add(hbox2, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox3= wx.BoxSizer(wx.HORIZONTAL)
        self.currentStatus= wx.StaticText(self, label="Current Status: Starting up")
        self.currentStatus.SetFont(parent.textFont)
        self.currentStatus.SetForegroundColour((255,255,255))
        hbox3.Add(self.currentStatus)
        vbox.Add(hbox3, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox9= wx.BoxSizer(wx.HORIZONTAL)
        self.hashBeingCrackedHeader= wx.StaticText(self, label="Hash Being Cracked: Not Specified")
        self.hashBeingCrackedHeader.SetFont(parent.textFont)
        self.hashBeingCrackedHeader.SetForegroundColour((255,255,255))
        hbox9.Add(self.hashBeingCrackedHeader)
        vbox.Add(hbox9, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox5= wx.BoxSizer(wx.HORIZONTAL)
        activityGaugeHeader= wx.StaticText(self, label="Activity Gauge:")
        activityGaugeHeader.SetFont(parent.textFont)
        activityGaugeHeader.SetForegroundColour((255,255,255)) 
        hbox5.Add(activityGaugeHeader)
        self.activityGauge= wx.Gauge(self, range=100, size=(250,15), style=wx.GA_HORIZONTAL )
        self.activityGauge.Pulse() #switch gauge to indeterminate mode
        hbox5.Add(self.activityGauge, flag=wx.LEFT, border=5)
        vbox.Add(hbox5, flag=wx.ALIGN_CENTER|wx.RIGHT, border=10)

        vbox.Add((-1,10))

        hbox6= wx.BoxSizer(wx.HORIZONTAL)
        progressBarHeader= wx.StaticText(self, label="Progress:")
        progressBarHeader.SetFont(parent.textFont)
        progressBarHeader.SetForegroundColour((255,255,255))
        hbox6.Add(progressBarHeader)
        self.progressBar= wx.Gauge(self, range=100, size=(250,15), style=wx.GA_HORIZONTAL )
        self.progressBar.SetValue(0) #set value to start at zero
        hbox6.Add(self.progressBar, flag=wx.LEFT, border=5)
        vbox.Add(hbox6, flag=wx.ALIGN_CENTER|wx.RIGHT, border=10)

        vbox.Add((-1,10))

        hbox8= wx.BoxSizer(wx.HORIZONTAL)
        self.numCompletedChunksHeader= wx.StaticText(self, label="Number of Completed Chunks: Calculating") #change in the update timer section
        self.numCompletedChunksHeader.SetFont(parent.textFont)
        self.numCompletedChunksHeader.SetForegroundColour((255,255,255))
        hbox8.Add(self.numCompletedChunksHeader)
        self.numTotalChunksHeader= wx.StaticText(self, label="Total Number of Chunks: Calculating") #change in the update timer function
        self.numTotalChunksHeader.SetFont(parent.textFont)
        self.numTotalChunksHeader.SetForegroundColour((255,255,255)) 
        hbox8.Add(self.numTotalChunksHeader, flag=wx.LEFT, border=25)
        vbox.Add(hbox8, flag=wx.ALIGN_CENTER|wx.RIGHT, border=10)

        vbox.Add((-1,10))

        hbox7= wx.BoxSizer(wx.HORIZONTAL)
        self.SolutionHeader= wx.StaticText(self, label="Solution: Search Not Finished Yet")
        self.SolutionHeader.SetFont(parent.textFont)
        self.SolutionHeader.SetForegroundColour((255,255,255)) 
        hbox7.Add(self.SolutionHeader)
        vbox.Add(hbox7, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox4= wx.BoxSizer(wx.HORIZONTAL)
        self.backToMainMenuButton= wx.Button(self, label="Back To Main Menu")
        hbox4.Add(self.backToMainMenuButton)
        self.CloseButton= wx.Button(self, label="Close")
        hbox4.Add(self.CloseButton, flag=wx.LEFT, border=5)
        vbox.Add(hbox4, flag=wx.ALIGN_CENTER|wx.RIGHT, border=10)

        self.SetSizer(vbox)

        #ToolTips
        self.activityGauge.SetToolTip(wx.ToolTip('Indicates that the program is still running'))
        self.progressBar.SetToolTip(wx.ToolTip('Shows how far the search is overall'))
        self.backToMainMenuButton.SetToolTip(wx.ToolTip('Go back to the main menu'))
        self.CloseButton.SetToolTip(wx.ToolTip('Close the program'))

        #create timer
        self.timer= wx.Timer()

        #Bind the buttons to events
        self.timer.Bind(wx.EVT_TIMER, parent.updateSingleTimer, self.timer ) #timer is started in the switch to panel 10 function. Once started the timer will call updateSingleTimer every 1000 milliseconds
        self.backToMainMenuButton.Bind(wx.EVT_BUTTON, parent.quitSingleStatusBackToMainMenu)
        self.CloseButton.Bind(wx.EVT_BUTTON, parent.OnClose)

#----------------------------------------------------------------
#           Rainbow Table Cracking Method Settings Screen
#               This Panel allows the user to configure the setting for the Rainbow Table Cracking method
#               Able to navigate to these panels from this panel:
#                   -Main Menu Panel (via Back To Main Menu button)
#                   -Single Mode Status Screen (if in Single Mode via Start/Connect button or Run Quick Sample Test button)
#                   -Network Mode Status Screen (if in Network Server Mode via Start/Connect button or Run Quick Sample Test button)
#----------------------------------------------------------------
class PanelEleven(wx.Panel):
#................................................................
#           Initialization Function for Panel 11
#               This function is automatically called when a new instance of panel eleven is made
#               Creates a screen header text that says 'rainbow table cracking method settings'
#                   Sets the screen header text to use the title font and sets the text color to white
#               Creates a text field that says ' current mode: not specified'
#                   Sets the current mode text to use the text font and sets the text color to white
#               Creates a text field that says 'Selected algorithm' and a dropdown menu that contains the algorithms
#                   Sets the selected algorithm text to use text font and sets the text color to white
#               Creates a text field that says 'selected rainbow table file: no file has been selected'
#                   Sets the text to use text font and sets text color to be white
#               Creates a button that says 'select file button'
#               Creates a text field that says 'hash to be cracked: no hash has been entered'
#                   Sets the hash to be cracked text to use the text font and sets the font color to white
#               Creates a button that says 'set hash to be cracked' and a button that says 'generate hash code'
#               Creates a buttton that says 'start/connect button'
#               Creates a button that says 'reset settings back to default'
#               Creates a button that says 'run quick sample test'
#               Creates a button that says 'back to main menu' and a button that says 'close'
#               Creates tooltips for the buttons and some of the text labels
#               Binds the buttons to their corresponding functions
#...............................................................
    def __init__ (self, parent):
        wx.Panel.__init__(self,parent)
        listOfAlgorithms= ['MD5', 'SHA1', 'SHA224', 'SHA256', 'SHA384', 'SHA512']
        vbox= wx.BoxSizer(wx.VERTICAL)

        hbox1=wx.BoxSizer(wx.HORIZONTAL)
        screenHeader= wx.StaticText(self, label="Rainbow Table Cracking Method Settings")
        screenHeader.SetFont(parent.titleFont)
        screenHeader.SetForegroundColour((255,255,255))
        hbox1.Add(screenHeader)
        vbox.Add(hbox1, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox2=wx.BoxSizer(wx.HORIZONTAL)
        self.currentMode= wx.StaticText(self, label="Current Mode: Not Specified")
        self.currentMode.SetFont(parent.textFont)
        self.currentMode.SetForegroundColour((255,255,255))
        hbox2.Add(self.currentMode)
        vbox.Add(hbox2, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox9=wx.BoxSizer(wx.HORIZONTAL)
        selectedAlgorithmHeader= wx.StaticText(self, label="Selected Algorithm: ")
        selectedAlgorithmHeader.SetFont(parent.textFont)
        selectedAlgorithmHeader.SetForegroundColour((255,255,255))
        hbox9.Add(selectedAlgorithmHeader)
        self.selectedAlgorithm= wx.ComboBox(self, choices=listOfAlgorithms, style=wx.CB_READONLY)
        hbox9.Add(self.selectedAlgorithm, flag=wx.LEFT, border=5)
        vbox.Add(hbox9, flag=wx.ALIGN_CENTER|wx.RIGHT, border=10)

        vbox.Add((-1,10))

        hbox3=wx.BoxSizer(wx.HORIZONTAL)
        self.selectedFileHeader= wx.StaticText(self, label="Selected Rainbow Table File: No File has been Selected")
        self.selectedFileHeader.SetFont(parent.textFont)
        self.selectedFileHeader.SetForegroundColour((255,255,255))
        hbox3.Add(self.selectedFileHeader)
        vbox.Add(hbox3, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox4=wx.BoxSizer(wx.HORIZONTAL)
        self.selectFileButton= wx.Button(self, label="Select File")
        hbox4.Add(self.selectFileButton)
        vbox.Add(hbox4, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox5= wx.BoxSizer(wx.HORIZONTAL)
        self.hashToBeCrackedHeader= wx.StaticText(self, label="Hash to be cracked: No Hash has been entered")
        self.hashToBeCrackedHeader.SetFont(parent.textFont)
        self.hashToBeCrackedHeader.SetForegroundColour((255,255,255))
        hbox5.Add(self.hashToBeCrackedHeader)
        vbox.Add(hbox5, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox6=wx.BoxSizer(wx.HORIZONTAL)
        self.setHashCodeButton= wx.Button(self, label="Set Hash To Be Cracked")
        hbox6.Add(self.setHashCodeButton)
        self.generateHashButton= wx.Button(self, label="Generate Hash Code")
        hbox6.Add(self.generateHashButton, flag=wx.LEFT, border=5)
        vbox.Add(hbox6, flag=wx.ALIGN_CENTER|wx.RIGHT, border=10)

        vbox.Add((-1,10))

        hbox7=wx.BoxSizer(wx.HORIZONTAL)
        self.StartConnectButton= wx.Button(self, label="Start/Connect Button")
        hbox7.Add(self.StartConnectButton)
        vbox.Add(hbox7, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox10= wx.BoxSizer(wx.HORIZONTAL)
        self.resetSettingsToDefaultButton= wx.Button(self, label="Reset Settings Back To Default")
        hbox10.Add(self.resetSettingsToDefaultButton)
        vbox.Add(hbox10, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox11= wx.BoxSizer(wx.HORIZONTAL)
        self.startRainbowTableQuickTestButton= wx.Button(self, label="Run Quick Sample Test")
        hbox11.Add(self.startRainbowTableQuickTestButton)
        vbox.Add(hbox11, flag=wx.CENTER, border=10)
        #DEFAULT SETTINGS-------------------
        #set selected algorithm back to MD5
        #reset the selected rainbow table file back to nothing
        #set hash to be cracked value back to nothing

        vbox.Add((-1,10))

        hbox8=wx.BoxSizer(wx.HORIZONTAL)
        self.backToMainMenuButton= wx.Button(self, label="Back To Main Menu")
        hbox8.Add(self.backToMainMenuButton)
        self.CloseButton= wx.Button(self, label="Close")
        hbox8.Add(self.CloseButton, flag=wx.LEFT, border=5)
        vbox.Add(hbox8, flag=wx.ALIGN_CENTER|wx.RIGHT, border=10)

        self.SetSizer(vbox)

        #ToolTips
        self.selectedAlgorithm.SetToolTip(wx.ToolTip('Select the algorithm you want to use for cracking the hash code'))
        self.selectFileButton.SetToolTip(wx.ToolTip('Select what rainbow table file you want to use'))
        self.setHashCodeButton.SetToolTip(wx.ToolTip('Set the hash code you want to crack'))
        self.generateHashButton.SetToolTip(wx.ToolTip('Generate the hash code you want to crack based on the key you input and the selected algorithm'))
        self.resetSettingsToDefaultButton.SetToolTip(wx.ToolTip('Resets all Rainbow Table User Settings Back to their default Values.'))
        self.startRainbowTableQuickTestButton.SetToolTip(wx.ToolTip('Run Quick Test using predefined settings. (Algorithm: MD5, '
                                                                    'Selected Rainbow Table File: rain.txt, Key: Popcorn)'))
        self.backToMainMenuButton.SetToolTip(wx.ToolTip('Go back to the main menu'))
        self.CloseButton.SetToolTip(wx.ToolTip('Close the program'))

        #bind the buttons to events
        self.selectFileButton.Bind(wx.EVT_BUTTON, parent.selectRUFileSelect)
        self.setHashCodeButton.Bind(wx.EVT_BUTTON, parent.setRUHashToBeCracked)
        self.generateHashButton.Bind(wx.EVT_BUTTON, parent.generateHashDialogRT)
        self.StartConnectButton.Bind(wx.EVT_BUTTON, parent.validateRainbowTableUserInputs)
        self.resetSettingsToDefaultButton.Bind(wx.EVT_BUTTON, parent.resetRainbowTableCrackingSettingsToDefault)
        self.startRainbowTableQuickTestButton.Bind(wx.EVT_BUTTON, parent.configureRainbowTableUserQuickTest)
        self.backToMainMenuButton.Bind(wx.EVT_BUTTON, parent.switchFromPanel11ToPanel1)
        self.CloseButton.Bind(wx.EVT_BUTTON, parent.OnClose)

#------------------------------------------------------------
#           Rainbow Table Maker Settings Screen
#               This Panels allows the user to configure the settings for creating a rainbow table
#               Able to navigate to these panels from this panel:
#                   -Main Menu Panel (via Back To Main Menu button)
#                   -Single Mode Status Screen (if in Single Mode via Start/Connect button or Run Quick Sample Test button)
#                   -Network Mode Status Screen (if in Network Server Mode via Start/Connect button or Run Quick Sample Test button)
#------------------------------------------------------------
class PanelTwelve(wx.Panel):
#...........................................................
#           Initialization Function for Panel 12
#               This function is automatically called when a new instance of panel 12 is made
#               Creates a screen header with the text 'Rainbow Table Maker'
#                   Sets the screen header text font to the title font and sets the text color to white
#               Creates a text field that says 'Current Mode: Not Specified'
#                   Sets the current mode text font to text font and sets text color to white
#               Creates a text field that says 'Selected Algorithm' and a dropdown menu containing the algorithms
#                   Sets the selected algorithm text to use text font and set the text color to white
#               Creates a text field that says ' Key Length: 10' and a button that says 'Set Key Length'
#                   Sets the key length text to use text font and sets the text color to white
#               Creates a text field that says 'select alphabet' and a dropdown menu containing the alphabets
#                   Sets the select alphabet text to use text font and sets the text color to white
#               Creates a text field that says 'table chain lengt: 100' and a button that says 'Set table chain length'
#                   Sets the table chain length text to use the text font and sets the text color to white
#               Creates a text fiels that says 'number of rows: 100' and a  button that says 'Set number of rows'
#                   Sets the number of rows text to use the text font and sets the text color to white
#               Creates a text field that says 'save rainbow table file as: myRainbowTable.txt'
#                   Sets the save rainbow table file text to use the text font and sets the text color to white
#               Creates a button that says 'change saved file name'
#               Creates a text field that displays the notice about the size of the rainbow table
#                   Sets the notice text to use the text font and sets the text color to white
#               Creates a button that says 'Start/connect'
#               Creates a button that says 'reset settings back to default'
#               Creates a button that says 'run quick sample test'
#               Creates a button that says 'back to main menu' and a button that says 'close'
#               Creates tooltips for the buttons and some of the labels
#               Binds the buttons to their corresponding function
#.............................................................
    def __init__ (self,parent):
        wx.Panel.__init__(self, parent)
        listOfAlgorithms= ['MD5', 'SHA1', 'SHA224', 'SHA256', 'SHA384', 'SHA512']
        listOfAlphabets= ["All","Letters and Digits","Letters and Punctuation","Letters Only","Uppercase Letters","Lowercase Letters",
                          "Digits"]
        vbox= wx.BoxSizer(wx.VERTICAL)

        hbox1=wx.BoxSizer(wx.HORIZONTAL)
        screenHeader= wx.StaticText(self, label="Rainbow Table Maker")
        screenHeader.SetFont(parent.titleFont)
        screenHeader.SetForegroundColour((255,255,255)) 
        hbox1.Add(screenHeader)
        vbox.Add(hbox1, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox2=wx.BoxSizer(wx.HORIZONTAL)
        self.currentMode= wx.StaticText(self, label="Current Mode: Not Specified")
        self.currentMode.SetFont(parent.textFont)
        self.currentMode.SetForegroundColour((255,255,255)) 
        hbox2.Add(self.currentMode)
        vbox.Add(hbox2, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox3=wx.BoxSizer(wx.HORIZONTAL)
        self.selectedAlgorithmHeader= wx.StaticText(self, label="Select Algorithm: ")
        self.selectedAlgorithmHeader.SetFont(parent.textFont)
        self.selectedAlgorithmHeader.SetForegroundColour((255,255,255)) 
        hbox3.Add(self.selectedAlgorithmHeader)
        self.selectedAlgorithm= wx.ComboBox(self, choices=listOfAlgorithms, style=wx.CB_READONLY)
        hbox3.Add(self.selectedAlgorithm, flag=wx.LEFT, border=5)
        vbox.Add(hbox3, flag=wx.ALIGN_CENTER|wx.RIGHT, border=10)

        vbox.Add((-1,10))

        hbox4=wx.BoxSizer(wx.HORIZONTAL)
        self.keyLengthHeader= wx.StaticText(self, label="Key Length: 10")
        self.keyLengthHeader.SetFont(parent.textFont)
        self.keyLengthHeader.SetForegroundColour((255,255,255))
        hbox4.Add(self.keyLengthHeader)
        self.changeKeyLengthButton= wx.Button(self, label="Set Key Length")
        hbox4.Add(self.changeKeyLengthButton, flag=wx.LEFT, border=25)
        vbox.Add(hbox4, flag=wx.ALIGN_CENTER|wx.RIGHT, border=10)

        vbox.Add((-1,10))

        hbox5=wx.BoxSizer(wx.HORIZONTAL)
        selectAlphabetHeader= wx.StaticText(self, label="Select Alphabet")
        selectAlphabetHeader.SetFont(parent.textFont)
        selectAlphabetHeader.SetForegroundColour((255,255,255))
        hbox5.Add(selectAlphabetHeader)
        self.selectedAlphabet= wx.ComboBox(self, choices=listOfAlphabets, style=wx.CB_READONLY)
        hbox5.Add(self.selectedAlphabet, flag=wx.LEFT, border=5)
        vbox.Add(hbox5, flag=wx.ALIGN_CENTER|wx.RIGHT, border=10)

        vbox.Add((-1,10))

        hbox6=wx.BoxSizer(wx.HORIZONTAL)
        self.chainLengthHeader= wx.StaticText(self, label="Table Chain Length: 100")
        self.chainLengthHeader.SetFont(parent.textFont)
        self.chainLengthHeader.SetForegroundColour((255,255,255))
        hbox6.Add(self.chainLengthHeader)
        self.changeChainLengthButton= wx.Button(self, label="Set Table Chain Length")
        hbox6.Add(self.changeChainLengthButton, flag=wx.LEFT, border=125)
        vbox.Add(hbox6, flag=wx.ALIGN_CENTER|wx.RIGHT, border=10)

        vbox.Add((-1,10))

        hbox7=wx.BoxSizer(wx.HORIZONTAL)
        self.numOfRowsHeader= wx.StaticText(self, label="Number of Rows: 100")
        self.numOfRowsHeader.SetFont(parent.textFont)
        self.numOfRowsHeader.SetForegroundColour((255,255,255))
        hbox7.Add(self.numOfRowsHeader)
        self.setNumOfRowsButton= wx.Button(self, label="Set Number Of Rows")
        hbox7.Add(self.setNumOfRowsButton, flag=wx.LEFT, border=125)
        vbox.Add(hbox7, flag=wx.ALIGN_CENTER|wx.RIGHT, border=10)

        vbox.Add((-1,10))

        hbox8=wx.BoxSizer(wx.HORIZONTAL)
        self.fileNameHeader= wx.StaticText(self, label="Save Rainbow Table File As: myRainbowTable.txt")
        self.fileNameHeader.SetFont(parent.textFont)
        self.fileNameHeader.SetForegroundColour((255,255,255))
        hbox8.Add(self.fileNameHeader)
        vbox.Add(hbox8, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox9=wx.BoxSizer(wx.HORIZONTAL)
        self.changeFileNameButton= wx.Button(self, label="Change Saved File Name")
        hbox9.Add(self.changeFileNameButton)
        vbox.Add(hbox9, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox14= wx.BoxSizer(wx.HORIZONTAL)
        tableSizeNotice= wx.StaticText(self, label="NOTICE: If the dimensions (width * height) of the table \n"
                                                   "are less than 1 million, your table width won't change but \n"
                                                   "rows will be automatically added to meet this requirement.")
        tableSizeNotice.SetFont(parent.textFont)
        tableSizeNotice.SetForegroundColour((255,255,255))
        hbox14.Add(tableSizeNotice)
        vbox.Add(hbox14, flag=wx.CENTER, border= 10)

        vbox.Add((-1,10))

        hbox10=wx.BoxSizer(wx.HORIZONTAL)
        self.startConnectButton= wx.Button(self, label="Start/Connect Button")
        hbox10.Add(self.startConnectButton)
        vbox.Add(hbox10, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox12=wx.BoxSizer(wx.HORIZONTAL)
        self.resetSettingsBackToDefault= wx.Button(self, label="Reset Settings Back To Default")
        hbox12.Add(self.resetSettingsBackToDefault)
        vbox.Add(hbox12, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox13= wx.BoxSizer(wx.HORIZONTAL)
        self.startRainbowTableMakerQuickTestButton= wx.Button(self, label="Run Quick Sample Test")
        hbox13.Add(self.startRainbowTableMakerQuickTestButton)
        vbox.Add(hbox13, flag=wx.CENTER, border=10)

        #DEFAULT SETTINGS-----------
        #set selected algorithm back to MD5
        #set key length back to 10
        #set selected alphabet back to All
        #set table chain length back to 100
        #set number of rows back to 100
        #set save rainbowtable file name back to default

        vbox.Add((-1,10))

        hbox11=wx.BoxSizer(wx.HORIZONTAL)
        self.backToMainMenuButton= wx.Button(self, label="Back to Main Menu")
        hbox11.Add(self.backToMainMenuButton)
        self.CloseButton= wx.Button(self, label="Close")
        hbox11.Add(self.CloseButton, flag=wx.LEFT, border=5)
        vbox.Add(hbox11, flag=wx.ALIGN_CENTER|wx.RIGHT, border=10)

        self.SetSizer(vbox)

        #ToolTips
        self.selectedAlgorithm.SetToolTip(wx.ToolTip('Set which algorithm to use for creating the table'))
        self.selectedAlphabet.SetToolTip(wx.ToolTip('Set which characters to use when making the rainbow table'))
        self.changeKeyLengthButton.SetToolTip(wx.ToolTip('Set how many characters the key will be'))
        self.changeChainLengthButton.SetToolTip(wx.ToolTip('Set how long the chains (which go horizontally) are in the table'))
        self.setNumOfRowsButton.SetToolTip(wx.ToolTip('Set how many rows there will be in the table (which run vertically)'))
        self.changeFileNameButton.SetToolTip(wx.ToolTip('Change the name of the rainbow table file that you want to save'))
        self.startConnectButton.SetToolTip(wx.ToolTip('Start making (or if server, start hosting) a rainbow table making session'))
        self.resetSettingsBackToDefault.SetToolTip(wx.ToolTip('Reset the rainbow table maker settings back to default values'))
        self.startRainbowTableMakerQuickTestButton.SetToolTip(wx.ToolTip('Run quick test using predefined settings. (Algorithm: MD5, '
                                                                         'Key Length: 10, Alphabet: Lowercase Letters, Table Chain Length: 100,'
                                                                         ' Number of Rows: 100, Save As: myRainbowTable.txt)'))
        self.backToMainMenuButton.SetToolTip(wx.ToolTip('Go back to the main menu'))
        self.CloseButton.SetToolTip(wx.ToolTip('Close the program'))

        #bind the buttons to events
        self.changeKeyLengthButton.Bind(wx.EVT_BUTTON, parent.setRMKeyLength)
        self.changeChainLengthButton.Bind(wx.EVT_BUTTON, parent.setRMChainLength)
        self.setNumOfRowsButton.Bind(wx.EVT_BUTTON, parent.setRMNumOfRows)
        self.changeFileNameButton.Bind(wx.EVT_BUTTON, parent.setRMFileName)
        self.startConnectButton.Bind(wx.EVT_BUTTON, parent.validateRainbowTableMakerInputs)
        self.resetSettingsBackToDefault.Bind(wx.EVT_BUTTON, parent.resetRainbowTableMakerSettingsToDefault)
        self.startRainbowTableMakerQuickTestButton.Bind(wx.EVT_BUTTON, parent.configureRainbowTableMakerQuickTest)
        self.backToMainMenuButton.Bind(wx.EVT_BUTTON, parent.switchFromPanel12ToPanel1)
        self.CloseButton.Bind(wx.EVT_BUTTON, parent.OnClose)

#----------------------------------------------------------
#           About Us Page Panel
#               This Panel displays information about the Mighty Cracker Program and the people who developed it
#               Able to navigate to these panels from this panel:
#                   -Main Menu Panel (via Back to Main Menu button)
#----------------------------------------------------------
class PanelThirteen(wx.Panel):
#..........................................................
#           Initialization Function for Panel Thirteen
#               This function is automatically called when a new instance of panel 13 is made
#               Sets the title text to 'About Us'
#               Sets the font of the title text to title font and sets the font color to white
#               Displays the About Us text to the textctrl using the appropriate new line character for the OS in use
#               Adds a Back to Main Menu button and a Close the Program button and displays them
#               Links all buttons to their corresponding functions
#..........................................................
    def __init__(self,parent):
        wx.Panel.__init__(self,parent)
        vbox= wx.BoxSizer(wx.VERTICAL)

        hbox1= wx.BoxSizer(wx.HORIZONTAL)
        aboutUsHeader= wx.StaticText(self, label="About Us", style=wx.ALIGN_CENTER_HORIZONTAL)
        aboutUsHeader.SetFont(parent.titleFont)
        aboutUsHeader.SetForegroundColour((255,255,255))
        hbox1.Add(aboutUsHeader)
        vbox.Add(hbox1, flag=wx.CENTER|wx.TOP, border=10)

        vbox.Add((-1,10)) #add an extra spacer to give more room between the aboutUsHeader and the TextCtrl

        hbox2= wx.BoxSizer(wx.HORIZONTAL)
        textBox= wx.TextCtrl(self, style=wx.TE_MULTILINE|wx.CB_READONLY|wx.HSCROLL)
        newLineCharacter= "" #this is used for the new line character,set according to your OS
        insertFourCharTab= "    "
        if(parent.compareString(str(parent.theDetectedOS), str('Windows'),0,0,len('Windows'),len('Windows'))==True): #if Windows
            newLineCharacter= "\r\n"
        elif(parent.compareString(str(parent.theDetectedOS), str('Linux'),0,0,len('Linux'),len('Linux'))==True): #if linux
            newLineCharacter= "\n"
        elif(parent.compareString(str(parent.theDetectedOS), str('Darwin'),0,0,len('Darwin'),len('Darwin'))==True): #if mac
            newLineCharacter= "\n"
        elif(parent.compareString(str(parent.theDetectedOS), str('FreeBSD'),0,0,len('FreeBSD'),len('FreeBSD'))==True): #if FreeBSD
            newLineCharacter="\n"
        elif(parent.compareString(str(parent.theDetectedOS), str('NetBSD'),0,0,len('NetBSD'),len('NetBSD'))==True): #if FreeBSD
            newLineCharacter="\n"
        elif(parent.compareString(str(parent.theDetectedOS), str('NetBSD'),0,0,len('NetBSD'),len('NetBSD'))==True): #if FreeBSD
            newLineCharacter="\n"
        else:
            print "=============================================================="
            print "GUI ERROR: invalid OS detected: '"+str(parent.theDetectedOS)+"'"
            print "=============================================================="
        #About Me text
        textBox.WriteText(newLineCharacter)
        textBox.WriteText(newLineCharacter+"Authors: Chris Hamm, Jon Wright, Nick Baum, and Chris Bugg.")
        textBox.WriteText(newLineCharacter)
        textBox.WriteText(newLineCharacter+"Description: ")
        textBox.WriteText(newLineCharacter+"============================================================")
        textBox.WriteText(newLineCharacter)
        textBox.WriteText(newLineCharacter+insertFourCharTab+"Our project, Mighty Cracker, is a program designed to crack hashed")
        textBox.WriteText(newLineCharacter+"passwords. It is stand-alone, GUI, and can run on Mac 10+, Linux 14+, BSD 10+")
        textBox.WriteText(newLineCharacter+"and Windows 7+. It uses the power of multiprocessing to fully utilize")
        textBox.WriteText(newLineCharacter+"every computer available, and can utilize a LAN to distribute the")
        textBox.WriteText(newLineCharacter+"workload over up to 90 computers (nodes). For now, the algorithms")
        textBox.WriteText(newLineCharacter+"that it can utilize are: sha 224,sha 256, sha 512, sha 1, and md5,")
        textBox.WriteText(newLineCharacter+"which cover a fair amount of the common hashing algorithms used.")
        textBox.WriteText(newLineCharacter)
        textBox.WriteText(newLineCharacter+insertFourCharTab+"We've implemented three common attack methods to find an original password.")
        textBox.WriteText(newLineCharacter+"Dictionary takes a list of passwords, hashes them, and compares the")
        textBox.WriteText(newLineCharacter+insertFourCharTab+"hashes to the original (user inputted) hash to find a match.")
        textBox.WriteText(newLineCharacter+"Brute Force will iterate through any combination (up to 16")
        textBox.WriteText(newLineCharacter+insertFourCharTab+"characters) of letters, numbers, and symbols to brute-force")
        textBox.WriteText(newLineCharacter+insertFourCharTab+"the password, returning an original if found.")
        textBox.WriteText(newLineCharacter+"Rainbow Tables are pre-computed arrays of hashes, organized to to")
        textBox.WriteText(newLineCharacter+insertFourCharTab+"provide a time-cost trade-off. The creator creates tables to")
        textBox.WriteText(newLineCharacter+insertFourCharTab+"be used at a later time, and the user uses created tables.")
        textBox.WriteText(newLineCharacter+insertFourCharTab+"This gives one a huge advantage if you know what the password")
        textBox.WriteText(newLineCharacter+insertFourCharTab+"will consist of ahead of time.")
        textBox.WriteText(newLineCharacter)
        textBox.WriteText(newLineCharacter+insertFourCharTab+"These three methods can all be used on either a single computer")
        textBox.WriteText(newLineCharacter+"(single-user mode) or on a network of computers (similar to")
        textBox.WriteText(newLineCharacter+"a Beowulf cluster). When using on headless systems, the program")
        textBox.WriteText(newLineCharacter+"can run in terminal (text-only) mode with a -c command.")
        textBox.WriteText(newLineCharacter)
        textBox.WriteText(newLineCharacter+insertFourCharTab+"Of the distributed, multi-process, simple GUI approach this program")
        textBox.WriteText(newLineCharacter+"takes, it is potentially more powerful and more user-friendly than")
        textBox.WriteText(newLineCharacter+"most other hash cracking software out there today, making it more")
        textBox.WriteText(newLineCharacter+"accessible for more people. Simply open the executable and crack")
        textBox.WriteText(newLineCharacter+"passwords.")
        textBox.WriteText(newLineCharacter)
        textBox.WriteText(newLineCharacter+insertFourCharTab+"In the future we'd like to add on the ability to crack the LMT-family")
        textBox.WriteText(newLineCharacter+"of hashes (Windows) as well as add in GPU support for additional power.")
        textBox.WriteText(newLineCharacter)
        #end of  insert aboout me text-----------------------------
        hbox2.Add(textBox, proportion=1, flag=wx.EXPAND)
        vbox.Add(hbox2, proportion=1, flag=wx.LEFT|wx.RIGHT|wx.EXPAND, border=10)

        vbox.Add((-1, 25)) #add extra space between the textctrl and the buttons

        hbox3= wx.BoxSizer(wx.HORIZONTAL)
        self.backToMainMenuButton= wx.Button(self, label="Back To Main Menu")
        hbox3.Add(self.backToMainMenuButton)
        self.closeButton= wx.Button(self, label="Close")
        hbox3.Add(self.closeButton, flag=wx.LEFT|wx.BOTTOM, border=5)
        vbox.Add(hbox3, flag=wx.ALIGN_RIGHT|wx.RIGHT, border=10)

        self.SetSizer(vbox)

        self.backToMainMenuButton.SetToolTip(wx.ToolTip('Go back to the main menu'))
        self.closeButton.SetToolTip(wx.ToolTip('Close the program'))

        #link the buttons up to events
        self.backToMainMenuButton.Bind(wx.EVT_BUTTON, parent.switchFromPanel13ToPanel1)
        self.closeButton.Bind(wx.EVT_BUTTON, parent.OnClose)

#=======================================================================================================================
#           Defining the Frame
#               The Frame contains all of the Graphical Display Panels
#=======================================================================================================================
class myFrame(wx.Frame):
#------------------------------------------------------------------
#           Initialization Function For the MyFrame Class
#               This function is called automatically when a new instance of myFrame is created.
#               This function defines the three custom fonts that are used (Title Font, Text Font, Enlarged Solution Font)
#               Initializes the detected OS variable
#               Calls the detect OS Function (which sets the detected OS variable)
#               Defines the thirteen panels and sets their background color to black
#               Hides all panels except for panel 1 (Main Menu Panel)
#               Adds all of the panels to the main box sizer
#               Resets all search settings to default on all panels
#               Add a menu bar to the top of the screen and define and add components to the menu bar
#               If this is the main process and not a subprocess
#                   -Declare the shared dictionary of shared values
#                   -Declare a shared a list of shared variables
#--------------------------------------------------------------------
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "Mighty Cracker", size=(1024, 768))

        #custom defined fonts
        self.titleFont= wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD) #custom font for the title
        self.textFont= wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)#custom font for the normal text
        self.enlargedSolutionFont= wx.Font(18, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD) #custom font for when solution is found/not found

        #initialize detectedOS variable
        self.theDetectedOS= "None"

        #detect the OS
        self.detectOS()

        #define the panels and set their background color to black
        self.panel_one= PanelOne(self)
        self.panel_one.SetBackgroundColour("Black")
        self.panel_two= PanelTwo(self)
        self.panel_two.SetBackgroundColour("Black")
        self.panel_three= PanelThree(self)
        self.panel_three.SetBackgroundColour("Black")
        self.panel_four= PanelFour(self)
        self.panel_four.SetBackgroundColour("Black")
        self.panel_five= PanelFive(self)
        self.panel_five.SetBackgroundColour("Black")
        self.panel_six= PanelSix(self)
        self.panel_six.SetBackgroundColour("Black")
        self.panel_seven= PanelSeven(self)
        self.panel_seven.SetBackgroundColour("Black")
        self.panel_eight= PanelEight(self)
        self.panel_eight.SetBackgroundColour("Black")
        self.panel_nine= PanelNine(self)
        self.panel_nine.SetBackgroundColour("Black")
        self.panel_ten= PanelTen(self)
        self.panel_ten.SetBackgroundColour("Black")
        self.panel_eleven= PanelEleven(self)
        self.panel_eleven.SetBackgroundColour("Black")
        self.panel_twelve= PanelTwelve(self)
        self.panel_twelve.SetBackgroundColour("Black")
        self.panel_thirteen= PanelThirteen(self)
        self.panel_thirteen.SetBackgroundColour("Black")
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

        #add all of the panels to the main boxsizer
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

        #set all panels to default configuration values at the start
        self.resetDictionarySettingsToDefault(None)
        self.resetBruteForceSettingsToDefault(None)
        self.resetRainbowTableCrackingSettingsToDefault(None)
        self.resetRainbowTableMakerSettingsToDefault(None)

        #add a menubar at the top of the window/screen
        menubar= wx.MenuBar()
        fileMenu= wx.Menu()
        fileMenuClose= fileMenu.Append(wx.ID_ANY, "Close","Close Application")
        menubar.Append(fileMenu, '&File')
        viewMenu= wx.Menu()
        viewMenuMaximizeScreen= viewMenu.Append(wx.ID_ANY, "Maximize Screen", "Make the window fill the entire screen")
        viewMenuNormalScreen= viewMenu.Append(wx.ID_ANY, "Normal Size", "Make the window it's native resolution")
        menubar.Append(viewMenu, '&View')
        runMenu= wx.Menu()
        dictionaryTestsLabel= runMenu.Append(wx.ID_ANY, "Dictionary Quick Tests", " ")
        dictionaryTestsLabel.Enable(False)
        runQuickStartSingleDictionaryTest= runMenu.Append(wx.ID_ANY, "Start Single Mode Dictionary Quick Test", "Starts a single mode, dictionary search using predefined settings")
        runQuickStartNetworkServerDictionaryTest= runMenu.Append(wx.ID_ANY, "Start Network Server Mode Dictionary Quick Test", "Starts a network server, dictionary search using predefined settings")
        bruteForceTestsLabel= runMenu.Append(wx.ID_ANY, "Brute-Force Quick Tests", " ")
        bruteForceTestsLabel.Enable(False)
        runQuickStartSingleBruteForceTest= runMenu.Append(wx.ID_ANY, "Start Single Mode Brute Force Quick Test", "Starts a single mode, brute force search using predefined settings")
        runQuickStartNetworkServerBruteForceTest= runMenu.Append(wx.ID_ANY, "Start Network Server Mode Brute Force Quick Test", "Starts a network server, brute force search using predefined settings")
        rainbowUserTestsLabel= runMenu.Append(wx.ID_ANY, "Rainbow Table User Quick Tests", " ")
        rainbowUserTestsLabel.Enable(False)
        runQuickStartSingleRainbowTableUserTest= runMenu.Append(wx.ID_ANY, "Start Single Mode Rainbow Table User Quick Test", "Starts a single mode, rainbow table user search using predefined settings")
        runQuickStartNetworkServerRainbowTableUserTest= runMenu.Append(wx.ID_ANY, "Start Network Server Mode Rainbow Table User Quick Test", "Starts a Network Server, rainbow table user search using predefined settings")
        rainbowMakerTestsLabel= runMenu.Append(wx.ID_ANY, "Rainbow Table Maker Quick Tests", " ")
        rainbowMakerTestsLabel.Enable(False)
        runQuickStartSingleRainbowTableMakerTest= runMenu.Append(wx.ID_ANY, "Start Single Mode Rainbow Table Maker Quick Test", "Starts a single mode, rainbow table maker using predefined setttings")
        runQuickStartNetworkServerRainbowTableMakerTest= runMenu.Append(wx.ID_ANY, "Start Network Server Mode Rainbow Table Maker Quick Test","Starts a Network Server, rainbow table maker session using predefined settings")
        menubar.Append(runMenu, '&Run')
        self.SetMenuBar(menubar)

        #bind menu items to events
        self.Bind(wx.EVT_MENU, self.OnClose, fileMenuClose)
        self.Bind(wx.EVT_MENU, self.viewMaximizedScreen, viewMenuMaximizeScreen)
        self.Bind(wx.EVT_MENU, self.viewNormalScreen, viewMenuNormalScreen)
        self.Bind(wx.EVT_MENU, self.startSingleDictionaryQuickTestFromMenu, runQuickStartSingleDictionaryTest)
        self.Bind(wx.EVT_MENU, self.startNetworkServerDictionaryQuickTestFromMenu, runQuickStartNetworkServerDictionaryTest)
        self.Bind(wx.EVT_MENU, self.startSingleBruteForceQuickTestFromMenu, runQuickStartSingleBruteForceTest)
        self.Bind(wx.EVT_MENU, self.startNetworkServerBruteForceQuickTestFromMenu, runQuickStartNetworkServerBruteForceTest)
        self.Bind(wx.EVT_MENU, self.startSingleRainbowTableUserTestFromMenu, runQuickStartSingleRainbowTableUserTest)
        self.Bind(wx.EVT_MENU, self.startNetworkServerRainbowTableUserQuickTestFromMenu, runQuickStartNetworkServerRainbowTableUserTest)
        self.Bind(wx.EVT_MENU, self.startSingleRainbowTableMakerQuickTestFromMenu, runQuickStartSingleRainbowTableMakerTest)
        self.Bind(wx.EVT_MENU, self.startNetworkServerRainbowTableMakerQuickTestFromMenu, runQuickStartNetworkServerRainbowTableMakerTest)

        #If this is the main process and not a subprocess
        if __name__ == '__main__':

            #Define the shared dictionary and it's values
            manager = Manager()
            self.dictionary = manager.dict()
            self.dictionary["key"] = ''
            self.dictionary["finished chunks"] = 0
            self.dictionary["total chunks"] = 0

            #client signals if it's connected or not
            self.is_connected = Event()
            self.is_connected.clear()

            #client signals if it's doing stuff or not
            self.is_doing_stuff = Event()
            self.is_doing_stuff.clear()

            #update is an event intended to be set by server to let the UI know that the shared dictionary has been updated
            self.update = Event()
            self.update.clear()

            #shutdown is linked the the server/client shared shutdown command. setting this should should down server and client.
            self.shutdown = Event()
            self.shutdown.clear()

            #Shared is a list of shared events
            self.shared = []
            self.shared.append(self.dictionary)
            self.shared.append(self.shutdown)
            self.shared.append(self.update)
            self.shared.append(self.is_connected)
            self.shared.append(self.is_doing_stuff)

#=======================================================================================================================
#           Frame Resizing Functions
#               Functions that resize the frame that displays the panels
#=======================================================================================================================
#------------------------------------------------------------------------
#           View Maximized Screen Function
#               This function makes the window fill the screen completely, (but not in a fullscreen mode)
#               NOTE: Full screen mode was removed because full screen mode glitches out and removes the menu bars
#               This sets the maximize flag to true
#-----------------------------------------------------------------------
    def viewMaximizedScreen(self, event):
        self.Maximize(True)

#------------------------------------------------------------------------
#           View Normal Screen Function
#               This function resizes the window to its native size.
#               This sets the maximize flag to false
#               This sets the full screen flag to false
#------------------------------------------------------------------------
    def viewNormalScreen(self, event):
        self.Maximize(False)
        self.ShowFullScreen(False)

#=======================================================================================================================
#                   Start Quick Test Functions
#                       These functions are called when the user selects Start Quick Test from the Menu
#                       These functions simply call the Quick Test functions that their corresponding button counterparts call
#=======================================================================================================================
#------------------------------------------------------------------------
#           Start Single Dictionary Quick Test From Menu Function
#               This function Sets the current mode to Single Mode
#               Then hides all panels except for panel 10 (single mode status screen)
#               Finally, it then calls the Configure Dictionary Quick Test Function
#------------------------------------------------------------------------
    def startSingleDictionaryQuickTestFromMenu(self, event):
        self.panel_three.currentMode.SetLabel("Current Mode: Single Mode")
        self.panel_one.Hide()
        self.panel_two.Hide()
        self.panel_three.Hide()
        self.panel_four.Hide()
        self.panel_five.Hide()
        self.panel_six.Hide()
        self.panel_seven.Hide()
        self.panel_eight.Hide()
        self.panel_nine.Hide()
        self.panel_eleven.Hide()
        self.panel_twelve.Hide()
        self.panel_thirteen.Hide()
        self.configureDictionaryQuickTest(None)

#-----------------------------------------------------------------------
#           Start Network Server Dictionary Quick Test From Menu Function
#               This function Sets the current mode to Network Mode
#               Then hides all panels except for panel 9 (network server status screen)
#               Finally, it then calls the Configure Dictionary Quick Test Function
#-----------------------------------------------------------------------
    def startNetworkServerDictionaryQuickTestFromMenu(self, event):
        self.panel_three.currentMode.SetLabel("Current Mode: Network Mode")
        self.panel_one.Hide()
        self.panel_two.Hide()
        self.panel_three.Hide()
        self.panel_four.Hide()
        self.panel_five.Hide()
        self.panel_six.Hide()
        self.panel_seven.Hide()
        self.panel_eight.Hide()
        self.panel_ten.Hide()
        self.panel_eleven.Hide()
        self.panel_twelve.Hide()
        self.panel_thirteen.Hide()
        self.configureDictionaryQuickTest(None)

#-------------------------------------------------------------------
#           Start Single Brute Force Quick Test From Menu Function
#               This function Sets the current mode to Single Mode
#               Then hides all panels except for panel 10 (single mode status screen)
#               Finally, it then calls the Configure Brute Force Quick Test Function
#------------------------------------------------------------------
    def startSingleBruteForceQuickTestFromMenu(self, event):
        self.panel_four.currentMode.SetLabel("Current Mode: Single Mode")
        self.panel_one.Hide()
        self.panel_two.Hide()
        self.panel_three.Hide()
        self.panel_four.Hide()
        self.panel_five.Hide()
        self.panel_six.Hide()
        self.panel_seven.Hide()
        self.panel_eight.Hide()
        self.panel_nine.Hide()
        self.panel_eleven.Hide()
        self.panel_twelve.Hide()
        self.panel_thirteen.Hide()
        self.configureBruteForceQuickTest(None)

#-------------------------------------------------------------------
#           Start Network Server Brute Force Quick Test From Menu Function
#               This function Sets the current mode to Network Mode
#               Then hides all panels except for panel 9 (network server status screen)
#               Finally, it then calls the Configure Brute Force Quick Test Function
#-------------------------------------------------------------------
    def startNetworkServerBruteForceQuickTestFromMenu(self, event):
        self.panel_four.currentMode.SetLabel("Current Mode: Network Mode")
        self.panel_one.Hide()
        self.panel_two.Hide()
        self.panel_three.Hide()
        self.panel_four.Hide()
        self.panel_five.Hide()
        self.panel_six.Hide()
        self.panel_seven.Hide()
        self.panel_eight.Hide()
        self.panel_ten.Hide()
        self.panel_eleven.Hide()
        self.panel_twelve.Hide()
        self.panel_thirteen.Hide()
        self.configureBruteForceQuickTest(None)

#-----------------------------------------------------------------
#           Start Single Rainbow Table User Test From Menu Function
#               This function Sets the current mode to Single Mode
#               Then hides all panels except for panel 10 (single mode status screen)
#               Finally, it then calls the Configure Rainbow Table User Quick Test Function
#----------------------------------------------------------------
    def startSingleRainbowTableUserTestFromMenu(self, event):
        self.panel_eleven.currentMode.SetLabel("Current Mode: Single Mode")
        self.panel_one.Hide()
        self.panel_two.Hide()
        self.panel_three.Hide()
        self.panel_four.Hide()
        self.panel_five.Hide()
        self.panel_six.Hide()
        self.panel_seven.Hide()
        self.panel_eight.Hide()
        self.panel_nine.Hide()
        self.panel_eleven.Hide()
        self.panel_twelve.Hide()
        self.panel_thirteen.Hide()
        self.configureRainbowTableUserQuickTest(None)

#----------------------------------------------------------------
#           Start Network Server Rainbow Table User Quick Test From Menu Function
#               This function Sets the Current Mode to Network Mode
#               Then hides all panels except for panel 9 (network server status screen)
#               Finally, it then calls the Configure Rainbow Table User Quick Test Function
#----------------------------------------------------------------
    def startNetworkServerRainbowTableUserQuickTestFromMenu(self, event):
        self.panel_eleven.currentMode.SetLabel("Current Mode: Network Mode")
        self.panel_one.Hide()
        self.panel_two.Hide()
        self.panel_three.Hide()
        self.panel_four.Hide()
        self.panel_five.Hide()
        self.panel_six.Hide()
        self.panel_seven.Hide()
        self.panel_eight.Hide()
        self.panel_ten.Hide()
        self.panel_eleven.Hide()
        self.panel_twelve.Hide()
        self.panel_thirteen.Hide()
        self.configureRainbowTableUserQuickTest(None)

#---------------------------------------------------------------
#           Start Single Rainbow Table Maker Quick Test From Menu Function
#               This function Sets the Current Mode to Single Mode
#               Then hides all of the panels except for panel 10 (single mode status screen)
#               Finally, it then calls the Configure Rainbow Table Maker Quick Test Function
#---------------------------------------------------------------
    def startSingleRainbowTableMakerQuickTestFromMenu(self, event):
        self.panel_twelve.currentMode.SetLabel("Current Mode: Single Mode")
        self.panel_one.Hide()
        self.panel_two.Hide()
        self.panel_three.Hide()
        self.panel_four.Hide()
        self.panel_five.Hide()
        self.panel_six.Hide()
        self.panel_seven.Hide()
        self.panel_eight.Hide()
        self.panel_nine.Hide()
        self.panel_eleven.Hide()
        self.panel_twelve.Hide()
        self.panel_thirteen.Hide()
        self.configureRainbowTableMakerQuickTest(None)

#--------------------------------------------------------------
#           Start Network Server Rainbow Table Maker Quick Test From Menu Function
#               This function Sets the Current Mode to Network Mode
#               Then hides all panels except for panel 9 (network server status screen)
#               Finally, it then calls the Configure Rainbow Table Maker Quick Test Function
#-------------------------------------------------------------
    def startNetworkServerRainbowTableMakerQuickTestFromMenu(self, event):
        self.panel_twelve.currentMode.SetLabel("Current Mode: Network Mode")
        self.panel_one.Hide()
        self.panel_two.Hide()
        self.panel_three.Hide()
        self.panel_four.Hide()
        self.panel_five.Hide()
        self.panel_six.Hide()
        self.panel_seven.Hide()
        self.panel_eight.Hide()
        self.panel_ten.Hide()
        self.panel_eleven.Hide()
        self.panel_twelve.Hide()
        self.panel_thirteen.Hide()
        self.configureRainbowTableMakerQuickTest(None)

#=======================================================================================================================
#           Switch Panel Functions
#               These functions are called when a gui panel needs to transition to the next panel
#=======================================================================================================================
    #---------switch from Panel 1=======================================================================================
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
        self.resetDictionarySettingsToDefault(None) #reset all settings back to the defualt settings
        self.SetTitle("Mighty Cracker")
        self.panel_three.Hide()
        self.panel_one.Show()
        self.Layout()

    def switchFromPanel3ToPanel9(self):
        self.SetTitle("Mighty Cracker: Network Server Status Screen")
        self.panel_nine.currentCrackingMode.SetLabel("Cracking Mode: Dictionary")
        tempIP= self.get_ip()
        self.panel_nine.serverIPAddress.SetLabel("Server IP Address: "+str(tempIP))
        tempHash= self.panel_three.inputHashHeader.GetLabel()
        theHash=""
        for i in range(20,len(tempHash)):
            theHash+= tempHash[i]
        self.panel_nine.crackingThisHashHeader.SetLabel("Hash Being Cracked: "+str(theHash))
        self.panel_three.Hide()
        self.panel_nine.Show()
        self.panel_nine.timer.Start(1000)
        self.Layout()

    def switchFromPanel3ToPanel10(self):
        self.SetTitle("Mighty Cracker: Single Mode Status Screen")
        self.panel_ten.currentCrackingMode.SetLabel("Cracking Mode: Dictionary")
        tempHash= self.panel_three.inputHashHeader.GetLabel()
        theHash=""
        for i in range(20,len(tempHash)):
            theHash+= tempHash[i]
        self.panel_ten.hashBeingCrackedHeader.SetLabel("Hash Being Cracked: "+str(theHash))
        self.panel_three.Hide()
        self.panel_ten.Show()
        self.panel_ten.timer.Start(1000)
        self.Layout()
    #----------end switch from panel 3

    #--------switch from panel 4
    def switchFromPanel4ToPanel1(self, event):
        self.resetBruteForceSettingsToDefault(None) #reset the inputs back to their default settings
        self.SetTitle("Mighty Cracker")
        self.panel_four.Hide()
        self.panel_one.Show()
        self.Layout()

    def switchFromPanel4ToPanel9(self):
        self.SetTitle("Mighty Cracker: Network Server Status Screen")
        self.panel_nine.currentCrackingMode.SetLabel("Cracking Mode: Brute-Force")
        tempIP= self.get_ip()
        self.panel_nine.serverIPAddress.SetLabel("Server IP Address: "+str(tempIP))
        tempHash= self.panel_four.inputHashHeader.GetLabel()
        theHash=""
        for i in range(20,len(tempHash)):
            theHash+= tempHash[i]
        self.panel_nine.crackingThisHashHeader.SetLabel("Hash Being Cracked: "+str(theHash))
        self.panel_four.Hide()
        self.panel_nine.Show()
        self.panel_nine.timer.Start(1000)
        self.Layout()

    def switchFromPanel4ToPanel10(self):
        self.SetTitle("Mighty Cracker: Single Mode Status Screen")
        self.panel_ten.currentCrackingMode.SetLabel("Cracking Mode: Brute-Force")
        tempHash= self.panel_four.inputHashHeader.GetLabel()
        theHash=""
        for i in range(20,len(tempHash)):
            theHash+= tempHash[i]
        self.panel_ten.hashBeingCrackedHeader.SetLabel("Hash Being Cracked: "+str(theHash))
        self.panel_four.Hide()
        self.panel_ten.Show()
        self.panel_ten.timer.Start(1000)
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
        self.panel_eight.timer.Start(1000)
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
        self.resetRainbowTableCrackingSettingsToDefault(None) #reset all settings back to default
        self.SetTitle("Mighty Cracker")
        self.panel_eleven.Hide()
        self.panel_one.Show()
        self.Layout()

    def switchFromPanel11ToPanel9(self):
        self.SetTitle("Mighty Cracker: Network Server Status Screen")
        self.panel_nine.currentCrackingMode.SetLabel("Cracking Mode: Rainbow Table")
        tempIP= self.get_ip()
        self.panel_nine.serverIPAddress.SetLabel("Server IP Address: "+str(tempIP))
        tempHash= self.panel_eleven.hashToBeCrackedHeader.GetLabel()
        theHash=""
        for i in range(20,len(tempHash)):
            theHash+= tempHash[i]
        self.panel_nine.crackingThisHashHeader.SetLabel("Hash to be cracked: "+str(theHash))
        self.panel_eleven.Hide()
        self.panel_nine.Show()
        self.panel_nine.timer.Start(1000)
        self.Layout()

    def switchFromPanel11ToPanel10(self):
        self.SetTitle("Mighty Cracker: Single Mode Status Screen")
        self.panel_ten.currentCrackingMode.SetLabel("Cracking Mode: Rainbow Table User")
        tempHash= self.panel_eleven.hashToBeCrackedHeader.GetLabel()
        theHash=""
        for i in range(20,len(tempHash)):
            theHash+= tempHash[i]
        self.panel_ten.hashBeingCrackedHeader.SetLabel("Hash to be cracked: "+str(theHash))
        self.panel_eleven.Hide()
        self.panel_ten.Show()
        self.panel_ten.timer.Start(1000) #1000 milliseconds = 1 second
        self.Layout()
    #-----------end of switch from panel 11

    #------------switch from panel 12
    def switchFromPanel12ToPanel1(self, event):
        self.resetRainbowTableMakerSettingsToDefault(None) #resey all settings back to default
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
        self.panel_nine.timer.Start(1000)
        self.Layout()

    def switchFromPanel12ToPanel10(self):
        self.SetTitle("Mighty Cracker: Single Mode Status Screen")
        self.panel_ten.currentCrackingMode.SetLabel("Cracking Mode: Rainbow Table Maker")
        self.panel_twelve.Hide()
        self.panel_ten.Show()
        self.panel_ten.timer.Start(1000)
        self.Layout()
    #-------------end of switch from panel 12

    #--------------switch from panel 13
    def switchFromPanel13ToPanel1(self, event):
        self.SetTitle("Mighty Cracker")
        self.panel_thirteen.Hide()
        self.panel_one.Show()
        self.Layout()
    #------------end of switch from panel 13

#=======================================================================================================================
#           Defining Main Functions
#               These are the functions that are called by the main code
#=======================================================================================================================
#-----------------------------------------------------------
#           Show Not Finished Message 1 Function
#               This function creates a dialog window that informs the user that a function has not been completed yet.
#               This prevents the user from going to the screen that the particular button went to.
#               Primary Purpose for this was debugging purposes indicating something was not completed yet.
#-----------------------------------------------------------
    def ShowNotFinishedMessage1(self, event):
        dial= wx.MessageDialog(None, 'This function has not been completed yet', 'Notice:', wx.OK)
        dial.ShowModal()

#--------------------------------------------------------------
#           Update Single Timer Function (Used in Single Mode)
#               This function is repeatedly called while a search is being conducted.
#               If the shutdown flag is not set, this function:
#                   -Sets the percent complete value to zero
#                   -If the total chunks value is greater than 0, then set the percent Complete value to
#                    number of finished chunks / number of total chunks
#                   -Set the new percent complete value
#                   -Set the number of completed chunks to the number of finished chunks
#                   -Set the number of total chunks label to the number of total chunks value
#                   -Set the Current Status label to say 'Searching'
#                   -If running OS X or Linux, check to see if the activity gauge is filled. If it is filled, set the activity
#                    gauge to be empty. If not filled, increment the activity guage by 10.
#                   -NOTE: If running windows, the activity gauge pulses properly
#                   -If in the Rainbow Table Maker Cracking Mode, set the hash to be cracked label to say 'There is no
#                    hash to be cracked in this mode'
#                   -Clear the update flag
#               Else if the shutdown flag has been set, this function:
#                   -Set the number of completed chunks label to the number of finished chunks value
#                   -Set the number of total chunks label to the number of total chunks value
#                   -Set the activity gauge to full (on windows, this stops the gauge pulsing also)
#                   -Set the progress bar to full
#                   -If a solution was not found, check to see if in Rainbow Table Maker Cracking Mode. If in Rainbow Table
#                    Maker Cracking Mode, set the solution header label to say 'There are no solutions for this mode'
#                    and set the current Status label to say 'Finished Creating Rainbow Table'
#                    If not in Rainbow Table Maker Cracking Mode, set the solution header label to say 'No solution
#                    found' and set the current Status label to say 'Finished Searching, no solution found.' (For this
#                    change the solution text color to red and change the font size)
#                   -If a solution was found, set the solution header label to say what the solution was.
#                    Then change the color of the solution text to be green and change the font size. Also, set the
#                    current Status Label to say 'Finished Searching, Solution was found'
#----------------------------------------------------------------
    def updateSingleTimer(self,  event):
        if(not self.shutdown.is_set()):
            percentComplete= 0
            if(int(self.dictionary["total chunks"]) > 0):
                percentComplete= 100 * float(float(self.dictionary['finished chunks']) / float(self.dictionary['total chunks']))
            self.panel_ten.progressBar.SetValue(percentComplete)
            self.panel_ten.numCompletedChunksHeader.SetLabel("Number of Completed Chunks: "+str(self.dictionary["finished chunks"]))
            self.panel_ten.numTotalChunksHeader.SetLabel("Total Number of Chunks: "+str(self.dictionary["total chunks"]))

            self.panel_ten.currentStatus.SetLabel("Current Status: Searching")

            if(self.compareString(self.theDetectedOS, "Linux",0,0,len("Linux"),len("Linux"))==True): #if running linux
                currentGaugeValue= self.panel_ten.activityGauge.GetValue()
                if(currentGaugeValue == 100):
                    self.panel_ten.activityGauge.SetValue(0)
                else:
                    self.panel_ten.activityGauge.SetValue(currentGaugeValue + 10)
            elif(self.compareString(self.theDetectedOS, "Darwin",0,0,len("Darwin"),len("Darwin"))==True):
                currentGaugeValue= self.panel_ten.activityGauge.GetValue()
                if(currentGaugeValue == 100):
                    self.panel_ten.activityGauge.SetValue(0)
                else:
                    self.panel_ten.activityGauge.SetValue(currentGaugeValue + 10)

            if(self.compareString(self.panel_ten.currentCrackingMode.GetLabel(),"Cracking Mode: Rainbow Table Maker",0,0,
                                  len("Cracking Mode: Rainbow Table Maker"),len("Cracking Mode: Rainbow Table Maker"))==True):
                self.panel_ten.hashBeingCrackedHeader.SetLabel("Hash Being Cracked: There is no hash to be cracked for this mode")

            self.update.clear()
        else: #if shutdown is set
            self.panel_ten.numCompletedChunksHeader.SetLabel("Number of Completed Chunks: "+str(self.dictionary["finished chunks"]))
            self.panel_ten.numTotalChunksHeader.SetLabel("Total Number of Chunks: "+str(self.dictionary["total chunks"]))
            self.panel_ten.activityGauge.SetValue(100) #set value to maximum to fill the gauge
            self.panel_ten.progressBar.SetValue(100) #set progress bar value to maximum to fill the gauge

            if(len(self.dictionary["key"]) < 1): #if no solution was found
                if(self.compareString(self.panel_ten.currentCrackingMode.GetLabel(),"Cracking Mode: Rainbow Table Maker",0,0,
                                      len("Cracking Mode: Rainbow Table Maker"),len("Cracking Mode: Rainbow Table Maker"))==True):
                    self.panel_ten.SolutionHeader.SetLabel("Solution: There is no solution for this mode")
                    self.panel_ten.currentStatus.SetLabel("Current Status: Finished Creating Rainbow Table")
                else:
                    self.panel_ten.SolutionHeader.SetLabel("Solution: Sorry, but no solution found")
                    self.panel_ten.SolutionHeader.SetForegroundColour((255,0,0)) #change text color to red
                    self.panel_ten.SolutionHeader.SetFont(self.enlargedSolutionFont)
                    self.panel_ten.currentStatus.SetLabel("Current Status: Finished Searching, No Solution Found")
            else: #if a solution was found
                self.panel_ten.SolutionHeader.SetLabel("Solution: "+str(self.dictionary["key"]))
                self.panel_ten.SolutionHeader.SetForegroundColour((0,255,0)) #change text color to green
                self.panel_ten.SolutionHeader.SetFont(self.enlargedSolutionFont)
                self.panel_ten.currentStatus.SetLabel("Current Status: Finished Searching, Solution was Found!")

#-------------------------------------------------------------
#           Update Network Server Timer Function
#               This function is repeatedly called while a search is being conducted.
#               If the shutdown flag is not set, this function:
#                   -Sets the percent complete value to zero
#                   -If the total chunks value is greater than 0, then set the percent Complete value to
#                    number of finished chunks / number of total chunks
#                   -Set the new percent complete value
#                   -Set the number of completed chunks to the number of finished chunks
#                   -Set the number of total chunks label to the number of total chunks value
#                   -Set the Current Status label to say 'Searching'
#                   -If running OS X or Linux, check to see if the activity gauge is filled. If it is filled, set the activity
#                    gauge to be empty. If not filled, increment the activity guage by 10.
#                   -NOTE: If running windows, the activity gauge pulses properly
#                   -If in the Rainbow Table Maker Cracking Mode, set the hash to be cracked label to say 'There is no
#                    hash to be cracked in this mode'
#                   -Clear the update flag
#               Else if the shutdown flag has been set, this function:
#                   -Set the number of completed chunks label to the number of finished chunks value
#                   -Set the number of total chunks label to the number of total chunks value
#                   -Set the activity gauge to full (on windows, this stops the gauge pulsing also)
#                   -Set the progress bar to full
#                   -If a solution was not found, check to see if in Rainbow Table Maker Cracking Mode. If in Rainbow Table
#                    Maker Cracking Mode, set the solution header label to say 'There are no solutions for this mode'
#                    and set the current Status label to say 'Finished Creating Rainbow Table'
#                    If not in Rainbow Table Maker Cracking Mode, set the solution header label to say 'No solution
#                    found' and set the current Status label to say 'Finished Searching, no solution found.' (For this
#                    change the solution text color to red and change the font size)
#                   -If a solution was found, set the solution header label to say what the solution was.
#                    Then change the color of the solution text to be green and change the font size. Also, set the
#                    current Status Label to say 'Finished Searching, Solution was found'
#----------------------------------------------------------------
    def updateNetworkServerTimer(self, event):
        if(not self.shutdown.is_set()):
            percentComplete= 0
            if(int(self.dictionary["total chunks"]) > 0):
                percentComplete= 100 * float(float(self.dictionary['finished chunks']) / float(self.dictionary['total chunks']))
            self.panel_nine.progressBar.SetValue(percentComplete)
            self.panel_nine.numCompletedChunksHeader.SetLabel("Number of Completed Chunks: "+str(self.dictionary["finished chunks"]))
            self.panel_nine.numTotalChunksHeader.SetLabel("Total Number of Chunks: "+str(self.dictionary["total chunks"]))
            self.panel_nine.currentStatus.SetLabel("Current Status: Searching")
            if(self.compareString(self.theDetectedOS, "Linux",0,0,len("Linux"),len("Linux"))==True): #if running linux
                currentGaugeValue= self.panel_nine.activityGauge.GetValue()
                if(currentGaugeValue == 100):
                    self.panel_nine.activityGauge.SetValue(0)
                else:
                    self.panel_nine.activityGauge.SetValue(currentGaugeValue + 10)
            elif(self.compareString(self.theDetectedOS, "Darwin",0,0,len("Darwin"),len("Darwin"))==True):
                currentGaugeValue= self.panel_nine.activityGauge.GetValue()
                if(currentGaugeValue == 100):
                    self.panel_nine.activityGauge.SetValue(0)
                else:
                    self.panel_nine.activityGauge.SetValue(currentGaugeValue + 10)
            if(self.compareString(self.panel_nine.currentCrackingMode.GetLabel(),"Cracking Mode: Rainbow Table Maker",0,0,
                                  len("Cracking Mode: Rainbow Table Maker"),len("Cracking Mode: Rainbow Table Maker"))==True):
                self.panel_nine.crackingThisHashHeader.SetLabel("Hash Being Cracked: There is no hash to be cracked for this mode")
            self.update.clear()
        else: #if shutdown flag has been set
            self.panel_nine.numCompletedChunksHeader.SetLabel("Number of Completed Chunks: "+str(self.dictionary["finished chunks"]))
            self.panel_nine.numTotalChunksHeader.SetLabel("Total Number of Chunks: "+str(self.dictionary["total chunks"]))
            self.panel_nine.activityGauge.SetValue(100) #set value to maximum to fill the gauge
            self.panel_nine.progressBar.SetValue(100) #set progress bar value to maximum to fill the gauge
            if(len(self.dictionary["key"]) < 1): #if no solution was found
                if(self.compareString(self.panel_nine.currentCrackingMode.GetLabel(),"Cracking Mode: Rainbow Table Maker",0,0,
                                      len("Cracking Mode: Rainbow Table Maker"),len("Cracking Mode: Rainbow Table Maker"))==True):
                    self.panel_nine.SolutionHeader.SetLabel("Solution: There is no solutions for this mode")
                    self.panel_nine.currentStatus.SetLabel("Current Status: Finished Creating Rainbow Table")
                else:
                    self.panel_nine.SolutionHeader.SetLabel("Solution: Sorry, but no solution found")
                    self.panel_nine.SolutionHeader.SetForegroundColour((255,0,0)) #set text color to red
                    self.panel_nine.SolutionHeader.SetFont(self.enlargedSolutionFont)
                    self.panel_nine.currentStatus.SetLabel("Current Status: Finished Searching, No Solution Found")
            else: #if a solution was found
                self.panel_nine.SolutionHeader.SetLabel("Solution: "+str(self.dictionary["key"]))
                self.panel_nine.SolutionHeader.SetForegroundColour((0,255,0)) #set text color to green
                self.panel_nine.SolutionHeader.SetFont(self.enlargedSolutionFont)
                self.panel_nine.currentStatus.SetLabel("Current Status: Finished Searching, Solution was Found!")

#-----------------------------------------------------------------
#           Update Network Client Timer Function
#               This function is repeatedly called while a search is being conducted.
#               If the shutdown flag is not set, this function:
#                   -(If running OS X or Linux) checks to see the activity gauge of the Network Client is completely filled,
#                    if it is, then reset it back to empty. If not full, then increment the activity guage by 10.
#                   -NOTE: If running windows, the activity gauge pulses properly.
#               Else if the shutdown flag is set, then this function:
#                   -Sets the Current Status Label to say 'Finished Searching'
#                   -Fills the activity gauge to full (regardless of OS)
#                   -If a solution was found, change the solution header label to print out the solution
#                   -If no solution was found, change the solution header label to say 'No solution was found'
#-----------------------------------------------------------------
    def updateNetworkClientTimer(self, event):
        if(not self.shutdown.is_set()):
            if(self.compareString(self.theDetectedOS, "Linux",0,0,len("Linux"),len("Linux"))==True): #if running linux
                currentGaugeValue= self.panel_eight.activityGauge.GetValue()
                if(currentGaugeValue == 100):
                    self.panel_eight.activityGauge.SetValue(0)
                else:
                    self.panel_eight.activityGauge.SetValue(currentGaugeValue + 10)
            elif(self.compareString(self.theDetectedOS, "Darwin",0,0,len("Darwin"),len("Darwin"))==True):
                currentGaugeValue= self.panel_eight.activityGauge.GetValue()
                if(currentGaugeValue == 100):
                    self.panel_eight.activityGauge.SetValue(0)
                else:
                    self.panel_eight.activityGauge.SetValue(currentGaugeValue + 10)

        else: #if shutdown variable is set
            self.panel_eight.currentStatus.SetLabel("Current Status: Finished Searching")
            self.panel_eight.activityGauge.SetValue(100) #set value to 100 to fill the activity gauge
            if(len(self.dictionary["key"])<1):  #if no solution was found
                self.panel_eight.solutionHeader.SetLabel("Solution: Sorry, No Solution Was Found")
            else:      #if there was a found solution
                self.panel_eight.solutionHeader.SetLabel("Solution: "+str(self.dictionary["key"]))

#------------------------------------------------------------
#           Configure Dictionary Quick Test Function
#               This function sets the Dictionary Crack settings to a predefined default value and then calls
#               the Validate Dictionary Inputs Function
#------------------------------------------------------------
    def configureDictionaryQuickTest(self, event):
        self.panel_three.selectedAlgorithm.SetValue("MD5")
        self.panel_three.selectedHashingMode.SetValue("Individual Hash Code")
        self.panel_three.inputHashHeader.SetLabel("Hash to be Cracked: 33da7a40473c1637f1a2e142f4925194")
        self.panel_three.inputDictFileHeader.SetLabel("Selected Dictionary File: dic.txt")
        fakeVariable= ""
        self.validateDictionaryInputs(fakeVariable)

#-----------------------------------------------------------
#           Configure Brute Force Quick Test Function
#               This function sets the Brute Force Crack settings to a predefined default value and then calls
#               the Validate Brute Force Inputs Function
#-----------------------------------------------------------
    def configureBruteForceQuickTest(self,event):
        self.panel_four.selectedAlgorithm.SetValue("MD5")
        self.panel_four.inputHashHeader.SetLabel("Hash To Be Cracked: 98ae126efdbc62e121649406c83337d9")
        self.panel_four.minKeyLengthHeader.SetLabel("Min Key Length: 4")
        self.panel_four.maxKeyLengthHeader.SetLabel("Max Key Length: 6")
        self.panel_four.selectedAlphabet.SetValue("Lowercase Letters")
        fakeVariable= ""
        self.validateBruteForceInputs(fakeVariable)

#------------------------------------------------------------
#           Configure Rainbow Table User Quick Test Function
#               This function sets the Rainbow Table Crack settings to a predefined default value and then calls
#               the Validate Rainbow Table Inputs Function
#------------------------------------------------------------
    def configureRainbowTableUserQuickTest(self, event):
        self.panel_eleven.selectedAlgorithm.SetValue("MD5")
        self.panel_eleven.selectedFileHeader.SetLabel("Selected Rainbow Table File: rain.txt")
        self.panel_eleven.hashToBeCrackedHeader.SetLabel("Hash to be cracked: 33da7a40473c1637f1a2e142f4925194")
        fakeVariable= ""
        self.validateRainbowTableUserInputs(fakeVariable)

#------------------------------------------------------------
#           Configure Rainbow Table Maker Quick Test Function
#               This function sets the Rainbow Table Maker settings to a predefined default value and then calls
#               the Validate Rainbow Table Maker Inputs Function.
#------------------------------------------------------------
    def configureRainbowTableMakerQuickTest(self, event):
        self.panel_twelve.selectedAlgorithm.SetValue("MD5")
        self.panel_twelve.keyLengthHeader.SetLabel("Key Length: 10")
        self.panel_twelve.selectedAlphabet.SetValue("Lowercase Letters")
        self.panel_twelve.chainLengthHeader.SetLabel("Table Chain Length: 100")
        self.panel_twelve.numOfRowsHeader.SetLabel("Number of Rows: 100")
        self.panel_twelve.fileNameHeader.SetLabel("Save Rainbow Table File As: myRainbowTable.txt")
        fakeVariable= ""
        self.validateRainbowTableMakerInputs(fakeVariable)

#----------------------------------------------------------
#           Validate Dictionary Inputs Function
#               This function checks to make sure that all of the input settings for Dictionary are valid.
#               First, checks to make sure that the selected algorithm is valid.
#               Then checks to make sure that the selected hashing mode is valid.
#               Then checks to make sure that the hash to be cracked value is not its default text.
#               Then checks to make sure the hash code to be cracked is the correct amount of characters based on the
#               selected algorithm.
#               Then checks to make sure that the selected dictionary file is not the default text.
#               Finally, evaluates whether or not any of the checks failed.
#               Any checks that failed are listed in a message box window that is displayed to the user.
#               If all checks succeeded, then the function calls the Start Dictionary Crack Function
#---------------------------------------------------------------------
    def validateDictionaryInputs(self, event): #call start dictionary if valid, else display dial error
        foundInvalidInput= "False"
        invalidAlgorithm= "False"
        inputAlgorithm= "" #added to store which algorithm was being used
        invalidHashingMode= "False"
        invalidHashToBeCracked= "False"
        invalidHashLength= "False" #added to indicate an ivalid length of hash based on the algorithm
        invalidDictionaryFile= "False"

        #check for valid algorithm
        if(self.compareString(self.panel_three.selectedAlgorithm.GetValue(), "MD5",0,0,len("MD5"),len("MD5"))==True):
            inputAlgorithm= "MD5"
        elif(self.compareString(self.panel_three.selectedAlgorithm.GetValue(), "SHA1",0,0,len("SHA1"),len("SHA1"))==True):
            inputAlgorithm= "SHA1"
        elif(self.compareString(self.panel_three.selectedAlgorithm.GetValue(), "SHA224",0,0,len("SHA224"),len("SHA224"))==True):
            inputAlgorithm= "SHA224"
        elif(self.compareString(self.panel_three.selectedAlgorithm.GetValue(), "SHA256",0,0,len("SHA256"),len("SHA256"))==True):
            inputAlgorithm= "SHA256"
        elif(self.compareString(self.panel_three.selectedAlgorithm.GetValue(), "SHA384",0,0,len("SHA384"),len("SHA384"))==True):
            inputAlgorithm= "SHA384"
        elif(self.compareString(self.panel_three.selectedAlgorithm.GetValue(), "SHA512",0,0,len("SHA512"),len("SHA512"))==True):
            inputAlgorithm= "SHA512"
        else:
            foundInvalidInput= "True"
            invalidAlgorithm= "True"

        #check for valid selected hashing mode
        if(self.compareString(self.panel_three.selectedHashingMode.GetValue(), "Individual Hash Code",0,0,len("Individual Hash Code"),len("Individual Hash Code"))==True):
            fakeVariable= False
        elif(self.compareString(self.panel_three.selectedHashingMode.GetValue(), "File of Hash Codes",0,0,len("File of Hash Codes"),len("File of Hash Codes"))==True):
            fakeVariable= False
        else:
            foundInvalidInput= "True"
            invalidHashingMode= "True"

        #check for valid hash to be cracked value
        if(self.compareString(self.panel_three.inputHashHeader.GetLabel(),"Hash to be Cracked: No Hash has been input",0,0,len("Hash to be Cracked: No Hash has been input"),len("Hash to be Cracked: No Hash has been input"))==True):
            foundInvalidInput= "True"
            invalidHashToBeCracked= "True"

        #check for valid hash code length
        if(self.compareString(inputAlgorithm, "MD5",0,0,len("MD5"),len("MD5"))==True):
            if(len(self.panel_three.inputHashHeader.GetLabel()) < 52):
                foundInvalidInput= "True"
                invalidHashLength= "True"
            elif(len(self.panel_three.inputHashHeader.GetLabel()) > 52):
                foundInvalidInput= "True"
                invalidHashLength= "True"

        elif(self.compareString(inputAlgorithm, "SHA1",0,0,len("SHA1"),len("SHA1"))==True):
            if(len(self.panel_three.inputHashHeader.GetLabel()) < 60):
                foundInvalidInput= "True"
                invalidHashLength= "True"
            elif(len(self.panel_three.inputHashHeader.GetLabel()) > 60):
                foundInvalidInput= "True"
                invalidHashLength= "True"

        elif(self.compareString(inputAlgorithm, "SHA224",0,0,len("SHA224"),len("SHA224"))==True):
            if(len(self.panel_three.inputHashHeader.GetLabel()) < 76):
                foundInvalidInput= "True"
                invalidHashLength= "True"
            elif(len(self.panel_three.inputHashHeader.GetLabel()) > 76):
                foundInvalidInput= "True"
                invalidHashLength= "True"

        elif(self.compareString(inputAlgorithm, "SHA256",0,0,len("SHA256"),len("SHA256"))==True):
            if(len(self.panel_three.inputHashHeader.GetLabel()) < 84):
                foundInvalidInput= "True"
                invalidHashLength= "True"
            elif(len(self.panel_three.inputHashHeader.GetLabel()) > 84):
                foundInvalidInput= "True"
                invalidHashLength= "True"

        elif(self.compareString(inputAlgorithm, "SHA384",0,0,len("SHA384"),len("SHA384"))==True):
            if(len(self.panel_three.inputHashHeader.GetLabel()) < 116):
                foundInvalidInput= "True"
                invalidHashLength= "True"
            elif(len(self.panel_three.inputHashHeader.GetLabel()) > 116):
                foundInvalidInput= "True"
                invalidHashLength= "True"

        elif(self.compareString(inputAlgorithm, "SHA512",0,0,len("SHA512"),len("SHA512"))==True):
            if(len(self.panel_three.inputHashHeader.GetLabel()) < 148):
                foundInvalidInput= "True"
                invalidHashLength= "True"
            elif(len(self.panel_three.inputHashHeader.GetLabel()) > 148):
                foundInvalidInput= "True"
                invalidHashLength= "True"

        #check for valid input dictionary file
        if(self.compareString(self.panel_three.inputDictFileHeader.GetLabel(),"Selected Dictionary File: No Dictionary File Selected",0,0,len("Selected Dictionary File: No Dictionary File Selected"),len("Selected Dictionary File: No Dictionary File Selected"))==True):
            foundInvalidInput= "True"
            invalidDictionaryFile= "True"

        #check to see if invalidinput was found
        if(self.compareString(foundInvalidInput, "False",0,0,len("False"),len("False"))==True): #no invalid entries
            self.startDictionaryCrack()
        else: #if invalid input detected
            invalidInputString= ""
            if(self.compareString(invalidAlgorithm, "True",0,0,len("True"),len("True"))==True):
                invalidInputString+= "Invalid Algorithm Detected \n"
            if(self.compareString(invalidHashingMode, "True",0,0,len("True"),len("True"))==True):
                invalidInputString+= "Invalid Hashing Mode Detected \n"
            if(self.compareString(invalidHashToBeCracked, "True",0,0,len("True"),len("True"))==True):
                invalidInputString+= "Invalid Hash to be Cracked Detected \n"
            if(self.compareString(invalidHashLength, "True",0,0,len("True"),len("True"))==True):
                invalidInputString+= "Invalid Hash length detected \n" \
                                     "  Proper MD5 length: 32 \n" \
                                     "  Proper SHA1 length: 40 \n" \
                                     "  Proper SHA224 length: 56 \n" \
                                     "  Proper SHA256 length: 64 \n" \
                                     "  Proper SHA384 length: 94 \n" \
                                     "  Proper SHA512 length: 128 \n"
            if(self.compareString(invalidDictionaryFile, "True",0,0,len("True"),len("True"))==True):
                invalidInputString+= "Invalid Dictionary File Detected \n"
            dial= wx.MessageBox(invalidInputString, "Invalid Input/Selection Detected", wx.OK, self)
        #end of validate dictionary input

#------------------------------------------------------------------
#           Validate Brute Force Inputs Function
#               This function checks to make sure that all of the input settings for Brute Force are valid.
#               First, checks to make sure that a valid algorithm is selected.
#               Then checks to make sure that the hash to be cracked is not the default text.
#               Then checks to make sure the hash to be cracked is the correct amount of characters based on
#               the selected algorithm.
#               Then checks to make sure the min key length value was left blank.
#               Then checks to make sure the max key length value was not left blank.
#               Then checks to make sure that the min key length value is less than or equal to the max key length value.
#               Then checks to make sure that the selected alphabet is valid.
#               Finally, evaluates whether or not any of the checks failed.
#               Any checks that failed are listed in a message box window that is displayed to the user.
#               If all checks succeeded, then the function calls the Start Brute Force Crack Function
#---------------------------------------------------------------------
    def validateBruteForceInputs(self, event):
        foundInvalidInput= "False"
        invalidAlgorithm= "False"
        inputAlgorithm= "" #store which algorithm is being used so that length can compare for proper length
        invalidHashToBeCracked= "False"
        invalidHashLength= "False"
        invalidMinKeyInput= "False"
        tempMinKey= 0
        invalidMaxKeyInput= "False"
        tempMaxKey= 0
        minKeyLessThanMaxKey= "True"
        invalidAlphabet= "False"

        #check for valid algorithm
        if(self.compareString(self.panel_four.selectedAlgorithm.GetValue(), "MD5",0,0,len("MD5"),len("MD5"))==True):
            inputAlgorithm= "MD5"
        elif(self.compareString(self.panel_four.selectedAlgorithm.GetValue(), "SHA1",0,0,len("SHA1"),len("SHA1"))==True):
            inputAlgorithm= "SHA1"
        elif(self.compareString(self.panel_four.selectedAlgorithm.GetValue(), "SHA224",0,0,len("SHA224"),len("SHA224"))==True):
            inputAlgorithm= "SHA224"
        elif(self.compareString(self.panel_four.selectedAlgorithm.GetValue(), "SHA256",0,0,len("SHA256"),len("SHA256"))==True):
            inputAlgorithm= "SHA256"
        elif(self.compareString(self.panel_four.selectedAlgorithm.GetValue(), "SHA384",0,0,len("SHA384"),len("SHA384"))==True):
            inputAlgorithm= "SHA384"
        elif(self.compareString(self.panel_four.selectedAlgorithm.GetValue(), "SHA512",0,0,len("SHA512"),len("SHA512"))==True):
            inputAlgorithm= "SHA512"
        else:
            foundInvalidInput= "True"
            invalidAlgorithm= "True"

        #check for valid hash to be cracked value
        if(self.compareString(self.panel_four.inputHashHeader.GetLabel(),"Hash To Be Cracked: No Hash has been Input",0,0,len("Hash To Be Cracked: No Hash has been Input"),len("Hash To Be Cracked: No Hash has been Input"))==True):
            foundInvalidInput= "True"
            invalidHashToBeCracked= "True"

        #check for hash code length
        if(self.compareString(inputAlgorithm, "MD5",0,0,len("MD5"),len("MD5"))==True):
            if(len(self.panel_four.inputHashHeader.GetLabel()) < 52):
                foundInvalidInput= "True"
                invalidHashLength= "True"
            elif(len(self.panel_four.inputHashHeader.GetLabel()) > 52):
                foundInvalidInput= "True"
                invalidHashLength= "True"

        elif(self.compareString(inputAlgorithm, "SHA1",0,0,len("SHA1"),len("SHA1"))==True):
            if(len(self.panel_four.inputHashHeader.GetLabel()) < 60):
                foundInvalidInput= "True"
                invalidHashLength= "True"
            elif(len(self.panel_four.inputHashHeader.GetLabel()) > 60):
                foundInvalidInput= "True"
                invalidHashLength= "True"

        elif(self.compareString(inputAlgorithm, "SHA224",0,0,len("SHA224"),len("SHA224"))==True):
            if(len(self.panel_four.inputHashHeader.GetLabel()) < 76):
                foundInvalidInput= "True"
                invalidHashLength= "True"
            elif(len(self.panel_four.inputHashHeader.GetLabel()) > 76):
                foundInvalidInput= "True"
                invalidHashLength= "True"

        elif(self.compareString(inputAlgorithm, "SHA256",0,0,len("SHA256"),len("SHA256"))==True):
            if(len(self.panel_four.inputHashHeader.GetLabel()) < 84):
                foundInvalidInput= "True"
                invalidHashLength= "True"
            elif(len(self.panel_four.inputHashHeader.GetLabel()) > 84):
                foundInvalidInput= "True"
                invalidHashLength= "True"

        elif(self.compareString(inputAlgorithm, "SHA384",0,0,len("SHA384"),len("SHA384"))==True):
            if(len(self.panel_four.inputHashHeader.GetLabel()) < 114):
                foundInvalidInput= "True"
                invalidHashLength= "True"
            elif(len(self.panel_four.inputHashHeader.GetLabel()) > 114):
                foundInvalidInput= "True"
                invalidHashLength= "True"

        elif(self.compareString(inputAlgorithm, "SHA512",0,0,len("SHA512"),len("SHA512"))==True):
            if(len(self.panel_four.inputHashHeader.GetLabel()) < 148):
                foundInvalidInput= "True"
                invalidHashLength= "True"
            elif(len(self.panel_four.inputHashHeader.GetLabel()) > 148):
                foundInvalidInput= "True"
                invalidHashLength= "True"

        #check for valid min key length
        if(len(str(self.panel_four.minKeyLengthHeader.GetLabel())) <= len("Min Key Length: ")):
            foundInvalidInput= "True"
            invalidMinKeyInput= "True"

        #check for valid max key length
        if(len(str(self.panel_four.maxKeyLengthHeader.GetLabel())) <= len("Max Key Length: ")):
            foundInvalidInput= "True"
            invalidMaxKeyInput= "True"

        #check to make sure that the min key is less than or equal to max key
        tempMaxKey1=""
        tempMinKey1=""
        for i in range(16,len(str(self.panel_four.minKeyLengthHeader.GetLabel()))):
            tempMinKey1+= str(self.panel_four.minKeyLengthHeader.GetLabel()[i])
        for j in range(15, len(str(self.panel_four.maxKeyLengthHeader.GetLabel()))):
            tempMaxKey1+= str(self.panel_four.maxKeyLengthHeader.GetLabel()[j])
        if(int(tempMinKey1) <= int(tempMaxKey1)):
            fakeVariable= False;
        else:
            foundInvalidInput= "True"
            minKeyLessThanMaxKey= "False"

        #check for valid selected alphabet
        if(self.compareString(self.panel_four.selectedAlphabet.GetValue(), "All",0,0,len("All"),len("All"))==True):
            fakeVariable= False;
        elif(self.compareString(self.panel_four.selectedAlphabet.GetValue(), "Letters and Digits",0,0,len("Letters and Digits"),len("Letters and Digits"))==True):
            fakeVariable= False;
        elif(self.compareString(self.panel_four.selectedAlphabet.GetValue(), "Letters and Punctuation",0,0,len("Letters and Punctuation"),len("Letters and Punctuation"))==True):
            fakeVariable= False;
        elif(self.compareString(self.panel_four.selectedAlphabet.GetValue(), "Letters Only",0,0,len("Letters Only"),len("Letters Only"))==True):
            fakeVariable= False;
        elif(self.compareString(self.panel_four.selectedAlphabet.GetValue(), "Uppercase Letters",0,0,len("Uppercase Letters"),len("Uppercase Letters"))==True):
            fakeVariable= False;
        elif(self.compareString(self.panel_four.selectedAlphabet.GetValue(), "Lowercase Letters",0,0,len("Lowercase Letters"),len("Lowercase Letters"))==True):
            fakeVariable= False;
        elif(self.compareString(self.panel_four.selectedAlphabet.GetValue(), "Digits",0,0,len("Digits"),len("Digits"))==True):
            fakeVariable= False;
        else:
            foundInvalidInput= "True"
            invalidAlphabet= "True"

        #check to see if any invalid input was detected
        if(self.compareString(foundInvalidInput, "False",0,0,len("False"),len("False"))==True):
            self.startBruteForceCrack()
        else:
            invalidInputString= ""
            if(self.compareString(invalidAlgorithm, "True",0,0,len("True"),len("True"))==True):
                invalidInputString+= "Invalid Algorithm Selected \n"
            if(self.compareString(invalidHashToBeCracked, "True",0,0,len("True"),len("True"))==True):
                invalidInputString+= "Invalid Hash to be cracked value detected \n"
            if(self.compareString(invalidHashLength, "True",0,0,len("True"),len("True"))==True):
                invalidInputString+= "Invalid Hash length detected \n" \
                                     "  Proper MD5 length: 32 \n" \
                                     "  Proper SHA1 length: 40 \n" \
                                     "  Proper SHA224 length: 56 \n" \
                                     "  Proper SHA256 length: 64 \n" \
                                     "  Proper SHA384 length: 94 \n" \
                                     "  Proper SHA512 length: 128 \n"
            if(self.compareString(invalidMinKeyInput, "True",0,0,len("True"),len("True"))==True):
                invalidInputString+= "Invalid Min Key Input Detected \n"
            if(self.compareString(invalidMaxKeyInput, "True",0,0,len("True"),len("True"))==True):
                invalidInputString+= "Invalid Max key input detected \n"
            if(self.compareString(minKeyLessThanMaxKey, "False",0,0,len("False"),len("False"))==True):
                invalidInputString+= "Invalid key values, min key must be equal to or less than max key \n"
            if(self.compareString(invalidAlphabet, "True",0,0,len("True"),len("True"))==True):
                invalidInputString+= "Invalid Alphabet selected \n"
            dial= wx.MessageBox(invalidInputString, "Invalid Input/Selection Detected", wx.OK, self)
        #end of validate brute force inputs

#------------------------------------------------------------------------
#           Validate Rainbow Table User Inputs Function
#               This function checks to make sure that all of the input settings for Rainbow Table User are valid.
#               First, checks to make sure that a valid algorithm was selected.
#               Then checks to make sure that the selected Rainbow Table File is not the default value.
#               Then checks to make sure that the hash to be cracked is not the default text.
#               Then checks to make sure that the hash to be cracked is the correct amount of characters based on the
#               selected algorithm.
#               Finally, evaluates whether or not any of the checks failed.
#               Any checks that failed are listed in a message box window that is displayed to the user.
#               If all checks succeeded, then the function calls the Start Rainbow Table Crack Function
#---------------------------------------------------------------------
    def validateRainbowTableUserInputs(self, event):
        foundInvalidInput= "False"
        invalidAlgorithm= "False"
        inputAlgorithm= ""#used to check the length of the hash
        invalidFile= "False"
        invalidHash="False"
        invalidHashLength= "False"

        #check for valid selected algorithm
        if(self.compareString(self.panel_eleven.selectedAlgorithm.GetValue(), "MD5",0,0,len("MD5"),len("MD5"))==True):
            inputAlgorithm= "MD5"
        elif(self.compareString(self.panel_eleven.selectedAlgorithm.GetValue(), "SHA1",0,0,len("SHA1"),len("SHA1"))==True):
            inputAlgorithm= "SHA1"
        elif(self.compareString(self.panel_eleven.selectedAlgorithm.GetValue(), "SHA224",0,0,len("SHA224"),len("SHA224"))==True):
            inputAlgorithm= "SHA224"
        elif(self.compareString(self.panel_eleven.selectedAlgorithm.GetValue(), "SHA256",0,0,len("SHA256"),len("SHA256"))==True):
            inputAlgorithm= "SHA256"
        elif(self.compareString(self.panel_eleven.selectedAlgorithm.GetValue(), "SHA384",0,0,len("SHA384"),len("SHA384"))==True):
            inputAlgorithm= "SHA384"
        elif(self.compareString(self.panel_eleven.selectedAlgorithm.GetValue(), "SHA512",0,0,len("SHA512"),len("SHA512"))==True):
            inputAlgorithm= "SHA512"
        else:
            foundInvalidInput= "True"
            invalidAlgorithm= "True"

        #check for valid rainbow table file
        if(self.compareString(self.panel_eleven.selectedFileHeader.GetLabel(),"Selected Rainbow Table File: No File has been Selected",0,0,len("Selected Rainbow Table File: No File has been Selected"),len("Selected Rainbow Table File: No File has been Selected"))==True):
            foundInvalidInput= "True"
            invalidFile= "True"

        #check for valid hash to be cracked
        if(self.compareString(self.panel_eleven.hashToBeCrackedHeader.GetLabel(),"Hash to be cracked: No Hash has been entered",0,0,len("Hash to be cracked: No Hash has been entered"),len("Hash to be cracked: No Hash has been entered"))==True):
            foundInvalidInput= "True"
            invalidHash= "True"

        #check for valid hash length
        if(self.compareString(inputAlgorithm, "MD5",0,0,len("MD5"),len("MD5"))==True):
            if(len(self.panel_eleven.hashToBeCrackedHeader.GetLabel()) < 52):
                foundInvalidInput= "True"
                invalidHashLength= "True"
            elif(len(self.panel_eleven.hashToBeCrackedHeader.GetLabel()) > 52):
                foundInvalidInput= "True"
                invalidHashLength= "True"
        elif(self.compareString(inputAlgorithm, "SHA1",0,0,len("SHA1"),len("SHA1"))==True):
            if(len(self.panel_eleven.hashToBeCrackedHeader.GetLabel()) < 60):
                foundInvalidInput= "True"
                invalidHashLength= "True"
            elif(len(self.panel_eleven.hashToBeCrackedHeader.GetLabel()) > 60):
                foundInvalidInput= "True"
                invalidHashLength= "True"
        elif(self.compareString(inputAlgorithm, "SHA224",0,0,len("SHA224"),len("SHA224"))==True):
            if(len(self.panel_eleven.hashToBeCrackedHeader.GetLabel()) < 76):
                foundInvalidInput= "True"
                invalidHashLength= "True"
            elif(len(self.panel_eleven.hashToBeCrackedHeader.GetLabel()) > 76):
                foundInvalidInput= "True"
                invalidHashLength= "True"
        elif(self.compareString(inputAlgorithm, "SHA256",0,0,len("SHA256"),len("SHA256"))==True):
            if(len(self.panel_eleven.hashToBeCrackedHeader.GetLabel()) < 84):
                foundInvalidInput= "True"
                invalidHashLength= "True"
            elif(len(self.panel_eleven.hashToBeCrackedHeader.GetLabel()) > 84):
                foundInvalidInput= "True"
                invalidHashLength= "True"
        elif(self.compareString(inputAlgorithm, "SHA384",0,0,len("SHA384"),len("SHA384"))==True):
            if(len(self.panel_eleven.hashToBeCrackedHeader.GetLabel()) < 114):
                foundInvalidInput= "True"
                invalidHashLength= "True"
            elif(len(self.panel_eleven.hashToBeCrackedHeader.GetLabel()) > 114):
                foundInvalidInput= "True"
                invalidHashLength= "True"
        elif(self.compareString(inputAlgorithm, "SHA512",0,0,len("SHA512"),len("SHA512"))==True):
            if(len(self.panel_eleven.hashToBeCrackedHeader.GetLabel()) < 148):
                foundInvalidInput= "True"
                invalidHashLength= "True"
            elif(len(self.panel_eleven.hashToBeCrackedHeader.GetLabel()) > 148):
                foundInvalidInput= "True"
                invalidHashLength= "True"

        #check to see if an invalid input was detected
        if(self.compareString(foundInvalidInput, "False",0,0,len("False"),len("False"))==True):
            self.startRainbowTableCrack()
        else:
            invalidInputString = ""
            if(self.compareString(invalidAlgorithm, "True",0,0,len("True"),len("True"))==True):
                invalidInputString+= "Invalid Algorithm Selected \n"
            if(self.compareString(invalidFile, "True",0,0,len("True"),len("True"))==True):
                invalidInputString+= "Invalid File Selected \n"
            if(self.compareString(invalidHash, "True",0,0,len("True"),len("True"))==True):
                invalidInputString+= "Invalid Hash Selected \n"
            if(self.compareString(invalidHashLength, "True",0,0,len("True"),len("True"))==True):
                invalidInputString+= "Invalid Hash length detected \n" \
                                     "  Proper MD5 length: 32 \n" \
                                     "  Proper SHA1 length: 40 \n" \
                                     "  Proper SHA224 length: 56 \n" \
                                     "  Proper SHA256 length: 64 \n" \
                                     "  Proper SHA384 length: 94 \n" \
                                     "  Proper SHA512 length: 128 \n"
            dial= wx.MessageBox(invalidInputString, "Invalid Input/Selection Detected", wx.OK, self )
        #end of validate rainbowtable user inputs

#----------------------------------------------------------------------
#           Validate Rainbow Table Maker Inputs Function
#               This function checks to make sure that all of the input settings for Rainbow Table are valid.
#               First, checks to see if a valid algorithm has been selected.
#               Then checks to make sure the key length is not left blank.
#               Then checks to see if a valid alphabet has been selected.
#               Then checks to make sure the table chain length was not left blank.
#               Then checks to make sure the number of rows is not left blank.
#               Then checks to make sure the Rainbow Table File Name was not left blank.
#               Finally, evaluates whether or not there were any checks that failed.
#               Any checks that failed are listed in a message box window that is displayed to the user.
#               If all checks succeeded, then the function calls the Start Rainbow Table Maker Creation Session Function
#---------------------------------------------------------------------
    def validateRainbowTableMakerInputs(self, event):
        foundInvalidInput= "False"
        invalidAlgorithm= "False"
        invalidKeyLength= "False"
        invalidAlphabet= "False"
        invalidTableChainLength= "False"
        invalidNumOfRows= "False"
        invalidRainbowTableFile= "False"

        #check for valid selected algorithm
        if(self.compareString(self.panel_twelve.selectedAlgorithm.GetValue(), "MD5",0,0,len("MD5"),len("MD5"))==True):
            fakeVariable= False;
        elif(self.compareString(self.panel_twelve.selectedAlgorithm.GetValue(), "SHA1",0,0,len("SHA1"),len("SHA1"))==True):
            fakeVariable= False;
        elif(self.compareString(self.panel_twelve.selectedAlgorithm.GetValue(), "SHA224",0,0,len("SHA224"),len("SHA224"))==True):
            fakeVariable= False;
        elif(self.compareString(self.panel_twelve.selectedAlgorithm.GetValue(), "SHA256",0,0,len("SHA256"),len("SHA256"))==True):
            fakeVariable= False;
        elif(self.compareString(self.panel_twelve.selectedAlgorithm.GetValue(), "SHA384",0,0,len("SHA384"),len("SHA384"))==True):
            fakeVariable= False;
        elif(self.compareString(self.panel_twelve.selectedAlgorithm.GetValue(), "SHA512",0,0,len("SHA512"),len("SHA512"))==True):
            fakeVariable= False;
        else:
            foundInvalidInput= "True"
            invalidAlgorithm= "True"

        #check for invalid key length
        if(len(self.panel_twelve.keyLengthHeader.GetLabel()) <= len("Key Length: ")):
            foundInvalidInput= "True"
            invalidKeyLength= "True"

        #check for invalid alphabet
        if(self.compareString(self.panel_twelve.selectedAlphabet.GetValue(), "All",0,0,len("All"),len("All"))==True):
            fakeVariable= False;
        elif(self.compareString(self.panel_twelve.selectedAlphabet.GetValue(), "Letters and Digits",0,0,len("Letters and Digits"),len("Letters and Digits"))==True):
            fakeVariable= False;
        elif(self.compareString(self.panel_twelve.selectedAlphabet.GetValue(), "Letters and Punctuation",0,0,len("Letters and Punctuation"),len("Letters and Punctuation"))==True):
            fakeVariable= False;
        elif(self.compareString(self.panel_twelve.selectedAlphabet.GetValue(), "Letters Only",0,0,len("Letters Only"),len("Letters Only"))==True):
            fakeVariable= False;
        elif(self.compareString(self.panel_twelve.selectedAlphabet.GetValue(), "Uppercase Letters",0,0,len("Uppercase Letters"),len("Uppercase Letters"))==True):
            fakeVariable= False;
        elif(self.compareString(self.panel_twelve.selectedAlphabet.GetValue(), "Lowercase Letters",0,0,len("Lowercase Letters"),len("Lowercase Letters"))==True):
            fakeVariable= False;
        elif(self.compareString(self.panel_twelve.selectedAlphabet.GetValue(), "Digits",0,0,len("Digits"),len("Digits"))==True):
            fakeVariable= False;
        else:
            foundInvalidInput= "True"
            invalidAlphabet= "True"

        #check for invalid table chain length
        if(len(self.panel_twelve.chainLengthHeader.GetLabel()) <= len("Table Chain Length: ")):
            foundInvalidInput= "True"
            invalidTableChainLength= "True"

        #check for invalid num of rows
        if(len(self.panel_twelve.numOfRowsHeader.GetLabel()) <= len("Number of Rows: ")):
            foundInvalidInput= "True"
            invalidNumOfRows= "True"

        #check for invalid rainbow table file
        if(len(self.panel_twelve.fileNameHeader.GetLabel()) <= len("Save Rainbow Table File As: ")):
            foundInvalidInput= "True"
            invalidRainbowTableFile= "True"

        #check if invalid input was detected
        if(self.compareString(foundInvalidInput, "False",0,0,len("False"),len("False"))==True):
            fakeVariable=""
            self.startRainbowTableCreationSession()
        else:
            invalidInputString= ""
            if(self.compareString(invalidAlgorithm, "True",0,0,len("True"),len("True"))==True):
                invalidInputString+= "Invalid Algorithm Detected \n"
            if(self.compareString(invalidKeyLength, "True",0,0,len("True"),len("True"))==True):
                invalidInputString+= "Invalid Key length Detected \n"
            if(self.compareString(invalidAlphabet, "True",0,0,len("True"),len("True"))==True):
                invalidInputString+= "Invalid Alphabet Detected \n"
            if(self.compareString(invalidTableChainLength, "True",0,0,len("True"),len("True"))==True):
                invalidInputString+= "Invalid table chain length Detected \n"
            if(self.compareString(invalidNumOfRows, "True",0,0,len("True"),len("True"))==True):
                invalidInputString+= "Invalid Num of rows Detected \n"
            if(self.compareString(invalidRainbowTableFile, "True",0,0,len("True"),len("True"))==True):
                invalidInputString+= "Invalid Rainbow table file Detected \n"
            dial= wx.MessageBox(invalidInputString, "Invalid Input/Selection Detected", wx.OK, self )
        #end of check for rainbow table maker inputs

#-------------------------------------------------------
#           Validate Network Client Input Function
#               This function checks to make sure that an IP address was entered and it is not the default message
#------------------------------------------------------
    def validateNetworkClientInput(self, event):
        foundInvalidInput= "False"
        if(len(self.panel_seven.serverIPAddress.GetLabel()) < 22): #check to see if ip is empty
            foundInvalidInput= "True"
        if(self.compareString(self.panel_seven.serverIPAddress.GetLabel(), "Server's IP Address: No IP Address Has been Input Yet",0,0,len("Server's IP Address: No IP Address Has been Input Yet"),len("Server's IP Address: No IP Address Has been Input Yet"))==True):
            #if still set to default
            foundInvalidInput= "True"
        if(self.compareString(foundInvalidInput, "False",0,0,len("False"),len("False"))==True):
            #if no error detected
            self.connectToServer()
        else:
            dial= wx.MessageBox("You must input an IP address", "No IP address entered", wx.OK, self)

#-------------------------------------------------------
#           Get Server IP Address From User Function
#               This function creates a dialog window that prompts the user for the IP address of the Network Server
#-------------------------------------------------------
    def getIPFromUser(self, event):
        dial = wx.TextEntryDialog(self, "What is the Server's IP Address?", "Input IP Address", "", style=wx.OK)
        dial.ShowModal()
        self.panel_seven.serverIPAddress.SetLabel("Server's IP Address: "+ str(dial.GetValue()))
        dial.Destroy()

#-------------------------------------------------------
#           Set Dictionary Hash To be Cracked Function
#               This function creates a dialog window that prompts the user to input the hash
#               code that they want to be cracked.
#-------------------------------------------------------
    def setDictionaryHashToBeCracked(self, event):
        dial = wx.TextEntryDialog(self, "Input the Hash To Be Cracked \n"
                                        "(Must be in hexadecimal form \n"
                                        "EX: popcorn = 33da7a40473c1637f1a2e142f4925194 )", "Input Hash", "", style=wx.OK)
        dial.ShowModal()
        self.panel_three.inputHashHeader.SetLabel("Hash To Be Cracked: "+str(dial.GetValue()))
        dial.Destroy()

#---------------------------------------------------------
#           Set Brute-Force Hash To be Cracked Function
#               This function creates a dialog window that prompts the user to input the hash
#               code that they want to be cracked.
#--------------------------------------------------------
    def setBruteForceHashToBeCracked(self, event):
        dial = wx.TextEntryDialog(self, "Input the Hash To Be Cracked \n"
                                        "(Must be in hexadecimal form \n"
                                        "EX: popcorn = 33da7a40473c1637f1a2e142f4925194 )", "Input Hash", "", style=wx.OK)
        dial.ShowModal()
        self.panel_four.inputHashHeader.SetLabel("Hash To Be Cracked: "+str(dial.GetValue()))
        dial.Destroy()

#---------------------------------------------------------------
#           Select Dictionary File Function
#               This function creates a file dialog window that allows the user to select which file
#               They want to use as their dictionary file.
#---------------------------------------------------------------
    def selectDictFile(self, event):
        dial= wx.FileDialog(self, message="Choose a Dictionary File", defaultFile="",
                             style=wx.OPEN|wx.MULTIPLE|wx.CHANGE_DIR)
        if(dial.ShowModal() == wx.ID_OK):
            paths = dial.GetPath()
            self.panel_three.inputDictFileHeader.SetLabel("Selected Dictionary File: "+ str(paths))
        dial.Destroy()

#--------------------------------------------------------------
#           On Close Function
#               This function is called when the Close button is pressed. This function creates
#               A dialog window to prompt the user if they are sure they want to close the application.
#               If yes, then set the shutdown flag and then close the program
#--------------------------------------------------------------
    def OnClose(self, event):
        dial = wx.MessageBox('Are you sure you want to quit?', 'Exit?', wx.YES_NO|wx.NO_DEFAULT, self)
        if dial == wx.YES:
            self.shutdown.set()
            self.Close()

#--------------------------------------------------------------
#           Quit Single Status and go Back To Main Menu Function
#               This function creates a dialog window that prompts the user with a confirmation message asking
#               If they are sure that they want to stop cracking the hash.
#               If yes, then terminate the Network Server Process and then return to Main Menu
#--------------------------------------------------------------
    def quitSingleStatusBackToMainMenu(self, event):
        dial = wx.MessageBox('Are you sure you want to stop cracking the hash \n'
                             'and return to the Main Menu?', 'Stop Cracking and Return to Main Menu?', wx.YES_NO|wx.NO_DEFAULT, self)
        if dial == wx.YES:
            self.NetworkServer.terminate()
            self.switchFromPanel10ToPanel1()

#----------------------------------------------------------------
#           Disconnect Client Function
#               This function creates a dialog window that prompts the user with a confirmation message asking
#               If they are sure they want to disconnect from the server.
#               If yes, then terminate the Network Client Process and then return to Main Menu
#---------------------------------------------------------------
    def disconnectClient(self, event):
        dial= wx.MessageBox('Are you sure you want to disconnect from the server? Disconnecting before the search is finished could cause errors',
                            'Disconnect from Server?', wx.YES_NO|wx.NO_DEFAULT, self)
        if dial == wx.YES:
            self.NetworkClient.terminate()
            self.switchFromPanel8ToPanel1()

#-----------------------------------------------------------------
#           Force Close Server Function
#               This function creates a dialog window that prompts the user with a confirmation message asking
#               If they are sure they want to forcifully close the server.
#               If yes, then terminates the Network Server process, sets the shutdown flag, then goes back to the main menu.
#-----------------------------------------------------------------
    def forceCloseServer(self, event):
        dial= wx.MessageBox('Are you sure you want to close the server? Closing the server will forcifully disconnect all clients.',
                            'Close the Server?', wx.YES_NO|wx.NO_DEFAULT, self)
        if(dial == wx.YES):
            self.NetworkServer.terminate()
            self.shutdown.set()
            self.switchFromPanel9ToPanel1()

#-----------------------------------------------------------------
#           Set Current Mode Function
#               This function is used to set the Current Mode value
#------------------------------------------------------------------
    def setCurrentMode(self, inputText):
        self.CurrentMode= inputText

#------------------------------------------------------------------
#           Reset To Default Functions
#               These functions reset all of the search configurations to their default settings
#------------------------------------------------------------------
    def resetDictionarySettingsToDefault(self, event):  #Reset the Dictionary Search Settings to Default
        self.panel_three.selectedAlgorithm.SetValue('MD5')
        self.panel_three.selectedHashingMode.SetValue('Individual Hash Code')
        self.panel_three.inputHashHeader.SetLabel("Hash to be Cracked: No Hash has been input")
        self.panel_three.inputDictFileHeader.SetLabel("Selected Dictionary File: No Dictionary File Selected")

    def resetBruteForceSettingsToDefault(self, event):  #Reset the Brute-Force Search Settings to Default
        self.panel_four.selectedAlgorithm.SetValue('MD5')
        self.panel_four.inputHashHeader.SetLabel('Hash To Be Cracked: No Hash has been Input')
        self.panel_four.minKeyLengthHeader.SetLabel('Min Key Length: 5')
        self.panel_four.maxKeyLengthHeader.SetLabel('Max Key Length: 15')
        self.panel_four.selectedAlphabet.SetValue('All')

    def resetRainbowTableCrackingSettingsToDefault(self, event): #Reset the Rainbow Table Search Settings to Default
        self.panel_eleven.selectedAlgorithm.SetValue('MD5')
        self.panel_eleven.selectedFileHeader.SetLabel('Selected Rainbow Table File: No File has been Selected')
        self.panel_eleven.hashToBeCrackedHeader.SetLabel('Hash to be cracked: No Hash has been entered')

    def resetRainbowTableMakerSettingsToDefault(self, event):  #Reset the Rainbow Table Maker Search Settings to Default
        self.panel_twelve.selectedAlgorithm.SetValue('MD5')
        self.panel_twelve.keyLengthHeader.SetLabel('Key Length: 10')
        self.panel_twelve.selectedAlphabet.SetValue('All')
        self.panel_twelve.chainLengthHeader.SetLabel('Table Chain Length: 100')
        self.panel_twelve.numOfRowsHeader.SetLabel('Number of Rows: 100')
        self.panel_twelve.fileNameHeader.SetLabel('Save Rainbow Table File As: myRainbowTable.txt')

#-----------------------------------------------------------------
#           Generate Hash Dialog Functions
#               These functions generate a dialog window that prompts the user to input the key that they want converted into a hash code
#               The input will be converted into a hash code using the currently selected algorithm in the drop down menu
#-----------------------------------------------------------------
    def generateHashDialogDic(self, event): #Hash Generator for Dictionary Crack
        dial= wx.TextEntryDialog(self, "Input Key To Be Hashed", "Input Key To Be Hashed","", style=wx.OK)
        dial.ShowModal()
        inputKey= str(dial.GetValue())
        inputAlgorithm= self.panel_three.selectedAlgorithm.GetValue()
        generatedHash= str(hashlib.new(str(inputAlgorithm), inputKey).hexdigest())
        self.panel_three.inputHashHeader.SetLabel("Hash To Be Cracked: "+str(generatedHash))
        dial.Destroy()

    def generateHashDialogBF(self, event): #Hash Generator for Brute-Force Crack
        dial= wx.TextEntryDialog(self, "Input Key To Be Hashed", "Input Key To Be Hashed","", style=wx.OK)
        dial.ShowModal()
        inputKey= str(dial.GetValue())
        inputAlgorithm= self.panel_four.selectedAlgorithm.GetValue()
        generatedHash= str(hashlib.new(str(inputAlgorithm), inputKey).hexdigest())
        self.panel_four.inputHashHeader.SetLabel("Hash To Be Cracked: "+str(generatedHash))
        dial.Destroy()

    def generateHashDialogRT(self, event): #Hash Generator for Rainbow Table Crack
        dial= wx.TextEntryDialog(self, "Input Key To Be Hashed", "Input Key To Be Hashed","", style=wx.OK)
        dial.ShowModal()
        inputKey= str(dial.GetValue())
        inputAlgorithm= self.panel_eleven.selectedAlgorithm.GetValue()
        generatedHash= str(hashlib.new(str(inputAlgorithm), inputKey).hexdigest())
        self.panel_eleven.hashToBeCrackedHeader.SetLabel("Hash To Be Cracked: "+str(generatedHash))
        dial.Destroy()

#-------------------------------------------------------------
#           Set Brute-Force Min Key Length Functions
#               This function creates a dialog window that prompts the user to input the new Min Key Length Value
#               Shortest allowed key length is 4. Longest allowed Key Length is 1000.
#-------------------------------------------------------------
    def setBFMinKeyLength(self, event):
        dial = wx.TextEntryDialog(self, "Input the Min Key Length \n"
                                        "Minimum: 3 \n"
                                        "Maximum: 1000", "Input Min Key Length", "", style=wx.OK)
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
        elif(int(input) < 3):
            dial2= wx.MessageDialog(None, "Key Length is too short.\n"
                                          "Must be 3 or more."
                                          "Min Key Length Value was not set.", "Invalid Input", wx.OK)
            dial2.ShowModal()
        elif(int(input) > 1000):
            dial2= wx.MessageDialog(None, "Key Length is too long.\n"
                                          "Must be 1000 or less."
                                          "Min Key Length Value was not set.", "Invalid Input", wx.OK)
            dial2.ShowModal()
        else:
            self.panel_four.minKeyLengthHeader.SetLabel("Min Key Length: "+str(input))
        dial.Destroy()

#-----------------------------------------------------------------
#           Set Brute-Force Max Key Length Function
#               This function creates a dialog window that prompts the user to input a new Max Key Length Value.
#               Shortest allowed key length is 4. Longest allowed key length is 1000.
#               Checks to make sure that the value being set as the Max Key length is greater than or equal to the Min Key Length
#-----------------------------------------------------------------
    def setBFMaxKeyLength(self, event):
        #get min key length so min and max can be compared
        bfMinKeyLength= ""
        tempBFMinKeyLength2 =""
        tempBFMinKeyLength= str(self.panel_four.minKeyLengthHeader.GetLabel())
        for i in range(15, len(tempBFMinKeyLength)):
            tempBFMinKeyLength2+= str(tempBFMinKeyLength[i])
        bfMinKeyLength= int(tempBFMinKeyLength2)
        dial= wx.TextEntryDialog(self, "Input the Max Key Length \n"
                                       "Minimum: 3 \n"
                                       "Maximum: 1000", "Input Max Key Length","", style=wx.OK)
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
        elif(int(input) < 3):
            dial2= wx.MessageDialog(None, "Key Length is too short.\n"
                                          "Must be 3 or more. \n"
                                          "Max Key Length Value was not set.", "Invalid Input", wx.OK)
            dial2.ShowModal()
        elif(int(input) > 1000):
            dial2= wx.MessageDialog(None, "Key Length is too long.\n"
                                          "Must be 1000 or less. \n"
                                          "Max Key Length Value was not set.", "Invalid Input", wx.OK)
            dial2.ShowModal()
        elif(int(input) < int(bfMinKeyLength)):
            dial2= wx.MessageDialog(None, "Min key length is greater than Max key length.\n"
                                          "Max key length must be greater than or equal to Min key length. \n"
                                          "Max Key Length Value was not set.", "Invalid Input", wx.OK)
            dial2.ShowModal()
        else:
            self.panel_four.maxKeyLengthHeader.SetLabel("Max Key Length: "+str(input))
        dial.Destroy()

#------------------------------------------------------------------
#           Set Rainbow Maker Key Length Function
#               This function creates a dialog window that prompts the user to input the new Key Length Value
#               Shortest Key Length allowed is 4. Longest Key Length allowed is 1000.
#------------------------------------------------------------------
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
        elif(len(input) < 1):
            dial2= wx.MessageDialog(None, "Cannot set value to nothing. \n"
                                          "Key Length was not set.", "Invalid Input", wx.OK)
            dial2.ShowModal()
        elif(input.isdigit() == False):
            dial2= wx.MessageDialog(None, "Must input a number.\n"
                                          "Key Length was not set.", "Invalid Input", wx.OK)
            dial2.ShowModal()
        elif(int(input) < 3):
            dial2= wx.MessageDialog(None, "Key Length is too short.\n"
                                          "Must be at least 3 \n"
                                          "Key Length was not set.", "Invalid Input", wx.OK)
            dial2.ShowModal()
        elif(int(input) > 1000):
            dial2= wx.MessageDialog(None, "Key Length too long.\n"
                                          "Must be 1000 or less.\n"
                                          "Key Length was not set.", "Invalid Input", wx.OK)
            dial2.ShowModal()
        else:
            self.panel_twelve.keyLengthHeader.SetLabel("Key Length: "+str(input))
        dial.Destroy()

#----------------------------------------------------------------
#           Set Rainbow Maker Chain Length Value Function
#               This function creates a dialog window that prompts the user to input a new Chain Length Value
#               The smallest value allowed is 1. The largest value allowed is the Max Int value.
#               Smallest chain length allowed is 1. Largest chain length allowed is Max Int value.
#----------------------------------------------------------------
    def setRMChainLength(self, event):
        #min = 1, max = maxint
        import sys
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
        elif(int(input) < 1):
            dial2= wx.MessageDialog(None, "Chain Length is too short.\n"
                                          "Must be at least 1.\n"
                                          "Chain Length was not set.", "Invalid Input", wx.OK)
            dial2.ShowModal()
        elif(int(input) > sys.maxint):
            dial2= wx.MessageDialog(None, "Chain Length is too long.\n"
                                          "Must be less than (2^63) -1 .\n"
                                          "Chain Length was not set.", "Invalid Input", wx.OK)
            dial2.ShowModal()
        else:
            self.panel_twelve.chainLengthHeader.SetLabel("Table Chain Length: "+str(input))
        dial.Destroy()

#-----------------------------------------------------------------
#           Change Rainbow Maker Number of Rows Function
#               This function creates a dialog window that prompts the user to input the new Number of Rows Value
#               Smallest value allowed is 1. Largest value allowed is Max Int value.
#-----------------------------------------------------------------
    def setRMNumOfRows(self, event):
        import sys
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
        elif(int(input) < 1):
            dial2= wx.MessageDialog(None, "Number of Rows is too few.\n"
                                          "Must be at least 1.\n"
                                          "Number of Rows was not set.", "Invalid Input", wx.OK)
            dial2.ShowModal()
        elif(int(input) > sys.maxint):
            dial2= wx.MessageDialog(None, "Number of Rows is too many.\n"
                                          "Must be less than (2^63) -1 .\n"
                                          "Number of Rows was not set.", "Invalid Input", wx.OK)
            dial2.ShowModal()
        else:
            self.panel_twelve.numOfRowsHeader.SetLabel("Number of Rows: "+str(input))
        dial.Destroy()

#---------------------------------------------------------------
#           Change Rainbow Maker File Name Function
#               This function creates a dialog window that prompts the user to input the new File Name Value
#--------------------------------------------------------------
    def setRMFileName(self,event):
        dial= wx.TextEntryDialog(self, "Input the name for this rainbow table file\n"
                                       "(The file extension will automatically be added)", "Enter in the new name", "", style=wx.OK)
        dial.ShowModal()
        if((self.checkForValidFileNameLength(dial.GetValue()) is True)):
                self.panel_twelve.fileNameHeader.SetLabel("Save Rainbow Table File As: "+str(dial.GetValue())+".txt")
        else:
            dial2= wx.MessageDialog(None, "Illegal File Name Length or Illegal first character. \n"
                                          "The new filename was not set.", "File Name needs to be less than 255 characters\n"
                                                                           "but more than zero characters long.\n"
                                                                           "Cannot start with a space.", wx.OK)
            dial2.ShowModal()
        dial.Destroy()

#--------------------------------------------------------------
#           Check for Valid File Name Length Function
#               This function makes sure that the file name that the user input is of legal length
#               Maximum legal file name length is 255 characters
#--------------------------------------------------------------
    def checkForValidFileNameLength(self, inputString):
        if((len(inputString) > 255) or (len(inputString) < 1)):
            return False
        elif(inputString.isspace() == True):
            return False
        else:
            return True

#---------------------------------------------------------------
#           Select Rainbow User File Function
#               This function creates a file selection dialog window that allows the user to pick what rainbow table file they wish to use
#---------------------------------------------------------------
    def selectRUFileSelect(self, event):
        import os
        fileDial= wx.FileDialog(None, "Select a rainbow table file", os.getcwd(), "", "All files (*.*)|*.*", wx.OPEN)
        if(fileDial.ShowModal() == wx.ID_OK):
            input= str(fileDial.GetPath())
            self.panel_eleven.selectedFileHeader.SetLabel("Selected Rainbow Table File: "+str(input))
        fileDial.Destroy()

#---------------------------------------------------------------
#           Set Hash to be Cracked For Rainbow User Function
#               This function creates a dialog window that prompts the user to input the hash that they wish to have cracked
#---------------------------------------------------------------
    def setRUHashToBeCracked(self, event):
        dial= wx.TextEntryDialog(self, "Insert the Hash Code to be cracked", "Insert the Hash Code to be cracked", "", style=wx.OK)
        dial.ShowModal()
        self.panel_eleven.hashToBeCrackedHeader.SetLabel("Hash to be cracked: "+str(dial.GetValue()))
        dial.Destroy()

#--------------------------------------------------------------
#           On Single Mode Button Click Function
#               This function sets all of the panel labels to use single tense on the start buttons labels
#--------------------------------------------------------------
    def onSingleModeButtonClick(self, e):
        self.panel_two.currentMode.SetLabel("Current Mode: Single Mode")
        self.panel_three.StartConnectButton.SetLabel("Start Dictionary Crack")
        self.panel_four.StartConnectButton.SetLabel("Start Brute Force Crack")
        self.panel_eleven.StartConnectButton.SetLabel("Start Rainbow Crack")
        self.panel_twelve.startConnectButton.SetLabel("Make Rainbow Table")
        self.switchFromPanel1ToPanel2()

#-------------------------------------------------------------
#           On Network Mode Button Click Function
#               This function sets all of the panel labels to use plural (networking) tense on the start button labels
#-------------------------------------------------------------
    def onNetworkModeButtonClick(self, e):
        self.panel_two.currentMode.SetLabel("Current Mode: Network Mode")
        self.panel_three.StartConnectButton.SetLabel("Start Hosting Dictionary Crack")
        self.panel_four.StartConnectButton.SetLabel("Start Hosting Brute Force Crack")
        self.panel_eleven.StartConnectButton.SetLabel("Start Hosting Rainbow Crack")
        self.panel_twelve.startConnectButton.SetLabel("Start Hosting a Rainbow Table Creation Session")
        self.switchFromPanel6ToPanel2()

#--------------------------------------------------------------
#           Connect To Server Function
#               This function retrieves the IP address and sets it to the status screens
#               Then it starts up a NetworkClient process
#-------------------------------------------------------------
    def connectToServer(self):
        tempServerIP= self.panel_seven.serverIPAddress.GetLabel()
        #remove the prefix to the ip address
        serverIP=""
        for i in range(21, len(tempServerIP)):
            serverIP+= tempServerIP[i]
        self.NetworkClient= Process(target=Client, args=(serverIP,self.shared))
        self.NetworkClient.start()
        self.panel_eight.connectedToIP.SetLabel("Connected To: "+str(serverIP))
        self.switchFromPanel7ToPanel8()

#---------------------------------------------------------
#           Start Dictionary Crack Function
#               This function retrieves all of the settings from the dictionary search settings panel (panel 3)
#               and stores all of the settings in a dictionary.
#               Then starts up a Network Server Process using the settings stored in the dictionary.
#               Then creates a list of shared variables to be shared amongst the processes
#---------------------------------------------------------
    def startDictionaryCrack(self):
        crackingMethodSetting= "dic"
        tempAlgorithmSetting= str(self.panel_three.selectedAlgorithm.GetValue())
        algorithmSetting= tempAlgorithmSetting
        tempHashSetting= str(self.panel_three.inputHashHeader.GetLabel())
        hashSetting= ""
        for i in range(20, len(tempHashSetting)):
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
        if(self.compareString(tempSingleSetting2, "Single Mode",0,0,len("Single Mode"), len("Single Mode"))==True):
            singleSetting="True"
        else:
            singleSetting="False"
        crackingSettings= {"cracking method":crackingMethodSetting, "algorithm": algorithmSetting, "hash":hashSetting,
                           "file name":FileName, "single": singleSetting}

        #shared variable array
        #[0]shared dictionary, [1]shutdown, [2]update
        listOfSharedVariables= []
        listOfSharedVariables.append(crackingSettings)
        listOfSharedVariables.append(self.shutdown)
        listOfSharedVariables.append(self.update)
        #if(self.compareString(singleSetting, "False",0,0,len("False"),len("False"))):
         #   self.NetworkServer= Process(target=Server, args=(crackingSettings,self.shared,))
        #else:
        self.NetworkServer= Process(target=Server, args=(crackingSettings, self.shared,))
        self.NetworkServer.start()
        if(singleSetting is 'False'): #if in Networking Mode
            self.switchFromPanel3ToPanel9()
        else:   #if in Single Mode
            self.switchFromPanel3ToPanel10()

#---------------------------------------------------------------------
#           Start Brute-Force Crack Function
#               This function retrieves all of the settings from the brute-force search settings panel (panel 4)
#               and stores all of the settings in a dictionary.
#               Then starts up a Network Server Process using the settings stored in the dictionary.
#               Then creates a list of shared variables to be shared amongst the processes
#--------------------------------------------------------------------
    def startBruteForceCrack(self):
        crackingMethodSetting= "bf"
        tempAlgorithmSetting= str(self.panel_four.selectedAlgorithm.GetValue())
        algorithmSetting= tempAlgorithmSetting
        tempHashSetting= str(self.panel_four.inputHashHeader.GetLabel())
        hashSetting=""
        for i in range(20, len(tempHashSetting)):
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
        tempAlphabetSetting2=""
        #check to see what alphabet was selected and convert to appropriate name
        if(self.compareString(tempAlphabetSetting, "All",0,0,len("All"),len('All'))==True):
            tempAlphabetSetting2= string.ascii_letters+string.digits+string.punctuation
        elif(self.compareString(tempAlphabetSetting, "Letters and Digits",0,0,len("Letters and Digits"), len("Letters and Digits"))==True):
            tempAlphabetSetting2= string.ascii_letters+string.digits
        elif(self.compareString(tempAlphabetSetting, "Letters and Punctuation",0,0,len("Letters and Punctuation"),len("Letters and Punctuation" ))==True):
            tempAlphabetSetting2=string.ascii_letters+string.punctuation
        elif(self.compareString(tempAlphabetSetting, "Letters Only",0,0,len("Letters Only"), len("Letters Only"))==True):
            tempAlphabetSetting2= string.ascii_letters
        elif(self.compareString(tempAlphabetSetting, "Uppercase Letters",0,0, len("Uppercase Letters"), len("Uppercase Letters"))==True):
            tempAlphabetSetting2= string.ascii_uppercase
        elif(self.compareString(tempAlphabetSetting, "Lowercase Letters",0,0, len("Lowercase Letters"), len("Lowercase Letters"))==True):
            tempAlphabetSetting2= string.ascii_lowercase
        elif(self.compareString(tempAlphabetSetting, "Digits",0,0,len("Digits"), len("Digits"))==True):
            tempAlphabetSetting2= string.digits
        else:
            fakeVariable= False;
        alphabetSetting= tempAlphabetSetting2
        tempSingleSetting= str(self.panel_four.currentMode.GetLabel())
        tempSingleSetting2=""
        for i in range(14, len(tempSingleSetting)):
            tempSingleSetting2+= tempSingleSetting[i]
        singleSetting=""
        #Tested, single mode is the correct value to check for
        if(self.compareString(tempSingleSetting2, "Single Mode",0,0,len("Single Mode"), len("Single Mode"))==True):
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
        #if(self.compareString(singleSetting,"False",0,0,len("False"),len("False"))):
         #   self.NetworkServer= Process(target=Server, args=(crackingSettings,self.shared,))
        #else:
        self.NetworkServer= Process(target=Server, args=(crackingSettings, self.shared,))
        self.NetworkServer.start()
        if(singleSetting is 'False'): #if in Network Mode
            self.switchFromPanel4ToPanel9()
        else:  #if in Single Mode
            self.switchFromPanel4ToPanel10()

#-------------------------------------------------------------------
#           Start Rainbow Table Crack Function
#               This function retrieves all of the settings from the Rainbow Table User search settings panel (panel 11)
#               and then stores the settings in a dictionary.
#               Then starts up a Network Server Process using the settings stored in the dictionary.
#               Then creates a list of shared variables to be shared amongst the processes
#-------------------------------------------------------------------
    def startRainbowTableCrack(self):
        crackingMethod= "rain"
        tempFileName= self.panel_eleven.selectedFileHeader.GetLabelText()
        #remove extra heading in from of the file path
        fileName= ""
        for i in range(29, len(tempFileName)):
            fileName+= str(tempFileName[i])
        tempHashToBeCracked= self.panel_eleven.hashToBeCrackedHeader.GetLabelText()
        #remove extra heading from the front of the hash code
        hashToBeCracked= ""
        for i in range(20, len(tempHashToBeCracked)):
            hashToBeCracked+= str(tempHashToBeCracked[i])
        tempSingleSetting= self.panel_eleven.currentMode.GetLabelText()
        #remove extra heading from current Mode
        tempSingleSetting2= ""
        for i in range (14, len(tempSingleSetting)):
            tempSingleSetting2+= str(tempSingleSetting[i])
        singleSetting = ""
        if(self.compareString(tempSingleSetting2, "Single Mode",0,0,len("Single Mode"), len("Single Mode"))==True):
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
        #if(self.compareString(singleSetting,"False",0,0,len("False"),len("False"))):
         #   self.NetworkServer= Process(target=Server, args=(crackingSettings,self.shared,))
        #else:
        self.NetworkServer= Process(target=Server, args=(crackingSettings, self.shared,))
        self.NetworkServer.start()
        if(singleSetting is 'False'): #if in Networking Mode
            self.switchFromPanel11ToPanel9()
        else:       #if in Single Mode
            self.switchFromPanel11ToPanel10()

#------------------------------------------------------------------------
#           Start Rainbow Table Creation Session Function
#               This function retrieves all of the settings from the Rainbow Table Maker settings panel (panel 12)
#               and stores them in a dictionary.
#               Then starts up a Network Server Process using the settings stored in the dictionary.
#               Then creates a list of shared variables to be shared amongst the processes.
#-----------------------------------------------------------------------
    def startRainbowTableCreationSession(self):
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
        tempAlphabetSetting2=""
        #check to see what alphabet was selected and convert to appropriate name
        if(self.compareString(tempAlphabetSettings, "All",0,0,len("All"),len('All'))==True):
            tempAlphabetSetting2= string.ascii_letters+string.digits+string.punctuation
        elif(self.compareString(tempAlphabetSettings, "Letters and Digits",0,0,len("Letters and Digits"), len("Letters and Digits"))==True):
            tempAlphabetSetting2= string.ascii_letters+string.digits
        elif(self.compareString(tempAlphabetSettings, "Letters and Punctuation",0,0,len("Letters and Punctuation"),len("Letters and Punctuation" ))==True):
            tempAlphabetSetting2=string.ascii_letters+string.punctuation
        elif(self.compareString(tempAlphabetSettings, "Letters Only",0,0,len("Letters Only"), len("Letters Only"))==True):
            tempAlphabetSetting2= string.ascii_letters
        elif(self.compareString(tempAlphabetSettings, "Uppercase Letters",0,0, len("Uppercase Letters"), len("Uppercase Letters"))==True):
            tempAlphabetSetting2= string.ascii_uppercase
        elif(self.compareString(tempAlphabetSettings, "Lowercase Letters",0,0, len("Lowercase Letters"), len("Lowercase Letters"))==True):
            tempAlphabetSetting2= string.ascii_lowercase
        elif(self.compareString(tempAlphabetSettings, "Digits",0,0,len("Digits"), len("Digits"))==True):
            tempAlphabetSetting2= string.digits
        else:
            fakeVariable= False;
        alphabetSetting= tempAlphabetSetting2
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
        if(self.compareString(tempSingleSetting2, "Single Mode",0,0,len("Single Mode"), len("Single Mode"))==True):
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
        #if(self.compareString(singleSetting,"False",0,0,len("False"),len("False"))):
         #   self.NetworkServer= Process(target=Server, args=(crackingSettings,self.shared,))
        #else:
        self.NetworkServer= Process(target=Server, args=(crackingSettings, self.shared,))
        self.NetworkServer.start()
        if(singleSetting is 'False'): #if in Networking mode
            self.switchFromPanel12ToPanel9()
        else:  #if in single mode
            self.switchFromPanel12ToPanel10()

#---------------------------------------------------------------------
#           Get IP Function
#               This function gets the local IP address of the users machine based on the OS the user is running.
#               Then returns the IP address.
#---------------------------------------------------------------------
    def get_ip(self):
        import platform
        import socket
            #detect the OS
        try:  # getOS try block
            if platform.system() == "Windows":  # Detecting IP for Windows
                self.IP= socket.gethostbyname(socket.gethostname())
                return self.IP
            elif platform.system() == "Linux":  # Detecting IP for Linux
                import fcntl
                import struct
                import os
                def get_interface_ip(ifname):
                    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915,
                                                        struct.pack('256s', ifname[:15]))[20:24])
                #end of inner def
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
            elif platform.system() == "Darwin":  # Detecting IP for OSX
                self.IP = socket.gethostbyname(socket.gethostname())
                return self.IP
            else:                           # Detecting an IP for an OS that is not listed
                self.IP = socket.gethostbyname(socket.gethostname())
                return self.IP

        except Exception as inst:
            print "========================================================================================"
            print "GUI ERROR: An exception was thrown in getOS try block"
            print type(inst)  # the exception instance
            print inst.args  # arguments stored in .args
            print inst  # _str_ allows args tto be printed directly
            print "========================================================================================"
        #end of detect the OS function

#-------------------------------------------------------------
#           Compare String Function
#               This function compares two strings character by character to see if they are equal.
#               Returns True/False
#-------------------------------------------------------------
    def compareString(self,inboundStringA, inboundStringB, startA, startB, endA, endB):
        try:
            posA = startA
            posB = startB
            if(len(inboundStringB) > len(inboundStringA)):
                tempA= inboundStringA
                inboundStringA= inboundStringB
                inboundStringB= tempA
                endA= len(inboundStringB)
                endB= len(inboundStringB)
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
            print "GUI ERROR: Exception thrown in compareString Function: " +str(inst)+"\n"
            print "inboundStringA: '"+str(inboundStringA)+"'"
            print "inboundStringB: '"+str(inboundStringB)+"'"
            print "========================================================================\n"
            return False

#--------------------------------------------------------------------
#           Detect OS Function
#               This function detects the Operating System that the user is running.
#               If unable to detect what OS the user is running, default to Linux.
#--------------------------------------------------------------------
    def detectOS(self):
        import platform
        print "OS DETECTION:"
        if(platform.system()=="Windows"): #Detecting Windows
            print platform.system()
            print platform.win32_ver()
            self.theDetectedOS= "Windows"
        elif(platform.system()=="Linux"): #Detecting Linux
            print platform.system()
            print platform.dist()
            self.theDetectedOS= "Linux"
        elif(platform.system()=="Darwin"): #Detecting OSX
            print platform.system()
            print platform.mac_ver()
            self.theDetectedOS= "Darwin"
        elif(platform.system()=="FreeBSD" or platform.system()=="OpenBSD" or platform.system()=="NetBSD"):
            print platform.system()
            self.theDetectedOS= "Linux"
        else:   #other, which defaults to linux
            print platform.system()
            print "Treating your OS as Linux by default."
            self.theDetectedOS= "Linux"

#=======================================================================================================================
#               Main
#                   The Main Function of the entire script
#=======================================================================================================================
if __name__ == '__main__':
    current_process()._authkey = "Popcorn is awesome!!!"
    app= wx.App(0)
    frame= myFrame()
    frame.Show()
    app.MainLoop()
