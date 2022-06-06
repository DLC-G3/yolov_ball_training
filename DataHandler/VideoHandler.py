import cv2
import random
import pathlib 
import os
import shutil

source_path = "DataHandler/SourceFiles"
video_path = f"{source_path}/Video"
image_path = f"{source_path}/Images"

def get_image_count(path_):
  count = 0
  for f in pathlib.Path(path_).iterdir():
    if f.is_file():
        count += 1
  return count

def get_all_frames(clip ="videoclip_963155",start_video=90):
  vidcap = cv2.VideoCapture(f'{video_path}/{clip}.mp4')
  success,image = vidcap.read()
  count = 0

  while success & (count < start_video):
    success,image = vidcap.read()
    count +=1
    continue

  while success:
    cv2.imwrite(f"{image_path}/frame{count}.jpg", image)     # save frame as JPEG file    
    success,image = vidcap.read()
    print(f'Read a new frame {count}: {success}')
    count += 1
    # if count > 320:
    #   break

def get_random_frames(clip="videoclip_963155",start_video=96,interval=12,random_offset=6):
  vidcap = cv2.VideoCapture(f'{source_path}/{clip}.mp4')
  success,image = vidcap.read()
  randomv = random.randint(interval-random_offset,interval+random_offset)
  print("starting image creation")

  # count = 0
  # while success and count < start_video:
  #   success,image = vidcap.read()
  #   count += 1

  count =  0
  img_count = get_image_count(f"{image_path}/variated/")
  while success:
    if count%randomv == 0:
      print(f"added image {count}")
      cv2.imwrite(f"{image_path}/variated/frame{img_count}.jpg", image)     # save frame as JPEG file
      randomv = random.randint(count + interval-random_offset,count + interval+random_offset)  
      img_count += 1 
      count += 1 
    success,image = vidcap.read()
    count += 1

def get_cropped_images(cam=6,cropped_under_line=True):
  vector = [{4:{"x":220,"y":680,"w":1700,"h":1080},6:{"x":380,"y":632,"w":1600,"h":1080}},{4:{"x":380,"y":908,"w":1600,"h":1080},6:{"x":420,"y":892,"w":1500,"h":1080}}][cropped_under_line][cam]
  temp_files = os.listdir(f"{image_path}")
  for file in temp_files:
    if file[-4:] == ".jpg":
      image = cv2.imread(f"{image_path}/{file}")
      cropped_image = image[vector["y"]:vector["h"],vector["x"]:vector["w"]]
      cv2.imwrite(f"{image_path}/cropped/{file[:-4]}.jpg", cropped_image)     # save frame as JPEG file
      print(f"cropped image: {file[:-4]}")

#get_all_frames("bal_thuis1")
#get_random_frames("videoclip_960115")

def clear_images():
  shutil.rmtree(image_path)
  

def get_all_cropped_images(clip,cam,start_video=90,cropped_under_line=True,clear=False):
  if clear: clear_images()
  vector = [{4:{"x":220,"y":680,"w":1700,"h":1080},6:{"x":380,"y":632,"w":1600,"h":1080}},{4:{"x":380,"y":908,"w":1600,"h":1080},6:{"x":420,"y":892,"w":1500,"h":1080}}][cropped_under_line][cam]
  vidcap = cv2.VideoCapture(f'{video_path}/{clip}.mp4')
  success,image = vidcap.read()
  count = 0

  while success & (count < start_video):
    success,image = vidcap.read()
    count +=1
    continue

  while success:
    image = image[vector["y"]:vector["h"],vector["x"]:vector["w"]]
    cv2.imwrite(f"{image_path}/frame{count}.jpg", image)     # save frame as JPEG file    
    success,image = vidcap.read()
    print(f'Read a new frame {count}: {success}')
    count += 1

#get_cropped_images()