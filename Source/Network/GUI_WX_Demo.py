__author__ = 'chris Hamm'
#GUI_WX_Demo

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

class primaryWindow(wx.Frame):
    def __init__(self, parent, title):
        super(primaryWindow, self).__init__(parent, title=title, size=(640,480))

        self.initUI()
        self.Centre()
        self.Show(True)

    def initUI(self):
        menuBar= wx.MenuBar()
        self.SetMenuBar(menuBar)
        pnl= wx.Panel(self)
        box = wx.BoxSizer(wx.VERTICAL)

        exitButton= wx.Button(pnl, wx.ID_ANY, label="Close Program"), 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL
        self.Bind(wx.EVT_BUTTON, self.OnExit, id=exitButton.getId())

        box.Add(exitButton,0, wx.ALIGN_CENTER_HORIZONTAL, 10)

        pnl.SetSizer(box)
        pnl.Layout()

    def onExit(self, event):
        self.Close()

def main():
    myApp= wx.App()
    primaryWindow(None, title="Mighty Cracker")
    myApp.MainLoop()

if __name__ == '__main__':
    main()
