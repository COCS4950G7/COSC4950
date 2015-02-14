__author__ = 'jwright'

# Text and pictures tutorial
# http://pythonprogramming.net/tkinter-adding-text-images/
import Tkinter as tk
import Tkconstants, tkFileDialog
from Tkinter import *

class TkDictionary(tk.Frame):

  def __init__(self, dictonary):

    tk.Frame.__init__(self, dictonary)

    # options for buttons
    button_opt = {'fill': Tkconstants.BOTH, 'padx': 5, 'pady': 5}

    # define buttons
    tk.Button(self, text='Select Dictionary', command=self.askopenfile).pack(**button_opt)

    # define options for opening or saving a file
    self.file_opt = options = {}
    options['defaultextension'] = '.txt'
    options['filetypes'] = [('all files', '.*'), ('text files', '.txt')]
    options['initialdir'] = 'C:\\'
    options['initialfile'] = 'myfile.txt'
    options['parent'] = dictonary
    options['title'] = 'This is a title'

    # defining options for opening a directory
    self.dir_opt = options = {}
    options['initialdir'] = 'C:\\'
    options['mustexist'] = False
    options['parent'] = dictonary
    options['title'] = 'This is a title'

  def askopenfile(self):

    return tkFileDialog.askopenfile(mode='r', **self.file_opt)

  def showText(self):
      text = Label(self, text="Choose a dictionary file to use.")
      text.pack()



if __name__=='__main__':
  dictonary = tk.Tk()
  dictonary.geometry("400x300")
  dictonary.title("Dictionary")
  TkDictionary(dictonary).pack()
  dictonary.mainloop()