import os
import openai
from dotenv import load_dotenv
load_dotenv('./.env')
import requests
import json
# new code get response openai
from typing import List, Tuple, Dict, Generator
from langchain.llms import OpenAI
import gradio as gr
import requests

#if you have OpenAI API key as an environment variable, enable the below
#openai.api_key = os.getenv("OPENAI_API_KEY")

#if you have OpenAI API key as a string, enable the below
OPEN_API_KEY = os.environ['OPEN_API_KEY']


model_name = "gpt-3.5-turbo"

def create_history_messages(history: List[Tuple[str, str]]) -> List[dict]:
    history_messages = [{"role": "user", "content": m[0]} for m in history]
    history_messages.extend([{"role": "assistant", "content": m[1]} for m in history])
    return history_messages

def create_formatted_history(history_messages: List[dict]) -> List[Tuple[str, str]]:
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

def chat(
    message: str, state: List[Dict[str, str]], temperature: float, api_key: str
) -> Generator[Tuple[List[Tuple[str, str]], List[Dict[str, str]]], None, None]:
    LLM = OpenAI(model_name=model_name, temperature=temperature, openai_api_key=api_key)
    history_messages = state
    if history_messages == None:
        history_messages = []
        history_messages.append({"role": "system", "content": "A helpful assistant."})

    history_messages.append({"role": "user", "content": message})
    # We have no content for the assistant's response yet but we will update this:
    history_messages.append({"role": "assistant", "content": ""})

    response_message = ""

    chat_generator = LLM.client.create(
        messages=history_messages, stream=True, model=model_name
    )
    print("State 1: ",state)
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
        formatted_history = create_formatted_history(history_messages)
        yield formatted_history, history_messages


def clear_history(state):
    return None