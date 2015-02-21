__author__ = 'jwright'

import Tkinter as tk
from Tkinter import *
import ttk
import commands

root = tk.Tk()
root.title('Main Window')
root.geometry('400x400')

def dic_win():
    DicWin = tk.Toplevel(root)
    DicWin.title('Dictionary')
    DicWin.geometry('300x300')
    DicWinButton.config(state='disable')

    def quit_win():
        DicWin.destroy()
        DicWinButton.config(state='normal')

    #progressbar = ttk.Progressbar(orient=HORIZONTAL, length=200, mode='determinate')
    #progressbar.pack(side="bottom")
    #progressbar.start()

    QuitButton = tk.Button(DicWin, text='Quit', command=quit_win)
    QuitButton.pack()

def dic_script():
    print commands.getstatusoutput('python frameGUI_DIC.py')

DicWinButton = tk.Button(root, text='Dictionary', command=dic_script)
DicWinButton.pack()

def brut_win():
    BrutWin = tk.Toplevel(root)
    BrutWin.title('Brute Force')
    BrutWin.geometry('300x300')
    BrutWinButton.config(state='disable')

    def quit_win():
        BrutWin.destroy()
        BrutWinButton.config(state='normal')

    QuitButton = tk.Button(BrutWin, text='Quit', command=quit_win)
    QuitButton.pack()

BrutWinButton = tk.Button(root, text='Brute Force', command=brut_win)
BrutWinButton.pack()


def quit_win():
        root.destroy()
        root.config(state='normal')
QuitButton = tk.Button(root, text='Quit', command=quit_win)
QuitButton.pack()

root.mainloop()
