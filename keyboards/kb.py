from aiogram.types import ReplyKeyboardMarkup,KeyboardButton

menu = ReplyKeyboardMarkup(row_width=1,resize_keyboard=True).add(
    KeyboardButton("🧮Расчитать"),
    KeyboardButton("💡Информация"))



admin = ReplyKeyboardMarkup(row_width=2,resize_keyboard=True).add(
    KeyboardButton("📊Статистика"),
    KeyboardButton("💬Рассылка"),
    KeyboardButton("🔃Выгрузить дб")).add(
    KeyboardButton("👥ОП"),
    KeyboardButton("🗑Удалить мертвых"))
