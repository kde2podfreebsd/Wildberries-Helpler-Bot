from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import set_report_callback, set_command_seller_id, order_or_returns_callback, \
    set_another_period_callback


def reports_keyboard(seller_id, filter_bought, filter_orders, back=None):
    keyboard = InlineKeyboardMarkup(row_width=2)
    if filter_bought is None:
        filter_bought = "subject"

    if filter_orders is None:
        filter_orders = "no_grouping"
    today_button = InlineKeyboardButton(text="Сегодня", callback_data=set_report_callback.new(method="today",
                                                                                              command_name=filter_bought,
                                                                                              seller_id=seller_id,
                                                                                              start=0,
                                                                                              end=9
                                                                                              ))
    yesterday_button = InlineKeyboardButton(text="Вчера", callback_data=set_report_callback.new(method="yesterday",
                                                                                                command_name=filter_bought,
                                                                                                seller_id=seller_id,
                                                                                                start=0,
                                                                                                end=9
                                                                                                ))
    in_7_days_button = InlineKeyboardButton(text="7 дней", callback_data=set_report_callback.new(method="in_7_days",
                                                                                                 command_name=filter_bought,
                                                                                                 seller_id=seller_id,
                                                                                                 start=0,
                                                                                                 end=9
                                                                                                 ))
    in_30_days_button = InlineKeyboardButton(text="30 дней", callback_data=set_report_callback.new(method="in_30_days",
                                                                                                   command_name=filter_bought,
                                                                                                   seller_id=seller_id,
                                                                                                   start=0,
                                                                                                   end=9
                                                                                                   ))
    another_period_button = InlineKeyboardButton(text="Другой период",
                                                 callback_data=set_another_period_callback.new(method="in_30_days",
                                                                                               command_name=filter_bought,
                                                                                               seller_id=seller_id,
                                                                                               start=0,
                                                                                               end=9,
                                                                                               filter="another_period"
                                                                                               ))
    sales_button = InlineKeyboardButton(text="💳 Выкупы", callback_data=order_or_returns_callback.new(method="sales",
                                                                                                      command_name=filter_orders,
                                                                                                      seller_id=seller_id,
                                                                                                      start=0,
                                                                                                      end=9
                                                                                                      ))
    returns_button = InlineKeyboardButton(text="🚚 Возвраты",
                                            callback_data=order_or_returns_callback.new(method="returns",
                                                                                      command_name=filter_orders,
                                                                                      seller_id=seller_id,
                                                                                      start=0,
                                                                                      end=9
                                                                                      ))
    orders_button = InlineKeyboardButton(text="🛒 Заказы",
                                         callback_data=order_or_returns_callback.new(method="orders",
                                                                                     command_name=filter_orders,
                                                                                     seller_id=seller_id,
                                                                                     start=0,
                                                                                     end=9
                                                                                     ))
    keyboard.row(today_button, yesterday_button)
    keyboard.row(in_7_days_button, in_30_days_button)
    keyboard.insert(another_period_button)
    keyboard.row(sales_button, returns_button)
    keyboard.row(orders_button)
    if back:
        back_buttons = InlineKeyboardButton(text="⬅️ Назад",
                                            callback_data=f"back_to_report_by_seller")
        keyboard.insert(back_buttons)

    return keyboard


def report_by_seller_keyboard(sellers: list):
    keyboard = InlineKeyboardMarkup(row_width=1)
    for seller in sellers:
        keyboard.insert(
            InlineKeyboardButton(text=seller.name,
                                 callback_data=set_command_seller_id.new(command_name="report_by_seller",
                                                                         seller_id=seller.id))
        )

    return keyboard


def back_to_reports(seller_id):
    keyboard = InlineKeyboardMarkup(row_width=1)
    back_button = InlineKeyboardButton(text="⬅️ Назад",
                                       callback_data=set_command_seller_id.new(command_name="report_by_seller",
                                                                               seller_id=seller_id))
    keyboard.insert(back_button)
    return keyboard
