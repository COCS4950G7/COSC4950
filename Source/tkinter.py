# tkinter.py
# Author: Jon Wright

# This is the first draft of the gui code, this includes the main page with buttons

import Tkinter
import tkMessageBox

main = Tkinter.Tk()
MTitle=main.title("Python")
main.minsize(500,225)
main.maxsize(1400,850)


def NodeCallBack():
	tkMessageBox.showinfo( "Python", "Python")
	
def ServerCallBack():
	tkMessageBox.showinfo( "Python", "Python")
	
def SumCallBack():
	tkMessageBox.showinfo( "Python", "Python")
	
def ExitCallBack():
	main.destroy()

NODE = Tkinter.Button(main, text = "Node", command = NodeCallBack)
SERVER = Tkinter.Button(main, text = "Server", command = ServerCallBack)
SUM = Tkinter.Button(main, text = "Single User Mode", command = SumCallBack)
EXIT = Tkinter.Button(main, text = "Exit", command = ExitCallBack)

NODE.pack()
SERVER.pack()
SUM.pack()
EXIT.pack()

main.mainloop()
