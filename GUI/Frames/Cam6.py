from tkinter import *

class Cam6(Frame):
    def __init__(self, master=None):
        Frame.__init__(self,master)
        self.master = master

        self.init_window()

    def init_window(self):
        Label(self, text="Cam 6: ").grid(row=0, sticky=W, padx=10, pady=4)

        Label(self, text="Top left: ").grid(row=2, sticky=W, padx=10, pady=4)
        Label(self, text="x: ").grid(row=3, sticky=W, padx=10)
        self.sli_1_x = Scale(self, from_=0, to=100, resolution=0.01, orient=HORIZONTAL, sliderlength=10, length=400, command=self.master.show_image_preview_cam_6)
        self.sli_1_x.grid(row=3, column=1, sticky=W+E, padx=10)

        Label(self, text="y: ").grid(row=4, sticky=W, padx=10)
        self.sli_1_y = Scale(self, from_=0, to=100, resolution=0.01, orient=HORIZONTAL, sliderlength=10, length=400, command=self.master.show_image_preview_cam_6)
        self.sli_1_y.grid(row=4, column=1, sticky=N+W, padx=10)

        Label(self, text="Bottom right: ").grid(row=5, sticky=W, padx=10, pady=4)
        Label(self, text="x: ").grid(row=6, sticky=W, padx=10)
        self.sli_2_x = Scale(self, from_=0, to=100, resolution=0.01, orient=HORIZONTAL, sliderlength=10, length=400, command=self.master.show_image_preview_cam_6)
        self.sli_2_x.grid(row=6, column=1, sticky=N+W, padx=10)

        Label(self, text="y: ").grid(row=7, sticky=W, padx=10)
        self.sli_2_y = Scale(self, from_=0, to=100, resolution=0.01, orient=HORIZONTAL, sliderlength=10, length=400, command=self.master.show_image_preview_cam_6)
        self.sli_2_y.grid(row=7, column=1, sticky=N+W, padx=10)


