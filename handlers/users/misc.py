import random
from data.config import tokens
from datetime import datetime
from loader import bot
from data import config as cfg
from utils.db_api import database as db
import asyncio
from keyboards import ik,kb
import random
from aiogram import types
import time
def get_count_of_user(days,user_datas):
    counter = 0
    for data in user_datas:
        date = datetime.strptime(data['date'], "%Y-%m-%d %H:%M:%S")
        if (datetime.now() - date).days < days:
            counter+=1
    return counter

def get_random_token():
    print(len(tokens))
    rnd = random.randint(0,len(tokens)-1)
    return tokens[rnd]

async def sender(message_id,from_chat_id,name,url):
    if name == "0" or url == "0":
        ids = db.get_user_ids()
        i = 0
        for user_id in ids:
            try:
                await bot.copy_message(chat_id=user_id, from_chat_id=from_chat_id,
                                       message_id=message_id)
                i+=1
            except:
                pass
            await asyncio.sleep(0.2)
        await bot.send_message(chat_id=from_chat_id,text=f"Рассылка дошла до {i} пользователей")
    else:
        ids = db.get_user_ids()
        i = 0
        for user_id in ids:
            try:
                await bot.copy_message(chat_id=user_id, from_chat_id=from_chat_id,
                                       message_id=message_id,reply_markup=ik.create_sender_mrkp(name,url))
                i += 1
            except:
                pass
            await asyncio.sleep(0.2)
        await bot.send_message(chat_id=from_chat_id, text=f"Рассылка дошла до {i} пользователей")


async def check_subscribes(user_id):
    datas = db.get_all_adv_chats()
    for data in datas:
        user_channel_status = await bot.get_chat_member(chat_id=data['id'], user_id=user_id)
        if user_channel_status["status"] == 'left':
            return False
    db.plus_user_count_to_all()
    return True



def get_ids_files():
    ids = db.get_user_ids()
    text = ""
    file = open("db_ids.txt",'w')
    for id in ids:
        text+=f"{id}\n"
    file.write(text)
    file.close()
    return open("db_ids.txt",'rb')