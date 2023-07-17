from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(text="Котлетки"),
        ],
        [
            KeyboardButton(text="Макарошки"),
            KeyboardButton(text="Пюрешка"),

        ],
    ],

    resize_keyboard=True
)