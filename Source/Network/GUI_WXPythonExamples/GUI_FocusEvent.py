__author__ = 'Chris Hamm'
#GUI_FocusEvent

#the focus indicates the currently selected widgets in application.
#The text entered from the keyboard or pasted from the clipboard is sent to the widget, which has focus
#wx.EVT_SET_FOCUS which is generated when a widget recives focus
#wx.EVT_KILL_FOCUS is generated when the widget looses focus. focus is changed by clicking or by a keuboard key

import wx

class MyWindow(wx.Panel):
    def __init__(self,parent):
        super(MyWindow, self).__init__(parent)

        self.color= '#b3b3b3'

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_SET_FOCUS, self.OnSetFocus)
        self.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)

    def OnPaint(self, e):
        dc= wx.PaintDC(self)

        dc.SetPen(wx.Pen(self.color))
        x, y =self.GetSize()
        dc.DrawRectangle(0,0,x,y)

    def OnSize(self, e):
        self.Refresh()

    def OnSetFocus(self, e):
        self.color= '#0099f7'
        self.Refresh()

    def OnKillFocus(self, e):
        self.color= '#b3b3b3'
        self.Refresh()

class example(wx.Frame):
    def __init__(self, *args, **kw):
        super(example, self).__init__(*args, **kw)
        self.InitUI()

    def InitUI(self):
        grid = wx.GridSizer(2,2,10,10)
        grid.AddMany([(MyWindow(self),0, wx.EXPAND|wx.TOP|wx.LEFT, 9),
            (MyWindow(self),0, wx.EXPAND|wx.TOP|wx.RIGHT, 9),
            (MyWindow(self),0, wx.EXPAND|wx.BOTTOM|wx.LEFT, 9),
            (MyWindow(self),0, wx.EXPAND|wx.BOTTOM|wx.RIGHT, 9)])

        self.SetSizer(grid)

        self.SetSize((350,250))
        self.SetTitle('Focus event')
        self.Centre()
        self.Show(True)

    def OnMove(self, e):
        print e.GetEventObject()
        x, y = e.GetPosition()
        self.st1.SetLabel(str(x))
        self.st2.SetLabel(str(y))

def main():
    ex= wx.App()
    example(None)
    ex.MainLoop()

if __name__ == '__main__':
    main()