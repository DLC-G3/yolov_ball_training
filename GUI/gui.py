import logging
from tkinter import *
from tkinter.ttk import Notebook
from queue import Queue
from tkinter import filedialog
from tracemalloc import start
from PIL import Image, ImageTk

import cv2

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

        frame_starting_point = Frame(self)
        frame_starting_point. grid(row=2, column=0, columnspan=6, sticky=N+S+E+W)
        Label(frame_starting_point, text="Cam 4: ").grid(row=0, sticky=W, padx=10, pady=4)


        self.cam_4_preview = Button(frame_starting_point, text = "Browse images", command=self.browse_files_cam_4)
        self.cam_4_preview.grid(row=1, column=0, sticky=N+W, padx=10)
        self.label_cam_4 = Label(frame_starting_point, textvariable=self.cam_4_image).grid(row=1, column=1, sticky=N+W)

        Label(frame_starting_point, text="Start point: ").grid(row=2, sticky=W, padx=10, pady=4)
        Label(frame_starting_point, text="x: ").grid(row=3, sticky=W, padx=10)
        self.sli_1_x = Scale(frame_starting_point, from_=0, to=100, resolution=0.01, orient=HORIZONTAL, sliderlength=10, length=400)
        self.sli_1_x.grid(row=3, column=1, sticky=W+E, padx=10)

        Label(frame_starting_point, text="y: ").grid(row=4, sticky=W, padx=10)
        self.sli_1_y = Scale(frame_starting_point, from_=0, to=100, resolution=0.01, orient=HORIZONTAL, sliderlength=10, length=400)
        self.sli_1_y.grid(row=4, column=1, sticky=N+W, padx=10)

        Label(frame_starting_point, text="End point: ").grid(row=5, sticky=W, padx=10, pady=4)
        Label(frame_starting_point, text="x: ").grid(row=6, sticky=W, padx=10)
        self.sli_2_x = Scale(frame_starting_point, from_=0, to=100, resolution=0.01, orient=HORIZONTAL, sliderlength=10, length=400)
        self.sli_2_x.grid(row=6, column=1, sticky=N+W, padx=10)

        Label(frame_starting_point, text="y: ").grid(row=7, sticky=W, padx=10)
        self.sli_2_y = Scale(frame_starting_point, from_=0, to=100, resolution=0.01, orient=HORIZONTAL, sliderlength=10, length=400)
        self.sli_2_y.grid(row=7, column=1, sticky=N+W, padx=10)

        self.preview_button_cam_4 = Button(frame_starting_point, text = "Preview image", command=self.show_image_preview_cam_4)
        self.preview_button_cam_4.grid(row=8, column=0, sticky=N+W, padx=10, pady=4)


        
        Label(self, text="Cam 6: ").grid(row=3, sticky=W, padx=10, pady=4)
        self.cam_4_preview = Button(self, text = "Browse images", command=self.browse_files_cam_6)
        self.cam_4_preview.grid(row=4, column=0, sticky=N+W, padx=10)
        Label(self, textvariable=self.cam_6_image).grid(row=6, column=1, sticky=N+W)

        self.preview_button_cam_6 = Button(self, text = "Preview image", command=self.show_image_preview_cam_6)
        self.preview_button_cam_6.grid(row=5, column=0, sticky=N+W, padx=10, pady=4)

        Grid.columnconfigure(self, 6, weight=1)
        Grid.rowconfigure(self, 5, weight=1)
        Grid.columnconfigure(frame_starting_point, 6, weight=1)


    def submit_name():
        pass

    def show_image_preview_cam_4(self):
        resize_x = 1920
        resize_y = 1080


        img = cv2.resize(cv2.imread(self.cam_4_image.get()), (resize_x,resize_y), interpolation= cv2.INTER_LINEAR)

        starting_point = (round(self.sli_1_x.get() / 100 * resize_x), round(self.sli_1_y.get() / 100 * resize_y))
        ending_point = (round(self.sli_2_x.get() / 100 * resize_x), round(self.sli_2_y.get() / 100 * resize_y))

        image = cv2.rectangle(img, starting_point, ending_point, (255,0,0), 2)

        


        cv2.imshow('Example', image)
        cv2.waitKey(0) # waits until a key is pressed
        cv2.destroyAllWindows() # destroys the window showing image

    def show_image_preview_cam_6(self):
        img = cv2.resize(cv2.imread(self.cam_6_image.get()), (1280,720), interpolation= cv2.INTER_LINEAR)
    
        cv2.imshow('Example', img)
        cv2.waitKey(0) # waits until a key is pressed
        cv2.destroyAllWindows() # destroys the window showing image
        

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