import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.markdown import hbold, hlink

from data.config import SUPPORT_LINK
from keyboards.inline.callback_datas import set_command_seller_id, change_api_callback
from keyboards.inline.profile_keyboard.change_api_keyboard import change_api_keyboard, change_api_insert_keyboard
from loader import dp, bot
from states import States
from utils.db_api.quick_commands.seller_inquiries import select_seller, update_api64

from utils.wb_api.method_warehouse import valid_token


@dp.callback_query_handler(set_command_seller_id.filter(command_name="change_api_x64"))
async def change_api_x64(call: CallbackQuery, callback_data: dict):
    seller_id = callback_data.get("seller_id")
    seller = await select_seller(seller_id=int(seller_id))
    await call.message.edit_text("\n".join(
        [
            f'🔑 {hbold("Управление API-ключом")}\n',
            f'{seller.name}\n',
            f'Выберите действие:',
        ]
    ), reply_markup=change_api_keyboard(version_api="x64", seller_id=seller_id)
    )


@dp.callback_query_handler(text="back_to_change_api_x64", state=States.CHANGE_API)
async def back_to_change_api_x64(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    seller_id = data.get("seller_id")
    await state.finish()
    seller = await select_seller(seller_id=int(seller_id))
    await call.message.edit_text("\n".join(
        [
            f'🔑 {hbold("Управление API-ключом")}\n',
            f'{seller.name}\n',
            f'Выберите действие:',
        ]
    ), reply_markup=change_api_keyboard(version_api="x64", seller_id=seller_id)
    )


@dp.callback_query_handler(change_api_callback.filter(method="change_api"))
async def change_api(call: CallbackQuery, callback_data: dict, state: FSMContext):
    version_api = callback_data.get("version_api")
    seller_id = callback_data.get("seller_id")
    seller = await select_seller(seller_id=int(seller_id))
    if version_api == "x64":
        await States.CHANGE_API.set()
        await state.update_data(seller_id=seller_id)
        await state.update_data(message_id=call.message.message_id)
        await call.message.edit_text("\n".join(
            [
                f'🔄 {hbold("Замена API-ключа (x64)")}\n',
                f'{hbold(seller.name)}\n',
                f'Замена требуется, если API-ключ (x64) был изменён в кабинете {hbold("Wildberries.")}\n',
                f'В личном кабинете WB пройдите в {hbold("Настройки > Доступ к API > ")}'
                f'{hbold("Ключ для работы с API статистики x64")}, затем скопируйте ваш API-ключ (x64) '
                f'({hlink("ссылка", "https://seller.wildberries.ru/supplier-settings/access-to-api")})\n',
                f'📝 Вставьте скопированный API-ключ (x64) в это сообщение:',
            ]
        ), reply_markup=change_api_insert_keyboard
        )
    elif version_api == "FBS":
        await call.message.edit_text("\n".join(
            [
                f'🔑 {hbold("Управление API-ключом")}\n',
                f'{seller.name}\n',
                f'Выберите действие:',
            ]
        ), reply_markup=change_api_keyboard(version_api="x64", seller_id=seller_id)
        )


@dp.message_handler(state=States.CHANGE_API)
async def back_seller_setting(message: types.Message, state: FSMContext):
    await message.delete()
    status = await valid_token(message.text)
    data = await state.get_data()
    message_id = data.get("message_id")
    seller_id = data.get("seller_id")
    if status == 200:
        api_x64 = message.text
        await update_api64(int(seller_id), api_x64)
        back_keyboard = InlineKeyboardMarkup(row_width=1)
        back_to_seller_button = InlineKeyboardButton(text="⬅️ Назад", callback_data=set_command_seller_id.new(
            command_name="back_to_seller_setting", seller_id=seller_id))
        back_keyboard.insert(back_to_seller_button)
        await bot.edit_message_text(chat_id=message.chat.id, message_id=message_id,
                                    text="\n".join(
                                        [
                                            f'🔄 {hbold("Замена API-ключа (x64)")}\n',
                                            f'✅ API-ключ успешно заменен',

                                        ]
                                    ), reply_markup=back_keyboard
                                    )
        await state.finish()
    elif status == 400 or status == 500:
        support_keyboard = InlineKeyboardMarkup(row_width=2)
        back_button = InlineKeyboardButton(text="⬅️ Назад",
                                           callback_data="back_to_change_api_x64")
        support_button = InlineKeyboardButton(text="👨🏻‍💻 Поддержка", url=SUPPORT_LINK)
        support_keyboard.row(back_button, support_button)
        await bot.edit_message_text(chat_id=message.chat.id, message_id=message_id,
                                    text="\n".join(
                                        [
                                            f'❌ {hbold("Ошибка!!")}',
                                            f'⏱ {datetime.datetime.now().time().strftime("%H:%M:%S")}\n',
                                            f'API-ключ (x64) некорректен!\n',
                                            f'Отправьте правильный ключ заново в этом сообщении:',

                                        ]
                                    ), reply_markup=support_keyboard
                                    )
