__author__ = 'Chris Hamm'
#GUI_Demo2

from Tkinter import Tk,RIGHT,TOP, BOTH, RAISED, Menu
from ttk import Frame, Button, Style
from NetworkServer_r15 import Server
from NetworkClient_r15 import Client
from multiprocessing import Process

class guiMainMenu(Frame):

    def __init__(self,parent):
        Frame.__init__(self,parent)

        self.parent= parent

        self.initUI()

    def initUI(self):
        try:
            self.parent.title("Main Menu")
            self.style = Style()
            self.style.theme_use("default")

            menuBar = Menu(self.parent)
            self.parent.config(menu=menuBar)

            fileMenu = Menu(menuBar)
            fileMenu.add_command(label="Exit", command=self.onExit)
            menuBar.add_cascade(label="File", menu=fileMenu)
            fileMenu.add_command(label="Settings")
            menuBar.add_cascade(label="Edit", menu=fileMenu)
            fileMenu.add_command(label="GUI Interface")
            fileMenu.add_command(label="Command Line Interface")
            menuBar.add_cascade(label="View", menu=fileMenu)


            self.pack(fill=BOTH, expand=1)

            self.closeButton= Button(self,text="Close", command=self.onExit)
            self.closeButton.pack(side=RIGHT, padx=5, pady=5)
            self.singleButton= Button(self, text="Single Computer")
            self.singleButton.pack(side=TOP, padx=5,pady=5)
            self.networkButton= Button(self, text="Network Mode", command=self.unpack_initUI_andLoadNetwork)
            self.networkButton.pack(side=TOP, padx=5, pady=5)
        except Exception as inst:
            print "============================================================================================="
            print "ERROR: An exception was thrown in initUI definition Try block"
            #the exception instance
            print type(inst)
            #srguments stored in .args
            print inst.args
            #_str_ allows args tto be printed directly
            print inst
            print "============================================================================================="

    def unpack_initUI_andLoadNetwork(self):
        self.closeButton.pack_forget()
        self.singleButton.pack_forget()
        self.networkButton.pack_forget()
        self.networkUI()

    def onExit(self):
        self.quit()

    def networkUI(self):
        try:
            self.parent.title("Network Mode")
            self.style= Style()
            self.style.theme_use("default")

            #load new buttons
            self.backToMMButton= Button(self, text="Back to Main Menu", command=self.unpack_networkUI_andLoadMM)
            self.backToMMButton.pack(side=RIGHT, padx=5, pady=5)
            self.runServerButton= Button(self, text="Run Server", command=self.startServer)
            self.runServerButton.pack(side=TOP, padx=5, pady=5)
            self.runClientButton= Button(self, text="Run Client", command=self.startClient)
            self.runClientButton.pack(side=TOP, padx=5, pady=5)
        except Exception as inst:
            print "============================================================================================="
            print "ERROR: An exception was thrown in networkUI definition Try block"
            #the exception instance
            print type(inst)
            #srguments stored in .args
            print inst.args
            #_str_ allows args tto be printed directly
            print inst
            print "============================================================================================="

    def unpack_networkUI_andLoadMM(self):
        self.backToMMButton.pack_forget()
        self.runServerButton.pack_forget()
        self.runClientButton.pack_forget()
        self.initUI()

    def startServer(self): #starts the network server
        try:
            self.networkServer = Process(target=Server)
            self.networkServer.start()
        except Exception as inst:
            print "============================================================================================="
            print "ERROR: An exception was thrown in startServer definition Try block"
            #the exception instance
            print type(inst)
            #srguments stored in .args
            print inst.args
            #_str_ allows args tto be printed directly
            print inst
            print "============================================================================================="

    def startClient(self): #starts the network client
        try:
            self.networkClient = Process(target=Client)
            self.networkClient.start()
        except Exception as inst:
            print "============================================================================================="
            print "ERROR: An exception was thrown in startClient definition Try block"
            #the exception instance
            print type(inst)
            #srguments stored in .args
            print inst.args
            #_str_ allows args tto be printed directly
            print inst
            print "============================================================================================="

def main():
    root =Tk()
    root.geometry("300x200+300+300")
    app = guiMainMenu(root)
    root.mainloop()

if __name__ == '__main__':
    main()

