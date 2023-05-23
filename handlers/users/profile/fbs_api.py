from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.markdown import hbold, hitalic, hlink

from data.config import BOT_NAME
from keyboards.inline.callback_datas import set_command_seller_id
from keyboards.inline.profile_keyboard.change_api_keyboard import add_fbs_api
from loader import dp, bot
from states import States
from utils.db_api.quick_commands.seller_inquiries import select_seller, update_fbs_api
from utils.wb_api.method_warehouse import valid_token_fbs


@dp.callback_query_handler(set_command_seller_id.filter(command_name="change_api_fbs"), state="*")
async def balance_and_paid(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await state.finish()
    seller_id = int(callback_data.get("seller_id"))
    seller = await select_seller(seller_id)
    if seller.api_fbs:
        fbs_string = "✅ работает (действий не требуется)"
        new_fbs_string = "📝 Введите новый токен если хотите заменить токен:"
    else:
        fbs_string = "️⚠️ не установлен"
        new_fbs_string = "📝 Введите новый токен:"

    await call.message.edit_text(
        "\n".join(
            [
                hbold(f"🔑 Редактирование API-ключа (FBS)\n"),
                f'Если вы полностью или частично работаете по схеме {hbold("FBS")} (продажа со склада поставщика), '
                f'используйте дополнительный API-ключ (токен), чтобы {BOT_NAME} мог отслеживать заказы.\n',
                hitalic("(Примечание: при этом первый API-ключ x64 также используется, его удалять не нужно.)\n"),
                f'1️⃣ Зайдите в личный кабинет Wildberries → Настройки → Доступ к новому API '
                f'({hlink("ссылка", "https://seller.wildberries.ru/supplier-settings/access-to-new-api")}).\n',
                f'2️⃣ Введите имя токена (например: {BOT_NAME}) и нажмите кнопку '
                f'{hbold("Сгенерировать токен")} (если ничего не происходит - это ошибка ВБ, попробуйте позже). \n',
                f'3️⃣ Скопируйте токен и вставьте в сообщении этого чата.\n',
                f'{hbold("Поставщик")}: {seller.name}\n',
                f'{hbold("Текущий токен")}: {fbs_string}\n',
                new_fbs_string,

            ]
        ), reply_markup=add_fbs_api(seller_id=seller_id)
    )
    await States.CONNECTING_API_FBS.set()
    await state.update_data(seller_id=seller_id)
    await state.update_data(message_id=call.message.message_id)


@dp.message_handler(state=States.CONNECTING_API_FBS)
async def back_seller_setting(message: types.Message, state: FSMContext):
    await message.delete()
    data = await state.get_data()
    message_id = data.get("message_id")
    seller_id = data.get("seller_id")
    seller = await select_seller(seller_id)
    if seller.api_fbs:
        fbs_string = "✅ работает (действий не требуется)"
        new_fbs_string = "📝 Введите новый токен если хотите заменить токен:"
    else:
        fbs_string = "️⚠️ не установлен"
        new_fbs_string = "📝 Введите новый токен:"
    if len(message.text) != 149:
        await bot.edit_message_text(chat_id=message.chat.id, message_id=message_id,
                                    text="\n".join(
                                        [
                                            hbold(f"🔑 Редактирование API-ключа (FBS)\n"),
                                            f'Если вы полностью или частично работаете по схеме {hbold("FBS")} (продажа со склада поставщика), '
                                            f'используйте дополнительный API-ключ (токен), чтобы {BOT_NAME} мог отслеживать заказы.\n',
                                            hitalic(
                                                "(Примечание: при этом первый API-ключ x64 также используется, его удалять не нужно.)\n"),
                                            f'1️⃣ Зайдите в личный кабинет Wildberries → Настройки → Доступ к новому API '
                                            f'({hlink("ссылка", "https://seller.wildberries.ru/supplier-settings/access-to-new-api")}).\n',
                                            f'2️⃣ Введите имя токена (например: {BOT_NAME}) и нажмите кнопку '
                                            f'{hbold("Сгенерировать токен")} (если ничего не происходит - это ошибка ВБ, попробуйте позже). \n',
                                            f'3️⃣ Скопируйте токен и вставьте в сообщении этого чата.\n',
                                            f'{hbold("Поставщик")}: {seller.name}\n',
                                            f'{hbold("Текущий токен")}: {fbs_string}\n',
                                            hbold(
                                                "❌ Внимание, вы ввели некорректный токен. Укажите правильный API-ключ!\n"),
                                            new_fbs_string,

                                        ]
                                    ),
                                    reply_markup=add_fbs_api(seller_id)
                                    )
        return
    status = valid_token_fbs(message.text)
    if status == 200:
        fbs_api = message.text
        await update_fbs_api(int(seller_id), fbs_api)
        await bot.edit_message_text(chat_id=message.chat.id, message_id=message_id,
                                    text="\n".join(
                                        [
                                            hbold(f"🔑 Редактирование API-ключа (FBS)\n"),
                                            f'Если вы полностью или частично работаете по схеме {hbold("FBS")} (продажа со склада поставщика), '
                                            f'используйте дополнительный API-ключ (токен), чтобы {BOT_NAME} мог отслеживать заказы.\n',
                                            hitalic(
                                                "(Примечание: при этом первый API-ключ x64 также используется, его удалять не нужно.)\n"),
                                            f'1️⃣ Зайдите в личный кабинет Wildberries → Настройки → Доступ к новому API '
                                            f'({hlink("ссылка", "https://seller.wildberries.ru/supplier-settings/access-to-new-api")}).\n',
                                            f'2️⃣ Введите имя токена (например: {BOT_NAME}) и нажмите кнопку '
                                            f'{hbold("Сгенерировать токен")} (если ничего не происходит - это ошибка ВБ, попробуйте позже). \n',
                                            f'3️⃣ Скопируйте токен и вставьте в сообщении этого чата.\n',
                                            f'{hbold("Поставщик")}: {seller.name}\n',
                                            f'{hbold("Текущий токен")}: ✅ работает (действий не требуется)\n',
                                            f'📝 Введите новый токен если хотите заменить токен:',

                                        ]
                                    ), reply_markup=add_fbs_api(seller_id)
                                    )
    elif status == 400 or status == 500:
        await bot.edit_message_text(chat_id=message.chat.id, message_id=message_id,
                                    text="\n".join(
                                        [
                                            hbold(f"🔑 Редактирование API-ключа (FBS)\n"),
                                            f'Если вы полностью или частично работаете по схеме {hbold("FBS")} (продажа со склада поставщика), '
                                            f'используйте дополнительный API-ключ (токен), чтобы {BOT_NAME} мог отслеживать заказы.\n',
                                            hitalic(
                                                "(Примечание: при этом первый API-ключ x64 также используется, его удалять не нужно.)\n"),
                                            f'1️⃣ Зайдите в личный кабинет Wildberries → Настройки → Доступ к новому API '
                                            f'({hlink("ссылка", "https://seller.wildberries.ru/supplier-settings/access-to-new-api")}).\n',
                                            f'2️⃣ Введите имя токена (например: {BOT_NAME}) и нажмите кнопку '
                                            f'{hbold("Сгенерировать токен")} (если ничего не происходит - это ошибка ВБ, попробуйте позже). \n',
                                            f'3️⃣ Скопируйте токен и вставьте в сообщении этого чата.\n',
                                            f'{hbold("Поставщик")}: {seller.name}\n',
                                            f'{hbold("Текущий токен")}: {fbs_string}\n',
                                            hbold(
                                                "❌ Внимание, вы ввели некорректный токен. Укажите правильный API-ключ!\n"),
                                            new_fbs_string,

                                        ]
                                    ),
                                    reply_markup=add_fbs_api(seller_id)
                                    )