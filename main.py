from RequestHandler.requestHandler import RequestHandler
from DataHandler.GoalDetection import GoalDetection
import DataHandler.VideoHandler as VideoHandler
import json

import requests

import logging
from tkinter import *
from tkinter.ttk import Notebook, Progressbar
from queue import Queue
from tkinter import filedialog
from tracemalloc import start
from turtle import clear
from PIL import Image, ImageTk
import cv2
from pyparsing import col

from GUI.Frames.RecordingFrame import RecordingFrame
from GUI.Frames.Cam4 import Cam4
from GUI.Frames.Cam6 import Cam6
from GUI.Frames.CanvasFrame import CanvasFrame

import yolov5_custom.detect as detect

from tkinter.messagebox import showinfo

class Main(Frame):
    def __init__(self, master=None):
        Frame.__init__(self,master)
        self.master = master

        self.init_window()

    def init_window(self):
        self.input_recording = ""
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

        self.progressbar = Progressbar(self, orient='horizontal', mode='determinate', length=400)
        self.progressbar.grid(row=5, column=0, columnspan=2, sticky=N, pady=10)

        self.progressbar_label = Label(self, text="Current Progress: ")
        self.progressbar_label.grid(row=6, column=0, columnspan=2, sticky=N)

        Grid.columnconfigure(self, 6, weight=1)
        Grid.rowconfigure(self, 6, weight=1)
    
    def update_progress_label(self):
        return f"Current Progress: {self.progressbar['value']}%"
    
    def progress(self):
        if self.progressbar['value'] != 100:
            self.progressbar['value'] += 100/3
            self.progressbar_label['text'] = self.update_progress_label()
        else:
            showinfo(message='The progress completed!')

    def submit_form(self):
        cams = [4,6]
        resize_x = 1920
        resize_y = 1080
    
        starting_point_4 = (round(self.cam_4_frame.sli_1_x.get() / 100 * resize_x), round(self.cam_4_frame.sli_1_y.get() / 100 * resize_y))
        ending_point_4 = (round(self.cam_4_frame.sli_2_x.get() / 100 * resize_x), round(self.cam_4_frame.sli_2_y.get() / 100 * resize_y))

        starting_point_6 = (round(self.cam_6_frame.sli_1_x.get() / 100 * resize_x), round(self.cam_6_frame.sli_1_y.get() / 100 * resize_y))
        ending_point_6 = (round(self.cam_6_frame.sli_2_x.get() / 100 * resize_x), round(self.cam_6_frame.sli_2_y.get() / 100 * resize_y))

        x_4 = starting_point_4[0]
        y_4 = starting_point_4[1]
        w_4 = ending_point_4[0] - x_4 + 1
        h_4 = ending_point_4[1] - y_4 + 1

        if x_4 + w_4 > resize_x:
            w_4 = resize_x - x_4

        if y_4 + h_4 > resize_y:
            h_4 = resize_y - y_4

        x_6 = starting_point_6[0]
        y_6 = starting_point_6[1]
        w_6 = ending_point_6[0] - x_6
        h_6 = ending_point_6[1] - y_6

        if x_6 + w_6 > resize_x:
            w_6 = resize_x - x_6

        if y_6 + h_6 > resize_y:
            h_6 = resize_y - y_6

        crop_vector = {4:{"x":x_4,"y":y_4,"w":w_4,"h":h_4},6:{"x":x_6,"y":y_6,"w":w_6,"h":h_6}}
        self.save_crop_vector(crop_vector)

        cams = [4]
        self.input_recording = self.recording_frame.entry_recording_name.get()
        canvas_name = self.canvas_frame.entry_canvas_name.get()
        th = 0.72
        record_id = 0

        with requests.Session() as s:
            requestHandler.login(s)
            record_id = requestHandler.get_recording_id(s,self.input_recording)
            requestHandler.download_recordings_by_cam(s,record_id,cams)
            self.progress()
        print("downloaded videos")

        for cam in cams:
            print(f"cropping video {cam}")
            VideoHandler.crop_video(f"ch{cam}",crop_vector[cam]) # max_frame=162000
            print("starting detection:")

            # for video testing:
            # detect.run(source=f"DataHandler/SourceFiles/CroppedVideos/ch{cam}.mp4",weights="trained_data/latest_3/weights/last.pt",conf_thres=(th),save_txt=True,project="./ball_output",line_thickness=2) 
            # detect.run(source=f"DataHandler/SourceFiles/CroppedVideos/ch{cam}_cropped_full.mp4",weights="trained_data/latest_3/weights/last.pt",conf_thres=(th),save_txt=True,project="./ball_output",line_thickness=2)
            
            # with open(f"ball_output/labels_detected_obj_{cam}.json", "r",encoding="utf8") as f:
            #     detected_objects = json.load(f)
            #     f.close()                

            detected_objects = detect.run_optimised_for_ball(source=f"DataHandler/SourceFiles/CroppedVideos/ch{cam}.mp4",weights="trained_data/latest_3/weights/last.pt",conf_thres=(th),project="./ball_output") 
            print(detected_objects)

            with open(f"ball_output/labels_detected_obj_{cam}_{record_id}.json","w") as f:
                json.dump(detected_objects,f)
                f.close()

            detected_goals = GoalDetection.get_filtered_frames(detected_objects)

            with open(f"ball_output/filtered_for_goals_{cam}_{record_id}.json","w") as f:
                json.dump(detected_goals,f)
                f.close()

            print("Sending flags")
            with requests.Session() as s:
                requestHandler.login(s)
                record_id = requestHandler.get_recording_id(s,self.input_recording)
                requestHandler.set_flag_for_frames(s,detected_goals,record_id,canvas_name,cam=cam)
            self.progress()

        print("requesting clip creation")
        with requests.Session() as s:
            requestHandler.login(s)
            record_id = requestHandler.get_recording_id(s,self.input_recording)
            canvas_id = requestHandler.get_canvas_by_name(s,record_id,canvas_name)["id"]
            requestHandler.request_clip_creation(s,record_id,canvas_id)
        self.progress()

    def submit_name(self, input_recording):
        self.input_recording = input_recording
        if self.input_recording != "":
            with requests.Session() as s:
                requestHandler.login(s)
                record_id = requestHandler.get_recording_id(s,input_recording)
                requestHandler.download_thumbnail_by_cam(s, record_id)
            self.load_image_c4("DataHandler/SourceFiles/Images/ch4.jpg")
            print("C4 Done")
            self.load_image_c6("DataHandler/SourceFiles/Images/ch6.jpg")
            print("C6 Done")  

    def show_image_preview_cam_4(self, previous_state=""):
        resize_x = 480
        resize_y = 270

        img = cv2.resize(cv2.imread(self.cam_4_image.get()), (resize_x,resize_y), interpolation= cv2.INTER_LINEAR)

        starting_point = (round(self.cam_4_frame.sli_1_x.get() / 100 * resize_x), round(self.cam_4_frame.sli_1_y.get() / 100 * resize_y))
        ending_point = (round(self.cam_4_frame.sli_2_x.get() / 100 * resize_x), round(self.cam_4_frame.sli_2_y.get() / 100 * resize_y))

        image = cv2.rectangle(img, starting_point, ending_point, (255,0,0), 2)

        self.update_cam_4(image)

    def show_image_preview_cam_6(self, previous_state=""):
        resize_x = 480
        resize_y = 270

        img = cv2.resize(cv2.imread(self.cam_6_image.get()), (resize_x,resize_y), interpolation= cv2.INTER_LINEAR)

        starting_point = (round(self.cam_6_frame.sli_1_x.get() / 100 * resize_x), round(self.cam_6_frame.sli_1_y.get() / 100 * resize_y))
        ending_point = (round(self.cam_6_frame.sli_2_x.get() / 100 * resize_x), round(self.cam_6_frame.sli_2_y.get() / 100 * resize_y))

        image = cv2.rectangle(img, starting_point, ending_point, (255,0,0), 2)

        self.update_cam_6(image)
        
    def load_image_c4(self, filename):
        self.cam_4_image.set(filename)
        filename_short = filename.split('/')[-1]
        self.cam_4_image_short.set(filename_short)

        image = cv2.imread(self.cam_4_image.get())
        half = cv2.resize(image, (480,270))
        self.update_cam_4(half)
        self.show_image_preview_cam_4()

    def load_image_c6(self, filename):
        self.cam_6_image.set(filename)
        filename_short = filename.split('/')[-1]
        self.cam_6_image_short.set(filename_short)

        image = cv2.imread(self.cam_6_image.get())
        half = cv2.resize(image, (480,270))
        self.update_cam_6(half)
        self.show_image_preview_cam_6()

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

    def save_crop_vector(self,vector):
        with open(f"DataHandler/data/crop.json","w") as f:
            json.dump(vector,f)
            f.close()

if __name__ == '__main__':
    requestHandler = RequestHandler()
    root = Tk()
    root.resizable(False, False)
    root.geometry('1120x720')
    app = Main(root)

    try:
        root.mainloop()
    except KeyboardInterrupt:
        app.on_closing()