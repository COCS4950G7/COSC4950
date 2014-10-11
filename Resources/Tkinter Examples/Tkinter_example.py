

#import Tkinter

#l = Tkinter.Label(text = "***************************See me?*************************")

#l.pack()

#l.mainloop()

#print("Howdy")

#omfg
#print("dostuff")




#   http://www.ferg.org/thinking_in_tkinter/all_programs.html


from Tkinter import *


class MyApp:

    def __init__(self, parent):

        self.myParent = parent  ### (7) remember my parent, the root
        self.myContainer1 = Frame(parent)
        self.myContainer1.pack()

        self.button1 = Button(self.myContainer1)
        self.button1.configure(text="OK", background= "green")
        self.button1.pack(side=LEFT)
        self.button1.bind("<Button-1>", self.button1Click) ### (1)

        self.button2 = Button(self.myContainer1)
        self.button2.configure(text="Cancel", background="red")
        self.button2.pack(side=RIGHT)
        self.button2.bind("<Button-1>", self.button2Click) ### (2)

    def button1Click(self, event):    ### (3)

        if self.button1["background"] == "green": ### (4)

            self.button1["background"] = "yellow"

        else:

            self.button1["background"] = "green"

    def button2Click(self, event):  ### (5)

        self.myParent.destroy()     ### (6)


root = Tk()
myapp = MyApp(root)
root.mainloop()