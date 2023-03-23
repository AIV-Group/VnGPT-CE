import os
import gradio as gr
from dotenv import load_dotenv
load_dotenv('./.env')
from chatgpt.app import *
from speech_to_text.app import *
from account.app import *
from lib_app.utils import *

OPEN_API_KEY = os.environ['OPEN_API_KEY']
first_key_lock = encode("encode", OPEN_API_KEY, SECRET_KEY)
SECRET_KEY = os.environ['SECRET_KEY']
#all function process app
# func check type account
def filter_type_account(type_account):
  if type_account == "OpenAI Token":
    return gr.update(visible=True), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False)
  elif type_account == "Tài khoản VnGPT":
    return gr.update(visible=False), gr.update(visible=True), gr.update(visible=True), gr.update(visible=True), gr.update(visible=True)
# func check ready result speech to text
def check_result_speech_to_text(whisper_result):
   if whisper_result:
      return gr.update(interactive=True)
   else:
      return gr.update(interactive=False)

# func check exits link youtube
def check_link_youtube(link_youtube):
   try:
      populate_metadata(link_youtube)
      return gr.update(interactive=True), gr.update(value="""<i style="color:#3ADF00"><center>Link youtube hợp lệ. Mời tiếp tục</center></i>""", visible=True), gr.update(interactive=True), gr.update(interactive=True)
   except:
      return gr.update(interactive=False), gr.update(value="""<i style="color:red"><center>Link youtube không hợp lệ. Xin thử lại</center></i>""", visible=True), gr.update(visible=False), gr.update(visible=False)

# func check type speech_to_text
def check_type_transcripts(type_transcripts):
   if type_transcripts == "Sử dụng subtitles của Youtube":
      return gr.update(visible=False), gr.update(visible=True), gr.update(visible=False)
   else:
      return gr.update(visible=True), gr.update(visible=False), gr.update(visible=True)

# process before speech_to_text
def process_speech_to_text(type_transcripts, language_transcripts,link_youtube, audio_youtube_convert, main_key):
   if type_transcripts == "Sử dụng subtitles của Youtube":
      if language_transcripts == "Tiếng Việt":
        transcripts = youtube_transcripts_with_subtitles(link_youtube, "vi")
      else:
        transcripts = youtube_transcripts_with_subtitles(link_youtube, "en")
      return transcripts
   else:
      transcripts = transcribe_with_file(audio_youtube_convert, main_key)
      return transcripts
def update_main_key(api_key_textbox):
   key_lock = encode("encode", api_key_textbox, SECRET_KEY)
   return gr.update(value=key_lock)

block = gr.Blocks(css="footer {display:none !important;} #chatbot_custom > .wrap > .message-wrap > .bot {font-size:20px !important; background-color: #b7bbd4 !important} #chatbot_custom > .wrap > .message-wrap > .user {font-size:20px !important} #custom_row {flex-direction: row-reverse;} #chatbot_custom > .wrap > .message-wrap {min-height: 150px;} #custom_title_h1 > h1 {margin-bottom:0px;}")


