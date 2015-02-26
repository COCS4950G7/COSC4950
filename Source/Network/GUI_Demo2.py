__author__ = 'Chris Hamm'
#GUI_Demo2

from Tkinter import Tk,RIGHT,TOP, BOTH, RAISED, Menu
from ttk import Frame, Button, Style

class guiMainMenu(Frame):

    def __init__(self,parent):
        Frame.__init__(self,parent)

        self.parent= parent

        self.initUI()

    def initUI(self):
        self.parent.title("Main Menu")
        self.style = Style()
        self.style.theme_use("default")

        #this is the additional frame
        #frame = Frame(self,relief=RAISED, borderwidth=1)
        #frame.pack(fill=BOTH, expand=1)

        menuBar = Menu(self.parent)
        self.parent.config(menu=menuBar)

        fileMenu = Menu(menuBar)
        fileMenu.add_command(label="Exit", command=self.onExit)
        menuBar.add_cascade(label="File", menu=fileMenu)

        self.pack(fill=BOTH, expand=1)

        closeButton= Button(self,text="Close", command=self.onExit)
        closeButton.pack(side=RIGHT, padx=5, pady=5)
        singleButton= Button(self, text="Single Computer")
        singleButton.pack(side=TOP, padx=5,pady=5)
        networkButton= Button(self, text="Network Mode")
        networkButton.pack(side=TOP, padx=5, pady=5)

    def onExit(self):
        self.quit()

def main():
    root =Tk()
    root.geometry("300x200+300+300")
    app = guiMainMenu(root)
    root.mainloop()

if __name__ == '__main__':
    main()

