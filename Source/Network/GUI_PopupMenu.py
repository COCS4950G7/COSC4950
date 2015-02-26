__author__ = 'Chris Hamm'
#GUI_POPup Menu

from Tkinter import Tk, Frame, Menu
#THIS DOESNT SEEM TO WORK CORRECTLY

#ALSO LOOK INTO TOOL BARS
class guiPopupMenu(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.parent = parent

        self.initUI()

    def initUI(self):
        self.parent.title("Popup Menu")
        self.menu = Menu(self.parent, tearoff=0)
        self.menu.add_command(label="Beep", command=self.bell())
        self.menu.add_command(label="Exit", command=self.onExit())

        self.parent.bind("<Button-3>", self.showMenu)
        self.pack()

    def showMenu(self, e):
            self.menu.post(e.x_root, e.y_root)

    def onExit(self):
            self.quit()

def main():
    root = Tk()
    root.geometry("250x150+300+300")
    app = guiPopupMenu(root)
    root.mainloop()

if __name__ == '__main__':
    main()
