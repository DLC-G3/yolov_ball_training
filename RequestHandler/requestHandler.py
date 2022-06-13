from DataHandler.UtilityHandler import UtilityHandler
# from UtilityHandler import UtilityHandler

from time import sleep
from datetime import datetime

import requests
from bs4 import BeautifulSoup
import json

import sys
from pathlib import Path

path = str(Path(sys.path[0])) + "/RequestHandler"
data_path = str(Path(sys.path[0])) + "/DataHandler"

status_codes = {200:"Succesfull",419:"Authorization error",500:"Internal server error"}

class RequestHandler():
    def __init__(self,url='https://app.360sportsintelligence.com',club_id=1071,user_id=108675,delay=0.2):
        self.url = url
        self.club_id = club_id
        self.user_id = user_id
        self.delay = delay

        self.recording_ids = [733515]
        self.canvas_ids = [1919205]
        
        self.headers = {
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chromium/80.0.3987.160 Chrome/80.0.3987.163 Safari/537.36'
        }

        self.flag_struct = {
            'id':'', 
            'channel_name': 'ch1',
            'time': UtilityHandler.convert_time(0,11,10), # h,m,s
            'comment': '',
            'offset_before': 10000,
            'offset_after': 5000,
            'hasValidationErrors': False,
            'getValidationErrorsList':'', 
        }

        self.login_data = UtilityHandler.get_environment_variable("login_data")

        # with requests.Session() as s:
        #     self.login(s)
        #     record_id = self.get_recording_by_name(s,"A-Team - Diest")["id"]
        #     self.download_recordings_by_cam(s,record_id)

        #     # self.request_clips_for_filtered_recordings(s)
        #     self.get_or_add_canvas(s,record_id,"Jorik et Cool =)")
        #     self.add_flag_to_canvas(s,record_id,"Jorik et Cool =)",self.flag_struct,'Kobe')

        #     print(self.get_flags_by_recording(s,self.recording_ids[0]))
        #     print(self.get_canvases_by_recording(s,self.recording_ids[0]))
        #     #print(self.get_canvas_by_name(s,self.recording_ids[0],'Doelpunten G3'))
        #     #print(self.get_annotation_events_by_name(s,self.recording_ids[0],"1-test",self.canvas_ids[0]))

        #     #self.add_flag_to_canvas(s,self.recording_ids[0],'Doelpunten G3',test_flags[0],'final_test')
        #     # self.request_clip_creation(s,self.recording_ids[0],'Doelpunten G3',["1 - 0 cam4","2 - 0 cam4","3 - 0 cam4"])

    def authenticate_session(self,s,url):
        r = s.get(url,headers=self.headers)
        soup = BeautifulSoup(r.text, 'lxml')

        csrf_token = soup.find('input',attrs = {'name':'_token'})['value']
        self.login_data['_token'] = csrf_token
        
    def login(self,s):
        url = self.url + '/login'
        self.authenticate_session(s,url)      

        r = s.post(url,data=self.login_data,headers=self.headers)
        self.headers['cookie'] = '; '.join([x.name + '=' + x.value for x in r.cookies])
        print(f'Login: {status_codes[r.status_code]}')
        
    # download videos    

    def get_recording_data(self,s,recording_id):
        url = self.url + f'/annotation-area/recordings/{recording_id}'
        r = s.get(url,headers={"Accept":"application/json"})
        return json.loads(r.content)

    def get_recording_urls(self,s,recording_id):
        recording_data = self.get_recording_data(s,recording_id)
        channels = recording_data["Channels"]
        urls = [channel["Streams"][0]["path"] for channel in channels]
        return urls

    def download_recordings_by_cam(self,s,recording_id,cams=[4,6]):
        urls = self.get_recording_urls(s,recording_id)
        filtered_urls = [self.download_video(urls[cam-1]) for cam in cams]
        print(filtered_urls)

    def download_video(self,url):
        file_name = url.split('/')[-1].split('?')[0]
        print(f"Downloading file: {file_name}, this may take a while")
    
        #create response object
        r = requests.get(url, stream = True)
    
        #download started
        with open(f"DataHandler/SourceFiles/Video/{file_name}", 'wb') as f:
            for chunk in r.iter_content(chunk_size = 1024*1024):
                if chunk:
                    f.write(chunk)
                    continue
                break

        print("Finished downloading file.")
        return url

    def get_flags_by_recording(self,s,recording_id):
        url = self.url + f'/annotation-area/recordings/{recording_id}/annotation-events'
        r = s.get(url)
        return json.loads(r.content)

    def get_flags_by_canvas_id(self,s,recording_id,canvas_id):
        flags = []
        for flag in self.get_flags_by_recording(s,recording_id):
            if flag['canvas_id'] == str(canvas_id):
                flags.append(flag)
        return flags

    def get_canvases_by_recording(self,s,recording_id):
        url = self.url + f'/annotation-area/recordings/{recording_id}/canvases?user_id={self.user_id}'
        r = s.get(url)
        return json.loads(r.content)

    def get_canvas_by_name(self,s,recording_id,canvas_name):
        canvases = self.get_canvases_by_recording(s,recording_id)
        for canvas in canvases:
            if UtilityHandler.is_similar(canvas['name'], canvas_name):
                return canvas
        return None

    def add_canvas(self,s,recording_id,canvas_name):
        url = self.url + '/annotation-area/canvases'
        canvas = {
            'recording_id': recording_id,
            'name': canvas_name,
            '_token': self.login_data['_token']
        }
        r = s.post(url,data=canvas)
        return json.loads(r.content)

    def get_or_add_canvas(self,s,recording_id,canvas_name):
        canvas = self.get_canvas_by_name(s,recording_id,canvas_name)
        if canvas == None:
            canvas = self.add_canvas(s,recording_id,canvas_name)
        return canvas

    def get_annotations_by_recording(self,s,recording_id):
        url = self.url + f'/annotation-area/recordings/{recording_id}/annotations'
        r =  s.get(url)
        return json.loads(r.content)

    def get_annotation_events_by_recording(self,s,recording_id):
       url = self.url + f'/annotation-area/recordings/{recording_id}/annotation-events'
       r = s.get(url)
       return json.loads(r.content)

    # internal name is channel, but refers to the labels of flags
    def add_annotation_event(self,s,recording_id,canvas_id,annotation_name):            
        url = self. url + '/annotation-area/annotation-events'
        annotation = {
            'annotation_name': 'ch1',
            'canvas_id': canvas_id,
            'recording_id': recording_id,
            'name': annotation_name,
            '_token': self.login_data['_token']
        }
        r = s.post(url,data=annotation)
        return json.loads(r.content)

    def get_annotation_event_by_names(self,s,recording_id,annotation_names,canvas_id=None):
        for annotation in self.get_annotation_events_by_recording(s,recording_id):
            if UtilityHandler.is_similar_to_item_in_list(annotation['name'],annotation_names):
                if canvas_id == None or annotation["canvas_id"] == canvas_id: 
                    return annotation  
        return None

    def get_annotation_events_by_names(self,s,recording_id,annotation_names,canvas_id=None):
        annotations = []
        for annotation in self.get_annotation_events_by_recording(s,recording_id):
            if UtilityHandler.is_similar_to_item_in_list(annotation['name'],annotation_names):
                if canvas_id == None or annotation["canvas_id"] == canvas_id: 
                    print(annotation["name"])
                    annotations.append(annotation)
                    continue
        
        return annotations

    def get_or_add_annotation_event(self,s,recording_id,annotation_name,canvas_id):
        annotation = self.get_annotation_event_by_names(s,recording_id,annotation_name,canvas_id)
        if annotation == None:
            if canvas_id != None:
                annotation = self.add_annotation_event(s,recording_id,canvas_id,annotation_name)
        return annotation

    def add_flag_to_canvas(self,s,recording_id,canvas_name,flag,annotation_name):
        try:
            canvas_id = self.get_or_add_canvas(s,recording_id,canvas_name)['id']
            annotation_id = self.get_or_add_annotation_event(s,recording_id,annotation_name,canvas_id)['id']
            url = self.url + '/annotation-area/annotations'
            flag['recording_id'] = recording_id
            flag['canvas_id'] = canvas_id
            flag['annotation_event_id'] = annotation_id
            flag['_token'] = self.login_data['_token']
            r = s.post(url,data=flag)
            print(f"Flag sent, server answered with following data: \n{r.content}")
            return json.loads(r.content)
        except Exception as ex:
            print(ex)

    def request_clip_creation(self,s,recording_id,canvas_id,annotation_names=["-"]):
        url = self.url + f'/annotation-area/canvases/{canvas_id}/export'

        clip_data = {
            'duplicate_annotations_without_players': 'true',
            'duplicate_annotations_without_annotation_events': 'true',
            'annotation_events[]':[ i['id'] for i in self.get_annotation_events_by_names(s,recording_id,annotation_names,canvas_id)],
            '_token':self.login_data['_token']
        }

        if len(clip_data['annotation_events[]']) != 0:
            print(clip_data)
            r = s.post(url,data=clip_data)
            print(f'Request for clip creation: {status_codes[r.status_code]}')
        
    def request_clips_for_filtered_recordings(self,s,canvas_filter=["Samenvatting"]):
        recording_ids = self.get_all_filtered_recording_ids(s)

        for recording_id in recording_ids:
            print(f'\nrecord: {recording_id}')
            print("  canvases:")
            canvases = self.get_canvases_by_recording(s,recording_id)
            sleep(self.delay)
            for canvas in canvases:
                # print(f'\t{canvas}')
                if UtilityHandler.is_similar_to_item_in_list(canvas["name"],canvas_filter):
                    print(f'\trequesting for {canvas["name"]}')
                    self.request_clip_creation(s,recording_id,canvas["id"])
                    continue
                print(f'\tignoring canvas: {canvas["name"]}')

            self.set_recording_as_clipped(recording_id)
        print("Done!")

    def get_all_recordings(self,s):
        # check cache first
        with open(f"{data_path}/cache/recordings.json", "r+",encoding="utf8") as f:
            json_ = json.load(f)
            current_date = datetime.today().date()
            if len(json_) == 2:
                cache_date = datetime.strptime(json_["date"], '%Y-%m-%d').date()
                if (current_date - cache_date).total_seconds() == 0:
                    f.close()
                    print("receiving from cache")
                    return json_["recordings"]
            print("getting recordings from server")

            json_["date"] = str(current_date)      
            url = self.url + f"/clubs/{self.club_id}/recordings"
            r = s.get(url)
            json_["recordings"] = json.loads(r.content)

            f.seek(0)
            f.write(json.dumps(json_))
            f.truncate()

            f.close()
            return json_["recordings"]

    def set_recording_as_clipped(self,recording_id):
        with open(f"{data_path}/data/clipped_recordings.json","r+",encoding="utf8") as f:
            json_ = json.load(f)
            if recording_id not in json_["recording_ids"]:
                json_["recording_ids"].append(recording_id)
            f.seek(0)
            f.write(json.dumps(json_))
            f.close()
            return json_["recording_ids"]

    def get_all_clipped_recording_ids(self):
        with open(f"{data_path}/data/clipped_recordings.json","r",encoding="utf8") as f:
            json_ = json.load(f)
            f.close()
            return json_["recording_ids"]

    def get_all_recording_ids(self,s):
        return [i["id"] for i in self.get_all_recordings(s)]

    def get_all_filtered_recording_ids(self,s):
        temp_recording_ids = []
        for recording_id in self.get_all_recording_ids(s):
            if recording_id not in self.get_all_clipped_recording_ids():
                temp_recording_ids.append(recording_id)
        return temp_recording_ids

    def get_recording_by_name(self,s,title):
        recordings = self.get_all_recordings(s)
        for recording in recordings:
            if UtilityHandler.is_similar(recording['title'],title):
                return recording
        return None

    def set_flags_for_video(self,s,recording_id,canvas_name): # for now, need to add your own canvas first to the video
        with open(f'{data_path}/data/flags.json','r',encoding='utf8') as f:
            json_ = json.load(f)
            for flag_data in json_:
                self.add_flag_to_canvas(s,recording_id,canvas_name,flag_data["flag"],flag_data["annotation_name"])
            f.close()

    def set_flag_for_frames(self,s,frames,record_id,canvas_name,cam,annotation_name="goals"):
        flag = {
            'id':'',
            'channel_name':f'ch{cam}',
            'comment': '',
            'offset_before': 10000,
            'offset_after': 5000,
            'hasValidationErrors': False,
            'getValidationErrorsList':'', 
        }
        for frame in frames:
            flag['time'] = UtilityHandler.convert_frame_to_time(frame)
            self.add_flag_to_canvas(s,record_id,canvas_name,flag,annotation_name)
            

    @staticmethod
    def request_session():
        return requests.Session()

if __name__ == '__main__':
    requestHandler = RequestHandler()