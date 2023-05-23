from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import CallbackQuery
from aiogram.utils.markdown import hcode, hbold

from data.config import BOT_NAME
from keyboards.inline.profile_keyboard.profile_keyboard import about_keyboard
from keyboards.inline.start_keyboard.choice_start import start_keyboard
from loader import dp
from states import States
from utils.db_api.quick_commands.seller_inquiries import count_seller_by_user
from utils.db_api.quick_commands.user_inquiries import select_user, add_user


@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: types.Message, state: FSMContext):
    user_id = message.chat.id
    await state.finish()
    user = await select_user(message.from_user.id)
    count_sellers = await count_seller_by_user(user_id=user_id)
    if not user or count_sellers == 0:
        await add_user(id=message.from_user.id, name=message.from_user.full_name, chat_id=message.chat.id,
                       balance=0)
        await message.answer(
            "\n".join(
                [
                    f'🤜🏻 {hbold(BOT_NAME)} - Это помощник, который позволит просто и эффективно '
                    f'контролировать продажи на {hbold("Wildberries")}. \n',
                    f'{hbold("БОТ ПОКАЖЕТ:")}\n',
                    f'🛒 Уведомления о новых заказах;',
                    f'💼 Фактическую комиссию по заказу;',
                    f'💎 Процент выкупа по текущему артикулу;',
                    f'🌐 Регион покупателя и стоимость логистики;',
                    f'🚛 Количество товара в пути до клиента и обратно;',
                    f'📦 Реальные остатки на складе и на сколько дней хватит резерва;',
                    f'{hbold("ОСОБЕННОСТИ:")}\n',
                    f'📊 Построение информативных отчетов по заказам, продажам, возвратам и штрафам;',
                    f'↔️ Возможность подключения нескольких кабинетов Wildberries;',
                    f'📑 Выгрузка данных в Google таблицы;',
                    f'🔥 Теперь вся горячая информация о продажах в вашем Telegram!\n',
                    f'{hcode(f"Ваш ID: {user_id}")}',
                ]
            ), reply_markup=start_keyboard
        )
    else:
        await message.answer("\n".join(
            [
                f'ID: {hcode(user.id)}',
                f'Поставщики: 1',
            ]
        ), reply_markup=about_keyboard)


@dp.callback_query_handler(text="back_to_start", state=States.FREE_CONNECTING_API)
async def back_connection(call: CallbackQuery, state: FSMContext):
    await state.finish()
    id = call.message.chat.id
    await call.message.edit_text("\n".join(
        [
            f'🤜🏻 {hbold(BOT_NAME)} - Это помощник, который позволит просто и эффективно '
            f'контролировать продажи на {hbold("Wildberries")}. \n',
            f'{hbold("БОТ ПОКАЖЕТ:")}\n',
            f'🛒 Уведомления о новых заказах;',
            f'💼 Фактическую комиссию по заказу;',
            f'💎 Процент выкупа по текущему артикулу;',
            f'🌐 Регион покупателя и стоимость логистики;',
            f'🚛 Количество товара в пути до клиента и обратно;',
            f'📦 Реальные остатки на складе и на сколько дней хватит резерва;',
            f'{hbold("ОСОБЕННОСТИ:")}\n',
            f'📊 Построение информативных отчетов по заказам, продажам, возвратам и штрафам;',
            f'↔️ Возможность подключения нескольких кабинетов Wildberries;',
            f'📑 Выгрузка данных в Google таблицы;',
            f'🔥 Теперь вся горячая информация о продажах в вашем Telegram!\n',
            f'{hcode(f"Ваш ID: {id}")}',
        ]
    ), reply_markup=start_keyboard)
