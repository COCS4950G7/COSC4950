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

    QuitButton = tk.Button(DicWin, text='Quit', command=quit_win)
    QuitButton.pack()

def dic_script():
    print commands.getstatusoutput('python frameGUI_DIC.py')
    quit_win()

DicWinButton = tk.Button(root, text='Dictionary', command=dic_script)
DicWinButton.pack()
#=======================================================================================
#def brut_win():
#    brutWin = tk.Toplevel(root)
#    brutWin.title('Brut Force')
#    brutWin.geometry('300x300')
#    brutWinButton.config(state='disable')

#    def quit_win():
#        brutWin.destroy()
#        brutWinButton.config(state='normal')

#    QuitButton = tk.Button(brutWin, text='Quit', command=quit_win)
#    QuitButton.pack()

def brut_script():
    hideRoot()
    print commands.getstatusoutput('python frameGUI_BRUT.py')
    showRoot()

brutWinButton = tk.Button(root, text='Brute Force', command=brut_script)
brutWinButton.pack()

def hideRoot():
    root.withdraw()

def showRoot():
    root.update()
    root.deiconify()


def quit_win():
        root.destroy()
        root.config(state='normal')
QuitButton = tk.Button(root, text='Quit', command=quit_win)
QuitButton.pack()

root.mainloop()
