import os
import gradio as gr
from dotenv import load_dotenv
load_dotenv('./.env')
from chatgpt.app import *
from speech_to_text.app import *
from account.app import *
from lib_app.utils import *
from summary_long_text.app import *
from docs.app import *

OPEN_API_KEY = os.environ['OPEN_API_KEY']
first_key_lock = encode("encode", OPEN_API_KEY, SECRET_KEY)
SECRET_KEY = os.environ['SECRET_KEY']
IMG_BANNER = os.environ['IMG_BANNER']
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
def process_speech_to_text(type_transcripts, language_transcripts,link_youtube, cut_fulltime, msecond_start, msecond_end, main_key):
   if type_transcripts == "Sử dụng subtitles của Youtube":
      if language_transcripts == "Tiếng Việt":
        transcripts = youtube_transcripts_with_subtitles(link_youtube, "vi")
      else:
        transcripts = youtube_transcripts_with_subtitles(link_youtube, "en")
      return transcripts
   else:
      transcripts = speech_to_text(link_youtube, cut_fulltime, msecond_start, msecond_end, main_key)
      return transcripts
   
# function process speech to text
def process_transcribe_with_cut_file(audio_upload, main_key):
   result = transcribe_with_cut_file(audio_upload, main_key)
   if result:
      return result, gr.update(value="""<i style="color:#3ADF00"><center>Bóc băng thành công. Mời tiếp tục</center></i>""", visible=True), gr.update(interactive=True), gr.update(interactive=True)
   else:
      return result, gr.update(value="""<i style="color:red"><center>Đã có lỗi xảy ra. Xin thử lại</center></i>""", visible=True), gr.update(interactive=False), gr.update(interactive=False)

# function update main key (openai api key) for all app
def update_main_key(api_key_textbox):
   key_lock = encode("encode", api_key_textbox, SECRET_KEY)
   return gr.update(value=key_lock)

# function check original_text and summary_text
def check_original_text(original_text):
   conversation = [{"role": "user", "content": original_text}]
   token_original_text = num_tokens_from_messages(conversation)
   if original_text and token_original_text < 2048:
      return gr.update(value="""<i style="color:#3ADF00"><center>Văn bản này phù hợp để sử dụng trực tiếp trong ChatGPT, không nhất thiết cần rút gọn</center></i>""", visible=True), gr.update(interactive=True)
   elif original_text and token_original_text > 2048:
      return gr.update(value="""<i style="color:#3ADF00"><center>Văn bản gốc phù hợp. Mời tiếp tục</center></i>""", visible=True), gr.update(interactive=True)
   else:
      return gr.update(value="""<i style="color:red"><center>Văn bản gốc không được trống. Xin thử lại</center></i>""", visible=True), gr.update(interactive=False)

block = gr.Blocks(css=".gradio-container {padding-top:0px !important; padding-bottom:0px !important;} footer {display:none !important;} #chatbot_custom > .wrap > .message-wrap > .bot {font-size:20px !important; background-color: #b7bbd4 !important} #chatbot_custom > .wrap > .message-wrap > .user {font-size:20px !important} #custom_row {flex-direction: row-reverse;} #chatbot_custom > .wrap > .message-wrap {min-height: 150px;} #custom_title_h1 > h1 {margin-bottom:0px;} #chatbot_custom > .wrap {max-height: 1500px;}")

# function check event change value of flag textbox
def check_flag_textbox(flag_textbox):
   return gr.update(value=flag_textbox)

