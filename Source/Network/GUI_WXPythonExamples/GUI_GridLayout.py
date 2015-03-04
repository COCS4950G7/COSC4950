__author__ = 'chris hamm'

import wx

class example(wx.Frame):
    def __init__(self, parent, title):
        super(example, self).__init__(parent, title=title, size=(300,250))

        self.initUI()
        self.Centre()
        self.Show()

    def initUI(self):

        menuBar= wx.MenuBar()
        fileMenu= wx.Menu()
        #menuBar.Append((fileMenu, '&File'))
        self.SetMenuBar(menuBar)

        vbox= wx.BoxSizer(wx.VERTICAL)
        self.display= wx.TextCtrl(self, style=wx.TE_RIGHT)
        vbox.Add(self.display, flag=wx.EXPAND|wx.TOP|wx.BOTTOM, border=4)
        gs= wx.GridSizer(5,4,5,5)

        gs.AddMany([(wx.Button(self, label='Cls'), 0 , wx.EXPAND), (wx.Button(self, label='Bck'), 0 , wx.EXPAND),
            (wx.StaticText(self),wx.EXPAND), (wx.Button(self, label='7' ),0, wx.EXPAND), (wx.Button(self, label='8'),0,wx.EXPAND)
        ,(wx.Button(self, label='9'),0, wx.EXPAND)])

        vbox.Add(gs, proportion=1, flag= wx.EXPAND)
        self.SetSizer(vbox)

if __name__ == '__main__':
    app = wx.App()
    example(None, title='Calculator')
    app.MainLoop()
