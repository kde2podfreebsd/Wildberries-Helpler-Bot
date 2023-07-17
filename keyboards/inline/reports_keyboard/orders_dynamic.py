from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import set_command_seller_id, order_or_returns_callback, set_search_callback
from keyboards.inline.reports_keyboard.tools import button_name_by_order


def report_dynamic_order_keyboard(seller_id, command_name, method, end, start, is_search, next=None, back=None):
    keyboard = InlineKeyboardMarkup(row_width=2)
    back_button = InlineKeyboardButton(text="← Пред", callback_data=order_or_returns_callback.new(method=method,
                                                                                                  command_name=command_name,
                                                                                                  seller_id=seller_id,
                                                                                                  start=start - 20,
                                                                                                  end=end - 20
                                                                                                  ))
    next_button = InlineKeyboardButton(text="След →", callback_data=order_or_returns_callback.new(method=method,
                                                                                                  command_name=command_name,
                                                                                                  seller_id=seller_id,
                                                                                                  start=start,
                                                                                                  end=end
                                                                                                  ))
    if next and back:
        keyboard.row(back_button, next_button)
    elif next and back is False:
        keyboard.insert(next_button)
    elif back and next is False:
        keyboard.insert(back_button)
    days, week, month, no_grouping = button_name_by_order(command_name)
    days_button = InlineKeyboardButton(text=days, callback_data=order_or_returns_callback.new(method=method,
                                                                                              command_name="by_days",
                                                                                              seller_id=seller_id,
                                                                                              start=0,
                                                                                              end=9
                                                                                              ))
    month_button = InlineKeyboardButton(text=month, callback_data=order_or_returns_callback.new(method=method,
                                                                                                command_name="by_month",
                                                                                                seller_id=seller_id,
                                                                                                start=0,
                                                                                                end=9
                                                                                                ))
    no_grouping_button = InlineKeyboardButton(text=no_grouping,
                                              callback_data=order_or_returns_callback.new(method=method,
                                                                                          command_name="no_grouping",
                                                                                          seller_id=seller_id,
                                                                                          start=0,
                                                                                          end=9
                                                                                          ))

    keyboard.row(days_button)
    keyboard.row(month_button, no_grouping_button)
    back_button = InlineKeyboardButton(text="⬅️ Назад",
                                       callback_data=set_command_seller_id.new(command_name="report_by_seller",
                                                                               seller_id=seller_id))
    if is_search is True:
        search_button = InlineKeyboardButton(text="❌ Поиск отмена", callback_data=set_search_callback.new(method=method,
                                                                                                          command_name=command_name,
                                                                                                          seller_id=seller_id,
                                                                                                          start=0,
                                                                                                          end=9,
                                                                                                          from_keyboard="delete_search"))
    else:
        search_button = InlineKeyboardButton(text="🔍 Поиск", callback_data=set_search_callback.new(method=method,
                                                                                                    command_name=command_name,
                                                                                                    seller_id=seller_id,
                                                                                                    start=0,
                                                                                                    end=9,
                                                                                                    from_keyboard="report_orders"
                                                                                                    ))
    keyboard.row(back_button, search_button)
    return keyboard
