from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    HumanMessage, SystemMessage
)
from langchain.callbacks.base import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from lib_app.utils import *
# print(resp.content + main_text)
SECRET_KEY = os.environ['SECRET_KEY']

def summary_long_text(text, api_key, max_tokens, language_summary, n=500):
    openai_key = encode("decode", api_key, SECRET_KEY)
    chat = ChatOpenAI(streaming=True, callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]), verbose=True, max_tokens=2048, temperature=0.7, openai_api_key=openai_key)
    words = text.split()
    result = []
    current_chunk = ''
    for word in words:
        current_chunk += word + ' '
        if len(current_chunk.split()) >= n:
            result.append(current_chunk.strip())
            current_chunk = ''
    if current_chunk:
        last_chunk = result[-1] + ' ' + current_chunk.strip()
        result[-1] = last_chunk
    new_paragraph = ''
    total_parts = len(result)*2
    max_words = int(round(max_tokens / total_parts))
    print(max_words)
    for x in result:
        resp = chat([HumanMessage(content=f"Summarize text below into {language_summary} with maximum {1024 / max_words} words: {x}"
)])
        new_paragraph += ''.join(resp.content) + ' '
    yield new_paragraph