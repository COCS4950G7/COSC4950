__author__ = 'uwadminuser'
#GUI_SimpleMessagebox

import wx

class example(wx.Frame):
    def __init__(self, *args, **kw):
        super(example, self).__init__(*args, **kw)
        self.initUI()

    def initUI(self):
        wx.FutureCall(5000, self.ShowMessage) #This shows a message box after 5 seconds


        self.SetSize((300,200))
        self.SetTitle('Message Box')
        self.Centre()
        self.Show(True)

    def ShowMessage(self):
        wx.MessageBox('Download completed', 'Info'  , wx.OK|wx.ICON_INFORMATION)

def main():
    ex= wx.App()
    example(None)
    ex.MainLoop()

if __name__ == '__main__':
    main()