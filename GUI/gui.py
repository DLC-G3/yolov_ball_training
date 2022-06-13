import logging
from tkinter import *
from tkinter.ttk import Notebook
from queue import Queue
from tkinter import filedialog
from tracemalloc import start
from turtle import clear
from PIL import Image, ImageTk
import cv2
from pyparsing import col

from Frames.ImagePreview import ImagePreview
from Frames.RecordingFrame import RecordingFrame
from Frames.Cam4 import Cam4
from Frames.Cam6 import Cam6
from Frames.CanvasFrame import CanvasFrame

logging.info("Creating serversocket...")

class Main(Frame):
    def __init__(self, master=None):
        Frame.__init__(self,master)
        self.master = master

        self.init_window()

    def init_window(self):
        self.cam_4_image = StringVar()
        self.cam_4_image_short = StringVar()
        self.cam_6_image = StringVar()
        self.cam_6_image_short = StringVar()

        self.master.title("DLC JTJ - GUI")
        self.pack(expand=1, fill="both")

        self.recording_frame = RecordingFrame(self)
        self.recording_frame.grid(row=0, column=0, sticky=W+E, padx=10, pady=4)

        self.canvas_frame = CanvasFrame(self)
        self.canvas_frame.grid(row=0, column=1, sticky=W+E, padx=10, pady=4)

        self.cam_4_frame = Cam4(self)
        self.cam_4_frame.grid(row=2, column=0, sticky=W+E, padx=10, pady=4)
        self.cam_6_frame = Cam6(self)
        self.cam_6_frame.grid(row=2, column=1, sticky=W+E, padx=10, pady=4)

        self.cam_4_label = Label(self)
        self.cam_4_label.grid(row=3, column=0, sticky=N+S+E+W)

        self.cam_6_label = Label(self)
        self.cam_6_label.grid(row=3, column=1, sticky=N+S+E+W)

        self.submit_form = Button(self, text = "Detect goals", command=self.submit_form)
        self.submit_form.grid(row=4, column=0, columnspan=2, sticky=S+E+W)

        Grid.columnconfigure(self, 6, weight=1)
        Grid.rowconfigure(self, 5, weight=1)

    def submit_form(self):
        pass

    def submit_name(self):
        pass


    def show_image_preview_cam_4(self, new_scale_value):
        resize_x = 480
        resize_y = 270

        img = cv2.resize(cv2.imread(self.cam_4_image.get()), (resize_x,resize_y), interpolation= cv2.INTER_LINEAR)

        starting_point = (round(self.cam_4_frame.sli_1_x.get() / 100 * resize_x), round(self.cam_4_frame.sli_1_y.get() / 100 * resize_y))
        ending_point = (round(self.cam_4_frame.sli_2_x.get() / 100 * resize_x), round(self.cam_4_frame.sli_2_y.get() / 100 * resize_y))

        image = cv2.rectangle(img, starting_point, ending_point, (255,0,0), 2)

        x = starting_point[0]
        y = starting_point[1]
        w = ending_point[0]
        h = ending_point[1]

        self.update_cam_4(image)

    def show_image_preview_cam_6(self, new_scale_value):
        resize_x = 480
        resize_y = 270

        img = cv2.resize(cv2.imread(self.cam_6_image.get()), (resize_x,resize_y), interpolation= cv2.INTER_LINEAR)

        starting_point = (round(self.cam_6_frame.sli_1_x.get() / 100 * resize_x), round(self.cam_6_frame.sli_1_y.get() / 100 * resize_y))
        ending_point = (round(self.cam_6_frame.sli_2_x.get() / 100 * resize_x), round(self.cam_6_frame.sli_2_y.get() / 100 * resize_y))

        image = cv2.rectangle(img, starting_point, ending_point, (255,0,0), 2)

        x = starting_point[0]
        y = starting_point[1]
        w = ending_point[0]
        h = ending_point[1]

        self.update_cam_6(image)
        

    def browse_files_cam_4(self):
        filename = filedialog.askopenfilename(initialdir = "/",
                                        title = "Select a File",
                                        filetypes = (("jpeg Files","*.jpg"),
                                                    ('png files', "*.png"),
                                                    ("all files", "*.*")))
        self.cam_4_image.set(filename)
        filename_short = filename.split('/')[-1]
        self.cam_4_image_short.set(filename_short)

        image = cv2.imread(self.cam_4_image.get())
        half = cv2.resize(image, (480,270))
        self.update_cam_4(half)

    def browse_files_cam_6(self):
        filename = filedialog.askopenfilename(initialdir = "/",
                                        title = "Select a File",
                                        filetypes = (("jpeg Files","*.jpg"),
                                                    ('png files', "*.png"),
                                                    ("all files", "*.*")))
        self.cam_6_image.set(filename)
        filename_short = filename.split('/')[-1]
        self.cam_6_image_short.set(filename_short)

        image = cv2.imread(self.cam_6_image.get())
        half = cv2.resize(image, (480,270))
        self.update_cam_6(half)

    def update_cam_4(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        image = ImageTk.PhotoImage(image)

        self.cam_4_label.image = image  # <== this is were we anchor the img object
        self.cam_4_label.configure(image=image)

    def update_cam_6(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        image = ImageTk.PhotoImage(image)

        self.cam_6_label.image = image  # <== this is were we anchor the img object
        self.cam_6_label.configure(image=image)
        
    def on_closing():
        pass


if __name__ == '__main__':
    root = Tk()
    root.resizable(False, False)
    root.geometry('1120x720')
    app = Main(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)

    try:
        root.mainloop()
    except KeyboardInterrupt:
        app.on_closing()