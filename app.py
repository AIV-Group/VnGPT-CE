import os
import gradio as gr
from dotenv import load_dotenv
load_dotenv('./.env')
from chatgpt.app import *
from speech_to_text.app import *
from account.app import *

block = gr.Blocks(css="footer {display:none !important;} #chatbot_custom > .wrap > .message-wrap > .bot {font-size:20px !important; background-color: #444654 !important} #chatbot_custom > .wrap > .message-wrap > .user {font-size:20px !important} #custom_row {flex-direction: row-reverse;} #chatbot_custom > .wrap > .message-wrap {min-height: 150px;} #custom_title_h1 > h1 {margin-bottom:0px;}")


with block:
    gr.Markdown("""<h1><center>VnGPT - AI cho mọi nhà</center></h1>""", elem_id="custom_title_h1")
    gr.Markdown("""<p><center>Phần mềm nguồn mở giúp mỗi cá nhân trực tiếp sử dụng ChatGPT và hơn thế nữa ngay trên máy tính của mình. <a href="https://github.com/AIV-Group/VnGPT-CE">Xem thêm tại đây</a></center></p>""")
    # Veri account
    with gr.Tab("Tài khoản"):
        gr.Markdown("""<h1><center>Dùng OpenAI Key hoặc tài khoản VNGPT để sử dụng</center></h1>""")
        # main_key = gr.Textbox(visible=False)
        type_account = gr.Radio(label="Loại tài khoản", choices=["OpenAI Token", "Tài khoản VnGPT"])
        def filter_type_account(type_account):
          if type_account == "OpenAI Token":
              return gr.update(visible=True), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False)
          elif type_account == "Tài khoản VnGPT":
              return gr.update(visible=False), gr.update(visible=True), gr.update(visible=True), gr.update(visible=True), gr.update(visible=True)
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
              max_tokens = gr.Slider(label="Max Tokens (tối thiểu 150, tối đa 1048)", minimum=150, maximum=1048, step=1, value=256)
              role=gr.Radio(["user", "system", "assistant"], label="Lựa chọn vai trò sẽ hỏi")
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
        gr.Markdown("""<h1><center>Bóc băng Youtube bằng Whisper (OpenAI)</center></h1>""")
        with gr.Row().style(equal_height=True):
          with gr.Column(scale=3, min_width=600):
            link = gr.Textbox(label="YouTube Link")
          with gr.Column(scale=3, min_width=600):
            fulltime = gr.Checkbox(label="Bóc toàn bộ video", visible=True, value=True)
            msecond_start = gr.Slider(label="Thời gian bắt đầu (phút)", minimum=0, maximum=180, step=1, value=0, elem_id="msecond_start", visible=False)
            msecond_end = gr.Slider(label="Thời gian kết thúc (phút)", minimum=0, maximum=180, step=1, value=0, elem_id="msecond_end", visible=False)
        with gr.Row().style(equal_height=True):
          with gr.Column(scale=3, min_width=600):
            title = gr.Label(label="Tiêu đề video")
          with gr.Column(scale=3, min_width=600):
            img = gr.Image(label="Thumbnail youtube")
        with gr.Row().style(equal_height=True):
          text = gr.Textbox(label="Bóc băng", placeholder="Kết quả bóc băng", lines=10)
        with gr.Row().style(equal_height=True):
          btn = gr.Button("Bóc băng")       
          btn.click(speech_to_text, inputs=[link, fulltime, msecond_start, msecond_end], outputs=[text])
          btn.click(lambda :"", None, message, scroll_to_output=True)
          link.change(populate_metadata, inputs=[link], outputs=[img, title])
          def filter_full_time(fulltime, link):
            if fulltime == True:
                return gr.update(visible=False), gr.update(visible=False)
            elif fulltime == False:
                print("This link: ",link)
                length = length_link(link)
                return gr.update(visible=True, maximum=length), gr.update(visible=True, maximum=length)
          fulltime.change(filter_full_time, inputs=[fulltime,link], outputs=[msecond_start, msecond_end])
          link.change(filter_full_time, inputs=[fulltime,link], outputs=[msecond_start, msecond_end])
    with gr.Tab("Stable Diffusion"):
        gr.Markdown("""<h1><center>Đang phát triển</center></h1>""")
ID = os.environ['ID']
PASSWORD = os.environ['PASSWORD']
AUTH = os.environ['AUTH']
if AUTH == "False":
  block.queue(concurrency_count=1)
  block.launch(server_name = "0.0.0.0",debug = True)
else:
  block.queue(concurrency_count=1)
  block.launch(server_name = "0.0.0.0", auth = (ID,PASSWORD),debug = True)
