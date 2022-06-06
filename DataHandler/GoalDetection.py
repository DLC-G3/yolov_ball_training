class GoalDetection():
    @staticmethod
    def detect_goals_from_json(data,consecutive_frames=3,wait_interval=100):
        for img,data in data.items():
            print(f"{img}, {data}")