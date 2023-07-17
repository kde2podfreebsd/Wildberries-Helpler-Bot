from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def news_keyboard(position):
    next = InlineKeyboardButton(text="След →", callback_data="not_working")
    back = InlineKeyboardButton(text="← Пред ", callback_data="not_working")
    keyboard = InlineKeyboardMarkup(row_width=1)
    if position == 'first':
        keyboard.insert(next)
    elif position == 'middle':
        keyboard = InlineKeyboardMarkup(row_width=1, inline_keyboard=[[back, next]])
    else:
        keyboard.insert(back)
    return keyboard
