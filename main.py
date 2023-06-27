import json, openai, pandas
import warnings
import os
warnings.filterwarnings('ignore')
import configparser
from gtts import gTTS
from mutagen.mp3 import MP3
from PIL import Image
from pathlib import Path
from moviepy import editor
import os 
from datetime import date

os.environ["IMAGEIO_FFMPEG_EXE"] = "/usr/bin/ffmpeg"

# Reading the credentials
readKey = configparser.ConfigParser()
readKey.read_file(open('apidata.config'))
audioFileName = str(date.today()) + ".mp3"
videoFileName = str(date.today()) + ".mp4"
# bringing the credentials to the python environment and store in variables
org = readKey["OPENAI"]["ORG"]
key = readKey["OPENAI"]["KEY"]

# Authenticate with the Open-AI servers
openai.organization = org
openai.api_key= key

# Start querying the API
modelList = [[data['id'],data['root']] for data in openai.Model.list()['data']]

modelList[:2]

[['babbage', 'babbage'],
 ['ada', 'ada'],
 ['davinci', 'davinci'],
 ['text-embedding-ada-002', 'text-embedding-ada-002'],
 ['babbage-code-search-text', 'babbage-code-search-text'],
 ['babbage-similarity', 'babbage-similarity']]


# Send the API request to open-ai

response = openai.Completion.create(
  model="davinci",
  prompt="In the post-apocalyptic setting, envision a captivating image of a female assassin who personifies the stealth and expertise of a ninja. She remains concealed within the shadows, biding her time with unwavering patience, effortlessly blending into the encompassing darkness until the opportune moment arises for her lethal strike.",
  temperature=0,
  max_tokens=128,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)

# converting the response to printable format
from pprint import pp
output = response["choices"][0]["text"]

# Pretty Printed output
print(output)


# # converting the response to audio clip format

gttsLang = 'en'
replyObj = gTTS(text=output,lang=gttsLang,slow=False)
replyObj.save(audioFileName)


# # converting the response to video format

# #Pre requisites

get_path ='./'
audio_path = audioFileName
video_path = videoFileName
folder_path = './'
full_audio_path = os.path.join(get_path, audio_path)
full_video_path = os.path.join(get_path, video_path)

# # Reading in the mp3 that we got from gTTS

song = MP3(audio_path)
audio_length = round(song.info.length)
audio_length

# Globbing the images and Stitching it to for the gif

path_images = Path(folder_path)

images = list(path_images.glob('*.png'))

image_list = list()

for image_name in images:
    image = Image.open(image_name).resize((800, 800), Image.ANTIALIAS)
    image_list.append(image)
    
#Checking Audio length

length_audio = audio_length
duration = int(length_audio / len(image_list)) * 1000


#Creating Gif

image_list[0].save(os.path.join(folder_path,"temp.gif"),
                   save_all=True,
                   append_images=image_list[1:],
                   duration=duration)


# Creating the video using the gif and the audio file

video = editor.VideoFileClip(os.path.join(folder_path,"temp.gif"))
print('done video')

audio = editor.AudioFileClip(full_audio_path)
print('done audio')

final_video = video.set_audio(audio)
print('Set Audio and writing')

final_video.set_fps(60)

final_video.write_videofile(full_video_path)

# The final mp4 file in the folder
