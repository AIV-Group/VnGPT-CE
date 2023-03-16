import os
import gradio as gr
from dotenv import load_dotenv
load_dotenv('./.env')
from chatgpt.app import *
from speech_to_text.app import *
from account.app import *

#all function process app
# func check type account
def filter_type_account(type_account):
  if type_account == "OpenAI Token":
    return gr.update(visible=True), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False)
  elif type_account == "Tài khoản VnGPT":
    return gr.update(visible=False), gr.update(visible=True), gr.update(visible=True), gr.update(visible=True), gr.update(visible=True)
#func check options cut video
def filter_full_time(fulltime, link_youtube):
  if fulltime == True:
    return gr.update(visible=False), gr.update(visible=False)
  elif fulltime == False:
    print("This link: ",link_youtube)
    length = length_link(link_youtube)
    return gr.update(visible=True, maximum=length), gr.update(visible=True, maximum=length)
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
      return gr.update(interactive=True), gr.update(value="""<i style="color:#3ADF00"><center>Link youtube hợp lệ. Mời tiếp tục</center></i>""", visible=True)
   except:
      return gr.update(interactive=False), gr.update(value="""<i style="color:red"><center>Link youtube không hợp lệ. Xin thử lại</center></i>""", visible=True)

# func check type speech_to_text
def check_type_transcripts(type_transcripts):
   if type_transcripts == "Sử dụng subtitles của Youtube":
      return gr.update(visible=False), gr.update(visible=True)
   else:
      return gr.update(visible=True), gr.update(visible=False)

# process before speech_to_text
def process_speech_to_text(type_transcripts, language_transcripts,link_youtube, cut_fulltime, msecond_start, msecond_end):
   if type_transcripts == "Sử dụng subtitles của Youtube":
      if language_transcripts == "Tiếng Việt":
        transcripts = youtube_transcripts(link_youtube, "vi")
      else:
        transcripts = youtube_transcripts(link_youtube, "en")
      return transcripts
   else:
      transcripts = speech_to_text(link_youtube, cut_fulltime, msecond_start, msecond_end)
      return transcripts

block = gr.Blocks(css="footer {display:none !important;} #chatbot_custom > .wrap > .message-wrap > .bot {font-size:20px !important; background-color: #b7bbd4 !important} #chatbot_custom > .wrap > .message-wrap > .user {font-size:20px !important} #custom_row {flex-direction: row-reverse;} #chatbot_custom > .wrap > .message-wrap {min-height: 150px;} #custom_title_h1 > h1 {margin-bottom:0px;}")


