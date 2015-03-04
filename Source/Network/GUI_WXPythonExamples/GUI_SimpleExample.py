__author__ = 'chris hamm'
#GUI_SimpleExample

import wx

#create an application object, each wpython program must have at least one app
app = wx.App()

#creatign a frame object, this is the parent widget to all widgets
#first parameter indicates this has no parent
frame = wx.Frame(None, -1, 'GUI_SimpleExample.py')
#display to the screen
frame.Show()

#enter the main loop
app.MainLoop()




