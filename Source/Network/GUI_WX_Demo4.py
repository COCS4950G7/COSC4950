__author__ = 'chris hamm'
#GUI_WX_Demo4

import wx

class PanelOne(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        listOfWidgets= []

        hbox= wx.BoxSizer(wx.HORIZONTAL)
        gsizer= wx.GridSizer(4,1,2,2)

        #defone the buttons
        SingleModeButton= wx.Button(self, label="Single Mode", size=(200,40))
        listOfWidgets.append(SingleModeButton)
        NetworkModeButton= wx.Button(self, label="Network Mode", size=(200,40))
        listOfWidgets.append(NetworkModeButton)
        CloseButton= wx.Button(self, label="Close", size=(200,40))
        listOfWidgets.append(CloseButton)

        #add buttons to the grid
        gsizer.AddMany([(SingleModeButton, 0,wx.ALIGN_CENTER, 9),
            (NetworkModeButton,0,wx.ALIGN_CENTER, 9),
            (CloseButton,0,wx.ALIGN_CENTER, 9)])

        hbox.Add(gsizer, wx.ALIGN_CENTER)
        self.SetSizer(hbox)

        #Bind the buttons to events
        SingleModeButton.Bind(wx.EVT_BUTTON,  parent.onSwitchPanels)
        NetworkModeButton.Bind(wx.EVT_BUTTON, parent.ShowNotFinishedMessage1)
        CloseButton.Bind(wx.EVT_BUTTON, parent.OnClose)

class PanelTwo(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self, parent=parent)
        listOfWidgets= []
        hbox= wx.BoxSizer(wx.HORIZONTAL)
        gsizer= wx.GridSizer(6,1,2,2)

        #define the buttons and widgets
        screenHeader= wx.StaticText(self, label="Select Cracking Method", size=(200,40))
        listOfWidgets.append(screenHeader)
        DictionaryMethodButton= wx.Button(self, label="Dictionary", size=(200,40))
        listOfWidgets.append(DictionaryMethodButton)
        BruteForceMethodButton= wx.Button(self, label="Brute Force (default)", size=(200,40))
        listOfWidgets.append(BruteForceMethodButton)
        RainbowTableMethodButton= wx.Button(self, label="Rainbow Table", size=(200,40))
        listOfWidgets.append(RainbowTableMethodButton)
        BackToMainMenuButton= wx.Button(self, label="Back To Main Menu", size=(200,40))
        listOfWidgets.append(BackToMainMenuButton)
        CloseButton= wx.Button(self, label="Close", size=(200,40))
        listOfWidgets.append(CloseButton)

        #add buttons to the grid
        gsizer.AddMany([(screenHeader,0, wx.ALIGN_CENTER, 9),
            (DictionaryMethodButton,0, wx.ALIGN_CENTER,9),
            (BruteForceMethodButton,0, wx.ALIGN_CENTER, 9),
            (RainbowTableMethodButton,0, wx.ALIGN_CENTER,9),
            (BackToMainMenuButton,0, wx.ALIGN_CENTER,9),
            (CloseButton,0, wx.ALIGN_CENTER,9)])

        hbox.Add(gsizer,wx.ALIGN_CENTER)
        self.SetSizer(hbox)

        #Bind the buttons to events
        DictionaryMethodButton.Bind(wx.EVT_BUTTON, parent.ShowNotFinishedMessage1)
        BruteForceMethodButton.Bind(wx.EVT_BUTTON, parent.ShowNotFinishedMessage1)
        RainbowTableMethodButton.Bind(wx.EVT_BUTTON, parent.ShowNotFinishedMessage1)
        BackToMainMenuButton.Bind(wx.EVT_BUTTON, parent.onSwitchPanels)
        CloseButton.Bind(wx.EVT_BUTTON, parent.OnClose)

class myFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "Mighty Cracker")

        self.panel_one= PanelOne(self)
        self.panel_two= PanelTwo(self)
        self.panel_two.Hide()

        self.sizer= wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.panel_one, 1, wx.EXPAND)
        self.sizer.Add(self.panel_two, 1, wx.EXPAND)
        self.SetSizer(self.sizer)

    def onSwitchPanels(self, event):
        if(self.panel_one.IsShown()):
            self.SetTitle("SHowing Panel 2")
            self.panel_one.Hide()
            self.panel_two.Show()
        else:
            self.SetTitle("PAnel one showing")
            self.panel_one.Show()
            self.panel_two.Hide()
        self.Layout()

    #defined functions
    def ShowNotFinishedMessage1(self, event):
        dial= wx.MessageDialog(None, 'This function has not been completed yet', 'Notice:', wx.OK)
        dial.ShowModal()

    def OnClose(self, event):
        dial = wx.MessageBox('Are you sure you want to quit?', 'Exit?', wx.YES_NO|wx.NO_DEFAULT, self)
        if dial == wx.YES:
            self.Close()

    def getPanelOne(self):
        return self.panel_one

    def getPanelTwo(self):
        return self.panel_two

if __name__ == '__main__':
    app= wx.App(False)
    frame= myFrame()
    frame.Show()
    app.MainLoop()
