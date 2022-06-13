import logging
from tkinter import *
from tkinter.ttk import Notebook
from queue import Queue
from tkinter import filedialog
from PIL import Image, ImageTk

from Frames.ImagePreview import ImagePreview

logging.info("Creating serversocket...")

class Main(Frame):
    def __init__(self, master=None):
        Frame.__init__(self,master)
        self.master = master

        self.init_window()

    def init_window(self):
        self.cam_4_image = StringVar()
        self.cam_6_image = StringVar()

        self.master.title("DLC JTJ - GUI")
        self.pack(expand=1, fill="both")

        Label(self, text="Recording name: ").grid(row=0, sticky=W, padx=10, pady=4)
        self.entry_recording_name = Entry(self)
        self.entry_recording_name.grid(row=1, column=0, columnspan=4, sticky=N+S+E+W, padx=10, pady=4)

        self.button_send_broadcast = Button(self, text = "Submit name", command=self.submit_name)
        self.button_send_broadcast.grid(row=1, column=5, sticky=N+S+E+W, padx=10)

        Label(self, text="Cam 4: ").grid(row=2, sticky=W, padx=10, pady=4)
        self.cam_4_preview = Button(self, text = "Browse images", command=self.browse_files_cam_4)
        self.cam_4_preview.grid(row=3, column=0, sticky=N+W, padx=10)
        self.label_cam_4 = Label(self, textvariable=self.cam_4_image).grid(row=3, column=1, sticky=N+W)

        self.preview_button_cam_4 = Button(self, text = "Preview image", command=self.show_image_preview)
        self.preview_button_cam_4.grid(row=4, column=0, sticky=N+W, padx=10, pady=4)

        
        Label(self, text="Cam 6: ").grid(row=5, sticky=W, padx=10, pady=4)
        self.cam_4_preview = Button(self, text = "Browse images", command=self.browse_files_cam_6)
        self.cam_4_preview.grid(row=6, column=0, sticky=N+W, padx=10)
        Label(self, textvariable=self.cam_6_image).grid(row=6, column=1, sticky=N+W)

        self.preview_button_cam_6 = Button(self, text = "Preview image", command=self.show_image_preview)
        self.preview_button_cam_6.grid(row=7, column=0, sticky=N+W, padx=10, pady=4)

        Grid.columnconfigure(self, 0, weight=1)
        Grid.rowconfigure(self, 7, weight=1)


    def submit_name():
        pass

    def show_image_preview(self):
        newWindow = Toplevel(self.master)
        newWindow.title("Preview")
        newWindow.geometry("750x270")
        f = Frame(newWindow)
        f.pack()
        canvas= Canvas(f, width= 600, height= 400)
        canvas.pack()

        Label(f, text="Ik ben gay. SSSSHHHH!").pack()

        #Load an image in the script
        img = ImageTk.PhotoImage(Image.open('img.jpg'))

        #Add image to the Canvas Items
        canvas.create_image(10,10,anchor=NW,image=img)
        

    def browse_files_cam_4(self):
        filename = filedialog.askopenfilename(initialdir = "/",
                                        title = "Select a File",
                                        filetypes = (("jpeg Files","*.jpg"),
                                                    ('png files', "*.png"),
                                                    ("all files", "*.*")))
        self.cam_4_image.set(filename)

    def browse_files_cam_6(self):
        filename = filedialog.askopenfilename(initialdir = "/",
                                        title = "Select a File",
                                        filetypes = (("jpeg Files","*.jpg"),
                                                    ('png files', "*.png"),
                                                    ("all files", "*.*")))
        self.cam_6_image.set(filename)
      

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