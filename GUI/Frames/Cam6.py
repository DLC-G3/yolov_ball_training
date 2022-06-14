from tkinter import *
import sys
from pathlib import Path
import json

class Cam6(Frame):
    def __init__(self, master=None):
        Frame.__init__(self,master)
        self.master = master

        self.init_window()

    def init_window(self):

        data_path = str(Path(sys.path[0])) + "/DataHandler"

        with open(f"{data_path}/data/crop.json", "r",encoding="utf8") as f:
            vector = json.load(f)["6"]
            f.close()
        
        resize_x = 1920
        resize_y = 1080

        print(f"loading vectors: {vector}")

        Label(self, text="Cam 6: ").grid(row=0, sticky=W, padx=10, pady=4)

        Label(self, text="Top left: ").grid(row=2, sticky=W, padx=10, pady=4)
        Label(self, text="x: ").grid(row=3, sticky=W, padx=10)
        self.sli_1_x = Scale(self, from_=0, to=100, resolution=0.01, orient=HORIZONTAL, sliderlength=10, length=400, command=self.master.show_image_preview_cam_6)
        self.sli_1_x.grid(row=3, column=1, sticky=W+E, padx=10)
        self.sli_1_x.set(round((vector["x"])/resize_x*100,2))

        Label(self, text="y: ").grid(row=4, sticky=W, padx=10)
        self.sli_1_y = Scale(self, from_=0, to=100, resolution=0.01, orient=HORIZONTAL, sliderlength=10, length=400, command=self.master.show_image_preview_cam_6)
        self.sli_1_y.grid(row=4, column=1, sticky=N+W, padx=10)
        self.sli_1_y.set(round((vector["y"])/resize_y*100,2))

        Label(self, text="Bottom right: ").grid(row=5, sticky=W, padx=10, pady=4)
        Label(self, text="x: ").grid(row=6, sticky=W, padx=10)
        self.sli_2_x = Scale(self, from_=0, to=100, resolution=0.01, orient=HORIZONTAL, sliderlength=10, length=400, command=self.master.show_image_preview_cam_6)
        self.sli_2_x.grid(row=6, column=1, sticky=N+W, padx=10)
        self.sli_2_x.set(round((vector["x"] + vector["w"])/resize_x*100,2))

        Label(self, text="y: ").grid(row=7, sticky=W, padx=10)
        self.sli_2_y = Scale(self, from_=0, to=100, resolution=0.01, orient=HORIZONTAL, sliderlength=10, length=400, command=self.master.show_image_preview_cam_6)
        self.sli_2_y.grid(row=7, column=1, sticky=N+W, padx=10)
        self.sli_2_y.set(round((vector["y"] + vector["h"])/resize_y*100,2))


