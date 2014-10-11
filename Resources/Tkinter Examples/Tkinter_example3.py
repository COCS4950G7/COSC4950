#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#


#   http://stackoverflow.com/questions/11100380/solution-python3-tkinter-jump-from-one-window-to-another-with-back-and-next-but

# Creates three "windows" that the user can navigate through using Back and Next - buttons.

import Tkinter

def create_widgets_in_first_frame():
    # Create the label for the frame
    first_window_label = Tkinter.Label(first_frame, text='Window 1')
    first_window_label.grid(column=0, row=0, pady=10, padx=10, sticky=(Tkinter.N))

    # Create the button for the frame
    first_window_quit_button = Tkinter.Button(first_frame, text = "Quit", command = quit_program)
    first_window_quit_button.grid(column=0, row=1, pady=10, sticky=(Tkinter.N))
    first_window_next_button = Tkinter.Button(first_frame, text = "Next", command = call_second_frame_on_top)
    first_window_next_button.grid(column=1, row=1, pady=10, sticky=(Tkinter.N))

def create_widgets_in_second_frame():
    # Create the label for the frame
    second_window_label = Tkinter.Label(second_frame, text='Window 2')
    second_window_label.grid(column=0, row=0, pady=10, padx=10, sticky=(Tkinter.N))

    # Create the button for the frame
    second_window_back_button = Tkinter.Button(second_frame, text = "Back", command = call_first_frame_on_top)
    second_window_back_button.grid(column=0, row=1, pady=10, sticky=(Tkinter.N))
    second_window_next_button = Tkinter.Button(second_frame, text = "Next", command = call_third_frame_on_top)
    second_window_next_button.grid(column=1, row=1, pady=10, sticky=(Tkinter.N))

def create_widgets_in_third_frame():
    # Create the label for the frame
    third_window_label = Tkinter.Label(third_frame, text='Window 3')
    third_window_label.grid(column=0, row=0, pady=10, padx=10, sticky=(Tkinter.N))

    # Create the button for the frame
    third_window_back_button = Tkinter.Button(third_frame, text = "Back", command = call_second_frame_on_top)
    third_window_back_button.grid(column=0, row=1, pady=10, sticky=(Tkinter.N))
    third_window_quit_button = Tkinter.Button(third_frame, text = "Quit", command = quit_program)
    third_window_quit_button.grid(column=1, row=1, pady=10, sticky=(Tkinter.N))

def call_first_frame_on_top():
    # This function can be called only from the second window.
    # Hide the second window and show the first window.
    second_frame.grid_forget()
    first_frame.grid(column=0, row=0, padx=20, pady=5, sticky=(Tkinter.W, Tkinter.N, Tkinter.E))

def call_second_frame_on_top():
    # This function can be called from the first and third windows.
    # Hide the first and third windows and show the second window.
    first_frame.grid_forget()
    third_frame.grid_forget()
    second_frame.grid(column=0, row=0, padx=20, pady=5, sticky=(Tkinter.W, Tkinter.N, Tkinter.E))

def call_third_frame_on_top():
    # This function can only be called from the second window.
    # Hide the second window and show the third window.
    second_frame.grid_forget()
    third_frame.grid(column=0, row=0, padx=20, pady=5, sticky=(Tkinter.W, Tkinter.N, Tkinter.E))

def quit_program():
    root_window.destroy()

###############################
# Main program starts here :) #
###############################

# Create the root GUI window.
root_window = Tkinter.Tk()

# Define window size
window_width = 200
window_heigth = 100

# Create frames inside the root window to hold other GUI elements. All frames must be created in the main program, otherwise they are not accessible in functions.
first_frame=Tkinter.Frame(root_window, width=window_width, height=window_heigth)
first_frame['borderwidth'] = 2
first_frame['relief'] = 'sunken'
first_frame.grid(column=0, row=0, padx=20, pady=5, sticky=(Tkinter.W, Tkinter.N, Tkinter.E))

second_frame=Tkinter.Frame(root_window, width=window_width, height=window_heigth)
second_frame['borderwidth'] = 2
second_frame['relief'] = 'sunken'
second_frame.grid(column=0, row=0, padx=20, pady=5, sticky=(Tkinter.W, Tkinter.N, Tkinter.E))

third_frame=Tkinter.Frame(root_window, width=window_width, height=window_heigth)
third_frame['borderwidth'] = 2
third_frame['relief'] = 'sunken'
third_frame.grid(column=0, row=0, padx=20, pady=5, sticky=(Tkinter.W, Tkinter.N, Tkinter.E))

# Create all widgets to all frames
create_widgets_in_third_frame()
create_widgets_in_second_frame()
create_widgets_in_first_frame()

# Hide all frames in reverse order, but leave first frame visible (unhidden).
third_frame.grid_forget()
second_frame.grid_forget()

# Start tkinter event - loop
root_window.mainloop()