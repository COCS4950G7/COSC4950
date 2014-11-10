__author__ = 'Jon'


import Tkinter as Tk

########################################################################
class MyApp(object):
    """"""
    #def close_window(self):
    #    self.destroy()
    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        self.root = parent
        self.root.title("Main frame")
        self.frame = Tk.Frame(parent)
        self.frame.pack()

        btn_node = Tk.Button(self.frame, text="Node", command=self.open_node)
        btn_node.pack()

        btn_server = Tk.Button(self.frame, text="Server", command=self.open_server)
        btn_server.pack()

        btn_sum = Tk.Button(self.frame, text="Single User Mode", command=self.open_sum)
        btn_sum.pack()

        #btnExit = Tk.Button(self, text="Exit", command=close_window)


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
        otherFrame = Tk.Toplevel()
        otherFrame.geometry("400x300")
        otherFrame.title("Node")
        handler = lambda: self.onCloseOtherFrame(otherFrame)
        btn = Tk.Button(otherFrame, text="Back", command=handler)
        btn.pack()

    #----------------------------------------------------------------------
    def open_server(self):
        """"""
        self.hide()
        otherFrame = Tk.Toplevel()
        otherFrame.geometry("400x300")
        otherFrame.title("Server")
        handler = lambda: self.onCloseOtherFrame(otherFrame)
        btn = Tk.Button(otherFrame, text="Back", command=handler)
        btn.pack()

    #----------------------------------------------------------------------
    def open_sum(self):
        """"""
        self.hide()
        otherFrame = Tk.Toplevel()
        otherFrame.geometry("400x300")
        otherFrame.title("Single User Mode")
        handler = lambda: self.onCloseOtherFrame(otherFrame)
        btn_brute_force = Tk.Button(self.frame, text="Node", command=self.open_brute_force)
        btn_brute_force.pack()
        btn_dictionary = Tk.Button(self.frame, text="Node", command=self.open_dictionary)
        btn_dictionary.pack()
        btn_rainbow = Tk.Button(self.frame, text="Node", command=self.open_rainbow)
        btn_rainbow.pack()
        btn = Tk.Button(otherFrame, text="Back", command=handler)
        btn.pack()

    #----------------------------------------------------------------------
    def open_brute_force(self):
        """"""
        self.hide()
        otherFrame = Tk.Toplevel()
        otherFrame.geometry("400x300")
        otherFrame.title("Server")
        handler = lambda: self.onCloseOtherFrame(otherFrame)
        btn = Tk.Button(otherFrame, text="Back", command=handler)
        btn.pack()

    #----------------------------------------------------------------------
    def open_dictionary(self):
        """"""
        self.hide()
        otherFrame = Tk.Toplevel()
        otherFrame.geometry("400x300")
        otherFrame.title("Server")
        handler = lambda: self.onCloseOtherFrame(otherFrame)
        btn = Tk.Button(otherFrame, text="Back", command=handler)
        btn.pack()

    #----------------------------------------------------------------------
    def open_rainbow(self):
        """"""
        self.hide()
        otherFrame = Tk.Toplevel()
        otherFrame.geometry("400x300")
        otherFrame.title("Server")
        handler = lambda: self.onCloseOtherFrame(otherFrame)
        btn = Tk.Button(otherFrame, text="Back", command=handler)
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
if __name__ == "__main__":
    root = Tk.Tk()
    root.geometry("800x600")
    app = MyApp(root)
    root.mainloop()