#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import messagebox
from tkinter.messagebox import *
import tkinter 
from PIL import Image, ImageTk
import os
#from tele.py import printCompanyInfo
from tkinter import filedialog
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import subprocess as sub



root = Tk()
root.geometry('600x500')


C = Canvas(root, bg="blue", height=250, width=300)
im = Image.open("tlf.png")
image = im.resize((400,200),Image.ANTIALIAS)
filename = ImageTk.PhotoImage(image)
background_label = Label(root, image=filename)
background_label.place(x=0, y=-100, relwidth=1, relheight=1)
C.pack()



class ABC(Frame):
    def __init__(self,parent=None):
        Frame.__init__(self,parent)
        self.parent = parent
        self.pack()
        self.make_widgets()

        # self.image = tkinter.PhotoImage('linkedin-logo.png')
        # label = tkinter.Label(self,image=self.image)
        # label.place(x=0, y=0, relwidth=1.0, relheight=1.0)

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

def combine_funcs(*funcs):
    def combined_func(*args, **kwargs):
        for f in funcs:
            f(*args, **kwargs)
    return combined_func

def enableEntry():
    entry_data.configure(state="normal")
    entry_data.update()

def disableEntry():
    entry_data.configure(state="disabled")
    entry_data.update()


def sel():

    if var.get()==1:
        text = "Name"
    else:
        text = "Location"
    
    if var_data.get()==1:
        text_data=" & partial data results"
        #starting_data = ". Starting from " + entry_data.get()
    else:
        text_data=" & full data results"


    selection = "\nYou selected to search by " + text + text_data
    label.config(text = selection)


text = StringVar()
E1 = StringVar()
var = IntVar()
var_data = IntVar()


L1 = Label(root, text="Welcome to the search tool. How do you want to query?")
L1.config(font=("Helvetica", 20))
L1.pack( anchor = W )



L2 = Label(root, text=" ")
L2.pack( anchor = W )

container = tkinter.Frame()

R1 = Radiobutton(root, text = "Search by Name     ", variable = var, value = 1, command = sel)
R1.pack( side="left", in_=container )
R1.config(font=("Helvetica", 15))

R3 = Radiobutton(root, text = "Retrieve all data", variable = var_data, value = 2, command=combine_funcs( disableEntry,sel))
R3.pack( side="left",in_=container )
R3.config(font=("Helvetica", 15))

container.pack(side="top", fill="x")

container = tkinter.Frame()

R2 = Radiobutton(root, text = "Search by location  ", variable = var, value = 2, command = sel)
R2.pack(  side="left",in_=container )
R2.config(font=("Helvetica", 15))

R4 = Radiobutton(root, text = "Retrieve up to 20 entries. Starting from: ", variable = var_data, value = 1, command = combine_funcs( enableEntry,sel))
R4.pack( side="left",in_=container )
R4.config(font=("Helvetica", 15))

entry_data = Entry(root, width=5)
entry_data.pack(side="left",in_=container )
entry_data.config(font=("Helvetica", 15))

container.pack(side="top", fill="x")


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

        

        container = tkinter.Frame()

        L2 = Label(text="Query input: ")
        L2.pack(in_=container, side="left")
        L2.config(font=("Helvetica", 15))        

        self.entry = tkinter.Entry( width=55)
        self.entry.pack( in_=container, side="left", expand=True)

        container.pack(side="top", fill="x")

        button = tkinter.Button(text="Search", command=self.on_button_click_search)
        button.pack(expand=0)
        button.config(font=("Helvetica", 15))

        button_2 = tkinter.Button(text="Show CSV", command=self.on_button_click_show_csv)
        button_2.pack( expand=0)
        button_2.config(font=("Helvetica", 15))

        self.NewWindow = tkinter.Button(self.master, 
                                text="Show Json", 
                                command=self.on_button_click_show_json)
        self.NewWindow.pack( expand=0)
        self.NewWindow.config(font=("Helvetica", 15))
        
        


    def on_button_click_show_json(self):
        self.root = tkinter.Toplevel()
        self.root.title("Showing: "+self.entry.get()+".json - Searched by Name")
        
        p = sub.Popen(['python','show_json.py',self.entry.get()],stdout=sub.PIPE,stderr=sub.PIPE)
        output, errors = p.communicate()

        text = Text(self.root)
        text.pack()
        text.insert(END, output)
    
        # self.txt = ScrolledText(self.root, undo=True)
        # self.txt['font'] = ('consolas', '12')
        # self.txt.pack(expand=True, fill='both')

        # scrollbar = Scrollbar(self.root)
        # scrollbar.pack( side = RIGHT, fill = Y )
        # mylist = Listbox(self.root, yscrollcommand = scrollbar.set )

        # with open("output/json/"+self.entry.get()+".json", "r") as f:
        #     Label(self.root, text=f.read()).pack()

        # mylist.pack( side = LEFT, fill = BOTH )
        # scrollbar.config( command = mylist.yview )

        

    def on_button_click_show_csv(self):
        # os.system("open 'output/csv/'"+self.entry.get()+".csv")
        self.root = tkinter.Toplevel()
        self.root.title("Showing: "+self.entry.get()+".json - Searched by Name")
        
        p = sub.Popen(['python','show_csv.py',self.entry.get()],stdout=sub.PIPE,stderr=sub.PIPE)
        output, errors = p.communicate()

        text = Text(self.root)
        text.pack()
        text.insert(END, output)

    def on_button_click_search(self):
        self.root = tkinter.Toplevel()
        self.root.title("Showing: "+self.entry.get()+".json - Searched by Name")
        
        if var.get()==1:
            if var_data.get()==1:
                print("sudo python tele.py -f -e -s " + self.entry.get() + " "+ entry_data.get())
                p = sub.Popen(['python','tele.py', '-f','-e', '-s', self.entry.get(), entry_data.get()],stdout=sub.PIPE,stderr=sub.PIPE)
            else:
                print("sudo python tele.py -f -c " + self.entry.get())
                p = sub.Popen(['python','tele.py', '-f','-c', self.entry.get()],stdout=sub.PIPE,stderr=sub.PIPE)
            
        else:
            if var_data.get()==1:
                print("sudo python tele.py -f -e -s -l " + self.entry.get() + " "+ entry_data.get())
                p = sub.Popen(['python','tele.py','-l', '-f','-e','-s', self.entry.get(), entry_data.get()],stdout=sub.PIPE,stderr=sub.PIPE)
            else:
                print("sudo python tele.py -f -e -l " + self.entry.get())
                p = sub.Popen(['python','tele.py', '-f','-e','-c', self.entry.get()],stdout=sub.PIPE,stderr=sub.PIPE)
            

        
        output, errors = p.communicate()

        text = Text(self.root)
        text.pack()
        text.insert(END, output)
        


label = Label(root)
label.pack()

abc = ABC(root)
application = Entry(root)
root.mainloop()
application.mainloop()