with block:
    gr.Markdown("""<h1><center>VnGPT - AI cho mọi nhà</center></h1>""", elem_id="custom_title_h1")
    gr.Markdown("""<p><center>Phần mềm nguồn mở giúp mỗi cá nhân trực tiếp sử dụng ChatGPT và hơn thế nữa ngay trên máy tính của mình. <a href="https://github.com/AIV-Group/VnGPT-CE">Xem thêm tại đây</a></center></p><p><center><a href="https://aivgroupworking.sg.larksuite.com/share/base/form/shrlgHpAepHZvbZFxp3KfMH19kf">Yêu cầu thêm tính năng tại đây</a></center></p>""")
    main_key = gr.Textbox(visible=False, value=first_key_lock)
    # ChatGPT--turbo3.5
    with gr.Tab("ChatGPT"):
        gr.Markdown("""<h1><center>Hội thoại với ChatGPT (OpenAI)</center></h1><p><center><a href="https://github.com/AIV-Group/VnGPT-CE/wiki/H%C6%B0%E1%BB%9Bng-d%E1%BA%ABn-s%E1%BB%AD-d%E1%BB%A5ng-ch%E1%BB%A9c-n%C4%83ng-ChatGPT-trong-VnGPT">Xem hướng dẫn sử dụng tại đây</a></center></p>""")
        with gr.Row(elem_id="custom_row"):
            with gr.Column(scale=3, min_width=600):
              # max_tokens = gr.Slider(label="Số từ tối đa trong câu hỏi", minimum=150, maximum=1048, step=1, value=256, visible=False)
              # role=gr.Radio(["user", "system", "assistant"], label="Lựa chọn vai trò sẽ hỏi", visible=False)
              temperature = gr.Slider(label="Độ sáng tạo của AI (tối thiểu 0, tối đa 1)", minimum=0, maximum=1, step=0.1, value=0.1, interactive=True)
            with gr.Column(scale=5, min_width=600):
              chatbot = gr.Chatbot(elem_id="chatbot_custom")
              alert_response_chatgpt = gr.Markdown(value="""<i style="color:#3ADF00"><center>Câu hỏi càng ngắn gọn số token càng nhỏ</center></i>""", visible=True) 
              message = gr.Textbox(placeholder="Hỏi chatgpt bất cứ vấn đề nào mà bạn muốn", label="Câu hỏi của bạn")
              state = gr.State()
              submit = gr.Button("Gửi câu hỏi")
              #submit gpt
              submit.click(chat, inputs=[message, state, temperature, main_key], outputs=[chatbot, state, alert_response_chatgpt])
              submit.click(lambda :"", None, message, scroll_to_output=True)
              message.submit(chat, inputs=[message, state, temperature, main_key], outputs=[chatbot, state, alert_response_chatgpt])
              message.submit(lambda :"", None, message, scroll_to_output=True)
              #clear history chat
              clear = gr.Button("Xóa lịch sử chat")
              clear.click(lambda: None, None, chatbot, queue=False)
              clear.click(fn=clear_history, inputs=state, outputs=state)
    # speech_to_text
    with gr.Tab("Bóc băng Youtube"):
        gr.Markdown("""<h1><center>Bóc băng Youtube</center></h1><p><center><a href="https://github.com/AIV-Group/VnGPT-CE/wiki/H%C6%B0%E1%BB%9Bng-d%E1%BA%ABn-s%E1%BB%AD-d%E1%BB%A5ng-ch%E1%BB%A9c-n%C4%83ng-B%C3%B3c-B%C4%83ng">Xem hướng dẫn sử dụng tại đây</a></center></p>""")
        with gr.Row().style(equal_height=True):
          # with gr.Column():
            link_youtube = gr.Textbox(label="YouTube Link")
        alert_check_link_youtube = gr.Markdown(visible=False)     
        with gr.Row().style(equal_height=True):
          with gr.Box():
            type_transcripts = gr.Dropdown(["Sử dụng subtitles của Youtube", "Sử dụng Whisper AI"], label="Loại bóc băng", info="Lựa chọn hình thức bóc băng", value="Sử dụng subtitles của Youtube", interactive=True)
            language_transcripts = gr.Dropdown(["Tiếng Việt", "Tiếng Anh"], label="Ngôn ngữ bóc băng", value="Tiếng Việt", interactive=True, visible=True)
            audio_youtube_convert = gr.Audio(label="File audio sẽ hiển thị tại đây", source="upload", type="filepath", visible=False, interactive=False)
            btn_get_audio_youtube = gr.Button("Lấy file audio", interactive=False, visible=False)
            btn_get_audio_youtube.click(get_audio_from_youtube, link_youtube, outputs=audio_youtube_convert)
            type_transcripts.change(check_type_transcripts, type_transcripts, outputs=[audio_youtube_convert,language_transcripts, btn_get_audio_youtube])
          with gr.Box():
              title = gr.Label(label="Tiêu đề video")
              img = gr.Image(label="Thumbnail youtube")
        with gr.Row().style(equal_height=True):
          whisper_result = gr.Textbox(label="Bóc băng", placeholder="Kết quả bóc băng", lines=10)
        alert_forward_chatgpt = gr.Markdown(value="""<i style="color:#0040FF"><center>Bạn có thể gửi kết quả bóc băng sang ChatGPT để tiếp tục xử lý</center></i>""", visible=True)  
        with gr.Row().style(equal_height=True):
          btn_transcripts = gr.Button("Bóc băng", interactive=False)   
          btn_send_gpt = gr.Button("Gửi kết quả sang ChatGPT", interactive=False)   
          btn_transcripts.click(process_speech_to_text, inputs=[type_transcripts, language_transcripts,link_youtube, audio_youtube_convert, main_key], outputs=[whisper_result, alert_forward_chatgpt, btn_transcripts, btn_send_gpt])
          btn_transcripts.click(lambda :"", None, message, scroll_to_output=True)
          btn_send_gpt.click(fn=lambda value: gr.update(value=value, lines=5), inputs=whisper_result, outputs=message)
          btn_send_gpt.click(fn=lambda value: gr.update(value="""<i style="color:#3ADF00"><center>Gửi kết quả sang ChatGPT thành công.</center></i>"""), inputs=btn_send_gpt, outputs=alert_forward_chatgpt)
          whisper_result.change(check_result_speech_to_text, whisper_result, btn_send_gpt)
          link_youtube.change(populate_metadata, inputs=[link_youtube], outputs=[img, title])
          link_youtube.change(check_link_youtube, link_youtube, outputs=[btn_transcripts, alert_check_link_youtube, audio_youtube_convert, btn_get_audio_youtube])
    with gr.Tab("Bóc băng Audio"):
        gr.Markdown("""<h1><center>Bóc băng tệp Audio</center></h1>""")
        audio_upload = gr.Audio(label="Tải lên file audio tại đây", source="upload", type="filepath")
        alert_result_speech_to_text_with_file = gr.Markdown(value="""<i style="color:#0040FF"><center></center></i>""", visible=False)
        result_speech_to_text_with_file = gr.Textbox(label="Kết quả bóc băng", interactive=True)
        with gr.Row().style(equal_height=True):
          submit_audio = gr.Button("Bóc băng", interactive=False)
          btn_audio_send_gpt = gr.Button("Gửi kết quả sang ChatGPT", interactive=False) 
          submit_audio.click(transcribe_with_file, inputs=[audio_upload, main_key], outputs=[result_speech_to_text_with_file, alert_result_speech_to_text_with_file, submit_audio, btn_audio_send_gpt])
          btn_audio_send_gpt.click(fn=lambda value: gr.update(value=value, lines=5), inputs=result_speech_to_text_with_file, outputs=message)
          btn_audio_send_gpt.click(fn=lambda value: gr.update(value="""<i style="color:#3ADF00"><center>Gửi kết quả sang ChatGPT thành công.</center></i>""", visible=True), inputs=btn_audio_send_gpt, outputs=alert_result_speech_to_text_with_file)
          audio_upload.change(fn=lambda value: gr.update(interactive=True), inputs=audio_upload, outputs=submit_audio)
    with gr.Tab("Stable Diffusion"):
        gr.Markdown("""<h1><center>Đang phát triển</center></h1>""")
    # Veri account
    with gr.Tab("Tài khoản"):
        gr.Markdown("""<h1><center>Dùng OpenAI Key hoặc tài khoản VNGPT để sử dụng</center></h1>""")
        type_account = gr.Radio(label="Loại tài khoản", choices=["OpenAI Token", "Tài khoản VnGPT"], value="OpenAI Token")
        api_key_textbox = gr.Textbox(placeholder="Nhập OpenAI Token vào đây" ,show_label=False, lines=1, type='password', interactive=True, visible=True, value=OPEN_API_KEY)
        username = gr.Textbox(label="Tài khoản", visible=False, interactive=True)
        password = gr.Textbox(label="Mật khẩu",type='password', visible=False, interactive=True)
        alert_login = gr.Markdown(value="""<i style="color:#0040FF"><center>Tài khoản này do AIV Group cấp</center></i>""", visible=False)
        login_btn = gr.Button("Đăng nhập", visible=False)
        login_btn.click(get_token, [username, password], outputs=[api_key_textbox, alert_login], scroll_to_output=True)
        password.submit(get_token, [username, password], outputs=[api_key_textbox, alert_login], scroll_to_output=True)
        type_account.change(filter_type_account, type_account, outputs=[api_key_textbox, username, password, login_btn, alert_login])
        api_key_textbox.change(update_main_key, api_key_textbox, main_key)

# info auth app
ID = os.environ['ID']
PASSWORD = os.environ['PASSWORD']
AUTH = os.environ['AUTH']
if AUTH == "False":
  block.queue(concurrency_count=1)
  block.launch(server_name = "0.0.0.0",debug = True)
else:
  block.queue(concurrency_count=1)
  block.launch(server_name = "0.0.0.0", auth = (ID,PASSWORD),debug = True)
 