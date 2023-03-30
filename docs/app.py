import os
import openai
from dotenv import load_dotenv
load_dotenv('./.env')
import json
# new code get response openai
from typing import List, Tuple, Dict, Generator
from langchain.llms import OpenAI
import gradio as gr
import requests
import tiktoken
from lib_app.utils import *
from .data_train import *
#if you have OpenAI API key as an environment variable, enable the below
#openai.api_key = os.getenv("OPENAI_API_KEY")

#if you have OpenAI API key as a string, enable the below
OPEN_API_KEY = os.environ['OPEN_API_KEY']
SECRET_KEY = os.environ['SECRET_KEY']

model_name = "gpt-3.5-turbo"

# def create_history_messages(history: List[Tuple[str, str]]) -> List[dict]:
#     history_messages = [{"role": "user", "content": m[0]} for m in history]
#     history_messages.extend([{"role": "assistant", "content": m[1]} for m in history])
#     return history_messages

def num_tokens_from_messages_docs(messages, model="gpt-3.5-turbo-0301"):
    encoding = tiktoken.encoding_for_model(model)
    num_tokens = 0
    for message in messages:
        num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":  # if there's a name, the role is omitted
                num_tokens += -1  # role is always required and always 1 token
    num_tokens += 2  # every reply is primed with <im_start>assistant
    return num_tokens

def create_formatted_history_docs(history_messages: List[dict]) -> List[Tuple[str, str]]:
    formatted_history = []
    user_messages = []
    assistant_messages = []

    for message in history_messages:
        if message["role"] == "user":
            user_messages.append(message["content"])
        elif message["role"] == "assistant":
            assistant_messages.append(message["content"])

        if user_messages and assistant_messages:
            formatted_history.append(
                ("".join(user_messages), "".join(assistant_messages))
            )
            user_messages = []
            assistant_messages = []

    # append any remaining messages
    if user_messages:
        formatted_history.append(("".join(user_messages), None))
    elif assistant_messages:
        formatted_history.append((None, "".join(assistant_messages)))

    return formatted_history

def chat_docs(
    message: str, state: List[Dict[str, str]], api_key: str
) -> Generator[Tuple[List[Tuple[str, str]], List[Dict[str, str]]], None, None]:
    key_open = encode("decode", api_key, SECRET_KEY)
    LLM = OpenAI(model_name=model_name, temperature=0.1, openai_api_key=key_open)
    print("State 1: ",state)
    history_messages = state
    if history_messages == None:
        history_messages = []
        history_messages.append({"role": "system", "content": "A helpful assistant."})

    # check max token
    max_response_tokens = 256
    token_limit= 4096
    conversation = [{"role": "user", "content": message}]
    conv_history_tokens = num_tokens_from_messages_docs(conversation)
    print("This token using with promt: ",conv_history_tokens)
    if conv_history_tokens+max_response_tokens >= token_limit:
        try:
            formatted_history = create_formatted_history_docs(state)
            yield formatted_history, state, gr.update(value="""<i style="color:red"><center>AI không thể xử lý câu hỏi quá dài. Xin thử lại.</center></i>""", visible=True)
        except:
            yield [], [], gr.update(value="""<i style="color:red"><center>AI không thể xử lý câu hỏi quá dài. Xin thử lại.</center></i>""", visible=True)
    else:
        history_messages.append({"role": "user", "content": message})
        # We have no content for the assistant's response yet but we will update this:
        history_messages.append({"role": "assistant", "content": ""})

        response_message = ""
        try:
            print("This history: ",history_messages)
            history_messages_final = data_chatbot_vngpt + history_messages[-2:]
            if len(history_messages) == 2:
                history_messages_process = history_messages
            else:
                history_messages_process = history_messages_final
            chat_generator = LLM.client.create(
                messages=history_messages_process, stream=True, model=model_name
            )
            # print("chat_generator", chat_generator)
            for chunk in chat_generator:
                if "choices" in chunk:
                    for choice in chunk["choices"]:
                        if "delta" in choice and "content" in choice["delta"]:
                            new_token = choice["delta"]["content"]
                            # Add the latest token:
                            response_message += new_token
                            # Update the assistant's response in our model:
                            history_messages[-1]["content"] = response_message

                        if "finish_reason" in choice and choice["finish_reason"] == "stop":
                            break
                formatted_history = create_formatted_history_docs(history_messages)
                yield formatted_history, history_messages, gr.update(value=f"""<i style="color:#3ADF00"><center>Số token của câu hỏi: {num_tokens_from_messages_docs(history_messages_final)+max_response_tokens}</center></i>""", visible=True)
        except:
            formatted_history = create_formatted_history_docs(state)
            yield formatted_history, state, gr.update(value="""<i style="color:red"><center>Có lỗi xảy ra. Có thể do tài khoản của bạn hoặc kết nối mạng.</center></i>""", visible=True)
            pass

def clear_history_docs(state):
    return None