__author__ = 'Jon'
import Tkconstants
import tkFileDialog
from Tkinter import *
import Tkinter as Tk

########################################################################
## adding a hashinng button, used to test basic functionality of enter text.

class MyApp(object):
    """"""
    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        self.root = parent
        self.root.title("Main frame")
        self.frame = Tk.Frame(parent)
        self.frame.pack()

        title1 = Label(root, text="Single User Mode")
        title1.grid(row=1, column=0)

        btn_dictionary = Tk.Button(self.frame, text="Dictionary", command=self.open_dictionary)
        btn_dictionary.grid(row=2, column=0)

        btn_brute_force = Tk.Button(self.frame , text="Brute Force", command=self.open_brute_force)
        btn_brute_force.grid(row=2, column=1)

        btn_rainbow = Tk.Button(self.frame, text="Rainbow Table", command=self.open_rainbow)
        btn_rainbow.grid(row=2, column=2)

        btn_node = Tk.Button(self.frame, text="Node", command=self.open_node)
        btn_node.grid(row=4, column=0)

        btn_server = Tk.Button(self.frame, text="Server", command=self.open_server)
        btn_server.grid(row=4, column=2)

        btn_hash = Tk.Button(self.frame, text="Hash", command=self.open_hash)
        btn_hash.grid(row=5, column=2)

    #----------------------------------------------------------------------
    def hide(self):
        """"""
        self.root.withdraw()

    #----------------------------------------------------------------------
    def openFrame(self):
        """"""
        self.hide()
        otherFrame = Tk.Toplevel()
        otherFrame.geometry("400x300")
        otherFrame.title("otherFrame")
        handler = lambda: self.onCloseOtherFrame(otherFrame)
        btn = Tk.Button(otherFrame, text="Close", command=handler)
        btn.pack()

    #----------------------------------------------------------------------
    def open_node(self):
        """"""
        self.hide()
        node_frame = Tk.Toplevel()
        node_frame.geometry("400x300")
        node_frame.title("Node")
        handler = lambda: self.onCloseOtherFrame(node_frame)
        btn = Tk.Button(node_frame, text="Back", command=handler)
        btn.pack()

    #----------------------------------------------------------------------
    def open_server(self):
        """"""
        self.hide()
        server_frame = Tk.Toplevel()
        server_frame.geometry("400x300")
        server_frame.title("Server")
        handler = lambda: self.onCloseOtherFrame(server_frame)
        btn = Tk.Button(server_frame, text="Back", command=handler)
        btn.pack()

    #----------------------------------------------------------------------
    def open_sum(self):
        """"""
        self.hide()
        sum_frame = Tk.Toplevel()
        sum_frame.geometry("400x300")
        sum_frame.title("Single User Mode")
        handler = lambda: self.onCloseOtherFrame(sum_frame)
        btn = Tk.Button(sum_frame, text="Back", command=handler)
        btn.pack()

    #----------------------------------------------------------------------
    def open_brute_force(self):
        """"""
        self.hide()
        brute_force_frame = Tk.Toplevel()
        brute_force_frame.geometry("400x300")
        brute_force_frame.title("Brute Force")
        handler = lambda: self.onCloseOtherFrame(brute_force_frame)
        btn = Tk.Button(brute_force_frame, text="Back", command=handler)
        btn.pack()

    #----------------------------------------------------------------------
    def open_dictionary(self):
        """"""
        self.hide()
        dictionary_frame = Tk.Toplevel()
        dictionary_frame.geometry("400x300")
        dictionary_frame.title("Dictionary")
        handler = lambda: self.onCloseOtherFrame(dictionary_frame)
        btn = Tk.Button(dictionary_frame, text="Back", command=handler)
        btn.pack()

    #----------------------------------------------------------------------
    def open_rainbow(self):
        """"""
        self.hide()
        rainbow_frame = Tk.Toplevel()
        rainbow_frame.geometry("400x300")
        rainbow_frame.title("Rainbow")
        handler = lambda: self.onCloseOtherFrame(rainbow_frame)
        btn = Tk.Button(rainbow_frame, text="Back", command=handler)
        btn.pack()

    #----------------------------------------------------------------------
    def open_hash(self):
        """"""
        self.hide()
        rainbow_frame = Tk.Toplevel()
        rainbow_frame.geometry("400x300")
        rainbow_frame.title("Hash")
        handler = lambda: self.onCloseOtherFrame(rainbow_frame)
        Tk.Button(self, text='ask open file', command=self.askopenfile).pack(**button_opt)
        btn = Tk.Button(rainbow_frame, text="Back", command=handler)
        btn.pack()
    #----------------------------------------------------------------------
    def onCloseOtherFrame(self, otherFrame):
        """"""
        otherFrame.destroy()
        self.show()

    #----------------------------------------------------------------------
    def show(self):
        """"""
        self.root.update()
        self.root.deiconify()
    #----------------------------------------------------------------------
    def askopenfile(self):

        """Returns an opened file in read mode."""
        self.file_opt = options = {}
        options['defaultextension'] = '.txt'
        options['filetypes'] = [('all files', '.*'), ('text files', '.txt')]
        options['initialdir'] = 'C:\\'
        options['initialfile'] = 'myfile.txt'
        options['parent'] = root
        options['title'] = 'This is a title'

        return tkFileDialog.askopenfile(mode='r', **self.file_opt)

#----------------------------------------------------------------------
if __name__ == "__main__":
    root = Tk.Tk()
    root.geometry("800x600")
    app = MyApp(root)
    root.mainloop()