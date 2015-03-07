__author__ = 'Chris Hamm'
#GUI_WX_Demo3

#runs with GUI_Demo3_PanelClass

import wx
from GUI_Demo3_PanelClass import myFrame
from GUI_Demo3_PanelClass import myPanel

if __name__ == '__main__':
    app= wx.App(False)
    frame= myFrame()
    app.MainLoop()
