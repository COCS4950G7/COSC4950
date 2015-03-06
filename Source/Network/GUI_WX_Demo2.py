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
        panel= wx.Panel(self)

        hbox= wx.BoxSizer(wx.HORIZONTAL)
        gsizer= wx.GridSizer(4,1,2,2)

        #defone the buttons
        SingleModeButton= wx.Button(panel, label="Single Mode", size=(200,20))
        NetworkModeButton= wx.Button(panel, label="Network Mode", size=(200,20))
        CloseButton= wx.Button(panel, label="Close", size=(200,20))

        #add buttons to the grid
        gsizer.AddMany([(SingleModeButton, 0,wx.ALIGN_CENTER, 9),
            (NetworkModeButton,0,wx.ALIGN_CENTER, 9),
            (CloseButton,0,wx.ALIGN_CENTER, 9)])

        hbox.Add(gsizer, wx.ALIGN_CENTER)
        panel.SetSizer(hbox)

        #Bind the buttons to events
        SingleModeButton.Bind(wx.EVT_BUTTON, self.ShowNotFinishedMessage1)
        NetworkModeButton.Bind(wx.EVT_BUTTON, self.ShowNotFinishedMessage1)
        CloseButton.Bind(wx.EVT_BUTTON, self.OnClose)

        self.SetSize((640,480))
        self.SetTitle('Mighty Cracker')
        self.Centre()
        self.Show(True)
    #end of InitUI()


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
