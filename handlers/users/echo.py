from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards import ik,kb
from loader import dp
from utils.db_api import database as db
from states import st
from data import config as cfg
from handlers.users import lt
from handlers.users import misc as ms
from data import text as txt


@dp.message_handler(state=None)
async def bot_echo(message: types.Message):
    if str(message.from_user.id) in cfg.ADMINS:
        match message.text:
            case "Админ":
                await message.answer("Админ меню:",reply_markup=kb.admin)
            case "📊Статистика":
                await message.answer(lt.admin_stat(),reply_markup=kb.admin)
            case "💬Рассылка":
                await message.answer("Пришлите мне сообщение, которое будет разослано пользователям")
                await st.UserState.sender.set()
                return
            case "🔃Выгрузить дб":
                document = ms.get_ids_files()
                await message.answer_document(document=document,
                                              caption="Файл с ID пользователей")
                return
            case "👥ОП":
                await message.answer("<b>Ваши каналы:</b>", reply_markup=ik.admin_adv_chats())
                return
            case "🗑Удалить мертвых":
                await message.answer('Пришлите .txt файл с ID пользователей, которых нужно удалить из дб',
                                     reply_markup=ik.off_state)
                await st.UserState.delete_users.set()
    sub_status = await ms.check_subscribes(message.from_user.id)
    if sub_status:
        match message.text:
            case "🧮Расчитать":
                await message.answer("<b>Задайте свой вопрос и бот вам поможет рассчитать сколько нужно взрывчатки.</b>\n\n"
                                     "Вам вопрос может звучать так: <u>Cколько нужно сачелей на рейд железной стены?</u>\n\n"
                                     "Чтобы закончить диалог с ботом воспользуйтесь командой /close.")
                await st.UserState.calculate.set()
            case "💡Информация":
                await message.answer(txt.info,reply_markup=kb.menu)
    else:
        await message.answer("Подпишитесь на каналы ниже, чтобы дальше использовать бота.\n"
                         "<b>Это нужно, для того, чтобы бот оставался бесплатным</b>",
                         reply_markup=ik.adv_chats())