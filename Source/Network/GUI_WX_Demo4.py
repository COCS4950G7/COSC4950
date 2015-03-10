__author__ = 'chris hamm'
#GUI_WX_Demo4

import wx
from multiprocessing import Process
from NetworkServer_r15b import Server
from NetworkClient_r15a import Client
import sys

class PanelOne(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        hbox= wx.BoxSizer(wx.HORIZONTAL)
        gsizer= wx.GridSizer(4,1,2,2)

        #defone the buttons
        screenHeader= wx.StaticText(self, label="Mighty Cracker", size=(200,40), style=wx.ALIGN_CENTER_HORIZONTAL)
        SingleModeButton= wx.Button(self, label="Single Mode", size=(200,40), style=wx.ALIGN_CENTER_HORIZONTAL)
        NetworkModeButton= wx.Button(self, label="Network Mode", size=(200,40), style=wx.ALIGN_CENTER_HORIZONTAL)
        CloseButton= wx.Button(self, label="Close", size=(200,40), style=wx.ALIGN_CENTER_HORIZONTAL)

        #add buttons to the grid
        gsizer.AddMany([(screenHeader, 0, wx.ALIGN_CENTER, 9),
                        (SingleModeButton, 0,wx.ALIGN_CENTER, 9),
                        (NetworkModeButton,0,wx.ALIGN_CENTER, 9),
                        (CloseButton,0,wx.ALIGN_CENTER, 9)])

        hbox.Add(gsizer, wx.ALIGN_CENTER)
        self.SetSizer(hbox)

        #Bind the buttons to events
        SingleModeButton.Bind(wx.EVT_BUTTON,  parent.onSingleModeButtonClick)
        NetworkModeButton.Bind(wx.EVT_BUTTON, parent.switchFromPanel1ToPanel6)
        CloseButton.Bind(wx.EVT_BUTTON, parent.OnClose)



class PanelTwo(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self, parent=parent)
        hbox= wx.BoxSizer(wx.HORIZONTAL)
        gsizer= wx.GridSizer(7,1,2,2)

        #define the buttons and widgets
        screenHeader= wx.StaticText(self, label="Select Cracking Method", size=(200,40), style=wx.ALIGN_CENTER_HORIZONTAL)
        self.currentMode= wx.StaticText(self, label="Current Mode: No yet specified", size=(300,40), style=wx.ALIGN_CENTER_HORIZONTAL)
        DictionaryMethodButton= wx.Button(self, label="Dictionary", size=(200,40), style=wx.ALIGN_CENTER_HORIZONTAL)
        BruteForceMethodButton= wx.Button(self, label="Brute Force (default)", size=(200,40), style=wx.ALIGN_CENTER_HORIZONTAL)
        RainbowTableMethodButton= wx.Button(self, label="Rainbow Table", size=(200,40), style=wx.ALIGN_CENTER_HORIZONTAL)
        BackToMainMenuButton= wx.Button(self, label="Back To Main Menu", size=(200,40), style=wx.ALIGN_CENTER_HORIZONTAL)
        CloseButton= wx.Button(self, label="Close", size=(200,40), style=wx.ALIGN_CENTER_HORIZONTAL)

        #add buttons to the grid
        gsizer.AddMany([(screenHeader,0, wx.ALIGN_CENTER, 9),
            (self.currentMode, 0, wx.ALIGN_CENTER, 9),
            (DictionaryMethodButton,0, wx.ALIGN_CENTER,9),
            (BruteForceMethodButton,0, wx.ALIGN_CENTER, 9),
            (RainbowTableMethodButton,0, wx.ALIGN_CENTER,9),
            (BackToMainMenuButton,0, wx.ALIGN_CENTER,9),
            (CloseButton,0, wx.ALIGN_CENTER,9)])

        hbox.Add(gsizer,wx.ALIGN_CENTER)
        self.SetSizer(hbox)

        #Bind the buttons to events
        DictionaryMethodButton.Bind(wx.EVT_BUTTON, parent.switchFromPanel2ToPanel3)
        BruteForceMethodButton.Bind(wx.EVT_BUTTON, parent.switchFromPanel2ToPanel4)
        RainbowTableMethodButton.Bind(wx.EVT_BUTTON, parent.switchFromPanel2ToPanel5)
        BackToMainMenuButton.Bind(wx.EVT_BUTTON, parent.switchFromPanel2ToPanel1)
        CloseButton.Bind(wx.EVT_BUTTON, parent.OnClose)

class PanelThree(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        hbox= wx.BoxSizer(wx.HORIZONTAL)
        gsizer= wx.GridSizer(11,1,2,2)
        listOfAlgorithms= ['MD5', 'SHA 1', 'SHA 224', 'SHA 256', 'SHA 512']

        #define buttons and widgets
        screenHeader= wx.StaticText(self, label="Dictionary Cracking Method Settings", size=(300,40), style=wx.ALIGN_CENTER_HORIZONTAL)
        self.currentMode= wx.StaticText(self, label="Current Mode: Not Specified", size=(300,40), style=wx.ALIGN_CENTER_HORIZONTAL)
        #setting needed for starting server
        #----cracking method
        #----algorithm
        #-----hash
        #-----file name
        #------single mode (yes/no)
        selectAlgorithmHeader= wx.StaticText(self, label="Select Algorithm:", style=wx.ALIGN_CENTER_HORIZONTAL)
        self.selectedAlgorithm= wx.ComboBox(self, choices= listOfAlgorithms, style=wx.ALIGN_CENTER_HORIZONTAL|wx.CB_READONLY)
        self.inputHashHeader= wx.StaticText(self, label="Hash to be Cracked: No Hash has been input", style=wx.ALIGN_CENTER_HORIZONTAL)
        inputHashButton= wx.Button(self, label="Set Hash To Be Cracked", style=wx.ALIGN_CENTER_HORIZONTAL)
        self.inputDictFileHeader= wx.StaticText(self, label="Selected Dictionary File: No Dictionary File Selected", style=wx.ALIGN_CENTER_HORIZONTAL)
        setDictFileButton= wx.Button(self, label="Select Dictionary File", style=wx.ALIGN_CENTER_HORIZONTAL)
        self.StartConnectButton= wx.Button(self, label="Start/Connect Button", size=(250,40), style=wx.ALIGN_CENTER_HORIZONTAL)
        BackToMainMenuButton= wx.Button(self, label="Back To Main Menu", size=(200,40), style=wx.ALIGN_CENTER_HORIZONTAL)
        CloseButton= wx.Button(self, label="Close", size=(200,40), style=wx.ALIGN_CENTER_HORIZONTAL)

        #add buttons to the grid
        gsizer.AddMany([(screenHeader, 0, wx.ALIGN_CENTER, 9),
            (self.currentMode, 0, wx.ALIGN_CENTER, 9),
            (selectAlgorithmHeader, 0, wx.ALIGN_CENTER, 9),
            (self.selectedAlgorithm, 0, wx.ALIGN_CENTER, 9),
            (self.inputHashHeader, 0, wx.ALIGN_CENTER, 9),
            (inputHashButton, 0, wx.ALIGN_CENTER, 9),
            (self.inputDictFileHeader, 0, wx.ALIGN_CENTER, 9),
            (setDictFileButton, 0, wx.ALIGN_CENTER, 9),
            (self.StartConnectButton, 0, wx.ALIGN_CENTER, 9),
            (BackToMainMenuButton, 0, wx.ALIGN_CENTER, 9),
            (CloseButton, 0, wx.ALIGN_CENTER, 9)])

        hbox.Add(gsizer, wx.ALIGN_CENTER)
        self.SetSizer(hbox)

        #Bind the buttons to events
        inputHashButton.Bind(wx.EVT_BUTTON, parent.setDictionaryHashToBeCracked)
        setDictFileButton.Bind(wx.EVT_BUTTON, parent.selectDictFile)
        self.StartConnectButton.Bind(wx.EVT_BUTTON, parent.startDictionaryCrack)
        BackToMainMenuButton.Bind(wx.EVT_BUTTON, parent.switchFromPanel3ToPanel1)
        CloseButton.Bind(wx.EVT_BUTTON, parent.OnClose)

class PanelFour(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        hbox= wx.BoxSizer(wx.HORIZONTAL)
        gsizer= wx.GridSizer(15,1,2,2)
        listOfAlgorithms= ['MD5', 'SHA 1', 'SHA 224', 'SHA 256', 'SHA 512']
        listOfAlphabets= ['All', 'ASCII_Uppercase', 'ASCII_Lowercase', 'Digits', 'Special_Symbols']
        #TODO add support for custom combinations of alphabets

        #define buttons and widgets
        screenHeader= wx.StaticText(self, label="Brute Force Cracking Method Settings", size=(300,40), style=wx.ALIGN_CENTER_HORIZONTAL)
        self.currentMode= wx.StaticText(self, label="Current Mode: Not Specified", size=(300,40), style=wx.ALIGN_CENTER_HORIZONTAL)
        #settings needed for starting server
        #---------cracking method
        #---------algorithm
        #--------hash
        #----------min key length
        #-----------max key length
        #----------alphabet
        #-----------single (yes/no)
        self.selectedAlgorithmHeader= wx.StaticText(self, label="Select Algorithm:", style=wx.ALIGN_CENTER_HORIZONTAL)
        self.selectedAlgorithm= wx.ComboBox(self, choices=listOfAlgorithms, style=wx.ALIGN_CENTER_HORIZONTAL|wx.CB_READONLY)
        self.StartConnectButton= wx.Button(self, label="Start/Connect Button", size=(250,40), style=wx.ALIGN_CENTER_HORIZONTAL)
        self.inputHashHeader= wx.StaticText(self, label="Hash To Be Cracked: No Hash has been Input", style=wx.ALIGN_CENTER_HORIZONTAL)
        inputHashButton= wx.Button(self, label="Set Hash To Be Cracked", style=wx.ALIGN_CENTER_HORIZONTAL)
        self.minKeyLengthHeader= wx.StaticText(self, label="Min Key Length: 5", style=wx.ALIGN_CENTER_HORIZONTAL)
        changeMinKeyLengthButton= wx.Button(self, label="Set Min Key Length", style=wx.ALIGN_CENTER_HORIZONTAL)
        self.maxKeyLengthHeader= wx.StaticText(self, label="Max Key Length: 15", style=wx.ALIGN_CENTER_HORIZONTAL)
        changeMaxKeyLengthButton= wx.Button(self, label="Set Max Key Length", style=wx.ALIGN_CENTER_HORIZONTAL)
        self.selectedAlphabetHeader= wx.StaticText(self, label="Selected Alphabet:", style=wx.ALIGN_CENTER_HORIZONTAL)
        self.selectedAlphabet= wx.ComboBox(self, choices=listOfAlphabets, style=wx.ALIGN_CENTER_HORIZONTAL)
        BackToMainMenuButton= wx.Button(self, label="Back To Main Menu", size=(200,40), style=wx.ALIGN_CENTER_HORIZONTAL)
        CloseButton= wx.Button(self, label="Close", size=(200,40), style=wx.ALIGN_CENTER_HORIZONTAL)

        #add buttons to the grid
        gsizer.AddMany([(screenHeader, 0, wx.ALIGN_CENTER, 9),
                        (self.currentMode, 0, wx.ALIGN_CENTER, 9),
                        (self.selectedAlgorithmHeader, 0, wx.ALIGN_CENTER, 9),
                        (self.selectedAlgorithm, 0, wx.ALIGN_CENTER, 9),
                        (self.inputHashHeader, 0, wx.ALIGN_CENTER, 9),
                        (inputHashButton, 0, wx.ALIGN_CENTER, 9),
                        (self.minKeyLengthHeader, 0, wx.ALIGN_CENTER, 9),
                        (changeMinKeyLengthButton,0, wx.ALIGN_CENTER, 9),
                        (self.maxKeyLengthHeader, 0, wx.ALIGN_CENTER, 9),
                        (changeMaxKeyLengthButton, 0, wx.ALIGN_CENTER, 9),
                        (self.selectedAlphabetHeader, 0, wx.ALIGN_CENTER, 9),
                        (self.selectedAlphabet,0, wx.ALIGN_CENTER, 9),
                        (self.StartConnectButton, 0 , wx.ALIGN_CENTER, 9),
                        (BackToMainMenuButton, 0, wx.ALIGN_CENTER, 9),
                        (CloseButton, 0, wx.ALIGN_CENTER, 9)])

        hbox.Add(gsizer, wx.ALIGN_CENTER)
        self.SetSizer(hbox)

        #Bind the buttons to events
        inputHashButton.Bind(wx.EVT_BUTTON, parent.setBruteForceHashToBeCracked)
        changeMinKeyLengthButton.Bind(wx.EVT_BUTTON, parent.setBFMinKeyLength)
        changeMaxKeyLengthButton.Bind(wx.EVT_BUTTON, parent.setBFMaxKeyLength)
        self.StartConnectButton.Bind(wx.EVT_BUTTON, parent.startBruteForceCrack)
        BackToMainMenuButton.Bind(wx.EVT_BUTTON, parent.switchFromPanel4ToPanel1)
        CloseButton.Bind(wx.EVT_BUTTON, parent.OnClose)

class PanelFive(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        hbox= wx.BoxSizer(wx.HORIZONTAL)
        gsizer= wx.GridSizer(6,1,2,2)

        #define buttons and widgets
        screenHeader= wx.StaticText(self, label="Rainbow Table Cracking Method Settings", size=(300,40), style=wx.ALIGN_CENTER_HORIZONTAL)
        self.currentMode= wx.StaticText(self, label="Current Mode: Not Specified", size=(300,40), style=wx.ALIGN_CENTER_HORIZONTAL)
        self.StartConnectButton= wx.Button(self, label="Start/Connect Button", size=(250,40), style=wx.ALIGN_CENTER_HORIZONTAL)
        BackToMainMenuButton= wx.Button(self, label="Back To Main Menu", size=(200,40), style=wx.ALIGN_CENTER_HORIZONTAL)
        CloseButton= wx.Button(self, label="Close", size=(200,40), style=wx.ALIGN_CENTER_HORIZONTAL)

        #add buttons to the grid
        gsizer.AddMany([(screenHeader, 0, wx.ALIGN_CENTER, 9),
            (self.currentMode, 0, wx.ALIGN_CENTER, 9),
            (self.StartConnectButton, 0, wx.ALIGN_CENTER, 9),
            (BackToMainMenuButton, 0, wx.ALIGN_CENTER, 9),
            (CloseButton, 0 , wx.ALIGN_CENTER, 9)])

        hbox.Add(gsizer, wx.ALIGN_CENTER)
        self.SetSizer(hbox)

        #Bind the buttons to events
        self.StartConnectButton.Bind(wx.EVT_BUTTON, parent.ShowNotFinishedMessage1)
        BackToMainMenuButton.Bind(wx.EVT_BUTTON, parent.switchFromPanel5ToPanel1)
        CloseButton.Bind(wx.EVT_BUTTON, parent.OnClose)

class PanelSix(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        hbox= wx.BoxSizer(wx.HORIZONTAL)
        gsizer= wx.GridSizer(5,1,2,2)

        #define buttons and widgets
        screenHeader= wx.StaticText(self, label="Select Node Type", size=(300,40), style=wx.ALIGN_CENTER_HORIZONTAL)
        NetworkServerButton= wx.Button(self, label="Network Server", size=(200,40), style=wx.ALIGN_CENTER_HORIZONTAL)
        NetworkClientButton= wx.Button(self, label="Network Client", size=(200,40), style=wx.ALIGN_CENTER_HORIZONTAL)
        BackToMainMenuButton= wx.Button(self, label="Back To Main Menu", size=(200,40), style=wx.ALIGN_CENTER_HORIZONTAL)
        CloseButton= wx.Button(self, label="Close", size=(200,40), style=wx.ALIGN_CENTER_HORIZONTAL)

        #add buttons to the grid
        gsizer.AddMany([(screenHeader, 0, wx.ALIGN_CENTER, 9),
                        (NetworkServerButton, 0, wx.ALIGN_CENTER, 9),
                        (NetworkClientButton, 0, wx.ALIGN_CENTER, 9),
                        (BackToMainMenuButton, 0, wx.ALIGN_CENTER, 9),
                        (CloseButton, 0, wx.ALIGN_CENTER, 9)])

        hbox.Add(gsizer, wx.ALIGN_CENTER)
        self.SetSizer(hbox)

        #Bind the buttons to events
        NetworkServerButton.Bind(wx.EVT_BUTTON, parent.onNetworkModeButtonClick)
        NetworkClientButton.Bind(wx.EVT_BUTTON, parent.switchFromPanel6ToPanel7)
        BackToMainMenuButton.Bind(wx.EVT_BUTTON, parent.switchFromPanel6ToPanel1)
        CloseButton.Bind(wx.EVT_BUTTON, parent.OnClose)

class PanelSeven(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        hbox= wx.BoxSizer(wx.HORIZONTAL)
        gsizer= wx.GridSizer(6,1,2,2)

        #define buttons and widgets
        screenHeader= wx.StaticText(self, label="Network Client Main Screen", size=(300,40), style=wx.ALIGN_CENTER_HORIZONTAL)
        self.serverIPAddress= wx.StaticText(self, label="Server's IP Address: No IP Address Has been Input Yet", size=(400,40), style=wx.ALIGN_CENTER_HORIZONTAL)
        InputServerIPButton= wx.Button(self, label="Input the Server IP", size=(200,40), style=wx.ALIGN_CENTER_HORIZONTAL)
        ConnectToServerButton= wx.Button(self, label="Connect To The Server", size=(200,40), style=wx.ALIGN_CENTER_HORIZONTAL)
        BackToMainMenuButton= wx.Button(self, label="Back To Main Menu", size=(200,40), style=wx.ALIGN_CENTER_HORIZONTAL)
        CloseButton= wx.Button(self, label="Close", size=(200,40), style=wx.ALIGN_CENTER_HORIZONTAL)

        #add buttons to the grid
        gsizer.AddMany([(screenHeader, 0, wx.ALIGN_CENTER, 9),
                        (self.serverIPAddress, 0, wx.ALIGN_CENTER, 9),
                        (InputServerIPButton, 0, wx.ALIGN_CENTER, 9),
                        (ConnectToServerButton, 0, wx.ALIGN_CENTER, 9),
                        (BackToMainMenuButton, 0, wx.ALIGN_CENTER, 9),
                        (CloseButton, 0, wx.ALIGN_CENTER, 9)])

        hbox.Add(gsizer, wx.ALIGN_CENTER)
        self.SetSizer(hbox)

        #Bind the buttons to events
        InputServerIPButton.Bind(wx.EVT_BUTTON, parent.getIPFromUser)
        ConnectToServerButton.Bind(wx.EVT_BUTTON, parent.connectToServer)
        BackToMainMenuButton.Bind(wx.EVT_BUTTON, parent.switchFromPanel7ToPanel1)
        CloseButton.Bind(wx.EVT_BUTTON, parent.OnClose)

class PanelEight(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self, parent)
        hbox= wx.BoxSizer(wx.HORIZONTAL)
        gsizer= wx.GridSizer(6,1,2,2)
        print "GUI DEBUG: connected to the server"

        #define buttons and widgets
        screenHeader= wx.StaticText(self, label="Network Client Status Screen", style=wx.ALIGN_CENTER_HORIZONTAL)
        self.currentStatus= wx.StaticText(self, label="Current Status: Running", style=wx.ALIGN_CENTER_HORIZONTAL)
        self.connectedToIP= wx.StaticText(self, label="Connected To: Not Connected to any Server", style=wx.ALIGN_CENTER_HORIZONTAL)
        disconnectClientButton= wx.Button(self, label="Disconnect From Server", style=wx.ALIGN_CENTER_HORIZONTAL)
        CloseButton= wx.Button(self, label="Close", style=wx.ALIGN_CENTER_HORIZONTAL)

        #add buttons to the grid
        gsizer.AddMany([(screenHeader, 0, wx.ALIGN_CENTER, 9),
            (self.currentStatus, 0, wx.ALIGN_CENTER, 9),
            (self.connectedToIP, 0, wx.ALIGN_CENTER, 9),
            (disconnectClientButton, 0, wx.ALIGN_CENTER, 9),
            (CloseButton, 0, wx.ALIGN_CENTER, 9)])

        hbox.Add(gsizer, wx.ALIGN_CENTER)
        self.SetSizer(hbox)

        #Bind the buttons to events
        disconnectClientButton.Bind(wx.EVT_BUTTON, parent.disconnectClient)
        CloseButton.Bind(wx.EVT_BUTTON, parent.OnClose)

class PanelNine(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        hbox= wx.BoxSizer(wx.HORIZONTAL)
        gsizer= wx.GridSizer(6,1,2,2)

        #define the buttons and widgets
        screenHeader= wx.StaticText(self, label="Network Server Status Screen", style=wx.ALIGN_CENTER_HORIZONTAL)
        self.currentStatus= wx.StaticText(self, label="Current Status: Running", style=wx.ALIGN_CENTER_HORIZONTAL)
        consoleOutputLog= wx.TextCtrl(self, size=(300,100),style=wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
        forceQuitServerButton= wx.Button(self, label="Close the server", style=wx.ALIGN_CENTER_HORIZONTAL)
        CloseButton= wx.Button(self, label="Close", style=wx.ALIGN_CENTER_HORIZONTAL)

        #add buttons the the grid
        gsizer.AddMany([(screenHeader, 0, wx.ALIGN_CENTER, 9),
                        (self.currentStatus, 0, wx.ALIGN_CENTER, 9),
                        (consoleOutputLog, 0, wx.ALIGN_CENTER, 9),
                        (forceQuitServerButton, 0, wx.ALIGN_CENTER, 9),
                        (CloseButton, 0, wx.ALIGN_CENTER, 9)])

        hbox.Add(gsizer, wx.ALIGN_CENTER)
        self.SetSizer(hbox)

        #Bind the buttons to events
        forceQuitServerButton.Bind(wx.EVT_BUTTON, parent.forceCloseServer)
        CloseButton.Bind(wx.EVT_BUTTON, parent.OnClose)

class PanelTen(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        hbox= wx.BoxSizer(wx.HORIZONTAL)
        gsizer= wx.GridSizer(6,1,2,2)

        #define the buttons and widgets
        screenHeader= wx.StaticText(self, label="Single Mode Status Screen", style= wx.ALIGN_CENTER_HORIZONTAL)
        self.currentStatus= wx.StaticText(self, label="Current Status: Running", style= wx.ALIGN_CENTER_HORIZONTAL)
        quitSearchButton= wx.Button(self, label="Quit Searching", style=wx.ALIGN_CENTER_HORIZONTAL)
        CloseButton= wx.Button(self, label="Close", style= wx.ALIGN_CENTER_HORIZONTAL)

        #add buttons to the grid
        gsizer.AddMany([(screenHeader, 0, wx.ALIGN_CENTER, 9),
            (self.currentStatus, 0, wx.ALIGN_CENTER, 9),
            (quitSearchButton, 0, wx.ALIGN_CENTER, 9),
            (CloseButton, 0, wx.ALIGN_CENTER, 9)])

        hbox.Add(gsizer, wx.ALIGN_CENTER)
        self.SetSizer(hbox)

        #Bind the buttons to events
        quitSearchButton.Bind(wx.EVT_BUTTON, parent.ShowNotFinishedMessage1)
        CloseButton.Bind(wx.EVT_BUTTON, parent.OnClose)

class RedirectText:
    def __init__(self,aWxTextCtrl):
        self.out=aWxTextCtrl

    def write(self,string):
        self.out.WriteText(string)

    def flush(self):
        pass

class myFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "Mighty Cracker", size=(800, 600))

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
        self.panel_two.Hide()
        self.panel_three.Hide()
        self.panel_four.Hide()
        self.panel_five.Hide()
        self.panel_six.Hide()
        self.panel_seven.Hide()
        self.panel_eight.Hide()
        self.panel_nine.Hide()
        self.panel_ten.Hide()

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
        self.SetSizer(self.sizer)

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
        self.panel_three.Hide()
        self.panel_nine.Show()
        self.Layout()

    def switchFromPanel3ToPanel10(self):
        self.SetTitle("Mighty Cracker: Single Mode Status Screen")
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
        self.panel_four.Hide()
        self.panel_nine.Show()
        self.Layout()

    def switchFromPanel4ToPanel10(self):
        self.SetTitle("Mighty Cracker: Single Mode Status Screen")
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
            self.switchFromPanel9ToPanel1()

    def setCurrentMode(self, inputText):
        self.CurrentMode= inputText

    def setBFMinKeyLength(self, event):
        dial = wx.TextEntryDialog(self, "Input the Min Key Length", "Input Min Key Length", "", style=wx.OK)
        dial.ShowModal()
        #TODO add check for valid input
        self.panel_four.minKeyLengthHeader.SetLabel("Min Key Length: "+str(dial.GetValue()))
        dial.Destroy()

    def setBFMaxKeyLength(self, event):
        dial= wx.TextEntryDialog(self, "Input the Max Key Length", "Input Max Key Length","", style=wx.OK)
        dial.ShowModal()
        #TODO add check for valid input
        self.panel_four.maxKeyLengthHeader.SetLabel("Max Key Length: "+str(dial.GetValue()))
        dial.Destroy()

    def onSingleModeButtonClick(self, e):
        self.panel_two.currentMode.SetLabel("Current Mode: Single Mode")
        self.panel_three.StartConnectButton.SetLabel("Start Dictionary Crack")
        self.panel_four.StartConnectButton.SetLabel("Start Brute Force Crack")
        self.panel_five.StartConnectButton.SetLabel("Start Rainbow Crack")
        self.switchFromPanel1ToPanel2()

    def onNetworkModeButtonClick(self, e):
        self.panel_two.currentMode.SetLabel("Current Mode: Network Mode")
        self.panel_three.StartConnectButton.SetLabel("Start Hosting Dictionary Crack")
        self.panel_four.StartConnectButton.SetLabel("Start Hosting Brute Force Crack")
        self.panel_five.StartConnectButton.SetLabel("Start Hosting Rainbow Crack")
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
        listOfSharedVariables.append(0)
        listOfSharedVariables.append(False)
        self.NetworkServer= Process(target=Server, args=(crackingSettings,listOfSharedVariables,))
        print "GUI DEBUG: before process is started"
        self.NetworkServer.start()
        print "GUI DEBUG: after process has started"
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
        listOfSharedVariables.append(0)
        listOfSharedVariables.append(False)
        self.NetworkServer= Process(target=Server, args=(crackingSettings,))
        self.NetworkServer.start()
        if(singleSetting is 'False'):
            self.switchFromPanel4ToPanel9()
        else:
            self.switchFromPanel4ToPanel10()



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
