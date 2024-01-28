'''
If using Ubuntu you must run the following before being able to use tkinter:

sudo apt-get install python3.11-tk

The out-of-the-box tkinter doesn't seem to work on Ubuntu without being explicitly installed with apt-get.
'''

import tkinter as tk
from PIL import Image, ImageTk

root = tk.Tk()
root.geometry('300x200')
root.resizable(width=False, height=False)

color1 = '#0a0b0c'
color2 = '#f5267b'
color3 = '#ff3d8d'
color4 = 'BLACK'
font1 = ('Arial', 15, 'bold')

main_frame = tk.Frame(root, bg=color1, pady=20)
main_frame.pack(fill=tk.BOTH, expand=True)
main_frame.columnconfigure(0, weight=1)
main_frame.rowconfigure(0, weight=1)

button1 = tk.Button(
    main_frame,
    # background=color2,
    # foreground=color4,
    width=10,
    height=2,
    # highlightthickness=0,
    # highlightbackground=color2,
    # highlightcolor="WHITE",
    # activebackground=color3,
    # activeforeground=color4,
    cursor="hand1",
    bd=2,
    text="ON",
    font=font1,
)

button2 = tk.Button(
    main_frame,
    text='test',
    width=10,
    height=2,
    font=font1)

button1.grid(column=0, row=0)

button2.grid(column=0, row=1)

def button1_enter(event):
    button1.config(
        highlightbackground=color3,
    )

def button1_leave(event):
    button1.config(
        highlightbackground=color2,
    )

button1.bind('<Enter>', button1_enter)
button1.bind('<Leave>', button1_leave)

root.mainloop()