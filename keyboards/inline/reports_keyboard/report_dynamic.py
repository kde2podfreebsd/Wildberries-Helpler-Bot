from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import set_report_callback, set_command_seller_id, set_search_callback
from keyboards.inline.reports_keyboard.tools import button_name_by_filter


def report_dynamic_keyboard(seller_id, command_name, period, end, start, is_search, next=None, back=None):
    keyboard = InlineKeyboardMarkup(row_width=2)
    back_button = InlineKeyboardButton(text="← Пред", callback_data=set_report_callback.new(method=period,
                                                                                            command_name=command_name,
                                                                                            seller_id=seller_id,
                                                                                            start=start - 20,
                                                                                            end=end - 20
                                                                                            ))
    next_button = InlineKeyboardButton(text="След →", callback_data=set_report_callback.new(method=period,
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
    subject, vendor_code, category, brand, region, no_grouping = button_name_by_filter(command_name)
    subject_button = InlineKeyboardButton(text=subject, callback_data=set_report_callback.new(method=period,
                                                                                              command_name="subject",
                                                                                              seller_id=seller_id,
                                                                                              start=0,
                                                                                              end=9
                                                                                              ))
    vendor_code_button = InlineKeyboardButton(text=vendor_code, callback_data=set_report_callback.new(method=period,
                                                                                                      command_name="vendor_code",
                                                                                                      seller_id=seller_id,
                                                                                                      start=0,
                                                                                                      end=9
                                                                                                      ))
    category_button = InlineKeyboardButton(text=category, callback_data=set_report_callback.new(method=period,
                                                                                                command_name="category",
                                                                                                seller_id=seller_id,
                                                                                                start=0,
                                                                                                end=9
                                                                                                ))
    brand_button = InlineKeyboardButton(text=brand, callback_data=set_report_callback.new(method=period,
                                                                                          command_name="brand",
                                                                                          seller_id=seller_id,
                                                                                          start=0,
                                                                                          end=9
                                                                                          ))
    region_button = InlineKeyboardButton(text=region, callback_data=set_report_callback.new(method=period,
                                                                                            command_name="region",
                                                                                            seller_id=seller_id,
                                                                                            start=0,
                                                                                            end=9
                                                                                            ))
    no_grouping_button = InlineKeyboardButton(text=no_grouping, callback_data=set_report_callback.new(method=period,
                                                                                                      command_name="grouping",
                                                                                                      seller_id=seller_id,
                                                                                                      start=0,
                                                                                                      end=9
                                                                                                      ))
    keyboard.row(subject_button, vendor_code_button)
    keyboard.row(category_button, brand_button)
    keyboard.row(region_button, no_grouping_button)
    back_button = InlineKeyboardButton(text="⬅️ Назад",
                                       callback_data=set_command_seller_id.new(command_name="report_by_seller",
                                                                               seller_id=seller_id))
    if is_search is True:
        search_button = InlineKeyboardButton(text="❌ Поиск отмена", callback_data=set_search_callback.new(method=period,
                                                                                                          command_name=command_name,
                                                                                                          seller_id=seller_id,
                                                                                                          start=0,
                                                                                                          end=9,
                                                                                                          from_keyboard="delete_search"
                                                                                                          ))
    else:
        search_button = InlineKeyboardButton(text="🔍 Поиск", callback_data=set_search_callback.new(method=period,
                                                                                                    command_name=command_name,
                                                                                                    seller_id=seller_id,
                                                                                                    start=0,
                                                                                                    end=9,
                                                                                                    from_keyboard="report_dynamic"
                                                                                                    ))
    keyboard.row(back_button, search_button)
    return keyboard
