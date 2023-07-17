from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.markdown import hbold

from data.config import AMOUNT_TARIFF
from handlers.users.profile.change_seller_settings import get_amount_tariff
from keyboards.inline.callback_datas import set_command_seller_id
from keyboards.inline.profile_keyboard.seller_settings import seller_settings_keyboard
from loader import dp
from utils.db_api.quick_commands.seller_inquiries import select_seller, count_seller_by_user
from utils.db_api.quick_commands.user_inquiries import select_user_by_seller


@dp.callback_query_handler(set_command_seller_id.filter(command_name="back_to_seller_setting"), state='*')
async def back_seller_setting(call: CallbackQuery, state: FSMContext, callback_data: dict):
    seller_id = callback_data.get("seller_id")
    seller = await select_seller(seller_id=int(seller_id))
    user = await select_user_by_seller(seller_id=int(seller_id))
    await state.finish()
    bot_enabled = seller.bot_enable
    reserve = seller.reserve

    if bot_enabled:
        bot_enabled_str = f'✅ 🛒 Заказы {hbold("отслеживаются")}\n'
    else:
        bot_enabled_str = f'⭕️ 🛒 Заказы {hbold("не отслеживаются")}\n'

    if seller.tarif:
        tariff = "✅ Активен"
    else:
        tariff = "❌ Не Активен"

    amount = await get_amount_tariff(seller.id)

    await call.message.edit_text("\n".join(
        [
            f'{hbold(seller.name)}',
            f'Тариф: {amount}₽ / мес',
            f'С учетом скидки: {amount - int(amount*0.01*user[0].discount)}₽ / мес',
            f'Статус тарифа: {tariff}\n',
            bot_enabled_str,

        ]
    ), reply_markup=seller_settings_keyboard(bot_enabled=bot_enabled, reserve=reserve,
                                             id_seller=seller.id)
    )


@dp.callback_query_handler(set_command_seller_id.filter(command_name="back_to_seller_setting"))
async def back_seller_setting(call: CallbackQuery, callback_data: dict):
    seller_id = callback_data.get("seller_id")
    seller = await select_seller(seller_id=int(seller_id))
    user = await select_user_by_seller(seller_id=int(seller_id))
    bot_enabled = seller.bot_enable
    reserve = seller.reserve
    if seller.tarif:
        tariff = "✅ Активен"
    else:
        tariff = "❌ Не Активен"

    if bot_enabled:
        bot_enabled_str = f'✅ 🛒 Заказы {hbold("отслеживаются")}\n'
    else:
        bot_enabled_str = f'⭕️ 🛒 Заказы {hbold("не отслеживаются")}\n'
    amount = await get_amount_tariff(seller.id)
    await call.message.edit_text("\n".join(
        [
            f'{hbold(seller.name)}',
            f'Тариф: {amount}₽ / мес',
            f'С учетом скидки: {amount - int(amount*0.01*user[0].discount)}₽ / мес',
            f'Статус тарифа: {tariff}\n',
            bot_enabled_str,
        ]
    ), reply_markup=seller_settings_keyboard(bot_enabled=bot_enabled, reserve=reserve,
                                             id_seller=seller.id)
    )


@dp.callback_query_handler(set_command_seller_id.filter(command_name="seller"))
async def seller_settings(call: types.CallbackQuery, callback_data: dict):
    seller_id = callback_data.get("seller_id")
    seller = await select_seller(seller_id=int(seller_id))
    user = await select_user_by_seller(seller_id=int(seller_id))
    bot_enabled = seller.bot_enable
    reserve = seller.reserve
    if seller.tarif:
        tariff = "✅ Активен"
    else:
        tariff = "❌ Не Активен"

    if bot_enabled:
        bot_enabled_str = f'✅ 🛒 Заказы {hbold("отслеживаются")}\n'
    else:
        bot_enabled_str = f'⭕️ 🛒 Заказы {hbold("не отслеживаются")}\n'

    amount = await get_amount_tariff(seller.id)
    await call.message.edit_text("\n".join(
        [
            f'{hbold(seller.name)}',
            f'Тариф: {amount}₽ / мес',
            f'С учетом скидки: {amount - int(amount*0.01*user[0].discount)}₽ / мес',
            f'Статус тарифа: {tariff}\n',
            bot_enabled_str,
        ]
    ), reply_markup=seller_settings_keyboard(bot_enabled=bot_enabled, reserve=reserve,
                                             id_seller=seller.id)
    )
