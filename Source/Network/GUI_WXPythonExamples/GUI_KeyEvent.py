__author__ = 'Chris HAmm'
#GUI_KeyEvent

#when we press a key on our keyboard, wx.KeyEvent is generated. This event is sent to the widget that currently has focus
#three different key  handlers
#wx.EVT_KEY_DOWN
#wx.EVT_KEY_UP
#wx.EVT_CHAR

#common request is to close the application when the ESC key is pressed

import wx

class example(wx.Frame):
    def __init__(self, *args, **kw):
        super(example, self).__init__(*args, **kw)

        self.InitUI()

    def InitUI(self):
        pnl= wx.Panel(self)
        pnl.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        pnl.SetFocus()

        self.SetSize((250, 180))
        self.SetTitle('Key Event')
        self.Centre()
        self.Show(True)

    def OnKeyDown(self, e):
        key = e.GetKeyCode()
        if key ==wx.WXK_ESCAPE: #get keycode for the pressed key, if it is the ESCAPE key....
            ret = wx.MessageBox('Are you sure you want to quit?', 'Question',wx.YES_NO|wx.NO_DEFAULT, self)

            if ret == wx.YES:
                self.Close()

def main():
    ex =wx.App()
    example(None)
    ex.MainLoop()

if __name__ == '__main__':
    main()
