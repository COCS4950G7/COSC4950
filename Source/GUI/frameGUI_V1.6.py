__author__ = 'jwright'

import Tkinter as tk
from Tkinter import *
import ttk

root = tk.Tk()
root.title('Main Window')
root.geometry('400x400')

def get_new_win():

    NewWin = tk.Toplevel(root)
    NewWin.title('New Window')
    NewWin.geometry('300x300')
    NewWinButton.config(state='disable')

    def quit_win():
        NewWin.destroy()
        NewWinButton.config(state='normal')

    QuitButton = tk.Button(NewWin, text='Quit', command=quit_win)
    QuitButton.pack()

    NewWin.protocol("WM_DELETE_WINDOW", quit_win)

NewWinButton = tk.Button(root, text='New Window', command=get_new_win)
NewWinButton.pack()

def dic_win():
    DicWin = tk.Toplevel(root)
    DicWin.title('Dictionary')
    DicWin.geometry('300x300')
    DicWinButton.config(state='disable')

    def quit_win():
        DicWin.destroy()
        DicWinButton.config(state='normal')

        progressbar = ttk.Progressbar(orient=HORIZONTAL, length=200, mode='determinate')
        progressbar.pack(side="bottom")
        progressbar.start()

    QuitButton = tk.Button(DicWin, text='Quit', command=quit_win)
    QuitButton.pack()

DicWinButton = tk.Button(root, text='Dictionary', command=dic_win)
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

root.mainloop()
