__author__ = 'uwadminuser'

import wx

class example(wx.Frame):
    def __init__(self, *args, **kw):
        super(example, self).__init__(*args, **kw)

        self.InitUI()

    def InitUI(self):
         pnl= wx.Panel(self)
         cbtn= wx.Button(pnl, label='Close',pos=(20,30))

         cbtn.Bind(wx.EVT_BUTTON, self.OnClose)

         self.SetSize((250,200))
         self.SetTitle('wx.Button')
         self.Centre()
         self.Show(True)

    def OnClose(self, e):
        self.Close(True)

def main():
    ex= wx.App()
    example(None)
    ex.MainLoop()

if __name__ == '__main__':
    main()
