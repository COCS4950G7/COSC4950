__author__ = 'uwadminuser'

import wx

class example(wx.Frame):

    def __init__(self, *args, **kw):
        super(example, self).__init__(*args, **kw)


        self.initUI()

    def initUI(self):
        wx.StaticText(self, label='x:', pos= (10,10))
        wx.StaticText(self, label ='y:', pos=(10,30))

        self.st1= wx.StaticText(self, label='', pos=(30,10))
        self.st2= wx.StaticText(self, label='', pos=(30,30))

        self.Bind(wx.EVT_MOVE, self.OnMove)

        self.SetSize((250,180))
        self.SetTitle('Move Event')
        self.Centre()
        self.Show(True)

    def OnMove(self,e ):
        x,y= e.GetPosition()
        self.st1.SetLabel(str(x))
        self.st2.SetLabel(str(y))

def main():
    ex= wx.App()
    example(None)
    ex.MainLoop()

if __name__== '__main__':
    main()