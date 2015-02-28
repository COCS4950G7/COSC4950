__author__ = 'jwright'

# Text and pictures tutorial
# http://pythonprogramming.net/tkinter-adding-text-images/
import Tkinter as tk
import Tkconstants, tkFileDialog
from Tkinter import *

class TkRainbow(tk.Frame):

  def __init__(self, rainbow):

    tk.Frame.__init__(self, rainbow)


if __name__=='__main__':
  rainbow = tk.Tk()
  rainbow.geometry("400x300")
  rainbow.title("Rainbow Table")
  TkRainbow(rainbow).pack()
  rainbow.mainloop()