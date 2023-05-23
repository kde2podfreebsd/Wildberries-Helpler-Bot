from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.markdown import hbold

from data.config import BOT_NAME
from keyboards.inline.callback_datas import set_command_seller_id
from keyboards.inline.profile_keyboard.seller_settings import back_to_seller_setting
from loader import dp, bot
from states import States
from utils.db_api.quick_commands.seller_inquiries import select_seller, update_seller_settings


@dp.callback_query_handler(set_command_seller_id.filter(command_name="reserve"))
async def add_seller(call: CallbackQuery, state: FSMContext, callback_data: dict):
    seller_id = callback_data.get("seller_id")
    seller = await select_seller(seller_id=int(seller_id))
    reserve = seller.reserve
    await call.message.edit_text(
        "\n".join(
            [
                f'📦 {hbold("Резерв склада")}\n',
                f'{hbold(BOT_NAME)} покажет оптимальное количество товара для новой поставки, '
                f'просто укажите на сколько дней вы планируете заполнять склад '
                f'(на сколько дней должно хватать товара при текущей динамике продаж).\n',
                f'Текущее значение: {reserve} дн.\n',
                f'📝 Введите новое значение в этом сообщении (от 3 до 60):',
            ]
        ), reply_markup=back_to_seller_setting(seller_id))
    await States.RESERVE_DAY.set()
    await state.update_data(message_id=call.message.message_id)
    await state.update_data(seller_id=seller_id)


@dp.message_handler(state=States.RESERVE_DAY)
async def set_reserve_day(message: types.Message, state: FSMContext):
    await message.delete()
    data = await state.get_data()
    message_id = data.get("message_id")
    seller_id = data.get("seller_id")

    if message.text.isdigit():
        if int(message.text) < 3:
            reserve = '3'
        elif int(message.text) > 60:
            reserve = '60'
        else:
            reserve = message.text
    else:
        reserve = '3'
    seller = await update_seller_settings(seller_id=int(seller_id), reserve=int(reserve))
    await bot.edit_message_text(chat_id=message.chat.id, message_id=message_id,
                                text="\n".join(
                                    [
                                        f'📦 {hbold("Резерв склада")}\n',
                                        f'{hbold(BOT_NAME)} покажет оптимальное количество товара для новой поставки, '
                                        f'просто укажите на сколько дней вы планируете заполнять склад '
                                        f'(на сколько дней должно хватать товара при текущей динамике продаж).\n',
                                        f'Текущее значение: ✅ {seller.reserve} дн.\n',
                                        f'📝 Введите новое значение в этом сообщении (от 3 до 60):',
                                    ]
                                ), reply_markup=back_to_seller_setting(seller_id)
                                )
