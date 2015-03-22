__author__ = 'chris hamm'
#GUI Demo

from Tkinter import Tk, Frame, BOTH
import tkMessageBox


class guiDemo(Frame): #used to create the root window

    def __init__(self, parent):
        Frame.__init__(self,parent, background= "white")

        self.parent= parent
        self.initUI()

    def initUI(self):
        self.parent.title("Simple")
        self.pack(fill=BOTH, expand= 1)

def main():
    root = Tk()
    root.geometry("250x150+300+300")
    app = guiDemo(root)
    root.mainloop()

if __name__ == '__main__':
    main()

