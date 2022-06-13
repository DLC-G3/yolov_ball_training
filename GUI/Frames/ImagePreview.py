from tkinter import *
from PIL import Image, ImageTk

class ImagePreview(Frame):
    def __init__(self, master=None):
        Frame.__init__(self,master)
        self.master = master
        self.init_window()

    def init_window(self):
        self.pack(fill=BOTH, expand=1)

        canvas= Canvas(self, width= 600, height= 400)
        canvas.pack()

        #Load an image in the script
        img= ImageTk.PhotoImage(Image.open("C:/Users/jonas/Pictures/IMG_4027.JPG"))

        #Add image to the Canvas Items
        canvas.create_image(10,10,anchor=NW,image=img)

