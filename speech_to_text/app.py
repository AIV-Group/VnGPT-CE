import os
import openai
from dotenv import load_dotenv
load_dotenv('./.env')
from pytube import YouTube
from pydub import AudioSegment
import gradio as gr
from youtube_transcript_api import YouTubeTranscriptApi
from lib_app.utils import *
import shutil
import time

#if you have OpenAI API key as an environment variable, enable the below
#openai.api_key = os.getenv("OPENAI_API_KEY")

#if you have OpenAI API key as a string, enable the below
OPEN_API_KEY = os.environ['OPEN_API_KEY']
SECRET_KEY = os.environ['SECRET_KEY']


def transcribe_with_cut_file(audio, api_key):
    openai.api_key = encode("decode", api_key, SECRET_KEY)
    main_result = ""
    sound = AudioSegment.from_file(audio)
    os.remove(audio)
    name_folder = get_random_string(4)
    os.mkdir(f"audio/{name_folder}")
    name_file = get_random_string(4)
    sound.export(f"audio/{name_folder}/{name_file}.mp3", format="mp3", bitrate="128k")
    # Load audio file
    audio_file = AudioSegment.from_file(f"audio/{name_folder}/{name_file}.mp3")

    # Calculate duration in minutes
    duration_minutes = audio_file.duration_seconds / 60.0
    print("Duration_minutes: ",duration_minutes)
    
    try:
            # Cut the audio into parts
        for i in range(int(duration_minutes)):
            # Calculate start and end time for each 1 minute segment
            start_time = i * 60 * 1000  # Milliseconds
            end_time = (i + 1) * 60 * 1000  # Milliseconds

            # Cut the audio segment
            audio_segment = audio_file[start_time:end_time]

            # Export the audio segment as a new file
            file_name = f"audio/{name_folder}/part_{i}.mp3"
            audio_segment.export(file_name, format="mp3")
            print(f"Exported {file_name}.")
            file_stt = open(file_name, "rb")
            transcription = openai.Audio.transcribe("whisper-1", file_stt)
            main_result += f" {transcription.text}"
            time.sleep(3)
            print("Done time: ",main_result)

        # Check if the last segment has duration less than 1 minute
        if duration_minutes % 1 != 0:
            start_time = int(duration_minutes) * 60 * 1000  # Milliseconds
            end_time = len(audio_file)  # Milliseconds
            audio_segment = audio_file[start_time:end_time]
            file_name = f"audio/{name_folder}/part_{int(duration_minutes)}.mp3"
            audio_segment.export(file_name, format="mp3")
            print(f"Exported {file_name}.")
            file_stt = open(file_name, "rb")
            transcription = openai.Audio.transcribe("whisper-1", file_stt)
            main_result += f" {transcription.text}"
            print("Done time: ",main_result)
        #process for whisper openai
        
        shutil.rmtree(f"audio/{name_folder}")
        return main_result
    except Exception as e:
        print(e)
        shutil.rmtree(f"audio/{name_folder}")
        return ""
    
# feature audio using pytube and whisper AI
def speech_to_text(link_youtube, fulltime, start_second, end_second, api_key):
    openai.api_key = encode("decode", api_key, SECRET_KEY)
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
        file = path_audio
        transcription = transcribe_with_cut_file(file, api_key)
        print(transcription)
        #remove file audio after process
        return transcription
    else:
        # process speech_to_text
        file = path_audio
        transcription = transcribe_with_cut_file(file, api_key)
        print(transcription)
        #remove file audio after process
        return transcription

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

def youtube_transcripts_with_subtitles(link_youtube, lang):
    yt = YouTube(link_youtube)
    video_id = yt.video_id
    transcript, no_of_words = generate_transcript(video_id, lang)
    # print(transcript)
    return transcript

def transcribe_with_file(audio, api_key):
    try:
        sound = AudioSegment.from_file(audio)
        name_file = get_random_string(4)
        sound.export(f"audio/{name_file}.mp3", format="mp3", bitrate="128k")
        audio_file = open(f"audio/{name_file}.mp3", "rb")
        openai.api_key = encode("decode", api_key, SECRET_KEY)
        #process for whisper openai
        transcription = openai.Audio.transcribe("whisper-1", audio_file)
        os.remove(f"audio/{name_file}.mp3")
        return transcription.text, gr.update(value="""<i style="color:#3ADF00"><center>Bóc băng thành công. Mời tiếp tục</center></i>""", visible=True), gr.update(interactive=True), gr.update(interactive=True)
    except Exception as e:
        print(e)
        os.remove(f"audio/{name_file}.mp3")
        return "", gr.update(value="""<i style="color:red"><center>Đã có lỗi xảy ra. Xin thử lại</center></i>""", visible=True), gr.update(interactive=False), gr.update(interactive=False)
    
