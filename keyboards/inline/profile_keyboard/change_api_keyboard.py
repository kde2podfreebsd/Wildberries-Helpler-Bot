from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data.config import SUPPORT_LINK
from keyboards.inline.callback_datas import set_command_seller_id, change_api_callback


def change_api_keyboard(version_api, seller_id):
    change_api_keyboard = InlineKeyboardMarkup(row_width=1)
    replace_api = InlineKeyboardButton(text=f"🔄 Заменить API-ключ ({version_api})",
                                       callback_data=change_api_callback.new(version_api=version_api,
                                                                             method="change_api",
                                                                             seller_id=seller_id))
    back_to_seller_button = InlineKeyboardButton(text="⬅️ Назад", callback_data=set_command_seller_id.new(
        command_name="back_to_seller_setting", seller_id=seller_id))
    change_api_keyboard.insert(replace_api)
    change_api_keyboard.insert(back_to_seller_button)
    return change_api_keyboard


change_api_insert_keyboard = InlineKeyboardMarkup(row_width=2,
                                                  inline_keyboard=[
                                                      [

                                                          InlineKeyboardButton(text="⬅️ Назад",
                                                                               callback_data="back_to_change_api_x64"),

                                                          InlineKeyboardButton(text="👨🏻‍💻 Поддержка",
                                                                               url=SUPPORT_LINK)

                                                      ],
                                                  ])


def add_fbs_api(seller_id):
    keyboard = InlineKeyboardMarkup(row_width=1)
    back_to_seller_button = InlineKeyboardButton(text="⬅️ Назад", callback_data=set_command_seller_id.new(
        command_name="back_to_seller_setting", seller_id=seller_id))
    keyboard.insert(back_to_seller_button)
    return keyboard


def back_crate_fbs(seller_id):
    keyboard = InlineKeyboardMarkup(row_width=1)
    back_to_seller_button = InlineKeyboardButton(text="⬅️ Назад", callback_data=set_command_seller_id.new(
        command_name="change_api_fbs", seller_id=seller_id))
    support_button = InlineKeyboardButton(text="👨🏻‍💻 Поддержка", url=SUPPORT_LINK)
    keyboard.insert(back_to_seller_button)
    keyboard.insert(support_button)
    return keyboard
