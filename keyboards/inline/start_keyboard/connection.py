from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

connection_keyboard = InlineKeyboardMarkup(row_width=1)

about_api = InlineKeyboardButton(text="👨🏻‍🎓 Подробнее про API", callback_data="about_api")
back_to_start = InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_start")
back_to_connection_button = InlineKeyboardButton(text="⬅️ Назад", callback_data="back_connection")

connection_keyboard.insert(about_api)
connection_keyboard.insert(back_to_start)

back_to_connection = InlineKeyboardMarkup(row_width=1)
back_to_connection.insert(back_to_connection_button)
