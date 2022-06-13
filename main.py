# import yolov5_custom.detect as detect
from RequestHandler.requestHandler import RequestHandler
from DataHandler.GoalDetection import GoalDetection
import DataHandler.VideoHandler as VideoHandler
import json

import requests

if __name__ == '__main__':
    requestHandler = RequestHandler()
    cams = [4,6]
    recording_name = "A-Team - Diest"
    canvas_name = "Auto test 10/06 JTJ"
    th = 0.72 # threshhold ball accuracy
    read_from_json = False

    with requests.Session() as s:
        requestHandler.login(s)
        record_id = requestHandler.get_recording(s,"https://app.360sportsintelligence.com/annotation-area/recordings/733515")["id"]
        requestHandler.download_thumbnail_by_cam(s,record_id,cams)

    # if read_from_json:
    #     for cam in cams:
    #         with open(f"ball_output/labels_detected_obj_{cam}.json","r",encoding="utf8") as f:
    #             json_ = json.load(f)
    #             print(json_)
    #         break
    # else:
    #     # with requests.Session() as s:
    #     #     requestHandler.login(s)
    #     #     record_id = requestHandler.get_recording_by_name(s,"A-Team - Diest")["id"]
    #     #     requestHandler.download_recordings_by_cam(s,record_id,cams)
    #     print("downloaded videos")

    #     for cam in cams:
    #         print(f"cropping video {cam}")
    #         # VideoHandler.crop_video(f"ch{cam}",cam=cam,max_frame=124650) # max_frame=162000
    #         print("starting detection:")
            
    #         # for video testing:
    #         #detect.run(source=f"DataHandler/SourceFiles/CroppedVideos/ch{cam}.mp4",weights="trained_data/latest_3/weights/last.pt",conf_thres=(th),save_txt=True,project="./ball_output",line_thickness=2) 
    #         #detect.run(source=f"DataHandler/SourceFiles/CroppedVideos/ch{cam}_cropped_full.mp4",weights="trained_data/latest_3/weights/last.pt",conf_thres=(th),save_txt=True,project="./ball_output",line_thickness=2)
            
    #         detected_objects = detect.run_optimised_for_ball(source=f"DataHandler/SourceFiles/CroppedVideos/ch{cam}.mp4",weights="trained_data/latest_3/weights/last.pt",conf_thres=(th),project="./ball_output") 
    #         print(detected_objects)

    #         with open(f"ball_output/labels_detected_obj_{cam}.json","w") as f:
    #             json.dump(detected_objects,f)
    #             f.close()

    #         detected_goals = GoalDetection.get_filtered_frames(detected_objects)
    #         with open(f"ball_output/filtered_for_goals_{cam}.json","w") as f:
    #             json.dump(detected_goals,f)
    #             f.close()

    #         # print("Sending flags")
    #         # with requests.Session() as s:
    #         #     requestHandler.login(s)
    #         #     record_id = requestHandler.get_recording_by_name(s,recording_name)["id"]
    #         #     requestHandler.set_flag_for_frames(s,detected_goals,record_id,canvas_name,cam=cam)
    #         # break

    
