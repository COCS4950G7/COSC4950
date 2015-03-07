__author__ = 'Chris Hamm'
#GUI_WX_Demo2

try:
    import wx

except ImportError as inst:
    print "============================================================================================="
    print "GUI IMPORT ERROR: You do not have the wxPython library installed."
    print "Please install wxPython, and then try again.\n"
    print "Installation Instructions can be found here: http://wiki.wxpython.org/How%20to%20install%20wxPython\n"
    print "============================================================================================="
except Exception as inst:
    print "============================================================================================="
    print "GUI ERROR: An exception was thrown in Import Library Try block"
    #the exception instance
    print type(inst)
    #srguments stored in .args
    print inst.args
    #_str_ allows args tto be printed directly
    print inst
    print "============================================================================================="


class guiWXDemo2(wx.Frame):
    def __init__(self, *args, **kw):
        super(guiWXDemo2, self).__init__(*args, **kw)
        self.InitUI()

    def InitUI(self):
        self.panel= wx.Panel(self)
        listOfWidgets= []
        hbox= wx.BoxSizer(wx.HORIZONTAL)
        gsizer= wx.GridSizer(4,1,2,2)

        #defone the buttons
        SingleModeButton= wx.Button(self.panel, label="Single Mode", size=(200,20))
        listOfWidgets.append(SingleModeButton)
        NetworkModeButton= wx.Button(self.panel, label="Network Mode", size=(200,20))
        listOfWidgets.append(NetworkModeButton)
        CloseButton= wx.Button(self.panel, label="Close", size=(200,20))
        listOfWidgets.append(CloseButton)

        #add buttons to the grid
        gsizer.AddMany([(SingleModeButton, 0,wx.ALIGN_CENTER, 9),
            (NetworkModeButton,0,wx.ALIGN_CENTER, 9),
            (CloseButton,0,wx.ALIGN_CENTER, 9)])

        hbox.Add(gsizer, wx.ALIGN_CENTER)
        self.panel.SetSizer(hbox)

        #Bind the buttons to events
        SingleModeButton.Bind(wx.EVT_BUTTON, lambda event: self.changeScreen(self.panel, listOfWidgets, self.selectCrackingMethodUI))
        NetworkModeButton.Bind(wx.EVT_BUTTON, self.ShowNotFinishedMessage1)
        CloseButton.Bind(wx.EVT_BUTTON, self.OnClose)

        self.SetSize((640,480))
        self.SetTitle('Mighty Cracker')
        self.Centre()
        self.Show(True)
    #end of InitUI()

    def selectCrackingMethodUI(self):
        self.panel2= wx.Panel(self)
        #panel2.Show(True)
        listOfWidgets= []
        hbox= wx.BixSizer(wx.HORIZONTAL)
        gsizer= wx.GridSizer(5,1,2,2)

        #define the buttons and widgets
        screenHeader= wx.StaticText(self.panel2, label="Select Cracking Method", size=(400,40))
        listOfWidgets.append(screenHeader)
        DictionaryMethodButton= wx.Button(self.panel2, label="Dictionary", size=(200,20))
        listOfWidgets.append(DictionaryMethodButton)
        BruteForceMethodButton= wx.Button(self.panel2, label="Brute Force (default)", size=(200,20))
        listOfWidgets.append(BruteForceMethodButton)
        RainbowTableMethodButton= wx.Button(self.panel2, label="Rainbow Table", size=(200,20))
        listOfWidgets.append(RainbowTableMethodButton)
        CloseButton= wx.Button(self.panel2, label="Close", size=(200,20))
        listOfWidgets.append(CloseButton)

        #add buttons to the grid
        gsizer.AddMany([(screenHeader,0, wx.ALIGN_CENTER, 9),
            (DictionaryMethodButton,0, wx.ALIGN_CENTER,9),
            (BruteForceMethodButton,0, wx.ALIGN_CENTER, 9),
            (RainbowTableMethodButton,0, wx.ALIGN_CENTER,9),
            (CloseButton,0, wx.ALIGN_CENTER,9)])

        hbox.Add(gsizer,wx.ALIGN_CENTER)
        self.panel2.SetSizer(hbox)

        #Bind the buttons to events
        DictionaryMethodButton.Bind(wx.EVT_BUTTON, self.ShowNotFinishedMessage1)
        BruteForceMethodButton.Bind(wx.EVT_BUTTON, self.ShowNotFinishedMessage1)
        RainbowTableMethodButton.Bind(wx.EVT_BUTTON, self.ShowNotFinishedMessage1)
        CloseButton.Bind(wx.EVT_BUTTON, self.OnClose)

        self.panel2.SetSize((640,480))
        self.SetTitle('Mighty Cracker')
        self.panel2.Centre()
        self.panel2.Show(True)
    #end of selectCrackingMethodUI

    def changeScreen(self, closingScreensPanel, inputListOfWidgets, screenToLoad):
        if(closingScreensPanel.GetChildren()):
            for i in range(0, len(inputListOfWidgets)):
                inputListOfWidgets[i].Hide()
        closingScreensPanel.Hide()
        screenToLoad


    #defined functions
    def ShowNotFinishedMessage1(self, event):
        dial= wx.MessageDialog(None, 'This function has not been completed yet', 'Notice:', wx.OK)
        dial.ShowModal()

    def OnClose(self, event):
        dial = wx.MessageBox('Are you sure you want to quit?', 'Exit?', wx.YES_NO|wx.NO_DEFAULT, self)
        if dial == wx.YES:
            self.Close()

def main():
    myApp= wx.App()
    guiWXDemo2(None)
    myApp.MainLoop()

if __name__ == '__main__':
    main()
