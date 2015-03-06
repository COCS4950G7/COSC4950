__author__ = 'Chris Hamm'
#GUI_WindowIdentifieers

import wx

#if we provide -1 or wx.ID_ANY for the id parameter of a widget, python will automatically create an id for us.
#automaticly created ids are always negative. Users set IDs must be positive


class example(wx.Frame):
    def __init__(self, *args, **kw):
        super(example, self).__init__(*args, **kw)
        self.InitUI()

    def InitUI(self):
        pnl= wx.Panel(self)
        exitButton= wx.Button(pnl, wx.ID_ANY, 'Exit',(10,10))
        self.Bind(wx.EVT_BUTTON, self.OnExit, id=exitButton.GetId()) #dont care about actual id
        self.SetTitle('Automatic id')
        self.Centre()
        self.Show(True)

    def OnExit(self, event):
        self.Close()

def main():
    ex= wx.App()
    example(None)
    ex.MainLoop()

if __name__ == '__main__':
    main()
