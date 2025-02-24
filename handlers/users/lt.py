from utils.db_api import database as db
from handlers.users import misc as ms
from loader import bot
from data import config as cfg



def admin_stat():
    users = db.get_all_users()
    u_lst = []
    b_lst = []
    for i in [1, 7, 30]:
        u_lst.append(ms.get_count_of_user(i, users))
    text = "<b>📊Статистика</b>\n\n" \
           f"<b>👥Пользователей в боте:</b> {len(users)}\n" \
           f"<b>👤Пользователей за 1 день:</b> {u_lst[0]}\n" \
           f"<b>👤Пользователей за 7 дней:</b> {u_lst[1]}\n" \
           f"<b>👤Пользователей за 30 дней:</b> {u_lst[2]}\n\n"
    return text


def adv_chat_stat(chat_id):
    data = db.get_adv_chat(chat_id)
    return f"Канал: <b>{data['name']}</b>\n" \
           f"ID: <code>{data['id']}</code>\n\n" \
           f"Привидено пользователей: <b>{data['user_count']}</b>"