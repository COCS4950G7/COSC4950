__author__ = 'jwright'

# Text and pictures tutorial
# http://pythonprogramming.net/tkinter-adding-text-images/
import Tkinter as tk
import Tkconstants, tkFileDialog
from Tkinter import *

class Tkbrut(tk.Frame):

  def __init__(self, brut):

    tk.Frame.__init__(self, brut)

  def quit_win(self):
        brut.destroy()

  QuitButton = tk.Button(brut, text='Back', command=quit_win)
  QuitButton.pack()


if __name__=='__main__':
  brut = tk.Tk()
  brut.geometry("400x300")
  brut.title("Brute Force")
  Tkbrut(brut).pack()
  brut.mainloop()