import os
import openai
from dotenv import load_dotenv
load_dotenv('./.env')
from pytube import YouTube

#if you have OpenAI API key as an environment variable, enable the below
#openai.api_key = os.getenv("OPENAI_API_KEY")

#if you have OpenAI API key as a string, enable the below
OPEN_API_KEY = os.environ['OPEN_API_KEY']
openai.api_key = OPEN_API_KEY
# feature audio
def speech_to_text(link_youtube):
    # video = 'https://www.youtube.com/watch?v=LFwU8byhFsI'
    video = link_youtube
    data = YouTube(video)
    # Converting and downloading as 'MP4' file
    audio = data.streams.get_audio_only()
    path_audio = audio.download()
    # process speech_to_text
    file = open(f"{path_audio}", "rb")
    transcription = openai.Audio.transcribe("whisper-1", file)
    print(transcription.text)
    #remove file audio after process
    os.remove(path_audio)
    return transcription.text

def populate_metadata(link_youtube):
    yt = YouTube(link_youtube)
    return yt.thumbnail_url, yt.title