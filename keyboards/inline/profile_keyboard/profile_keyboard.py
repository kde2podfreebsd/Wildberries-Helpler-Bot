from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data.config import SUPPORT_LINK

# about_keyboard = InlineKeyboardMarkup(row_width=2)
#
# settings = InlineKeyboardButton(text="⚙️ Настройки", callback_data="settings")
# support_link = InlineKeyboardButton(text="👨🏻‍💻 Поддержка", url=SUPPORT_LINK)
# balance = InlineKeyboardButton(text="💰 Баланс", callback_data="balance")
#
# about_keyboard.insert([settings, support_link])
# about_keyboard.insert(balance)
from keyboards.inline.callback_datas import set_command_seller_id

about_keyboard = InlineKeyboardMarkup(row_width=2,
                                      inline_keyboard=[
                                          [
                                              InlineKeyboardButton(text="⚙️ Настройки", callback_data="settings"),
                                              InlineKeyboardButton(text="👨🏻‍💻 Поддержка", url=SUPPORT_LINK)
                                          ],
                                          [
                                              InlineKeyboardButton(text="💰 Баланс", callback_data="balance_and_paid")
                                          ]
                                      ])


def settings_keyboard(sellers: list):
    settings_keyboard = InlineKeyboardMarkup(row_width=1)
    for seller in sellers:
        if seller.bot_enable:
            seller_name = seller.name
        else:
            seller_name = f"⭕️ {seller.name}"
        settings_keyboard.insert(
            InlineKeyboardButton(text=seller_name,
                                 callback_data=set_command_seller_id.new(command_name="seller", seller_id=seller.id))
        )
    add_seller_button = InlineKeyboardButton(text="➕ Добавить продавца", callback_data="add_seller")
    back_to_settings = InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_profile")
    settings_keyboard.insert(add_seller_button)
    settings_keyboard.insert(back_to_settings)
    return settings_keyboard


back_to_add_seller = InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_settings")
support_button = InlineKeyboardButton(text="👨🏻‍💻 Поддержка", url=SUPPORT_LINK)
add_seller_keyboard = InlineKeyboardMarkup(row_width=1, inline_keyboard=[[back_to_add_seller, support_button]])
