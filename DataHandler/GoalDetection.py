class GoalDetection():
    @staticmethod
    def detect_goals_from_json(data,consecutive_frames=3,wait_interval=100,suffix="frame",extension=".jpg",consecutive_th=2):
        consecutive_balls = 1
        prev_frame = 0
        check_delay = 0
        for img,data in data.items():
            for obj in data:
                frame = int(img.replace(suffix,"").replace(extension,""))
                class_ = obj["class"]
                coords = [round(coord,2) for coord in obj["coords"]]
                confidence = round(obj["confidence"]*100,2)
                print(f"{frame}: {class_}, {coords}, {confidence} % confident")

                if class_ == "Ball":
                    if frame < prev_frame+5: # small range if detection isn't perfect
                        consecutive_balls += 1
                        if consecutive_balls >= consecutive_th:
                            if check_delay == 0:
                                print(f"Placing flag at {frame}")
                                check_delay = 200+1 # delay for frames not to put flag

            consecutive_balls = 1
            check_delay = max(0,check_delay-1)
            prev_frame = frame