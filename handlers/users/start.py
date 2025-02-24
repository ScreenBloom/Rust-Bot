from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from keyboards import kb
from loader import dp
from data import config as cfg
from utils.db_api import database as db


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    db.create_user(message.from_user.id,message.from_user.username)
    await message.answer_photo(photo=cfg.photo_start,
                 caption=f"<b>Привет, уважаемый игрок</b> <u>{message.from_user.full_name}</u>🛠️🔥!\n\n"
                         f"Позвольте мне помочь вам рассчитать необходимое количество серы для успешного рейда!\n\n"
                         f"С помощью этого бота вы точно узнаете, сколько серы нужно на вашего соседа! 😉✨",reply_markup=kb.menu)
