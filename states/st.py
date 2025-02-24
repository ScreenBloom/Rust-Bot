from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext
from loader import dp,bot
from handlers.users import gpt
from keyboards import ik,kb
from utils.db_api import database as db
import os

class UserState(StatesGroup):
    calculate = State()
    sender = State()
    name = State()
    chat = State()
    add_btn_url = State()
    add_btn_name = State()
    delete_users = State()

class Add_Channel(StatesGroup):
    c_id = State()
    c_name = State()
    c_url = State()


@dp.message_handler(commands=['close'],state="*")
async def close(message:types.Message,state: FSMContext):
    await state.finish()
    await message.answer("❌Чат закрыт!\nЧтобы возобновить общение с ботом, воспользуйтесь клавиатурой ниже.💠",reply_markup=kb.menu)

@dp.message_handler(state=UserState.calculate,content_types=[types.ContentType.TEXT,types.ContentType.VOICE])
async def main(message: types.Message, state: FSMContext):
    try:
        msg = await message.answer("🪄")
        prompt = message.text.replace("\"", "")
        bot_response = await gpt.question_answer(prompt)
        await msg.delete()
        await message.answer(bot_response)
    except Exception as e:
        pass
        print(e)

@dp.message_handler(state=UserState.sender,content_types=types.ContentType.ANY)
async def main(message: types.Message,state: FSMContext):
    msg_id = message.message_id
    await bot.copy_message(chat_id=message.from_user.id,from_chat_id=message.from_user.id,
                           message_id=msg_id)
    await message.answer("Рассылаем?",reply_markup=ik.send(msg_id))
    await state.finish()

@dp.message_handler(state=UserState.add_btn_url)
async def main(message: types.Message,state: FSMContext):
    url = message.text
    await state.update_data(url=url)
    await message.answer("Введите надпись на кнопке")
    await UserState.add_btn_name.set()

@dp.message_handler(state=UserState.add_btn_name)
async def main(message: types.Message,state: FSMContext):
    name = message.text
    await state.update_data(name=name)
    data = await state.get_data()
    mrkp = ik.create_sender_mrkp(name,data['url'])
    message_to_send = await bot.copy_message(chat_id=message.from_user.id, from_chat_id=message.from_user.id,
                           message_id=data['message_id'],reply_markup=mrkp)
    await message.answer('Рассылаем?',reply_markup=ik.send(message_to_send.message_id))


@dp.message_handler(state=Add_Channel.c_id)
async def main(message: types.Message,state: FSMContext):
    try:
        await state.update_data(id=int(message.text))
        await message.answer("Введите имя канала",reply_markup=ik.off_state)
        await Add_Channel.c_name.set()
    except:
        await message.answer("❌Введите число",reply_markup=ik.off_state)

@dp.message_handler(state=Add_Channel.c_name)
async def main(message: types.Message,state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введите ссылку на вступление",reply_markup=ik.off_state)
    await Add_Channel.c_url.set()

@dp.message_handler(state=Add_Channel.c_url)
async def main(message: types.Message,state: FSMContext):
    data = await state.get_data()
    await state.finish()
    url = message.text
    db.create_adv_chat(data['id'],url,data['name'])
    await message.answer("✅Ваш канал успешно создан")


@dp.message_handler(state=UserState.delete_users,content_types=types.ContentType.DOCUMENT)
async def main(message: types.Message,state: FSMContext):
    await state.finish()
    file_path = (await message.document.get_file())['file_path']
    await message.document.download()
    file = open(file_path,'r')
    msg = await message.answer("⏳")
    s = list(map(int, (file.read().split("\n"))[0:-1]))
    await msg.delete()
    file.close()
    db.delete_users_for_ids(s)
    os.remove(file_path)
    await message.answer("✅Мертвые пользователи удалены")