__author__ = 'chris hamm'
#GUI Demo

import Tkinter
import tkMessageBox

top = Tkinter.Tk()
#widgets go here
def testMessageBox():
    tkMessageBox.showinfo( "Hello python", "Hello world")

button1 = Tkinter.Button(top, text= "Test", command = testMessageBox())

button1.pack() #example glitches out on OS X

top.mainloop()