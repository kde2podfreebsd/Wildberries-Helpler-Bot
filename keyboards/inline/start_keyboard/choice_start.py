from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data.config import SUPPORT_LINK

start_keyboard = InlineKeyboardMarkup(row_width=1)

start_support_link = InlineKeyboardButton(text="👨🏻‍💻 Поддержка", url=SUPPORT_LINK)
# connection_button = InlineKeyboardButton(text="🏠 Перейти в меню", callback_data="free_connection")

start_keyboard.insert(start_support_link)
# start_keyboard.insert(connection_button)
