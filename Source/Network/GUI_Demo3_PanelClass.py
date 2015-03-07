__author__ = 'Chris Hamm'
#GUI_Demo3_PanelClass

import wx

class myPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.listOfWidgets= []
        self.frame= parent

        self.mainSizer= wx.BoxSizer(wx.VERTICAL)
        controlSizer= wx.BoxSizer(wx.HORIZONTAL)
        self.widgetSizer= wx.BoxSizer(wx.VERTICAL)

        self.addButton= wx.Button(self, label="add")
        self.addButton.Bind(wx.EVT_BUTTON, self.preAddWidget)
        controlSizer.Add(self.addButton,0, wx.CENTER|wx.ALL, 5)

        self.removeButton= wx.Button(self, label="Remove")
        self.removeButton.Bind(wx.EVT_BUTTON, self.onRemoveWidget)
        controlSizer.Add(self.removeButton,0, wx.CENTER|wx.ALL, 5)

        self.mainSizer.Add(controlSizer,0, wx.CENTER)
        self.mainSizer.Add(self.widgetSizer,0, wx.CENTER|wx.ALL, 10)

        self.SetSizer(self.mainSizer)

    def preAddWidget(self, e):
        dial = wx.TextEntryDialog(myPanel, 'What is the button label?', 'New button info', "", style=wx.OK)
        dial.ShowModal()
        self.txt.SetValue(dial.GetValue())
        dial.Destroy()

    def onAddWidget(self, inputLabel, inputName, event):
        new_button= wx.Button(self, label= inputLabel, name= inputName)
        self.widgetSizer.Add(new_button, 0, wx.ALL, 5)
        self.frame.fSizer.Layout()
        self.frame.Fit()

    def onRemoveWidget(self, event):
        if self.widgetSizer.GetChildren():
            self.widgetSizer.Hide(len(self.listOfWidgets))
            self.widgetSizer.Remove(len(self.listOfWidgets))
            self.frame.fSizer.Layout()
            self.frame.Fit()

class myFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, parent=None, title="Add / Remove Buttons")
        self.fSizer= wx.BoxSizer(wx.VERTICAL)
        panel = myPanel(self)
        self.fSizer.Add(panel, 1, wx.EXPAND)
        self.SetSizer(self.fSizer)
        self.Fit()
        self.Show()

