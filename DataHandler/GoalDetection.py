class GoalDetection():
    @staticmethod
    def detect_goals_images(data,consecutive_frames=3,wait_interval=100,suffix="frame",extension=".jpg",consecutive_th=2):
        consecutive_balls = 1
        prev_frame = 0
        check_delay = 0
        for img,data in data.items():
            print(data)
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

    @staticmethod
    def get_filtered_frames(data):
        filtered_objects = GoalDetection.filter_objects(data)
        print(f"flags: {filtered_objects}")
        return [obj["frame"] for obj in filtered_objects]
        
    @staticmethod
    def filter_objects(data):
        valid_frames = []
        for frame,detected_objects in data.items():
            for obj in detected_objects:
                class_,coords,confidence = obj["class"],[round(coord,2) for coord in obj["coords"]],round(obj["confidence"]*100,2)
                
                if class_ != "Ball":
                    continue
                # implement extra checks with coords
                # implement extra checks with confidence?

                valid_frames.append({"frame":int(frame),"coords":coords,"confidence":confidence})
                continue
        return GoalDetection.normalize_consecutive_frames(valid_frames)

    # @staticmethod
    # def normalize_consecutive_frames(frames,allowed_difference=2,delay = 750):
    #     normalized_frames ={}
    #     prev_frame = 0
    #     for frame,obj in frames.items():
    #         if frame <= prev_frame + allowed_difference:
    #             normalized_frames[frame] = obj
    #             prev_frame = 0
    #             continue
    #         prev_frame = frame
    #     return normalized_frames

    @staticmethod
    def normalize_consecutive_frames(frames,allowed_difference=2,consecutive_threshhold=2,delay=750):
        print(f"frames: {frames}")
        norm_frames = []
        consecutive_count = 0

        for i,f_data in enumerate(frames):
            if i == len(frames)-1:
                break
            f = f_data["frame"]
            if len(norm_frames):
                if f < (norm_frames[-1]["frame"] + delay): # if current frame is within delay of last set flag
                    continue # skip rest of checks
            
            if f >= (frames[i+1]["frame"] - allowed_difference): # if current frame is close to next frame
                consecutive_count +=1 
                if consecutive_count >= consecutive_threshhold: # if multiple frames have been noticed close to each other
                    norm_frames.append(f_data) # add the current frame to the normalized frames
                    consecutive_count = 0 # reset the consecutive count
                continue

            consecutive_count = 0
        return norm_frames
