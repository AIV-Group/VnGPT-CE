import os
import openai
from dotenv import load_dotenv
load_dotenv('./.env')
import requests
import json


#if you have OpenAI API key as an environment variable, enable the below
#openai.api_key = os.getenv("OPENAI_API_KEY")

#if you have OpenAI API key as a string, enable the below
OPEN_API_KEY = os.environ['OPEN_API_KEY']

prompt = "Hỏi chatbot gpt bất cứ vấn đề nào mà bạn muốn"

model_id = 'gpt-3.5-turbo'

def ChatGPT_conversation(conversation, type_account, api_key, max_tokens=1000, temperature=0.7):
    if type_account == "OpenAI Token":
        openai.api_key = api_key
        print(conversation)
        response = openai.ChatCompletion.create(
            model=model_id,
            messages=conversation,
            presence_penalty=0,
            temperature=temperature,
            top_p=1,
            # max_tokens=max_tokens,
        )
        print(type(response))
        conversation.append({'role': response.choices[0].message.role, 'content': response.choices[0].message.content})
        return conversation
    elif type_account == "Tài khoản VnGPT":
        url = "https://api-vngpt.aivgroup.vn/api/chat/"

        payload = json.dumps({
            "model": model_id,
            "messages": conversation,
            "temperature": temperature,
            "max_tokens": max_tokens
                })
        headers = {
        'Authorization': f'Token {api_key}',
        'Content-Type': 'application/json',
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        response = response.json()
        conversation.append({'role': response["choices"][0]["message"]["role"], 'content': response["choices"][0]["message"]["content"]})
        return conversation




conversation = []
def chatgpt_process(input, max_tokens, temperature, role, type_account, api_token, history):
    # print(history)
    if type_account:  
        if role:
            role=role
        else:
            role="user"
        global conversation
        prompt = input
        conversation.append({'role': f'{role}', 'content': prompt})
        api_key = api_token
        try:
            conversation = ChatGPT_conversation(conversation, type_account, api_key, max_tokens, temperature)
            response = conversation[-1]['content'].strip()
        except:
            response = "Đã có lỗi. Vui lòng kiểm tra lại câu hỏi hoặc tài khoản hệ thống."
        print('{0}: {1}\n'.format(conversation[-1]['role'].strip(), response))
    else:
        response = "Bạn chưa cài đặt thông tin tài khoản để sử dụng VnGPT"
    ## history for chatbot gradio
    history = history or []
    output = response.replace("\n", "<br/>")
    return history + [[input, output]]

def clear_history():
    global conversation
    conversation = []