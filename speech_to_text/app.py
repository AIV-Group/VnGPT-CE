import os
import openai
from dotenv import load_dotenv
load_dotenv('./.env')
from pytube import YouTube
from pydub import AudioSegment
import gradio as gr

#if you have OpenAI API key as an environment variable, enable the below
#openai.api_key = os.getenv("OPENAI_API_KEY")

#if you have OpenAI API key as a string, enable the below
OPEN_API_KEY = os.environ['OPEN_API_KEY']
openai.api_key = OPEN_API_KEY
# feature audio
def speech_to_text(link_youtube, fulltime, start_second, end_second):
    # video = 'https://www.youtube.com/watch?v=LFwU8byhFsI'
    video = link_youtube
    data = YouTube(video)
    # Converting and downloading as 'MP4' file
    audio = data.streams.get_audio_only()
    path_audio = audio.download()
    if fulltime == True:
        # process cut audio
        song = AudioSegment.from_file(path_audio, format="mp4")
        # PyDub handles time in milliseconds
        start_second = start_second * 60 * 1000
        end_second = end_second * 60 * 1000
        cut_audio = song[start_second:end_second]
        cut_audio.export(path_audio, format="mp4")
        # process speech_to_text
        file = open(f"{path_audio}", "rb")
        transcription = openai.Audio.transcribe("whisper-1", file)
        print(transcription.text)
        #remove file audio after process
        os.remove(path_audio)
        return transcription.text
    else:
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

def length_link(link_youtube):
    yt = YouTube(link_youtube)
    print(yt.length)
    return yt.length
