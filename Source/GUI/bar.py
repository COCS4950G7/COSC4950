# __author__ = 'jwright'
# This is the GUI version of progress bar.
from Tkinter import *
import ttk
root = Tk()
progressbar = ttk.Progressbar(orient=HORIZONTAL, length=200, mode='determinate')
progressbar.pack(side="bottom")
progressbar.start()
root.mainloop()


# Here is a command line version of progress bar, Chris's lookes better.
# import time
# import sys
#
# toolbar_width = 40
#
# # setup toolbar
# sys.stdout.write("[%s]" % (" " * toolbar_width))
# sys.stdout.flush()
# sys.stdout.write("\b" * (toolbar_width+1)) # return to start of line, after '['
#
# for i in xrange(toolbar_width):
#     time.sleep(0.1) # do real work here
#     # update the bar
#     sys.stdout.write("-")
#     sys.stdout.flush()
#
# sys.stdout.write("\n")