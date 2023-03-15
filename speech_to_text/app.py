import os
import openai
from dotenv import load_dotenv
load_dotenv('./.env')
from pytube import YouTube
from pydub import AudioSegment
import gradio as gr
from youtube_transcript_api import YouTubeTranscriptApi

#if you have OpenAI API key as an environment variable, enable the below
#openai.api_key = os.getenv("OPENAI_API_KEY")

#if you have OpenAI API key as a string, enable the below
OPEN_API_KEY = os.environ['OPEN_API_KEY']
openai.api_key = OPEN_API_KEY
# feature audio using pytube and whisper AI
def speech_to_text(link_youtube, fulltime, start_second, end_second):
    # video = 'https://www.youtube.com/watch?v=LFwU8byhFsI'
    video = link_youtube
    data = YouTube(video)
    # Converting and downloading as 'MP4' file
    audio = data.streams.get_audio_only()
    path_audio = audio.download()
    if fulltime == False:
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

#function get thumbnail title video
def populate_metadata(link_youtube):
    yt = YouTube(link_youtube)
    return yt.thumbnail_url, yt.title

#function get length video
def length_link(link_youtube):
    try:
        yt = YouTube(link_youtube)
        print(yt.length)
        return round(yt.length/60)
    except:
        return 180

def generate_transcript(id, lang):
    transcript = YouTubeTranscriptApi.get_transcript(id, languages=[f'{lang}'])
    script = ""

    for text in transcript:
        t = text["text"]
        if t != '[Music]' and t != '[âm nhạc]':
            script += t + " "

    return script, len(script.split())

def youtube_transcripts(link_youtube, lang):
    yt = YouTube(link_youtube)
    video_id = yt.video_id
    transcript, no_of_words = generate_transcript(video_id, lang)
    # print(transcript)
    return transcript
