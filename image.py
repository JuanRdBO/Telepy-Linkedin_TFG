from tkinter import *

from PIL import Image, ImageTk

root = Tk()
root.title("Title")
root.geometry("600x600")
root.configure(background="black")



class Example(Frame):
    def __init__(self, master, *pargs, parent=None):
        Frame.__init__(self, master, *pargs, parent)
        self.parent = parent
        self.pack()
        self.make_widgets()


        self.image = Image.open("linkedin-logo.png")
        self.img_copy= self.image.copy()


        self.background_image = ImageTk.PhotoImage(self.image)

        self.background = Label(self, image=self.background_image)
        self.background.pack(fill=BOTH, expand=YES)
        self.background.bind('<Configure>', self._resize_image)

    def make_widgets(self):
        # don't assume that self.parent is a root window.
        # instead, call `winfo_toplevel to get the root window
        self.winfo_toplevel().title("Telepy search tool")

        # this adds something to the frame, otherwise the default
        # size of the window will be very small
        L1 = Label(root, text = "Search term")
        L1.pack( side = LEFT)
        E1 = Entry(root)
        E1.pack(side = RIGHT)
    
    def _resize_image(self,event):

        new_width = event.width
        new_height = event.height

        self.image = self.img_copy.resize((new_width, new_height))

        self.background_image = ImageTk.PhotoImage(self.image)
        self.background.configure(image =  self.background_image)



e = Example(root)
e.pack(fill=BOTH, expand=YES)


root.mainloop()