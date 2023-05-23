from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import set_paid


def paid_keyboard_complete(url):
    paid_keyboard = InlineKeyboardMarkup(row_width=2,
                                         inline_keyboard=[
                                             [
                                                 InlineKeyboardButton(
                                                     text="Перейти к оплате по ссылке",
                                                     url=url

                                                 ),

                                             ],
                                             [
                                                 InlineKeyboardButton(
                                                     text="✅ Проверить пополнение ✅",
                                                     callback_data=set_paid.new(text_name="paid")

                                                 ),

                                             ],
                                             [
                                                 InlineKeyboardButton(
                                                     text="❌ Отменить пополнение ❌",
                                                     callback_data="back_to_profile"

                                                 ),

                                             ]

                                         ]
                                         )
    return paid_keyboard