with block:
    gr.Markdown("""<h1><center>VnGPT - AI cho mọi nhà</center></h1>""", elem_id="custom_title_h1")
    gr.Markdown("""<p><center>Phần mềm nguồn mở giúp mỗi cá nhân trực tiếp sử dụng ChatGPT và hơn thế nữa ngay trên máy tính của mình. <a href="https://github.com/AIV-Group/VnGPT-CE">Xem thêm tại đây</a></center></p>""")
    # Veri account
    with gr.Tab("Tài khoản"):
        gr.Markdown("""<h1><center>Dùng OpenAI Key hoặc tài khoản VNGPT để sử dụng</center></h1>""")
        # main_key = gr.Textbox(visible=False)
        type_account = gr.Radio(label="Loại tài khoản", choices=["OpenAI Token", "Tài khoản VnGPT"])
        api_key_textbox = gr.Textbox(placeholder="Nhập OpenAI Token vào đây",show_label=False, lines=1, type='password', interactive=True, visible=False)
        username = gr.Textbox(label="Tài khoản", visible=False, interactive=True)
        password = gr.Textbox(label="Mật khẩu",type='password', visible=False, interactive=True)
        alert_login = gr.Markdown(value="""<i style="color:#0040FF"><center>Tài khoản này do AIV Group cấp</center></i>""", visible=False)
        login_btn = gr.Button("Đăng nhập", visible=False)
        login_btn.click(get_token, [username, password], outputs=[api_key_textbox, alert_login], scroll_to_output=True)
        password.submit(get_token, [username, password], outputs=[api_key_textbox, alert_login], scroll_to_output=True)
        type_account.change(filter_type_account, type_account, outputs=[api_key_textbox, username, password, login_btn, alert_login])
    # ChatGPT--turbo3.5
    with gr.Tab("ChatGPT"):
        gr.Markdown("""<h1><center>Hội thoại với ChatGPT (OpenAI)</center></h1>""")
        with gr.Row(elem_id="custom_row"):
            with gr.Column(scale=3, min_width=600):
              max_tokens = gr.Slider(label="Số từ tối đa trong câu hỏi", minimum=150, maximum=1048, step=1, value=256, visible=False)
              role=gr.Radio(["user", "system", "assistant"], label="Lựa chọn vai trò sẽ hỏi", visible=False)
              temperature = gr.Slider(label="Độ sáng tạo của AI (tối thiểu 0, tối đa 1)", minimum=0, maximum=1, step=0.1, value=0.7)
            with gr.Column(scale=5, min_width=600):
              chatbot = gr.Chatbot(elem_id="chatbot_custom")
              message = gr.Textbox(placeholder=prompt, label="Câu hỏi của bạn")
              state = gr.State()
              submit = gr.Button("Gửi câu hỏi")
              submit.click(chatgpt_process, [message, max_tokens, temperature, role, type_account, api_key_textbox, chatbot], chatbot, scroll_to_output=True)
              submit.click(lambda :"", None, message, scroll_to_output=True)
              message.submit(chatgpt_process, [message, max_tokens, temperature, role, type_account, api_key_textbox, chatbot], chatbot, scroll_to_output=True)
              message.submit(lambda :"", None, message, scroll_to_output=True)
              #clear history chat
              clear = gr.Button("Xóa lịch sử chat")
              clear.click(lambda: None, None, chatbot, queue=False)
              clear.click(lambda: clear_history(), queue=False)
    # speech_to_text
    with gr.Tab("Bóc băng Youtube"):
        gr.Markdown("""<h1><center>Bóc băng Youtube</center></h1>""")
        with gr.Row().style(equal_height=True):
          # with gr.Column():
            link_youtube = gr.Textbox(label="YouTube Link")
        alert_check_link_youtube = gr.Markdown(visible=False)     
        with gr.Row().style(equal_height=True):
          with gr.Box():
            type_transcripts = gr.Dropdown(["Sử dụng subtitles của Youtube", "Sử dụng Whisper AI"], label="Loại bóc băng", info="Lựa chọn hình thức bóc băng", value="Sử dụng subtitles của Youtube", interactive=True)
            language_transcripts = gr.Dropdown(["Tiếng Việt", "Tiếng Anh"], label="Ngôn ngữ bóc băng", value="Tiếng Việt", interactive=True, visible=True)
            cut_fulltime = gr.Checkbox(label="Bóc toàn bộ video", visible=False, value=True)
            msecond_start = gr.Slider(label="Thời gian bắt đầu (phút)", minimum=0, maximum=180, step=1, value=0, elem_id="msecond_start", visible=False)
            msecond_end = gr.Slider(label="Thời gian kết thúc (phút)", minimum=0, maximum=180, step=1, value=0, elem_id="msecond_end", visible=False)
            type_transcripts.change(check_type_transcripts, type_transcripts, outputs=[cut_fulltime,language_transcripts])
          with gr.Box():
              title = gr.Label(label="Tiêu đề video")
              img = gr.Image(label="Thumbnail youtube")
        with gr.Row().style(equal_height=True):
          whisper_result = gr.Textbox(label="Bóc băng", placeholder="Kết quả bóc băng", lines=10)
        alert_forward_chatgpt = gr.Markdown(value="""<i style="color:#0040FF"><center>Bạn có thể gửi kết quả bóc băng sang ChatGPT để tiếp tục xử lý</center></i>""", visible=True)  
        with gr.Row().style(equal_height=True):
          btn_transcripts = gr.Button("Bóc băng", interactive=False)     
          btn_transcripts.click(process_speech_to_text, inputs=[type_transcripts, language_transcripts,link_youtube, cut_fulltime, msecond_start, msecond_end], outputs=[whisper_result])
          btn_transcripts.click(lambda :"", None, message, scroll_to_output=True)
          btn_send_gpt = gr.Button("Gửi kết quả sang ChatGPT", interactive=False) 
          btn_send_gpt.click(fn=lambda value: gr.update(value=value, lines=5), inputs=whisper_result, outputs=message)
          btn_send_gpt.click(fn=lambda value: gr.update(value="""<i style="color:#3ADF00"><center>Gửi kết quả sang ChatGPT thành công.</center></i>"""), inputs=btn_send_gpt, outputs=alert_forward_chatgpt)
          whisper_result.change(check_result_speech_to_text, whisper_result, btn_send_gpt)
          link_youtube.change(populate_metadata, inputs=[link_youtube], outputs=[img, title])
          cut_fulltime.change(filter_full_time, inputs=[cut_fulltime,link_youtube], outputs=[msecond_start, msecond_end])
          link_youtube.change(filter_full_time, inputs=[cut_fulltime,link_youtube], outputs=[msecond_start, msecond_end])
          link_youtube.change(check_link_youtube, link_youtube, outputs=[btn_transcripts, alert_check_link_youtube])
    with gr.Tab("Stable Diffusion"):
        gr.Markdown("""<h1><center>Đang phát triển</center></h1>""")

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
