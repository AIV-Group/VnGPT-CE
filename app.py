import os
import openai
import gradio as gr
from dotenv import load_dotenv
load_dotenv('./.env')

#if you have OpenAI API key as an environment variable, enable the below
#openai.api_key = os.getenv("OPENAI_API_KEY")

#if you have OpenAI API key as a string, enable the below
OPEN_API_KEY = os.environ['OPEN_API_KEY']
openai.api_key = OPEN_API_KEY

prompt = "Hỏi chatbot gpt bất cứ vấn đề nào mà bạn muốn"

model_id = 'gpt-3.5-turbo'

def ChatGPT_conversation(conversation, max_tokens=2000, temperature=0.7):
    print(conversation)
    response = openai.ChatCompletion.create(
        model=model_id,
        messages=conversation,
        presence_penalty=0,
        temperature=temperature,
        top_p=1,
        max_tokens=max_tokens,
    )
    conversation.append({'role': response.choices[0].message.role, 'content': response.choices[0].message.content})
    return conversation


conversation = []
def chatgpt_process(input, max_tokens, temperature, role, history):
    print(history)
    if role:
        role=role
    else:
        role="user"
    global conversation
    prompt = input
    conversation.append({'role': f'{role}', 'content': prompt})
    conversation = ChatGPT_conversation(conversation, max_tokens, temperature)
    response = conversation[-1]['content'].strip()
    print('{0}: {1}\n'.format(conversation[-1]['role'].strip(), response))
    ## history for chatbot
    history = history or []
    # s = list(sum(history, ()))
    # s.append(input)
    # inp = ' '.join(s)
    output = response.replace("\n", "<br/>")
    # history.append((input, output))
    # print(history)
    return history + [[input, output]]

def clear_history():
    global conversation
    conversation = []

block = gr.Blocks(css="footer {display:none !important;} #chatbot_custom > .wrap > .message-wrap > .bot {font-size:20px !important; background-color: #444654 !important} #chatbot_custom > .wrap > .message-wrap > .user {font-size:20px !important} #custom_row {flex-direction: row-reverse;} #chatbot_custom > .wrap > .message-wrap {min-height: 150px;} #custom_title_h1 > h1 {margin-bottom:0px;}")


with block:
    gr.Markdown("""<h1><center>VnGPT - AI cho mọi nhà</center></h1>""", elem_id="custom_title_h1")
    gr.Markdown("""<p><center>Phần mềm nguồn mở giúp mỗi cá nhân trực tiếp sử dụng ChatGPT và hơn thế nữa ngay trên máy tính của mình. <a href="https://github.com/AIV-Group/VnGPT-CE">Xem thêm tại đây</a></center></p>""")
    with gr.Tab("ChatGPT"):
        gr.Markdown("""<h1><center>Hội thoại GPT</center></h1>""")
        with gr.Row(elem_id="custom_row"):
            with gr.Column(scale=3, min_width=600):
              max_tokens = gr.Slider(label="Max Tokens (tối thiểu 150, tối đa 4000)", minimum=150, maximum=4000, step=1, value=256)
              role=gr.Radio(["user", "system", "assistant"], label="Lựa chọn vai trò sẽ hỏi")
              temperature = gr.Slider(label="Độ sáng tạo của AI (tối thiểu 0, tối đa 1)", minimum=0, maximum=1, step=0.1, value=0.7)
            with gr.Column(scale=5, min_width=600):
              chatbot = gr.Chatbot(elem_id="chatbot_custom")
              message = gr.Textbox(placeholder=prompt, label="Câu hỏi của bạn")
              state = gr.State()
              message.submit(chatgpt_process, [message, max_tokens, temperature, role, chatbot], chatbot, scroll_to_output=True)
              message.submit(lambda :"", None, message, scroll_to_output=True)
              #clear history chat
              clear = gr.Button("Xóa lịch sử chat")
              clear.click(lambda: None, None, chatbot, queue=False)
              clear.click(lambda: clear_history(), queue=False)
    with gr.Tab("Stable Diffusion"):
        gr.Markdown("""<h1><center>Đang phát triển</center></h1>""")

block.launch(server_name = "0.0.0.0",debug = True)
