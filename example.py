#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import messagebox
from tkinter.messagebox import *
import tkinter
from PIL import Image, ImageTk
import os
#from tele.py import printCompanyInfo



class ABC(Frame):
    def __init__(self,parent=None):
        Frame.__init__(self,parent)
        self.parent = parent
        self.pack()
        self.make_widgets()

    def make_widgets(self):
        # don't assume that self.parent is a root window.
        # instead, call `winfo_toplevel to get the root window
        self.winfo_toplevel().title("Telepy search tool")

        # this adds something to the frame, otherwise the default
        # size of the window will be very small
        # L1 = Label(root, text = "Search term")
        # L1.pack( side = LEFT)
        # E1 = Entry(root)
        # E1.pack(side = RIGHT)
        # E1.focus_set()





def sel():
    if var.get()==1:
        text = "Name"
    else:
        text = "Location"
    selection = "You selected to search by " + text
    label.config(text = selection)

root = Tk()

text = StringVar()
E1 = StringVar()
var = IntVar()
R1 = Radiobutton(root, text = "Search by Name", variable = var, value = 1, command = sel)
R1.pack( anchor = W )

R2 = Radiobutton(root, text = "Search by location", variable = var, value = 2, command = sel)
R2.pack( anchor = W )




# C = Canvas(root, bg = "blue", height = 250, width = 300)
# coord = 10, 50, 240, 210
# arc = C.create_arc(coord, start = 0, extent = 150, fill = "red")
# line = C.create_line(10,10,200,200,fill = 'white')


# ------ Menubutton -----
# mb =  Menubutton ( root, text = "Search by...", relief = RAISED )
# mb.menu  =  Menu ( mb, tearoff = 10 )
# mb["menu"]  =  mb.menu
    
# name_search  = IntVar()
# location_search = IntVar()

# mb.menu.add_checkbutton ( label = "Name", variable = name_search )
# mb.menu.add_checkbutton ( label = "Location", variable = location_search )

# mb.pack(side="bottom", fill='both', expand=False, padx=2, pady=2)


#C.pack()
class Entry(Frame):
    def __init__(self,parent=None):
        Frame.__init__(self,parent)
        #self.title("Entry")

        self.entry = tkinter.Entry()
        self.entry.pack(fill=tkinter.BOTH, expand=0)

        button = tkinter.Button(text="Search", command=self.on_button_click)
        button.pack(fill=tkinter.BOTH, expand=0)

        button_2 = tkinter.Button(text="Show CSV", command=self.on_button_click_show)
        button_2.pack(fill=tkinter.BOTH, expand=0)

    def on_button_click_show(self):
        os.system("open 'output/csv/'"+self.entry.get()+".csv")

    def on_button_click(self):
        if var.get()==1:
            print("sudo python tele.py -f -e " + self.entry.get()+".csv")
            os.system("sudo python tele.py -f -e " + self.entry.get())
        else:
            os.system("sudo python tele.py -l -f -e " + self.entry.get())


label = Label(root)
label.pack()

abc = ABC(root)
application = Entry(root)
root.mainloop()
application.mainloop()