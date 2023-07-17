from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import set_command_seller_id, order_or_returns_callback, set_search_callback
from keyboards.inline.stock_keyboard.tools import button_name_by_stock


def stock_dynamic_keyboard(seller_id, command_name, method, end, start, is_search, next=None, back=None):
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
    in_stock, to_client, from_client, on_sale, reverse_in_stock, \
    revers_to_client, revers_from_client, revers_on_sale = button_name_by_stock(command_name)
    in_stock_button = InlineKeyboardButton(text=in_stock, callback_data=order_or_returns_callback.new(method=method,
                                                                                                      command_name="in_stock",
                                                                                                      seller_id=seller_id,
                                                                                                      start=0,
                                                                                                      end=9
                                                                                                      ))
    reverse_in_stock_button = InlineKeyboardButton(text=reverse_in_stock,
                                                   callback_data=order_or_returns_callback.new(method=method,
                                                                                               command_name="reverse_in_stock",
                                                                                               seller_id=seller_id,
                                                                                               start=0,
                                                                                               end=9
                                                                                               ))
    to_client_button = InlineKeyboardButton(text=to_client, callback_data=order_or_returns_callback.new(method=method,
                                                                                                        command_name="to_client",
                                                                                                        seller_id=seller_id,
                                                                                                        start=0,
                                                                                                        end=9
                                                                                                        ))
    revers_to_client_button = InlineKeyboardButton(text=revers_to_client,
                                                   callback_data=order_or_returns_callback.new(method=method,
                                                                                               command_name="revers_to_client",
                                                                                               seller_id=seller_id,
                                                                                               start=0,
                                                                                               end=9
                                                                                               ))
    from_client_button = InlineKeyboardButton(text=from_client,
                                              callback_data=order_or_returns_callback.new(method=method,
                                                                                          command_name="from_client",
                                                                                          seller_id=seller_id,
                                                                                          start=0,
                                                                                          end=9
                                                                                          ))
    revers_from_client_button = InlineKeyboardButton(text=revers_from_client,
                                                     callback_data=order_or_returns_callback.new(method=method,
                                                                                                 command_name="revers_from_client",
                                                                                                 seller_id=seller_id,
                                                                                                 start=0,
                                                                                                 end=9
                                                                                                 ))
    on_sale_button = InlineKeyboardButton(text=on_sale,
                                          callback_data=order_or_returns_callback.new(method=method,
                                                                                      command_name="on_sale",
                                                                                      seller_id=seller_id,
                                                                                      start=0,
                                                                                      end=9
                                                                                      ))
    revers_on_sale_button = InlineKeyboardButton(text=revers_on_sale,
                                                 callback_data=order_or_returns_callback.new(method=method,
                                                                                             command_name="revers_on_sale",
                                                                                             seller_id=seller_id,
                                                                                             start=0,
                                                                                             end=9
                                                                                             ))

    keyboard.row(in_stock_button, reverse_in_stock_button)
    # keyboard.row(to_client_button, revers_to_client_button)
    keyboard.row(from_client_button, revers_from_client_button)
    keyboard.row(on_sale_button, revers_on_sale_button)
    back_button = InlineKeyboardButton(text="⬅️ Назад",
                                       callback_data=set_command_seller_id.new(command_name="stocks_by_seller",
                                                                               seller_id=seller_id))
    if is_search is True:
        search_button = InlineKeyboardButton(text="❌ Поиск отмена", callback_data=set_search_callback.new(method=method,
                                                                                                          command_name=command_name,
                                                                                                          seller_id=seller_id,
                                                                                                          start=0,
                                                                                                          end=9,
                                                                                                          from_keyboard="delete_search"
                                                                                                          ))
    else:
        search_button = InlineKeyboardButton(text="🔍 Поиск", callback_data=set_search_callback.new(method=method,
                                                                                                    command_name=command_name,
                                                                                                    seller_id=seller_id,
                                                                                                    start=0,
                                                                                                    end=9,
                                                                                                    from_keyboard="report_stocks"
                                                                                                    ))
    keyboard.row(back_button, search_button)
    return keyboard
