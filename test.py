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

def ChatGPT_conversation(conversation, open_api_key, max_tokens=2000, temperature=0.7):
    # openai.api_key = open_api_key
    # print(conversation)
    # response = openai.ChatCompletion.create(
    #     model=model_id,
    #     messages=conversation,
    #     presence_penalty=0,
    #     temperature=temperature,
    #     top_p=1,
    #     max_tokens=max_tokens,
    # )
    # conversation.append({'role': response.choices[0].message.role, 'content': response.choices[0].message.content})
    # return conversation

    

    url = "https://api-vngpt.aivgroup.vn/api/chat/"

    payload = json.dumps({
    "model": f'{model_id}',
    "messages": f'{conversation}',
    "temperature": f'{temperature}',
    "max_tokens": f'{max_tokens}'
    })
    headers = {
    'Authorization': 'Token e243aa0167e7bff149e324fc410573af387c2224',
    'Content-Type': 'application/json',
    'Cookie': 'csrftoken=Q0tPeW7rP9fi5oSwc4uYNTxYET3xdfwN; messages=W1siX19qc29uX21lc3NhZ2UiLDAsMjUsIlN1Y2Nlc3NmdWxseSBzaWduZWQgaW4gYXMgZG9hbmhpZXVjbnBtMjIwLiIsIiJdXQ:1pbfne:FDXfwYWbYv9gP3HKGQcGZYmtSyXajAyqvpmvjWfoMVI; sessionid=8koqghrg1lngh2s66uwxmia3gwexa0t8'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    response = response.json()
    conversation.append({'role': response.choices[0].message.role, 'content': response.choices[0].message.content})
    return conversation




conversation = []
def chatgpt_process(input, max_tokens, temperature, role, api_token, history):
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
        open_api_key = api_token
        # try:
        conversation = ChatGPT_conversation(conversation, open_api_key, max_tokens, temperature)
        print(conversation)
        response = conversation[-1]['content'].strip()
        # except:
        #     response = "Đã có lỗi. Vui lòng kiểm tra lại số dư tài khoản OpenAI của bạn hoặc kết nối."
        print('{0}: {1}\n'.format(conversation[-1]['role'].strip(), response))
    ## history for chatbot gradio
    history = history or []
    output = response.replace("\n", "<br/>")
    return history + [[input, output]]

def clear_history():
    global conversation
    conversation = []