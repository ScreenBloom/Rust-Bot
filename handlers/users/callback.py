from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from handlers.users import misc as ms
from loader import dp
from keyboards import ik,kb
from aiogram.dispatcher import FSMContext
from data import config as cfg
from utils.db_api import database as db
from states import st
from handlers.users import lt

@dp.callback_query_handler(state="*")
async def main(call: types.CallbackQuery, state: FSMContext):
    params = call.data.split("-")
    match params[0]:
        case "off_state":
            await call.message.delete()
            await state.finish()
            await call.message.answer("✅Действие отменено")
        case "send":
            await call.message.delete()
            message_id = int(params[1])
            data = await state.get_data()
            await state.finish()
            if len(data) != 0:
                name = data['name']
                url = data['url']
            else:
                name = "0"
                url = "0"
            from_chat_id = call.from_user.id
            await call.message.answer("Рассылка запущена")
            await ms.sender(message_id, from_chat_id, name, url)

        case 'add_button_to_send':
            message_id = int(params[1])
            await call.message.answer("Введите ссылку кнопки", reply_markup=ik.off_state)
            await st.UserState.add_btn_url.set()
            await state.update_data(message_id=message_id)

        case "chat_manage":
            chat_id = int(call.data.split("*")[1])
            match params[1]:
                case 'add_channel':
                    await call.message.delete()
                    await call.message.answer("Введите ID канала", reply_markup=ik.off_state)
                    await st.Add_Channel.c_id.set()
                case 'show':
                    await call.message.delete()
                    await call.message.answer(lt.adv_chat_stat(chat_id), reply_markup=ik.admin_delete_adv_chat(chat_id))
                case 'delete':
                    db.delete_adv_chat(chat_id)
                    await call.message.delete()
                    await call.message.answer("✅Чат удален")
        case "im_subscribed":
            sub_status = await ms.check_subscribes(call.from_user.id)
            if sub_status:
                await call.message.edit_text("Спасибо за поддержку нашего бота.\n"
                                             "<b>Благодаря Вам он остаётся полностью бесплатным.</b>\n")
            else:
                await call.answer("☹️Вы не подписаны на один из каналов")