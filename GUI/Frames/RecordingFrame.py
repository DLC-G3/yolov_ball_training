from tkinter import *

class RecordingFrame(Frame):
    def __init__(self, master=None):
        Frame.__init__(self,master)
        self.master = master

        self.init_window()

    def init_window(self):
        Label(self, text="Recording name or url: ").grid(row=0, column=0, sticky=W)

        self.entry_recording_name = Entry(self)
        self.entry_recording_name.grid(row=1, column=0, columnspan=4, sticky=N+S+E+W)
        self.entry_recording_name.insert(0, "A-Team - Diest")
        
        self.button_send_broadcast = Button(self, text = "Detect cameras", command=lambda: self.master.submit_name(self.entry_recording_name.get()))
        self.button_send_broadcast.grid(row=1, column=4, columnspan=1, sticky=N+S+E+W)

        Grid.rowconfigure(self, 0, weight=1)
        Grid.columnconfigure(self, 3, weight=1)
