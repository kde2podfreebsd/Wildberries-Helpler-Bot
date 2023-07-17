import datetime

from aiogram import types
from aiogram.utils.markdown import hbold, hcode

from data.config import AMOUNT_TARIFF
from keyboards.inline.callback_datas import change_sellers_callback
from keyboards.inline.profile_keyboard.seller_settings import seller_settings_keyboard, back_to_seller_setting
from loader import dp
from utils.db_api.quick_commands.product_inquiries import count_mouth_order
from utils.db_api.quick_commands.seller_inquiries import update_seller_settings, select_seller, count_seller_by_user, \
    update_trail
from utils.db_api.quick_commands.user_inquiries import select_user, update_balance


@dp.callback_query_handler(change_sellers_callback.filter(group="change_sellers"))
async def seller_settings(call: types.CallbackQuery, callback_data: dict):
    seller_id = callback_data.get("seller_id")
    seller = await select_seller(int(seller_id))
    command_name = callback_data.get("command_name")
    if command_name == 'change_enabled_false':
        seller = await update_seller_settings(seller_id=int(seller_id), bot_enable=False)
    else:
        if seller.tarif is not False:
            seller = await update_seller_settings(seller_id=int(seller_id), bot_enable=True)
        else:
            await pay_the_fare(call, seller)
            return
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
            f'Статус тарифа: {tariff}\n',
            bot_enabled_str,
        ]
    ), reply_markup=seller_settings_keyboard(bot_enabled=bot_enabled, reserve=reserve,
                                             id_seller=seller.id)
    )


async def pay_the_fare(call, seller):
    amount = await get_amount_tariff(seller.id)
    user_id = call.message.chat.id
    user = await select_user(user_id=user_id)
    if user.balance < amount:
        return await call.message.edit_text("\n".join(
            [
                f'❌ Включение Бота для {hbold(seller.name)} недоступно\n',
                f'Пополните свой баланс для активации тарифа.',
                f'С учетом скидки: {amount - int(amount * 0.01 * user.discount)}₽ / мес',
                f'Тариф: {amount}₽ / мес\n',
            ]
        ), reply_markup=back_to_seller_setting(seller_id=seller.id)
        )
    else:
        user = await update_balance(id=user_id, summ=(amount - (amount*0.01*user.discount)) * -1)
        await update_trail("paid", seller.id)
        now = datetime.datetime.now() + datetime.timedelta(days=30)
        await call.message.edit_text("\n".join(
            [
                f'✅ Тариф успешно оплачен для {hbold(seller.name)}\n',
                f'Дата окончания подписки {hcode(now.strftime("%Y-%m-%d %H:%M:%S"))}',
                f'Ваш текущий баланс: {user.balance}'
            ]
        ), reply_markup=back_to_seller_setting(seller_id=seller.id)
        )


async def get_amount_tariff(seller_id):
    orders = await count_mouth_order(seller_id)
    if len(orders) < 200:
        amount = 340
    elif 201 < len(orders) < 1000:
        amount = 490
    elif 1001 < len(orders) < 3000:
        amount = 790
    elif 3001 < len(orders) < 10000:
        amount = 1040
    else:
        amount = 1290
    return amount
