from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    HumanMessage, SystemMessage
)
from langchain.callbacks.base import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from lib_app.utils import *
# print(resp.content + main_text)
SECRET_KEY = os.environ['SECRET_KEY']

def summary_long_text(text, api_key, max_tokens, language_summary, prompts_summary, custom_prompts_summary, n=500):
    if language_summary == 'Tiếng Việt':
        language_summary = 'Vietnamese'
    else:
        language_summary = 'English'
    openai_key = encode("decode", api_key, SECRET_KEY)
    chat = ChatOpenAI(streaming=True, callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]), verbose=True, max_tokens=2048, temperature=0.7, openai_api_key=openai_key)
    words = text.split()
    num_words = len(words)
    if num_words > 500:
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
            prompt = ""
            if prompts_summary == 'Tùy chỉnh prompt':
                prompt = f"Summarize text below into {language_summary} with maximum {1024 / max_words} words and {custom_prompts_summary}: {x}"
            elif prompts_summary == 'Rút gọn văn bản bằng ngôn ngữ chọn và xuống gần với giá trị max_tokens':
                prompt = f"Summarize text below into {language_summary} with maximum {1024 / max_words} words: {x}"
            else:
                prompt = f"Summarize text below into {language_summary} with maximum {1024 / max_words} words: {x}"
            resp = chat([HumanMessage(content=prompt)])
            new_paragraph += ''.join(resp.content) + ' '
        yield new_paragraph
    else:
        prompt = ""
        if prompts_summary == 'Tùy chỉnh prompt':
            prompt = f"Summarize text below into {language_summary} with maximum {max_tokens} words and {custom_prompts_summary}: {text}"
        elif prompts_summary == 'Rút gọn văn bản bằng ngôn ngữ chọn và xuống gần với giá trị max_tokens':
            prompt = f"Summarize text below into {language_summary} with maximum {max_tokens} words: {text}"
        else:
            prompt = f"Summarize text below into {language_summary} with maximum {max_tokens} words: {text}"
        resp = chat([HumanMessage(content=prompt)])
        new_paragraph = ''
        new_paragraph += ''.join(resp.content) + ' '
        yield new_paragraph