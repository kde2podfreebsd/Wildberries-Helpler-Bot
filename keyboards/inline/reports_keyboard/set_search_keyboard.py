from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import set_report_callback, order_or_returns_callback


def from_report_dynamic_keyboard(seller_id, command_name, period, end, start):
    back_keyboard = InlineKeyboardMarkup(row_width=1)
    back_button = InlineKeyboardButton(text="⬅️ Назад",
                                       callback_data=set_report_callback.new(method=period,
                                                                             command_name=command_name,
                                                                             seller_id=seller_id,
                                                                             start=start,
                                                                             end=end
                                                                             ))
    back_keyboard.insert(back_button)
    return back_keyboard


def from_report_orders_keyboard(seller_id, command_name, method, end, start):
    back_keyboard = InlineKeyboardMarkup(row_width=1)
    back_button = InlineKeyboardButton(text="⬅️ Назад",
                                       callback_data=order_or_returns_callback.new(method=method,
                                                                             command_name=command_name,
                                                                             seller_id=seller_id,
                                                                             start=start,
                                                                             end=end
                                                                             ))
    back_keyboard.insert(back_button)
    return back_keyboard
