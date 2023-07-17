from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import CallbackQuery
from aiogram.utils.markdown import hcode, hbold, hlink

from data.config import AMOUNT_TARIFF
from handlers.users.start.start import bot_start
from keyboards.inline.profile_keyboard.profile_keyboard import about_keyboard, settings_keyboard, add_seller_keyboard
from keyboards.inline.tarif_keyboard.tarif_keyboard import paid_keyboard
from loader import dp
from states import States
from utils.db_api.quick_commands.seller_inquiries import count_seller_by_user, select_seller_by_user
from utils.db_api.quick_commands.user_inquiries import select_user


@dp.message_handler(Command("my"), state='*')
async def show_about_user(message: types.Message, state: FSMContext):
    await message.delete()
    await state.finish()
    user_id = message.chat.id
    user = await select_user(user_id=user_id)
    count_sellers = await count_seller_by_user(user_id=user_id)
    await message.answer("\n".join(
        [
            f'ID: {hcode(user.id)}',
            f'Поставщики: {count_sellers}',
        ]
    ), reply_markup=about_keyboard
    )


@dp.callback_query_handler(text="back_to_profile", state="*")
async def back_to_profile(call: CallbackQuery, state: FSMContext):
    await state.finish()
    user_id = call.message.chat.id
    user = await select_user(user_id=user_id)
    count_sellers = await count_seller_by_user(user_id=user_id)
    await call.message.edit_text("\n".join(
        [
            f'ID: {hcode(user.id)}',
            f'Поставщики: {count_sellers}',
        ]
    ), reply_markup=about_keyboard
    )


@dp.callback_query_handler(Text(equals=["settings", "back_to_settings"]))
async def show_settings(call: CallbackQuery):
    user_id = call.message.chat.id
    list_sellers = await select_seller_by_user(user_id=user_id)
    await call.message.edit_text("\n".join(
        [
            f'📝 Выберите продавца для редактирования:',
        ]
    ), reply_markup=settings_keyboard(list_sellers))


@dp.callback_query_handler(text="back_to_settings", state=States.CONNECTING_API)
async def back_to_choose_sellers(call: CallbackQuery, state: FSMContext):
    await state.finish()
    user_id = call.message.chat.id
    list_sellers = await select_seller_by_user(user_id=user_id)
    await call.message.edit_text("\n".join(
        [
            f'📝 Выберите продавца для редактирования:',
        ]
    ), reply_markup=settings_keyboard(list_sellers))


@dp.callback_query_handler(text="add_seller")
async def add_seller(call: CallbackQuery):
    await call.message.edit_text("\n".join(
        [
            f'👤 {hbold("Добавление продавца")}\n',
            f'↔️ Чтобы отслеживать заказы сразу для нескольких кабинетов WB, добавьте еще один API-ключ.\n',
            f'1️⃣ Зайдите в личный кабинет Wildberries → Настройки → Доступ к API '
            f'({hlink("ссылка", "https://seller.wildberries.ru/supplier-settings/access-to-api")}).\n',
            f'2️⃣ Скопируйте ключ для работы с {hbold("API статистики x64")} (если ключа нет, создайте его и потом скопируйте).\n',
            f'3️⃣ Вставьте ключ в сообщении этого чата.\n',
            f'📝 Введите API-ключ в этом сообщении:\n',
        ]
    ), reply_markup=add_seller_keyboard
    )
    await States.CONNECTING_API.set()


@dp.callback_query_handler(text="balance_and_paid")
async def balance_and_paid(call: CallbackQuery):
    user_id = call.message.chat.id
    user = await select_user(user_id=user_id)
    count_sellers = await count_seller_by_user(user_id=user_id)
    await call.message.edit_text(
        "\n".join(
            [
                hbold(f"💰 Баланс: {user.balance}₽"),
                f'· Поставщики: {hbold(count_sellers)}\n',
                f'👨‍💼👩🏻‍💼 Если к вашему API-ключу подключены несколько сотрудников, то оплачивает кто-то один, пользуются все.\n',
                f'🔒 Пополнение баланса производится только по Вашему согласию.\n',
                f'🛡 Деньги с карты в автоматическом режиме не списываются.\n',
                f'ℹ️ Описание тарифов 👉🏻 /tarif \n',

            ]
        ), reply_markup=paid_keyboard()
    )