with block:
    # gr.Markdown("""<h1><center><image></center></h1>""", elem_id="custom_title_h1")
    gr.Markdown(f"""![VnGPT]({IMG_BANNER})""")
    # gr.Markdown("""<p><center>Phần mềm nguồn mở giúp mỗi cá nhân trực tiếp sử dụng ChatGPT và hơn thế nữa ngay trên máy tính của mình. <a href="https://github.com/AIV-Group/VnGPT-CE">Xem thêm tại đây</a></center></p><p><center><a href="https://aivgroupworking.sg.larksuite.com/share/base/form/shrlgHpAepHZvbZFxp3KfMH19kf">Yêu cầu thêm tính năng tại đây</a></center></p>""")
    main_key = gr.Textbox(visible=False, value=first_key_lock)
    flag_textbox = gr.Textbox(visible=False)
    # ChatGPT--turbo3.5
    with gr.Tab("ChatGPT"):
        gr.Markdown("""<h1><center></center></p>""")
        with gr.Row(elem_id="custom_row"):
            with gr.Column(scale=3, min_width=600):
              # max_tokens = gr.Slider(label="Số từ tối đa trong câu hỏi", minimum=150, maximum=1048, step=1, value=256, visible=False)
              # role=gr.Radio(["user", "system", "assistant"], label="Lựa chọn vai trò sẽ hỏi", visible=False)
              temperature = gr.Slider(label="Độ sáng tạo của AI (tối thiểu 0, tối đa 1)", minimum=0, maximum=1, step=0.1, value=0.1, interactive=True)
              num_history = gr.Slider(label="Số lịch sử hội thoại AI có thể nhớ", minimum=1, maximum=10, step=1, value=2, interactive=True)
            with gr.Column(scale=5, min_width=600):
              chatbot = gr.Chatbot(elem_id="chatbot_custom")
              alert_response_chatgpt = gr.Markdown(value="""<i style="color:#3ADF00"><center>Câu hỏi càng ngắn gọn số token càng nhỏ</center></i>""", visible=True) 
              message = gr.Textbox(placeholder="Hỏi chatgpt bất cứ vấn đề nào mà bạn muốn", label="Câu hỏi của bạn", lines=1)
              state = gr.State()
              submit = gr.Button("Gửi câu hỏi")
              #submit gpt
              submit_gpt_event = submit.click(chat, inputs=[message, state, temperature, main_key, num_history], outputs=[chatbot, state, alert_response_chatgpt])
              submit.click(lambda :"", None, message, scroll_to_output=True)
              message_ent_gpt_event = message.submit(chat, inputs=[message, state, temperature, main_key, num_history], outputs=[chatbot, state, alert_response_chatgpt])
              message.submit(lambda :"", None, message, scroll_to_output=True)
              #clear history chat
              with gr.Row():
                clear = gr.Button("Xóa lịch sử chat")
                stop_gpt = gr.Button("Dừng chat")
                stop_gpt.click(lambda: None,cancels=[submit_gpt_event, message_ent_gpt_event])
                clear.click(lambda: None, None, chatbot, queue=False)
                clear.click(fn=clear_history, inputs=state, outputs=state)
    # speech_to_text
    with gr.Tab("Bóc băng Youtube"):
        gr.Markdown("""<h1><center></center></p>""")
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
        btn_transcripts = gr.Button("Bóc băng", interactive=False) 
        with gr.Row().style(equal_height=True):   
          btn_transcripts.click(process_speech_to_text, inputs=[type_transcripts, language_transcripts,link_youtube, cut_fulltime, msecond_start, msecond_end, main_key], outputs=[whisper_result])
          btn_transcripts.click(lambda :"", None, message, scroll_to_output=True)
          btn_send_gpt = gr.Button("Gửi kết quả sang ChatGPT", interactive=False) 
          btn_send_summary = gr.Button("Gửi kết quả sang Rút gọn", interactive=True) 
          btn_send_gpt.click(fn=lambda value: gr.update(value=value), inputs=whisper_result, outputs=message)
          btn_send_gpt.click(fn=lambda value: gr.update(value="""<i style="color:#3ADF00"><center>Gửi kết quả sang ChatGPT thành công.</center></i>"""), inputs=btn_send_gpt, outputs=alert_forward_chatgpt)
          btn_send_summary.click(fn=lambda value: gr.update(value=value), inputs=whisper_result, outputs=flag_textbox)
          btn_send_summary.click(fn=lambda value: gr.update(value="""<i style="color:#3ADF00"><center>Gửi kết quả sang Rút gọn thành công.</center></i>"""), inputs=btn_send_summary, outputs=alert_forward_chatgpt)
          whisper_result.change(check_result_speech_to_text, whisper_result, btn_send_gpt)
          link_youtube.change(populate_metadata, inputs=[link_youtube], outputs=[img, title])
          cut_fulltime.change(filter_full_time, inputs=[cut_fulltime,link_youtube], outputs=[msecond_start, msecond_end])
          link_youtube.change(filter_full_time, inputs=[cut_fulltime,link_youtube], outputs=[msecond_start, msecond_end])
          link_youtube.change(check_link_youtube, link_youtube, outputs=[btn_transcripts, alert_check_link_youtube])
    with gr.Tab("Bóc băng Audio"):
        gr.Markdown("""<h1><center>Bóc băng tệp Audio</center></h1>""")
        audio_upload = gr.Audio(source="upload", type="filepath")
        alert_result_speech_to_text_with_file = gr.Markdown(value="""<i style="color:#0040FF"><center></center></i>""", visible=False)
        result_speech_to_text_with_file = gr.Textbox(label="Kết quả bóc băng", interactive=True)
        submit_audio = gr.Button("Bóc băng", interactive=True)
        with gr.Row().style(equal_height=True):          
          btn_audio_send_gpt = gr.Button("Gửi kết quả sang ChatGPT", interactive=False) 
          btn_audio_send_summary = gr.Button("Gửi kết quả sang Rút gọn", interactive=True) 
          submit_audio.click(process_transcribe_with_cut_file, inputs=[audio_upload, main_key], outputs=[result_speech_to_text_with_file, alert_result_speech_to_text_with_file, submit_audio, btn_audio_send_gpt])
          btn_audio_send_gpt.click(fn=lambda value: gr.update(value=value), inputs=result_speech_to_text_with_file, outputs=message)
          btn_audio_send_gpt.click(fn=lambda value: gr.update(value="""<i style="color:#3ADF00"><center>Gửi kết quả sang ChatGPT thành công.</center></i>""", visible=True), inputs=btn_audio_send_gpt, outputs=alert_result_speech_to_text_with_file)
          btn_audio_send_summary.click(fn=lambda value: gr.update(value=value), inputs=result_speech_to_text_with_file, outputs=flag_textbox)
          btn_audio_send_summary.click(fn=lambda value: gr.update(value="""<i style="color:#3ADF00"><center>Gửi kết quả sang Rút gọn thành công.</center></i>""", visible=True), inputs=btn_audio_send_summary, outputs=alert_result_speech_to_text_with_file)
          audio_upload.change(fn=lambda value: gr.update(interactive=True), inputs=audio_upload, outputs=submit_audio)
    # summary text
    with gr.Tab("Rút gọn văn bản"):
        gr.Markdown("""<h1><center>Rút gọn văn bản dài</center></h1>""")
        original_text = gr.Textbox(label="Văn bản gốc", placeholder="Nhập văn bản gốc vào đây", lines=10)
        alert_check_original_text = gr.Markdown(value="""<i style="color:#0040FF"><center></center></i>""", visible=False)
        max_tokens = gr.Slider(label="Token tối đa", minimum=850, maximum=1024, step=1, value=1000, elem_id="msecond_start", visible=True)
        prompts_summary = gr.Dropdown(["Rút gọn văn bản bằng ngôn ngữ chọn và xuống gần với giá trị max_tokens", "Tùy chỉnh prompt"], label="Prompt rút gọn", value="Rút gọn văn bản bằng ngôn ngữ chọn và xuống gần với giá trị max_tokens", interactive=True, visible=True)
        custom_prompts_summary = gr.Textbox(label="Prompt tùy chỉnh", placeholder="Nhập prompt tùy chỉnh vào đây", lines=2, visible=False)
        language_summary = gr.Dropdown(["Tiếng Việt", "Tiếng Anh"], label="Ngôn ngữ rút gọn", value="Tiếng Việt", interactive=True, visible=True)
        result_summary_long_text = gr.Textbox(label="Kết quả rút gọn", interactive=True)
        with gr.Row().style(equal_height=True):
          btn_submit_summary = gr.Button("Rút gọn", interactive=False)
          btn_summary_send_gpt = gr.Button("Gửi kết quả sang ChatGPT", interactive=True) 
          btn_submit_summary.click(summary_long_text, inputs=[original_text, main_key, max_tokens, language_summary, prompts_summary, custom_prompts_summary], outputs=[result_summary_long_text])
          btn_submit_summary.click(lambda :"", None, message, scroll_to_output=True)
          btn_summary_send_gpt.click(fn=lambda value: gr.update(value=value), inputs=result_summary_long_text, outputs=message)
          btn_summary_send_gpt.click(fn=lambda value: gr.update(value="""<i style="color:#3ADF00"><center>Gửi kết quả sang ChatGPT thành công.</center></i>""", visible=True), inputs=btn_summary_send_gpt, outputs=alert_check_original_text)
          original_text.change(check_original_text, original_text, outputs=[alert_check_original_text, btn_submit_summary])
          prompts_summary.change(lambda value: gr.update(visible=True if value == "Tùy chỉnh prompt" else False), inputs=prompts_summary, outputs=custom_prompts_summary)
    with gr.Tab("Stable Diffusion"):
        gr.Markdown("""<h1><center>Đang phát triển</center></h1>""")
    # Bot hướng dẫn sử dụng
    with gr.Tab("Hướng dẫn sử dụng"):
        gr.Markdown("""<h1><center>Chatbot hướng dẫn sử dụng</center></h1>""")
        with gr.Box(elem_id="custom_row"):
              chatbot_docs = gr.Chatbot(elem_id="chatbot_custom")
              alert_response_chatgpt_docs = gr.Markdown(value="""<i style="color:#3ADF00"><center>Câu hỏi càng ngắn gọn số token càng nhỏ</center></i>""", visible=True) 
              message_docs = gr.Textbox(placeholder="Hỏi chatbot bất cứ vấn đề nào về VnGPT mà bạn muốn", label="Câu hỏi của bạn")
              state_docs = gr.State()
              with gr.Row().style(equal_height=True):
                submit_docs = gr.Button("Gửi câu hỏi")
                #submit gpt
                submit_docs.click(chat_docs, inputs=[message_docs, state_docs, main_key], outputs=[chatbot_docs, state_docs, alert_response_chatgpt_docs])
                submit_docs.click(lambda :"", None, message_docs, scroll_to_output=True)
                message_docs.submit(chat_docs, inputs=[message_docs, state_docs, main_key], outputs=[chatbot_docs, state_docs, alert_response_chatgpt_docs])
                message_docs.submit(lambda :"", None, message_docs, scroll_to_output=True)
                #clear history chat
                clear_docs = gr.Button("Xóa lịch sử chat")
                clear_docs.click(lambda: None, None, chatbot_docs, queue=False)
                clear_docs.click(fn=clear_history_docs, inputs=state_docs, outputs=state_docs)
    # Veri account
        api_key_textbox = gr.Textbox(placeholder="Nhập OpenAI Token vào đây" ,show_label=False, lines=1, type='password', interactive=True, visible=False, value=OPEN_API_KEY)
        api_key_textbox.change(update_main_key, api_key_textbox, main_key)
    flag_textbox.change(check_flag_textbox, flag_textbox, original_text)
# info auth app
ID = os.environ['ID']
PASSWORD = os.environ['PASSWORD']
AUTH = os.environ['AUTH']
HOST = os.environ['HOST']
if AUTH == "False":
  block.queue(concurrency_count=1)
  block.launch(server_name = HOST,debug = True)
else:
  block.queue(concurrency_count=1)
  block.launch(server_name = HOST, auth = (ID,PASSWORD),debug = True)
 