from tkinter import *

class CanvasFrame(Frame):
    def __init__(self, master=None):
        Frame.__init__(self,master)
        self.master = master

        self.init_window()

    def init_window(self):
        Label(self, text="Name for the new canvas: ").grid(row=0, column=0, sticky=W)

        self.entry_canvas_name = Entry(self)
        self.entry_canvas_name.grid(row=1, column=0, columnspan=4, sticky=N+S+E+W)

        Grid.rowconfigure(self, 0, weight=1)
        Grid.columnconfigure(self, 3, weight=1)
