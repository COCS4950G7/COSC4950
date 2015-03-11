__author__ = 'jwright'

import Tkinter as tk
from Tkinter import *
import hashlib

class HashIt(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.inputHashTextFieldLabel= Label(self, text="Enter a string to Hash")
        self.inputHashTextFieldLabel.pack(side=TOP, padx=5, pady=5)

        #First Text Field
        self.inputHashTextField= Entry(self, bd=5)
        self.inputHashTextField.pack(side=TOP, padx=5, pady=5)

        #Hash Button
        self.HashButton = tk.Button(self, text="Hash", command=self.on_button)
        self.HashButton.pack()

        self.outputHashTextFieldLabel= Label(self, text="Results")
        self.outputHashTextFieldLabel.pack(side=TOP, padx=5, pady=5)

        #Second Text Field
        #This will display the results, is there a better way that allows user to copy?
        self.outputHashTextField= Entry(self, bd=5)
        #self.outputHashTextField.insert(0, "Test") #This will prefill it with "Test"
        self.outputHashTextField.insert(0, self.on_button)
        self.outputHashTextField.pack(side=TOP,padx=5, pady=5)

    def on_button(self):
        hash_object = hashlib.md5(self.inputHashTextField.get())
        #print self.inputHashTextField.get()
        #print(hash_object.hexdigest())
        #
        print hash_object.hexdigest()
        return hash_object.hexdigest()

app = HashIt()
app.geometry("400x300")
app.title("Hash It")
app.mainloop()