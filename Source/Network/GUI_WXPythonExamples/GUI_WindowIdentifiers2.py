__author__ = 'Chris Hamm'
#GUI_WindowIdentifiers2

#this uses standard identifiers instead of auto ids

import wx

ID_MENU_NEW = wx.NewId() #defines a globally defined ID

class example(wx.Frame):
    def __init__(self, *args, **kw):
        super(example, self).__init__(*args,**kw)

        self.InitUI()

    def InitUI(self):
        pnl= wx.Panel(self)
        grid= wx.GridSizer(3,2)


        #IN linux, these standard IDs have buttons
        grid.AddMany([(wx.Button(pnl, wx.ID_CANCEL),0, wx.TOP | wx.LEFT, 9),
            (wx.Button(pnl, wx.ID_DELETE),0, wx.TOP, 9),
            (wx.Button(pnl, wx.ID_SAVE),0, wx.LEFT, 9),
            (wx.Button(pnl, wx.ID_EXIT)),
            (wx.Button(pnl, wx.ID_STOP),0, wx.LEFT,9),
            (wx.Button(pnl, wx.ID_NEW))])

        self.Bind(wx.EVT_BUTTON, self.OnQuitApp, id=wx.ID_EXIT)

        pnl.SetSizer(grid)

        self.SetSize((220, 180))
        self.SetTitle('Standard IDs')
        self.Centre()
        self.Show(True)

    def OnQuitApp(self, event):
        self.Close()

def main():
    ex= wx.App()
    example(None)
    ex.MainLoop()

if __name__ == '__main__':
    main()
