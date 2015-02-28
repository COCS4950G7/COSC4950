__author__ = 'jwright'

import Tkinter as tk
from Tkinter import *
import hashlib

class HashIt(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.inputHashTextFieldLabel= Label(self, text="Enter a string to Hash")
        self.inputHashTextFieldLabel.pack(side=TOP, padx=5, pady=5)
        self.inputHashTextField= Entry(self, bd=5)
        self.inputHashTextField.pack(side=TOP, padx=5, pady=5)

        self.HashButton = tk.Button(self, text="Hash", command=self.on_button2)
        self.HashButton.pack()


        #This will display the results, could set to show up after the program is run.
        self.outputHashTextFieldLabel= Label(self, text="Results")
        self.outputHashTextFieldLabel.pack(side=TOP, padx=5, pady=5)
        self.outputHashTextField= Entry(self, bd=5)
        #self.outputHashTextField.insert(0, "Test")
        self.outputHashTextField.insert(0, self.on_button2)
        #This will disable modification but you cant hightlight and copy it.
        #self.outputHashTextField.config(state='disabled')
        self.outputHashTextField.pack(side=TOP,padx=5, pady=5)

    def on_button(self):
        print self.entry.get()

    def on_button2(self):
        hash_object = hashlib.md5(self.inputHashTextField.get())
        #print self.inputHashTextField.get()
        print(hash_object.hexdigest())

app = HashIt()
app.geometry("400x300")
app.title("Hash It")
#HashIt(app).pack()
app.mainloop()