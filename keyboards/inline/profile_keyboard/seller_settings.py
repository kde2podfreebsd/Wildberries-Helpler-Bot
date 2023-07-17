from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import set_command_seller_id, change_sellers_callback, choice_date_xlsx_callback


def seller_settings_keyboard(bot_enabled, reserve, id_seller):
    seller_settings = InlineKeyboardMarkup(row_width=1)

    if bot_enabled:
        bot_enabled_button = InlineKeyboardButton(text="✅ Бот включен",
                                                  callback_data=change_sellers_callback.new(group="change_sellers",
                                                                                            command_name="change_enabled_false",
                                                                                            seller_id=id_seller))
    else:
        bot_enabled_button = InlineKeyboardButton(text="⭕️ Бот выключен (включить?)",
                                                  callback_data=change_sellers_callback.new(group="change_sellers",
                                                                                            command_name="change_enabled_true",
                                                                                            seller_id=id_seller))

    reserve_button = InlineKeyboardButton(text=f"📦 Резерв склада {reserve} дн.",
                                          callback_data=set_command_seller_id.new(command_name="reserve",
                                                                                  seller_id=id_seller))

    api_key_x64 = InlineKeyboardButton(text="🔑 API-ключ (статистика)",
                                       callback_data=set_command_seller_id.new(command_name="change_api_x64",
                                                                               seller_id=id_seller))
    api_key_FBS = InlineKeyboardButton(text="🔑 API-ключ (стандарт)",
                                       callback_data=set_command_seller_id.new(command_name="change_api_fbs",
                                                                               seller_id=id_seller))
    exel_statistics = InlineKeyboardButton(text="📥 Скачать статистику (excel)",
                                           callback_data=set_command_seller_id.new(command_name="exel_statistics",
                                                                                   seller_id=id_seller))
    rename_seller = InlineKeyboardButton(text="👤 Переименовать поставщика",
                                         callback_data=set_command_seller_id.new(command_name="rename_seller_keyboard",
                                                                                 seller_id=id_seller))
    delete_seller = InlineKeyboardButton(text="🗑 Удалить поставщика",
                                         callback_data=set_command_seller_id.new(command_name="delete_seller_keyboard",
                                                                                 seller_id=id_seller))
    back_to_add_seller = InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_settings")
    seller_settings.insert(bot_enabled_button)
    seller_settings.insert(reserve_button)
    seller_settings.insert(api_key_x64)
    seller_settings.insert(api_key_FBS)
    seller_settings.insert(exel_statistics)
    seller_settings.insert(rename_seller)
    seller_settings.insert(delete_seller)
    seller_settings.insert(back_to_add_seller)
    return seller_settings


def back_to_seller_setting(seller_id):
    keyboard = InlineKeyboardMarkup(row_width=1)
    button = InlineKeyboardButton(text="⬅️ Назад",
                                  callback_data=set_command_seller_id.new(
                                      command_name="back_to_seller_setting", seller_id=seller_id))
    keyboard.insert(button)
    return keyboard


def choice_date_xlsx(seller_id):
    kb = InlineKeyboardMarkup(row_width=1)
    button_1 = InlineKeyboardButton(text="За 7 дней",
                                    callback_data=choice_date_xlsx_callback.new(command_name="show_stats_x",
                                                                                seller_id=seller_id,
                                                                                days="7"
                                                                                ))
    button_2 = InlineKeyboardButton(text="За 14 дней",
                                    callback_data=choice_date_xlsx_callback.new(command_name="show_stats_x",
                                                                                seller_id=seller_id,
                                                                                days="14"
                                                                                ))
    button_3 = InlineKeyboardButton(text="За 30 дней",
                                    callback_data=choice_date_xlsx_callback.new(command_name="show_stats_x",
                                                                                seller_id=seller_id,
                                                                                days="30"
                                                                                ))
    button_4 = InlineKeyboardButton(text="За 90 дней",
                                    callback_data=choice_date_xlsx_callback.new(command_name="show_stats_x",
                                                                                seller_id=seller_id,
                                                                                days="90"
                                                                                ))
    button = InlineKeyboardButton(text="⬅️ Назад",
                                  callback_data=set_command_seller_id.new(
                                      command_name="back_to_seller_setting", seller_id=seller_id))
    kb.insert(button_1)
    kb.insert(button_2)
    kb.insert(button_3)
    kb.insert(button_4)
    kb.insert(button)
    return kb
