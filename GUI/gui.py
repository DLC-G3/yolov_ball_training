import logging
from tkinter import *
from tkinter.ttk import Notebook
from queue import Queue

logging.info("Creating serversocket...")

class Main(Frame):
    def __init__(self, master=None):
        Frame.__init__(self,master)

    def init_window(self):
        self.master.title("DLC JTJ - GUI")
        self.pack(expand=1, fill="both")

    def on_closing():
        pass


if __name__ == '__main__':
    root = Tk()

    root.geometry('600x400')
    app = Main(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)

    try:
        root.mainloop()
    except KeyboardInterrupt:
        app.on_closing()