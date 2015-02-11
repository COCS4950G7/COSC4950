__author__ = 'jwright'

# Text and pictures tutorial
# http://pythonprogramming.net/tkinter-adding-text-images/
import Tkinter, Tkconstants, tkFileDialog
from Tkinter import *

class TkDictionary(Tkinter.Frame):

  def __init__(self, root):

    Tkinter.Frame.__init__(self, root)

    # options for buttons
    button_opt = {'fill': Tkconstants.BOTH, 'padx': 5, 'pady': 5}

    # define buttons
    Tkinter.Button(self, text='Select Dictionary', command=self.askopenfile).pack(**button_opt)

    # define options for opening or saving a file
    self.file_opt = options = {}
    options['defaultextension'] = '.txt'
    options['filetypes'] = [('all files', '.*'), ('text files', '.txt')]
    options['initialdir'] = 'C:\\'
    options['initialfile'] = 'myfile.txt'
    options['parent'] = root
    options['title'] = 'This is a title'

    # defining options for opening a directory
    self.dir_opt = options = {}
    options['initialdir'] = 'C:\\'
    options['mustexist'] = False
    options['parent'] = root
    options['title'] = 'This is a title'

  def askopenfile(self):

    return tkFileDialog.askopenfile(mode='r', **self.file_opt)

  def showText(self):
      text = Label(self, text="Choose a dictionary file to use.")
      text.pack()


if __name__=='__main__':
  root = Tkinter.Tk()
  root.geometry("800x600")
  root.title("Dictionary")
  TkDictionary(root).pack()
  root.mainloop()