__author__ = 'Chris Hamm'
#GUI_PaintEvent

#Paint event is generated when a window is redrawn
#When you minimze a window, no paint event is generated

import wx

class example(wx.Frame):
    def __init__(self, *args, **kw):
        super(example, self).__init__(*args, **kw)
        self.InitUI()

    def InitUI(self):
        self.count=0
        self.Bind(wx.EVT_PAINT, self.OnPaint)

        self.SetSize((250,180))
        self.Centre()
        self.Show(True)

    def OnPaint(self,e):
        self.count += 1
        self.SetTitle(str(self.count))

def main():
    ex= wx.App()
    example(None)
    ex.MainLoop()

if __name__ == '__main__':
    main()
