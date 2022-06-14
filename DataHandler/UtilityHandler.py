import json
import sys
from pathlib import Path

path = str(Path(sys.path[0])) + "/DataHandler"

class UtilityHandler():
    @staticmethod
    def convert_time(h,m,s,frame=1,fps=25.033316316784834):
        ms = (h*3600 +m*60 + s)*1000+(1000/fps*frame)
        return ms

    @staticmethod
    def convert_frame_to_time(frame,fps=24):
        # 25.033316316784834
        ms = 1000/fps*frame
        return ms

    @staticmethod
    def is_similar(str1,str2):
        str1,str2 = str1.replace(" ","").lower(),str2.replace(" ","").lower()
        if str1 in str2 or str2 in str1:
            return True
        return False

    @staticmethod
    def is_similar_to_item_in_list(str1,items):
        for item in items:
            if UtilityHandler.is_similar(str1, item):
                # print(f'is similar: {str1}, {item}')
                return True
        return False

    @staticmethod
    def get_environment_variable(var):
        with open(f'{path}/environment_data.json') as f:
            json_ = json.load(f)
            f.close()
            return json_[var]