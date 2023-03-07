import os
import openai
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
    # print(history)
    token_input = len(input) + max_tokens
    if token_input > 1800: 
        response = "Bạn đã vượt quá hạn mức, vui lòng rút gọn câu hỏi phù hợp hơn"
    else:
        if role:
            role=role
        else:
            role="user"
        global conversation
        prompt = input
        conversation.append({'role': f'{role}', 'content': prompt})
        try:
            conversation = ChatGPT_conversation(conversation, max_tokens, temperature)
            response = conversation[-1]['content'].strip()
        except:
            response = "Đã có lỗi. Vui lòng kiểm tra lại số dư tài khoản OpenAI của bạn hoặc kết nối."
        print('{0}: {1}\n'.format(conversation[-1]['role'].strip(), response))
    ## history for chatbot gradio
    history = history or []
    output = response.replace("\n", "<br/>")
    return history + [[input, output]]

def clear_history():
    global conversation
    conversation = []