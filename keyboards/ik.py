from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup
from utils.db_api import database as db

def send(message_id):
    return InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton(text="💬Разослать",callback_data=f'send-{message_id}'),
        InlineKeyboardButton(text="➕Добавить кнопку",callback_data=f'add_button_to_send-{message_id}'),
        InlineKeyboardButton(text="❌Отмена", callback_data='off_state')
    )


def create_sender_mrkp(name,url):
    return InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton(text=name,url=url)
    )

off_state = InlineKeyboardMarkup().add(InlineKeyboardButton(text="❌Отмена",callback_data='off_state'))


def admin_delete_adv_chat(chat_id):
    return InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton(text='🪣Удалить чат',callback_data=f'chat_manage-delete-*{chat_id}')
    )


def admin_adv_chats():
    datas = db.get_all_adv_chats()
    mrkp = InlineKeyboardMarkup(row_width=1)
    for data in datas:
        mrkp.add(
            InlineKeyboardButton(text=data['name'],callback_data=f'chat_manage-show-*{data["id"]}')
        )
    mrkp.add(
        InlineKeyboardButton(text="➕Добавить канал",callback_data='chat_manage-add_channel-*0')
    )
    return mrkp

def adv_chats():
    mrkp = InlineKeyboardMarkup(row_width=1)
    datas = db.get_all_adv_chats()
    for data in datas:
        mrkp.add(
            InlineKeyboardButton(text=data['name'],url=data['url'])
        )
    mrkp.add(
        InlineKeyboardButton(text="✅Я подписался",callback_data=f'im_subscribed')
    )
    return mrkp