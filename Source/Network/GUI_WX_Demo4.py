__author__ = 'chris hamm'
#GUI_WX_Demo4

import wx
import string
import hashlib
from multiprocessing import Process, Event, Manager
from NetworkServer_r15b import Server
from NetworkClient_r15b import Client



class PanelOne(wx.Panel):           #========================Main Menu=====================
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)

        vbox= wx.BoxSizer(wx.VERTICAL)

        hbox6= wx.BoxSizer(wx.HORIZONTAL)
        logo= wx.StaticBitmap(self, -1, wx.Bitmap("Mighty_cracker_logo_r2.png", wx.BITMAP_TYPE_ANY))
        hbox6.Add(logo)
        vbox.Add(hbox6, flag=wx.CENTER, border=10)

        vbox.Add((-1,25))

        ''' #the picture is currently taking place of this
        hbox1= wx.BoxSizer(wx.HORIZONTAL)
        screenHeader= wx.StaticText(self, label="Mighty Cracker")
        hbox1.Add(screenHeader)
        vbox.Add(hbox1, flag=wx.TOP|wx.CENTER, border=10)
        '''

        #vbox.Add((-1, 25)) #add extra space between header and the first button

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

class PanelThree(wx.Panel):         #========================Dictionary Cracking Method Settings=================
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        listOfAlgorithms= ['MD5', 'SHA1', 'SHA224', 'SHA256', 'SHA512']
        listOfHashingModes= ['Individual Hash Code','File of Hash Codes']

        #TODO FINISH adding support for cracking a file of hash codes
        #TODO (supposed to work for single mode already)
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
        self.selectAlgorithmHeader= wx.StaticText(self, label="Select Algorithm: ")
        hbox3.Add(self.selectAlgorithmHeader)
        self.selectedAlgorithm= wx.ComboBox(self, choices= listOfAlgorithms, style=wx.CB_READONLY)
        hbox3.Add(self.selectedAlgorithm, flag=wx.LEFT, border=5)
        vbox.Add(hbox3, flag=wx.ALIGN_CENTER|wx.RIGHT, border=10)

        vbox.Add((-1,10))

        hbox10=wx.BoxSizer(wx.HORIZONTAL)
        hashTypeHeader= wx.StaticText(self, label="Select Hashing Mode: (NOT FUNCTIONING YET) ")
        hbox10.Add(hashTypeHeader)
        self.selectedHashingMode= wx.ComboBox(self, choices= listOfHashingModes, style=wx.CB_READONLY)
        hbox10.Add(self.selectedHashingMode, flag=wx.LEFT, border=5)
        vbox.Add(hbox10, flag=wx.ALIGN_CENTER|wx.RIGHT, border=10)

        vbox.Add((-1,10))

        hbox4= wx.BoxSizer(wx.HORIZONTAL)
        self.inputHashHeader= wx.StaticText(self, label="Hash to be Cracked: No Hash has been input")
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
        #make sure that  selected algorithm is not the empty string
        #make sure a hashing mode has been selected (not the empty string)
        #make sure a hash has been entered in
        #make sure a dictionary file is selected
        hbox8.Add(self.StartConnectButton)
        vbox.Add(hbox8, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox11= wx.BoxSizer(wx.HORIZONTAL)
        self.resetToDefaultsButton= wx.Button(self, label="Reset Settings Back To Default")
        hbox11.Add(self.resetToDefaultsButton)
        vbox.Add(hbox11, flag=wx.CENTER, border=10)
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
        self.BackToMainMenuButton.SetToolTip(wx.ToolTip('Go back to the main menu'))
        self.CloseButton.SetToolTip(wx.ToolTip('Close the program'))

        #Bind the buttons to events
        self.inputHashButton.Bind(wx.EVT_BUTTON, parent.setDictionaryHashToBeCracked)
        self.generateHashButton.Bind(wx.EVT_BUTTON, parent.generateHashDialogDic)
        self.setDictFileButton.Bind(wx.EVT_BUTTON, parent.selectDictFile)
        self.StartConnectButton.Bind(wx.EVT_BUTTON, parent.validateDictionaryInputs)
        self.resetToDefaultsButton.Bind(wx.EVT_BUTTON, parent.resetDictionarySettingsToDefault)
        self.BackToMainMenuButton.Bind(wx.EVT_BUTTON, parent.switchFromPanel3ToPanel1)
        self.CloseButton.Bind(wx.EVT_BUTTON, parent.OnClose)

class PanelFour(wx.Panel):            #==================Brute Force Cracking method Settings==================
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        listOfAlgorithms= ['MD5', 'SHA1', 'SHA224', 'SHA256', 'SHA512']
        listOfAlphabets= ["All","Letters and Digits","Letters and Punctuation","Letters Only","Uppercase Letters","Lowercase Letters",
                          "Digits"]
        #TODO add support for spaces, but uses ' ' instead of strring library!
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
        self.selectedAlgorithm= wx.ComboBox(self, choices=listOfAlgorithms, style=wx.CB_READONLY)
        hbox3.Add(self.selectedAlgorithm, flag=wx.LEFT, border=5)
        vbox.Add(hbox3, flag=wx.ALIGN_CENTER|wx.RIGHT, border=10)

        vbox.Add((-1,10))

        hbox4= wx.BoxSizer(wx.HORIZONTAL)
        self.inputHashHeader= wx.StaticText(self, label="Hash To Be Cracked: No Hash has been Input")
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
        hbox6.Add(self.minKeyLengthHeader)
        self.changeMinKeyLengthButton= wx.Button(self, label="Set Min Key Length")
        hbox6.Add(self.changeMinKeyLengthButton, flag=wx.LEFT, border=25)
        vbox.Add(hbox6, flag=wx.ALIGN_CENTER|wx.RIGHT, border=10)

        vbox.Add((-1,10))

        hbox7= wx.BoxSizer(wx.HORIZONTAL)
        self.maxKeyLengthHeader= wx.StaticText(self, label="Max Key Length: 15")
        hbox7.Add(self.maxKeyLengthHeader)
        self.changeMaxKeyLengthButton= wx.Button(self, label="Set Max Key Length")
        hbox7.Add(self.changeMaxKeyLengthButton, flag=wx.LEFT, border=25)
        vbox.Add(hbox7, flag=wx.ALIGN_CENTER|wx.RIGHT, border=10)

        vbox.Add((-1,10))

        hbox8= wx.BoxSizer(wx.HORIZONTAL)
        self.selectedAlphabetHeader= wx.StaticText(self, label="Selected Alphabet: ")
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
        self.BackToMainMenuButton.SetToolTip(wx.ToolTip('Go back to main menu'))
        self.CloseButton.SetToolTip(wx.ToolTip('Close the program'))

        #Bind the buttons to events
        self.inputHashButton.Bind(wx.EVT_BUTTON, parent.setBruteForceHashToBeCracked)
        self.generateHashButton.Bind(wx.EVT_BUTTON, parent.generateHashDialogBF)
        self.changeMinKeyLengthButton.Bind(wx.EVT_BUTTON, parent.setBFMinKeyLength)
        self.changeMaxKeyLengthButton.Bind(wx.EVT_BUTTON, parent.setBFMaxKeyLength)
        self.StartConnectButton.Bind(wx.EVT_BUTTON, parent.validateBruteForceInputs)
        self.resetBackToDefaultValues.Bind(wx.EVT_BUTTON, parent.resetBruteForceSettingsToDefault)
        self.BackToMainMenuButton.Bind(wx.EVT_BUTTON, parent.switchFromPanel4ToPanel1)
        self.CloseButton.Bind(wx.EVT_BUTTON, parent.OnClose)

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

class PanelEight(wx.Panel):       #========================Network Client Status Screen===========================
    def __init__(self,parent):
        wx.Panel.__init__(self, parent)

        #TODO launch status monitor process at end of window

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
        self.disconnectClientButton= wx.Button(self, label="Disconnect From Server")
        hbox4.Add(self.disconnectClientButton)
        vbox.Add(hbox4, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox5=wx.BoxSizer(wx.HORIZONTAL)
        self.CloseButton= wx.Button(self, label="Close")
        hbox5.Add(self.CloseButton)
        vbox.Add(hbox5, flag=wx.CENTER, border=10)

        self.SetSizer(vbox)

        #ToolTips
        self.disconnectClientButton.SetToolTip(wx.ToolTip('Disconnect from the server'))
        self.CloseButton.SetToolTip(wx.ToolTip('Close the program'))

        #Bind the buttons to events
        self.disconnectClientButton.Bind(wx.EVT_BUTTON, parent.disconnectClient)
        self.CloseButton.Bind(wx.EVT_BUTTON, parent.OnClose)

class PanelNine(wx.Panel):                     #================Network Server Status Screen======================
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        #TODO for dictionary, add a progress bar to indicated where in  the dictionary the program is looking at
        #TODO start up status monitor process at end of window

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
        self.forceQuitServerButton= wx.Button(self, label="Close the server")
        hbox5.Add(self.forceQuitServerButton)
        self.CloseButton= wx.Button(self, label="Close")
        hbox5.Add(self.CloseButton, flag=wx.LEFT, border=5)
        vbox.Add(hbox5, flag=wx.ALIGN_CENTER|wx.RIGHT, border=10)

        self.SetSizer(vbox)

        #ToolTips
        self.forceQuitServerButton.SetToolTip(wx.ToolTip('Forcefully stop the server'))
        self.CloseButton.SetToolTip(wx.ToolTip('Close the program'))

        #Bind the buttons to events
        self.forceQuitServerButton.Bind(wx.EVT_BUTTON, parent.forceCloseServer)
        self.CloseButton.Bind(wx.EVT_BUTTON, parent.OnClose)

class PanelTen(wx.Panel):                          #====================Single Mode Status Screen==================
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        #TODO for dictionary, add a progress bar to indicated where in  the dictionary the program is looking at
        #TODO for rainbow table maker ditto

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

        hbox5= wx.BoxSizer(wx.HORIZONTAL)
        activityGaugeHeader= wx.StaticText(self, label="Activity Gauge:")
        hbox5.Add(activityGaugeHeader)
        #TODO size parameter is fo rtesting purposes only (Needs to be tested on Linux)
        self.activityGauge= wx.Gauge(self, range=100, size=(250,15), style=wx.GA_HORIZONTAL )
        self.activityGauge.Pulse() #switch gauge to indeterminate mode
        hbox5.Add(self.activityGauge, flag=wx.LEFT, border=5)
        vbox.Add(hbox5, flag=wx.ALIGN_CENTER|wx.RIGHT, border=10)
        #TODO ask about a shared variable indicating when the the search is complete, so i can stop the activity gauge
        #TODO activity gauge does not pulse on Linux

        vbox.Add((-1,10))

        hbox6= wx.BoxSizer(wx.HORIZONTAL)
        progressBarHeader= wx.StaticText(self, label="Progress:")
        hbox6.Add(progressBarHeader)
        self.progressBar= wx.Gauge(self, range=100, style=wx.GA_HORIZONTAL )
        self.progressBar.SetValue(0) #set value to start at zero
        hbox6.Add(self.progressBar, flag=wx.LEFT, border=5)
        vbox.Add(hbox6, flag=wx.ALIGN_CENTER|wx.RIGHT, border=10)
        #TODO need to set up how to increment progress bar
        #TODO gauge is tiny on OSX

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
        print "GUI DEBUG: created timer"

        #Bind the buttons to events
        self.timer.Bind(wx.EVT_TIMER, parent.updateTimer, self.timer ) #timer is started in the switch to panel 10 function. Once started the timer will call updateTimer every 1000 milliseconds
        self.backToMainMenuButton.Bind(wx.EVT_BUTTON, parent.quitSingleStatusBackToMainMenu)
        self.CloseButton.Bind(wx.EVT_BUTTON, parent.OnClose)

        '''
        #start up the status monitoring process #CAUSING PICKLING ISSUES
        myStatusMonitor= Process(target=parent.startStatusMonitor, args=(True,self.currentCrackingMode.GetLabel,))
        myStatusMonitor.start() #THIS FUNCTION IS ALSO COMMENTED OUT BELOW
        #TODO this process needs to be killed!
        '''

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
        self.selectedAlgorithm= wx.ComboBox(self, choices=listOfAlgorithms, style=wx.CB_READONLY)
        hbox9.Add(self.selectedAlgorithm, flag=wx.LEFT, border=5)
        vbox.Add(hbox9, flag=wx.ALIGN_CENTER|wx.RIGHT, border=10)

        vbox.Add((-1,10))

        hbox3=wx.BoxSizer(wx.HORIZONTAL)
        self.selectedFileHeader= wx.StaticText(self, label="Selected Rainbow Table File: No File has been Selected")
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
        self.backToMainMenuButton.SetToolTip(wx.ToolTip('Go back to the main menu'))
        self.CloseButton.SetToolTip(wx.ToolTip('Close the program'))

        #bind the buttons to events
        self.selectFileButton.Bind(wx.EVT_BUTTON, parent.selectRUFileSelect)
        self.setHashCodeButton.Bind(wx.EVT_BUTTON, parent.setRUHashToBeCracked)
        self.generateHashButton.Bind(wx.EVT_BUTTON, parent.generateHashDialogRT)
        self.StartConnectButton.Bind(wx.EVT_BUTTON, parent.validateRainbowTableUserInputs)
        self.resetSettingsToDefaultButton.Bind(wx.EVT_BUTTON, parent.resetRainbowTableCrackingSettingsToDefault)
        self.backToMainMenuButton.Bind(wx.EVT_BUTTON, parent.switchFromPanel11ToPanel1)
        self.CloseButton.Bind(wx.EVT_BUTTON, parent.OnClose)

class PanelTwelve(wx.Panel):              #=========================Rainbow Table Maker===========================
    def __init__ (self,parent):
        wx.Panel.__init__(self, parent)

        listOfAlgorithms= ['MD5', 'SHA1', 'SHA224', 'SHA256', 'SHA512']
        listOfAlphabets= ["All","Letters and Digits","Letters and Punctuation","Letters Only","Uppercase Letters","Lowercase Letters",
                          "Digits"]
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
        self.changeKeyLengthButton= wx.Button(self, label="Set Key Length")
        hbox4.Add(self.changeKeyLengthButton, flag=wx.LEFT, border=25)
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
        self.chainLengthHeader= wx.StaticText(self, label="Table Chain Length: 100")
        hbox6.Add(self.chainLengthHeader)
        self.changeChainLengthButton= wx.Button(self, label="Set Table Chain Length")
        hbox6.Add(self.changeChainLengthButton, flag=wx.LEFT, border=125)
        vbox.Add(hbox6, flag=wx.ALIGN_CENTER|wx.RIGHT, border=10)

        vbox.Add((-1,10))

        hbox7=wx.BoxSizer(wx.HORIZONTAL)
        self.numOfRowsHeader= wx.StaticText(self, label="Number of Rows: 100")
        hbox7.Add(self.numOfRowsHeader)
        self.setNumOfRowsButton= wx.Button(self, label="Set Number Of Rows")
        hbox7.Add(self.setNumOfRowsButton, flag=wx.LEFT, border=125)
        vbox.Add(hbox7, flag=wx.ALIGN_CENTER|wx.RIGHT, border=10)

        vbox.Add((-1,10))

        hbox8=wx.BoxSizer(wx.HORIZONTAL)
        self.fileNameHeader= wx.StaticText(self, label="Save Rainbow Table File As: myRainbowTable.txt")
        hbox8.Add(self.fileNameHeader)
        vbox.Add(hbox8, flag=wx.CENTER, border=10)

        vbox.Add((-1,10))

        hbox9=wx.BoxSizer(wx.HORIZONTAL)
        self.changeFileNameButton= wx.Button(self, label="Change Saved File Name")
        hbox9.Add(self.changeFileNameButton)
        vbox.Add(hbox9, flag=wx.CENTER, border=10)

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
        self.backToMainMenuButton.SetToolTip(wx.ToolTip('Go back to the main menu'))
        self.CloseButton.SetToolTip(wx.ToolTip('Close the program'))

        #bind the buttons to events
        self.changeKeyLengthButton.Bind(wx.EVT_BUTTON, parent.setRMKeyLength)
        self.changeChainLengthButton.Bind(wx.EVT_BUTTON, parent.setRMChainLength)
        self.setNumOfRowsButton.Bind(wx.EVT_BUTTON, parent.setRMNumOfRows)
        self.changeFileNameButton.Bind(wx.EVT_BUTTON, parent.setRMFileName)
        self.startConnectButton.Bind(wx.EVT_BUTTON, parent.startRainbowTableCreationSession)
        self.resetSettingsBackToDefault.Bind(wx.EVT_BUTTON, parent.resetRainbowTableMakerSettingsToDefault)
        self.backToMainMenuButton.Bind(wx.EVT_BUTTON, parent.switchFromPanel12ToPanel1)
        self.CloseButton.Bind(wx.EVT_BUTTON, parent.OnClose)

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
        newLineCharacter= "" #this is used for the new line character,set according to your OS
        insertFourCharTab= "    "
        if(parent.compareString(str(parent.theDetectedOS), str('Windows'),0,0,len('Windows'),len('Windows'))==True): #if Windows
            newLineCharacter= "\r\n"
        elif(parent.compareString(str(parent.theDetectedOS), str('Linux'),0,0,len('Linux'),len('Linux'))==True): #if linux
            newLineCharacter= "\n"
        elif(parent.compareString(str(parent.theDetectedOS), str('Darwin'),0,0,len('Darwin'),len('Darwin'))==True): #if mac
            newLineCharacter= "\n"
        else:
            print "=============================================================="
            print "GUI ERROR: invalid OS detected: '"+str(parent.theDetectedOS)+"'"
            print "=============================================================="
        #insert the about me text----------------------------------
        textBox.WriteText(newLineCharacter)
        textBox.WriteText(newLineCharacter+"Authors: Chris Hamm, John Wright, Nick Baum, and Chris Bugg.")
        textBox.WriteText(newLineCharacter)
        textBox.WriteText(newLineCharacter+"Description: ")
        textBox.WriteText(newLineCharacter+"============================================================")
        textBox.WriteText(newLineCharacter)
        textBox.WriteText(newLineCharacter+insertFourCharTab+"Our project, Mighty Cracker, is a program designed to crack hashed")
        textBox.WriteText(newLineCharacter+"passwords. It is stand-alone, GUI, and can run on Mac 10+, Linux 14+,")
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
        #TODO update the about me, there are several out of date items and typos
        #TODO brute force can do more than 16 characters
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

class myFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "Mighty Cracker", size=(1024, 768))

        #detectedOS variable
        self.theDetectedOS= "None"

        #detect the OS
        self.detectOS()

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

        #add a menubar at the top of the window/screen
        menubar= wx.MenuBar()
        fileMenu= wx.Menu()
        fileMenuClose= fileMenu.Append(wx.ID_ANY, "Close","Close Application")
        menubar.Append(fileMenu, '&File')
        viewMenu= wx.Menu()
        #viewMenuFullScreen= viewMenu.Append(wx.ID_ANY, "Full Screen", "View in Full Screen Mode") #omitted due to bug in python
        viewMenuMaximizeScreen= viewMenu.Append(wx.ID_ANY, "Maximize Screen", "Make the window fill the entire screen")
        viewMenuNormalScreen= viewMenu.Append(wx.ID_ANY, "Normal Size", "Make the window it's native resolution")
        menubar.Append(viewMenu, '&View')
        self.SetMenuBar(menubar)

        #bind menu items to events
        self.Bind(wx.EVT_MENU, self.OnClose, fileMenuClose)
        #self.Bind(wx.EVT_MENU, self.viewInFullScreen, viewMenuFullScreen) #omittwed due to bug in python
        self.Bind(wx.EVT_MENU, self.viewMaximizedScreen, viewMenuMaximizeScreen)
        self.Bind(wx.EVT_MENU, self.viewNormalScreen, viewMenuNormalScreen)

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


    #specail frame resizing functions====================================================================================
    def viewMaximizedScreen(self, event):
        self.Maximize(True)

    def viewNormalScreen(self, event):
        self.Maximize(False)
        self.ShowFullScreen(False)

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
        self.panel_ten.timer.Start(1000)
        print "GUI DEBUG: starting panel ten timer"
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
        self.panel_ten.timer.Start(1000)
        print "GUI DEBUG: starting panel ten timer"
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
        self.panel_ten.timer.Start(1000) #1000 milliseconds = 1 second
        print "GUI DEBUG: starting panel ten timer"
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
        self.panel_ten.timer.Start(1000)
        print "GUI DEBUG: starting panel ten timer"
        self.Layout()
    #-------------end of switch from panel 12

    #--------------switch from panel 13
    def switchFromPanel13ToPanel1(self, event):
        self.SetTitle("Mighty Cracker")
        self.panel_thirteen.Hide()
        self.panel_one.Show()
        self.Layout()
    #------------end of switch from panel 13


    #defined functions ========================================================================================
    def ShowNotFinishedMessage1(self, event):
        dial= wx.MessageDialog(None, 'This function has not been completed yet', 'Notice:', wx.OK)
        dial.ShowModal()

    def updateTimer(self,  event):
        if(not self.shutdown.is_set()):
            #print "GUI DEBUG: updated timer: "+str(time.ctime())
            print "GUI DEBUG: dictionary[finished chunks]: '"+str(self.dictionary['finished chunks'])+"'"
            #print "GUI DEBUG: type of dic finished chunks: "+str(type(self.dictionary['finished chunks']))
            print "GUI DEBUG: dictionary[total chunks]: '"+str(self.dictionary['total chunks'])+"'"
            #print "GUI DEBUG: type of dictionary total chunks: "+str(self.dictionary['total chunks'])
            percentComplete= 0
            if(int(self.dictionary["total chunks"]) > 0):
                percentComplete= float(int(self.dictionary['finished chunks']) / int(self.dictionary['total chunks']))
            print "GUI DEBUG: percent complete: '"+str(percentComplete)+"'"
            self.panel_ten.progressBar.SetValue(percentComplete)
            #import time
            #time.sleep(1)
            #self.update.wait() #<--THIS CAUSES APPLICATION TO CRASH, IN ADDITION, PYTHON STOPS RESPONDING (windows)
            self.update.clear()
        #TODO add if shut down is issued , stop activity bar and display results

    def validateDictionaryInputs(self, event): #call start dictionary if valid, else display dial error
        foundInvalidInput= "False"
        invalidAlgorithm= "False"
        invalidHashingMode= "False"
        invalidHashToBeCracked= "False"
        invalidDictionaryFile= "False"

        #check for valid algorithm
        if(self.compareString(self.panel_three.selectedAlgorithm.GetValue(), "MD5",0,0,len("MD5"),len("MD5"))==True):
            print "GUI DEBUG: valid dictionary algorithm detected"
        elif(self.compareString(self.panel_three.selectedAlgorithm.GetValue(), "SHA1",0,0,len("SHA1"),len("SHA1"))==True):
            print "GUI DEBUG: valid dictionary algorithm detected"
        elif(self.compareString(self.panel_three.selectedAlgorithm.GetValue(), "SHA224",0,0,len("SHA224"),len("SHA224"))==True):
            print "GUI DEBUG: valid dictionary algorithm detected"
        elif(self.compareString(self.panel_three.selectedAlgorithm.GetValue(), "SHA256",0,0,len("SHA256"),len("SHA256"))==True):
            print "GUI DEBUG: valid dictionary algorithm detected"
        elif(self.compareString(self.panel_three.selectedAlgorithm.GetValue(), "SHA512",0,0,len("SHA512"),len("SHA512"))==True):
            print "GUI DEBUG: valid dictionary algorithm detected"
        else:
            foundInvalidInput= "True"
            invalidAlgorithm= "True"
            print "GUI DEBUG: Invalid dictionary algorithm detected"

        #check for valid selected hashing mode
        if(self.compareString(self.panel_three.selectedHashingMode.GetValue(), "Individual Hash Code",0,0,len("Individual Hash Code"),len("Individual Hash Code"))==True):
            print "GUI DEBUG: valid dictionary selected hashing mode detected"
        elif(self.compareString(self.panel_three.selectedHashingMode.GetValue(), "File of Hash Codes",0,0,len("File of Hash Codes"),len("File of Hash Codes"))==True):
            print "GUI DEBUG: valid dictionary selected hashing mode detected"
        else:
            foundInvalidInput= "True"
            invalidHashingMode= "True"
            print "GUI DEBUG: Invlaid dictionary selected hashing mode detected"

        #check for valid hash to be cracked value
        if(self.compareString(self.panel_three.inputHashHeader.GetLabel(),"Hash to be Cracked: No Hash has been input",0,0,len("Hash to be Cracked: No Hash has been input"),len("Hash to be Cracked: No Hash has been input"))==True):
            foundInvalidInput= "True"
            invalidHashToBeCracked= "True"
            print "GUI DEBUG: Default hash entry detected, not a valid hash"
        else:
            print "GUI DEBUG: valid hash entry detected"

        #check for valid input dictionary file
        if(self.compareString(self.panel_three.inputDictFileHeader.GetLabel(),"Selected Dictionary File: No Dictionary File Selected",0,0,len("Selected Dictionary File: No Dictionary File Selected"),len("Selected Dictionary File: No Dictionary File Selected"))==True):
            foundInvalidInput= "True"
            invalidDictionaryFile= "True"
            print "GUI DEBUG: Default dictionary entry detected, not a valid dictionary file"
        else:
            print "GUI DEBUG: valid dictionary file detected"

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
            if(self.compareString(invalidDictionaryFile, "True",0,0,len("True"),len("True"))==True):
                invalidInputString+= "Invalid Dictionary File Detected \n"
            #TODO these string entries need to be adapted to work for windos also!
            dial= wx.MessageBox(invalidInputString, "Invalid Input/Selection Detected", wx.OK, self)
        #end of validate dictionary input

    def validateBruteForceInputs(self, event):
        foundInvalidInput= "False"
        invalidAlgorithm= "False"
        invalidHashToBeCracked= "False"
        invalidMinKeyInput= "False"
        tempMinKey= 0
        invalidMaxKeyInput= "False"
        tempMaxKey= 0
        minKeyLessThanMaxKey= "True"
        invalidAlphabet= "False"

        #check for valid algorithm
        if(self.compareString(self.panel_four.selectedAlgorithm.GetValue(), "MD5",0,0,len("MD5"),len("MD5"))==True):
            print "GUI DEBUG: valid bf algorithm detected"
        elif(self.compareString(self.panel_four.selectedAlgorithm.GetValue(), "SHA1",0,0,len("SHA1"),len("SHA1"))==True):
            print "GUI DEBUG: valid bf algorithm detected"
        elif(self.compareString(self.panel_four.selectedAlgorithm.GetValue(), "SHA224",0,0,len("SHA224"),len("SHA224"))==True):
            print "GUI DEBUG: valid bf algorithm detected"
        elif(self.compareString(self.panel_four.selectedAlgorithm.GetValue(), "SHA256",0,0,len("SHA256"),len("SHA256"))==True):
            print "GUI DEBUG: valid bf algorithm detected"
        elif(self.compareString(self.panel_four.selectedAlgorithm.GetValue(), "SHA512",0,0,len("SHA512"),len("SHA512"))==True):
            print "GUI DEBUG: valid bf algorithm detected"
        else:
            foundInvalidInput= "True"
            invalidAlgorithm= "True"
            print "GUI DEBUG: Invalid bf algorithm detected"

        #check for valid hash to be cracked value
        if(self.compareString(self.panel_four.inputHashHeader.GetLabel(),"Hash To Be Cracked: No Hash has been Input",0,0,len("Hash To Be Cracked: No Hash has been Input"),len("Hash To Be Cracked: No Hash has been Input"))==True):
            foundInvalidInput= "True"
            invalidHashToBeCracked= "True"
            print "GUI DEBUG: Default hash entry detected, not a valid hash"
        else:
            print "GUI DEBUG: valid hash entry detected"

        #check for valid min key length
        if(len(str(self.panel_four.minKeyLengthHeader.GetLabel())) <= len("Min Key Length: ")):
            foundInvalidInput= "True"
            invalidMinKeyInput= "True"
            print "GUI DEBUG: Invalid bf minkey input detected"
        else:
            print "GUI DEBUG: valid bf minkey input detected"

        #check for valid max key length
        if(len(str(self.panel_four.maxKeyLengthHeader.GetLabel())) <= len("Max Key Length: ")):
            foundInvalidInput= "True"
            invalidMaxKeyInput= "True"
            print "GUI DEBUG: Invalid bf max key input detected"
        else:
            print "GUI DEBUG: valid bf max key input detected"

        #check to make sure that the min key is less than or equal to max key
        tempMaxKey1=""
        tempMinKey1=""
        for i in range(16,len(str(self.panel_four.minKeyLengthHeader.GetLabel()))):
            tempMinKey1+= str(self.panel_four.minKeyLengthHeader.GetLabel()[i])
        for j in range(15, len(str(self.panel_four.maxKeyLengthHeader.GetLabel()))):
            tempMaxKey1+= str(self.panel_four.maxKeyLengthHeader.GetLabel()[j])
        if(int(tempMinKey1) <= int(tempMaxKey1)):
            print "GUI DEBUG: valid keys, minkey is <= maxkey"
        else:
            foundInvalidInput= "True"
            minKeyLessThanMaxKey= "False"
            print "GUI DEBUG: Invalid keys, min key is greater than max key"

        #check for valid selected alphabet
        if(self.compareString(self.panel_four.selectedAlphabet.GetValue(), "All",0,0,len("All"),len("All"))==True):
            print "GUI DEBUG: valid bf alphabet selected"
        elif(self.compareString(self.panel_four.selectedAlphabet.GetValue(), "Letters and Digits",0,0,len("Letters and Digits"),len("Letters and Digits"))==True):
            print "GUI DEBUG: valid bf alphabet selected"
        elif(self.compareString(self.panel_four.selectedAlphabet.GetValue(), "Letters and Punctuation",0,0,len("Letters and Punctuation"),len("Letters and Punctuation"))==True):
            print "GUI DEBUG: valid bf alphabet selected"
        elif(self.compareString(self.panel_four.selectedAlphabet.GetValue(), "Letters Only",0,0,len("Letters Only"),len("Letters Only"))==True):
            print "GUI DEBUG: valid bf alphabet selected"
        elif(self.compareString(self.panel_four.selectedAlphabet.GetValue(), "Uppercase Letters",0,0,len("Uppercase Letters"),len("Uppercase Letters"))==True):
            print "GUI DEBUG: valid bf alphabet selected"
        elif(self.compareString(self.panel_four.selectedAlphabet.GetValue(), "Lowercase Letters",0,0,len("Lowercase Letters"),len("Lowercase Letters"))==True):
            print "GUI DEBUG: valid bf alphabet selected"
        elif(self.compareString(self.panel_four.selectedAlphabet.GetValue(), "Digits",0,0,len("Digits"),len("Digits"))==True):
            print "GUI DEBUG: valid bf alphabet selected"
        else:
            foundInvalidInput= "True"
            invalidAlphabet= "True"
            print "GUI DEBUG: Invalid bf alphabet selected"

        #check to see if any invalid input was detected
        if(self.compareString(foundInvalidInput, "False",0,0,len("False"),len("False"))==True):
            self.startBruteForceCrack()
        else:
            invalidInputString= ""
            if(self.compareString(invalidAlgorithm, "True",0,0,len("True"),len("True"))==True):
                invalidInputString+= "Invalid Algorithm Selected \n"
            if(self.compareString(invalidHashToBeCracked, "True",0,0,len("True"),len("True"))==True):
                invalidInputString+= "Invalid Hash to be cracked value detected \n"
            if(self.compareString(invalidMinKeyInput, "True",0,0,len("True"),len("True"))==True):
                invalidInputString+= "Invalid Min Key Input Detected \n"
            if(self.compareString(invalidMaxKeyInput, "True",0,0,len("True"),len("True"))==True):
                invalidInputString+= "Invalid Max key input detected \n"
            if(self.compareString(minKeyLessThanMaxKey, "False",0,0,len("False"),len("False"))==True):
                invalidInputString+= "Invalid key values, min key must be equal to or less than max key \n"
            if(self.compareString(invalidAlphabet, "True",0,0,len("True"),len("True"))==True):
                invalidInputString+= "Invalid Alphabet selected \n"
            #TODO make this new line friendly with windows
            dial= wx.MessageBox(invalidInputString, "Invalid Input/Selection Detected", wx.OK, self)
        #end of validate brute force inputs

    def validateRainbowTableUserInputs(self, event):
        foundInvalidInput= "False"
        invalidAlgorithm= "False"
        invalidFile= "False"
        invalidHash="False"

        #check for valid selected algorithm
        if(self.compareString(self.panel_eleven.selectedAlgorithm.GetValue(), "MD5",0,0,len("MD5"),len("MD5"))==True):
            print "GUI DEBUG: valid algorithm detected"
        elif(self.compareString(self.panel_eleven.selectedAlgorithm.GetValue(), "SHA1",0,0,len("SHA1"),len("SHA1"))==True):
            print "GUI DEBUG: valid algorithm detected"
        elif(self.compareString(self.panel_eleven.selectedAlgorithm.GetValue(), "SHA224",0,0,len("SHA224"),len("SHA224"))==True):
            print "GUI DEBUG: valid algorithm detected"
        elif(self.compareString(self.panel_eleven.selectedAlgorithm.GetValue(), "SHA256",0,0,len("SHA256"),len("SHA256"))==True):
            print "GUI DEBUG: valid algorithm detected"
        elif(self.compareString(self.panel_eleven.selectedAlgorithm.GetValue(), "SHA512",0,0,len("SHA512"),len("SHA512"))==True):
            print "GUI DEBUG: valid algorithm detected"
        else:
            print "GUI DEBUG: Invalid algorithm detected"
            foundInvalidInput= "True"
            invalidAlgorithm= "True"

        #check for valid rainbow table file
        if(self.compareString(self.panel_eleven.selectedFileHeader.GetLabel(),"Selected Rainbow Table File: No File has been Selected",0,0,len("Selected Rainbow Table File: No File has been Selected"),len("Selected Rainbow Table File: No File has been Selected"))==True):
            print "GUI DEBUG: Invalid file selected"
            foundInvalidInput= "True"
            invalidFile= "True"
        else:
            print "GUI DEBUG: valid file detected"

        #check for valid hash to be cracked
        if(self.compareString(self.panel_eleven.hashToBeCrackedHeader.GetLabel(),"Hash to be cracked: No Hash has been entered",0,0,len("Hash to be cracked: No Hash has been entered"),len("Hash to be cracked: No Hash has been entered"))==True):
            print "GUI DEBUG: Invalid hash entry detected"
            foundInvalidInput= "True"
            invalidHash= "True"
        else:
            print "GUI DEBUG: valid hash detected"

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
            #TODO MAKE THIS NEW LINE WINDOWS COMPATIBLE!!!!!!!!!!!!
            dial= wx.MessageBox(invalidInputString, "Invalid Input/Selection Detected", wx.OK, self )
        #end of validate rainbowtable user inputs

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
            print "GUI DEBUG: valid algorithm detected"
        elif(self.compareString(self.panel_twelve.selectedAlgorithm.GetValue(), "SHA1",0,0,len("SHA1"),len("SHA1"))==True):
            print "GUI DEBUG: valid algorithm detected"
        elif(self.compareString(self.panel_twelve.selectedAlgorithm.GetValue(), "SHA224",0,0,len("SHA224"),len("SHA224"))==True):
            print "GUI DEBUG: valid algorithm detected"
        elif(self.compareString(self.panel_twelve.selectedAlgorithm.GetValue(), "SHA256",0,0,len("SHA256"),len("SHA256"))==True):
            print "GUI DEBUG: valid algorithm detected"
        elif(self.compareString(self.panel_twelve.selectedAlgorithm.GetValue(), "SHA512",0,0,len("SHA512"),len("SHA512"))==True):
            print "GUI DEBUG: valid algorithm detected"
        else:
            print "GUI DEBUG: Invalid algorithm detected"
            foundInvalidInput= "True"
            invalidAlgorithm= "True"

        #check for invalid key length
        if(len(self.panel_twelve.keyLengthHeader.GetLabel()) <= len("Key Length: ")):
            foundInvalidInput= "True"
            invalidKeyLength= "True"
            print "GUI DEBUG: Invalid key length detected"
        else:
            print "GUI DEBUG: valid key length detected"

        #check for invalid alphabet
        if(self.compareString(self.panel_twelve.selectedAlphabet.GetValue(), "All",0,0,len("All"),len("All"))==True):
            print "GUI DEBUG: valid bf alphabet selected"
        elif(self.compareString(self.panel_twelve.selectedAlphabet.GetValue(), "Letters and Digits",0,0,len("Letters and Digits"),len("Letters and Digits"))==True):
            print "GUI DEBUG: valid bf alphabet selected"
        elif(self.compareString(self.panel_twelve.selectedAlphabet.GetValue(), "Letters and Punctuation",0,0,len("Letters and Punctuation"),len("Letters and Punctuation"))==True):
            print "GUI DEBUG: valid bf alphabet selected"
        elif(self.compareString(self.panel_twelve.selectedAlphabet.GetValue(), "Letters Only",0,0,len("Letters Only"),len("Letters Only"))==True):
            print "GUI DEBUG: valid bf alphabet selected"
        elif(self.compareString(self.panel_twelve.selectedAlphabet.GetValue(), "Uppercase Letters",0,0,len("Uppercase Letters"),len("Uppercase Letters"))==True):
            print "GUI DEBUG: valid bf alphabet selected"
        elif(self.compareString(self.panel_twelve.selectedAlphabet.GetValue(), "Lowercase Letters",0,0,len("Lowercase Letters"),len("Lowercase Letters"))==True):
            print "GUI DEBUG: valid bf alphabet selected"
        elif(self.compareString(self.panel_twelve.selectedAlphabet.GetValue(), "Digits",0,0,len("Digits"),len("Digits"))==True):
            print "GUI DEBUG: valid bf alphabet selected"
        else:
            foundInvalidInput= "True"
            invalidAlphabet= "True"
            print "GUI DEBUG: Invalid bf alphabet selected"

        #check for invalid table chain length
        if(len(self.panel_twelve.chainLengthHeader.GetLabel()) <= len("Table Chain Length: ")):
            foundInvalidInput= "True"
            invalidTableChainLength= "True"
            print "GUI DEBUG: invalid table chain length detected"
        else:
            print "GUI DEBUG: valid table chain length detected"

        #check for invalid num of rows
        if(len(self.panel_twelve.numOfRowsHeader.GetLabel()) <= len("Number of Rows: ")):
            foundInvalidInput= "True"
            invalidNumOfRows= "True"
            print "GUI DEBUG: invalid num of rows detected"
        else:
            print "GUI DEBUG: valid num of rows detected"

        #check for invalid rainbow table file
        if(len(self.panel_twelve.fileNameHeader.GetLabel()) <= len("Save Rainbow Table File As: ")):
            foundInvalidInput= "True"
            invalidRainbowTableFile= "True"
            print "GUI DEBUG: invalid rainbow table file detected"
        else:
            print "GUI DEBUG: valid rainbow table file detected"

        #check if invalid input was detected
        if(self.compareString(foundInvalidInput, "False",0,0,len("False"),len("False"))==True):
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
            #TODO MAKE THIS NEW LINE WINDOWS COMPATIBLE!!!!!!!!!!!!
            dial= wx.MessageBox(invalidInputString, "Invalid Input/Selection Detected", wx.OK, self )

        #end of check for rainbow table maker inputs

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


    def getIPFromUser(self, event):
        dial = wx.TextEntryDialog(self, "What is the Server's IP Address?", "Input IP Address", "", style=wx.OK)
        dial.ShowModal()
        self.panel_seven.serverIPAddress.SetLabel("Server's IP Address: "+ str(dial.GetValue()))
        dial.Destroy()

    def setDictionaryHashToBeCracked(self, event):
        dial = wx.TextEntryDialog(self, "Input the Hash To Be Cracked \n"
                                        "(Must be )", "Input Hash", "", style=wx.OK)
        #TODO chanhge to say input in hexaddecimal only for all windows!!!!
        dial.ShowModal()
        self.panel_three.inputHashHeader.SetLabel("Hash To Be Cracked: "+str(dial.GetValue()))
        dial.Destroy()

    def setBruteForceHashToBeCracked(self, event):
        dial = wx.TextEntryDialog(self, "Input the Hash To Be Cracked \n"
                                        "(Must be Standard ASCII Characters)", "Input Hash", "", style=wx.OK)
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

    def quitSingleStatusBackToMainMenu(self, event):
        dial = wx.MessageBox('Are you sure you want to stop cracking the hash \n'
                             'and return to the Main Menu?', 'Stop Cracking and Return to Main Menu?', wx.YES_NO|wx.NO_DEFAULT, self)
        if dial == wx.YES:
            self.NetworkServer.terminate()
            self.switchFromPanel10ToPanel1()

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

    def resetDictionarySettingsToDefault(self, event):
        self.panel_three.selectedAlgorithm.SetValue('MD5')
        self.panel_three.selectedHashingMode.SetValue('Individual Hash Code')
        self.panel_three.inputHashHeader.SetLabel("Hash to be Cracked: No Hash has been input")
        self.panel_three.inputDictFileHeader.SetLabel("Selected Dictionary File: No Dictionary File Selected")

    def resetBruteForceSettingsToDefault(self, event):
        self.panel_four.selectedAlgorithm.SetValue('MD5')
        self.panel_four.inputHashHeader.SetLabel('Hash To Be Cracked: No Hash has been Input')
        self.panel_four.minKeyLengthHeader.SetLabel('Min Key Length: 5')
        self.panel_four.maxKeyLengthHeader.SetLabel('Max Key Length: 15')
        self.panel_four.selectedAlphabet.SetValue('All')

    def resetRainbowTableCrackingSettingsToDefault(self, event):
        self.panel_eleven.selectedAlgorithm.SetValue('MD5')
        self.panel_eleven.selectedFileHeader.SetLabel('Selected Rainbow Table File: No File has been Selected')
        self.panel_eleven.hashToBeCrackedHeader.SetLabel('Hash to be cracked: No Hash has been entered')

    def resetRainbowTableMakerSettingsToDefault(self, event):
        self.panel_twelve.selectedAlgorithm.SetValue('MD5')
        self.panel_twelve.keyLengthHeader.SetLabel('Key Length: 10')
        self.panel_twelve.selectedAlphabet.SetValue('All')
        self.panel_twelve.chainLengthHeader.SetLabel('Table Chain Length: 100')
        self.panel_twelve.numOfRowsHeader.SetLabel('Number of Rows: 100')
        self.panel_twelve.fileNameHeader.SetLabel('Save Rainbow Table File As: myRainbowTable.txt')


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
        if((self.checkForValidFileNameLength(dial.GetValue()) is True)):
                self.panel_twelve.fileNameHeader.SetLabel("Save Rainbow Table File As: "+str(dial.GetValue())+".txt")
        else:
            dial2= wx.MessageDialog(None, "Illegal File Name Length or Illegal first character. \n"
                                          "The new filename was not set.", "File Name needs to be less than 255 characters\n"
                                                                           "but more than zero characters long.\n"
                                                                           "Cannot start with a space.", wx.OK)
            dial2.ShowModal()
        dial.Destroy()

    def checkForValidFileNameLength(self, inputString):
        if((len(inputString) > 255) or (len(inputString) < 1)):
            return False
        elif(inputString.isspace() == True):
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
    '''
    def startStatusMonitor(self, singleMode, crackingMode):
        #monitor the status of the server for either single or network mode
        self.singleMode= singleMode
        self.myCrackingMode=crackingMode

        #TODO implement this into client, server, and single status screens
        while not self.shutdown.is_set():
            if(singleMode == True): #if in single mode
                if(self.is_connected == True):
                    self.panel_ten.currentStatus.SetLabel("Current Status: Connected to Internal Server")
                else:
                    self.panel_ten.currentStatus.SetLabel("Current Status: Not Connected To Internal Server")
            else: #if network mode
                if(self.is_connected == True):
                    self.panel_nine.currentStatus.SetLabel("Current Status: Server is Connected To Network")
                    self.panel_eight.currentStatus.SetLabel("Current Status: Connected to Server")
                else:
                    self.panel_nine.currentStatus.SetLabel("Current Status: Server is Not Connected to the Network")
                    self.panel_eight.currentStatus.SetLabel("Current Status: Not Connected to the Server")
            #TODO if doing_stuff is true, show the activity guage
            #end of if by single/network mode
            if(self.compareString(self.myCrackingMode, "Current Mode: Dictionary",0,0,len("Dictionary"),len("Dictionary"))==True):
                self.panel_ten.progressBar.SetValue(self.dictionary['finished chunks'] / self.dictionary['total chunks'])
                #TODO add this for panels 8 and 9
        #end of while not self.shutdown
    '''

    def connectToServer(self):
        tempServerIP= self.panel_seven.serverIPAddress.GetLabel()
        #remove the prefix to th eip address
        serverIP=""
        for i in range(21, len(tempServerIP)):
            serverIP+= tempServerIP[i]
        #print "GUI DEBUG: started Network Client"
        #print "GUI DEBUG: server IP: '"+str(serverIP)+"'"
        self.NetworkClient= Process(target=Client, args=(serverIP,self.shared))
        self.NetworkClient.start()
        self.panel_eight.connectedToIP.SetLabel("Connected To: "+str(serverIP))
        self.switchFromPanel7ToPanel8()

    def startDictionaryCrack(self):
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
        crackingSettings= {"cracking method":crackingMethodSetting, "algorithm": algorithmSetting, "hash":hashSetting,
                           "file name":FileName, "single": singleSetting, "finished chunks":0}


        #shared variable array
        #[0]shared dictionary, [1]shutdown, [2]update
        listOfSharedVariables= []
        listOfSharedVariables.append(crackingSettings)
        listOfSharedVariables.append(self.shutdown)
        listOfSharedVariables.append(self.update)
        #print "GUI DEBUG: Starting up Server Process"
        self.NetworkServer= Process(target=Server, args=(crackingSettings,self.shared,))
        #print "GUI DEBUG: before process is started"
        self.NetworkServer.start()
        #print "GUI DEBUG: after process has started"
        if(singleSetting is 'False'):
            self.switchFromPanel3ToPanel9()
        else:
            self.switchFromPanel3ToPanel10()


    def startBruteForceCrack(self):
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
            print "GUI ERROR: alphabet not recognized: '"+str(tempAlphabetSetting)+"'"
        alphabetSetting= tempAlphabetSetting2
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
                           "max key length":finalMaxKeyLengthSetting, "alphabet":alphabetSetting, "single":singleSetting
                            , "finished chunks":0}

        #shared variable array
        #[0]shared dictionary, [1]shutdown, [2]update
        listOfSharedVariables= []
        listOfSharedVariables.append(crackingSettings)
        listOfSharedVariables.append(self.shutdown)
        listOfSharedVariables.append(self.update)
        self.NetworkServer= Process(target=Server, args=(crackingSettings,self.shared,))
        self.NetworkServer.start()
        if(singleSetting is 'False'):
            self.switchFromPanel4ToPanel9()
        else:
            self.switchFromPanel4ToPanel10()

    def startRainbowTableCrack(self):
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
        crackingSettings= {"cracking method":crackingMethod, "file name":fileName, "hash":hashToBeCracked, "single":singleSetting
                            , "finished chunks":0}

        #shared variable array
        #[0]shared dictionary, [1]shutdown, [2]update
        listOfSharedVariables= []
        listOfSharedVariables.append(crackingSettings)
        listOfSharedVariables.append(self.shutdown)
        listOfSharedVariables.append(self.update)
        self.NetworkServer= Process(target=Server, args=(crackingSettings,self.shared,))
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
            print "GUI ERROR: alphabet not recognized: '"+str(tempAlphabetSettings)+"'"
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
        if(self.compareString(tempSingleSetting2, "Single Mode",0,0,len(tempSingleSetting2), len("Single Mode"))==True):
            singleSetting="True"
        else:
            singleSetting="False"
        crackingSettings = {"cracking method":crackingMethod, "algorithm":algorithmSetting, "key length":keyLengthSetting,
                            "alphabet":alphabetSetting, "chain length":chainLengthSetting, "num rows":numberOfRowsSetting,
                            "file name":fileNameSetting, "single":singleSetting, "finished chunks":0}

        #shared variable array
        #[0]shared dictionary, [1]shutdown, [2]update
        listOfSharedVariables= []
        listOfSharedVariables.append(crackingSettings)
        listOfSharedVariables.append(self.shutdown)
        listOfSharedVariables.append(self.update)
        self.NetworkServer= Process(target=Server, args=(crackingSettings,self.shared,))
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

    def detectOS(self):
        import platform
        print "OS DETECTION:"
        if(platform.system()=="Windows"): #Detecting Windows
            print "GUI DEBUG: Windows OS detected"
            print platform.system()
            print platform.win32_ver()
            self.theDetectedOS= "Windows"
        elif(platform.system()=="Linux"): #Detecting Linux
            print "GUI DEBUG: Linux OS detected"
            print platform.system()
            print platform.dist()
            self.theDetectedOS= "Linux"
        elif(platform.system()=="Darwin"): #Detecting OSX
            print "GUI DEBUG: Darwin OS detected"
            print platform.system()
            print platform.mac_ver()
            self.theDetectedOS= "Darwin"
        else:   #other, which defaults to linux
            print "GUI DEBUG: Unknown OS detected"
            print platform.system()
            print "Treating your OS as Linux by default."
            self.theDetectedOS= "Linux"


if __name__ == '__main__':
    app= wx.App(0)
    frame= myFrame()
    frame.Show()
    app.MainLoop()
