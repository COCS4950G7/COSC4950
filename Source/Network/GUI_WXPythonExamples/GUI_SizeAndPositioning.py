__author__ = 'chris hamm'

import wx

class example(wx.Frame):

    def __init__(self, parent, title):
        super(example, self).__init__(parent, title=title, size=(250, 250))
        #self.Move((800,250))
        self.Centre()
        self.Show()

if __name__ == '__main__':
    app = wx.App()
    example(None, title='Size')
    app.MainLoop()
