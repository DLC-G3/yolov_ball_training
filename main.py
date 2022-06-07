import yolov5_custom.detect as detect
from RequestHandler.requestHandler import RequestHandler
from DataHandler.GoalDetection import GoalDetection
import DataHandler.VideoHandler as VideoHandler

import requests

if __name__ == '__main__':
    requestHandler = RequestHandler()
    
    with requests.Session() as s:
        requestHandler.login(s)

        # record_id = requestHandler.get_recording_by_name(s,"A-Team - Diest")["id"]
        # requestHandler.download_recordings_by_cam(s,record_id,cams=[4,6])


    #VideoHandler.get_all_cropped_images("videoclip_977455",4)
    # detected_balls = detect.run_optimised_for_ball(source="DataHandler/SourceFiles/Images/",weights="trained_data/latest_/weights/last.pt",imgsz=(416),conf_thres=(0.06),save_txt=True,project="./ball_output")  
    #print(json_)
    # detected_goals = GoalDetection.detect_goals_from_json(detected_balls)
    #requestHandler.send_goals(detected_goals,cam=4)
    

