__author__ = 'Chris Hamm'
#GUI_CenterWindow

from Tkinter import Tk, Frame, BOTH

class centerTheWindow(Frame):

    def __init__(self, parent):
        Frame.__init__(self,parent, background= "white")

        self.parent = parent
        self.parent.title("Centered Window")
        self.pack(fill=BOTH, expand=1)
        self.centerWindow()

    def centerWindow(self):
        w= 290
        h= 150

        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()

        x = (sw - w)/2
        y = (sh - h)/2
        self.parent.geometry('%dx%d+%d+%d' % (w,h,x,y))

def main():
    root = Tk()
    ex = centerTheWindow(root)
    root.mainloop()

if __name__ == '__main__':
    main()
