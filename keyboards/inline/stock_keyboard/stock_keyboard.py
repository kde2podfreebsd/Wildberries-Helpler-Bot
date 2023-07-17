from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import set_command_seller_id, order_or_returns_callback


def show_info_stock(seller_id, filter_stocks, back=None):
    keyboard = InlineKeyboardMarkup(row_width=1)
    if filter_stocks is None:
        filter_stocks = "in_stock"
    my_products_button = InlineKeyboardButton(text="📦 Мои товары",
                                              callback_data=order_or_returns_callback.new(method="stocks",
                                                                                          command_name=filter_stocks,
                                                                                          seller_id=seller_id,
                                                                                          start=0,
                                                                                          end=9
                                                                                          ))
    back_button = InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_stocks_by_seller")

    keyboard.insert(my_products_button)
    if back is True:
        keyboard.insert(back_button)

    return keyboard


def stocks_by_seller_keyboard(sellers: list):
    keyboard = InlineKeyboardMarkup(row_width=1)
    for seller in sellers:
        keyboard.insert(
            InlineKeyboardButton(text=seller.name,
                                 callback_data=set_command_seller_id.new(command_name="stocks_by_seller",
                                                                         seller_id=seller.id))
        )

    return keyboard
