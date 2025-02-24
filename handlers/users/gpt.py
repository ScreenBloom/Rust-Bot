import random
import openai
from data import config as cfg

openai.api_key = random.choice(cfg.tokens)


async def question_answer(prompt):
    message = {
        'role': 'user',
        'content': f"{read_text_from_file()} + {prompt}",
    }
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[message]
    )
    chatbot_response = response.choices[0].message['content']
    return chatbot_response


def read_text_from_file():
    with open('table.txt', 'r', encoding='utf-8') as file:
        file_text = file.read()
        return file_text







