from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data.config import SUPPORT_LINK
from keyboards.inline.callback_datas import set_command_seller_id

fail_add_seller_keyboard = InlineKeyboardMarkup(row_width=2,
                                                inline_keyboard=[
                                                    [

                                                        InlineKeyboardButton(text="⬅️ Назад",
                                                                             callback_data="back_to_settings"),

                                                        InlineKeyboardButton(text="👨🏻‍💻 Поддержка", url=SUPPORT_LINK)

                                                    ],
                                                ])


def seller_added_keyboard(seller_id):
    keyboard = InlineKeyboardMarkup(row_width=1)
    add_fbs_button = InlineKeyboardButton(text="🔑 Подключить FBS API-ключ",
                                          callback_data=set_command_seller_id.new(command_name="change_api_fbs",
                                                                                  seller_id=seller_id))
    back_button = InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_settings")
    keyboard.insert(add_fbs_button)
    keyboard.insert(back_button)
    return keyboard


def delete_seller_keyboard(seller_id):
    seller_delete_keyboard = InlineKeyboardMarkup(row_width=2,
                                                  inline_keyboard=[
                                                      [

                                                          InlineKeyboardButton(text="⬅️ Назад",
                                                                               callback_data=set_command_seller_id.new(
                                                                                   command_name="back_to_seller_setting",
                                                                                   seller_id=seller_id))
                                                          , InlineKeyboardButton(text="❌ Удалить",
                                                                                 callback_data=set_command_seller_id.new(
                                                                                     command_name="delete_seller_confirm",
                                                                                     seller_id=seller_id))

                                                      ],

                                                  ])
    return seller_delete_keyboard


def rename_seller_keyboard(seller_id):
    seller_delete_keyboard = InlineKeyboardMarkup(row_width=2,
                                                  inline_keyboard=[
                                                      [

                                                          InlineKeyboardButton(text="⬅️ Назад",
                                                                               callback_data=set_command_seller_id.new(
                                                                                   command_name="back_to_seller_setting",
                                                                                   seller_id=seller_id))
                                                      ],

                                                  ])
    return seller_delete_keyboard