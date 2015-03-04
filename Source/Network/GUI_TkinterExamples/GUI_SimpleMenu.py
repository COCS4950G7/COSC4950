__author__ = 'Chris Hamm'
#GUI_SimpleMenu

from Tkinter import Tk,Frame, Menu

class guiSimpleMenu(Frame):

    def __init__(self,parent):
        Frame.__init__(self, parent)

        self.parent = parent
        self.initUI()

    def initUI(self):
        self.parent.title("Simple Menu")

        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)

        fileMenu = Menu(menubar)
        fileMenu.add_command(label="Exit", command=self.onExit)
        menubar.add_cascade(label="File", menu=fileMenu)

    def onExit(self):
        self.quit()

def main():
    root = Tk()
    root.geometry("250x150+300+300")
    app = guiSimpleMenu(root)
    root.mainloop()

if __name__ == '__main__':
    main()
