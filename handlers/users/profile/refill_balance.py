from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType
from aiogram.utils.markdown import hbold

from data.config import BOT_NAME, YOOTOKEN
from loader import dp
from utils.db_api.quick_commands.user_inquiries import update_balance, update_discount


@dp.callback_query_handler(lambda text: text.data.split('#')[0] == "other_amount")
async def back_profile(call: types.CallbackQuery, state: FSMContext):
    if call.data.split('#')[1] == '1000':
        discount = 1
    elif call.data.split('#')[1] == '3000':
        discount = 3
    elif call.data.split('#')[1] == '5000':
        discount = 5
    elif call.data.split('#')[1] == '490':
        discount = 0
    else:
        discount = 10
    amount = int(call.data.split('#')[1]) * 100
    await call.message.edit_text(
        "\n".join(
            [
                f'''{hbold(f"ПОПОЛНЕНИЕ БАЛАНСА НА СУММУ {call.data.split('#')[1]}")}\n''',
                f'Скидка составит {discount} %',

            ]
        )
    )
    await state.finish()
    await send_payment(chat_id=call.message.chat.id, amount=amount, bot=call.message.bot)


# @dp.message_handler(lambda message: not message.text.split('#')[1].isdigit(),\
#                     lambda state: state.split('#')[0] == "other_amount")
# async def process_sum_invalid(message: types.Message):
#     return await message.reply("\n".join(
#         [
#             f'{hbold("ПОПОЛНЕНИЕ БАЛАНСА")}\n',
#             f'Некорректная сумма , {hbold("сумма должна быть числом")}',
#
#         ]
#     ))


# @dp.callback_query_handler(lambda text: text.data.split('#')[0] == "other_amount", \
#                            )
# async def seller_settings(message: types.Message, state: FSMContext):
#     data = await state.get_data()
#     print(data)
#     await message.delete()
#     await state.finish()
#     amount = int(message.text.split('#')[1]) * 100
#     await send_payment(chat_id=message.chat.id, amount=amount, bot=message.bot)


@dp.pre_checkout_query_handler()
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await pre_checkout_query.bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def process_pay(message: types.Message):
    amount = message.successful_payment.total_amount / 100
    if int(amount) == 1000:
        discount = 1
    elif int(amount) == 3000:
        discount = 3
    elif int(amount) == 5000:
        discount = 5
    elif int(amount) == 490:
        discount = 0
    else:
        discount = 10
    await update_discount(id=message.chat.id, discount=discount)
    user = await update_balance(id=message.chat.id, summ=amount)
    await message.answer(f"Ваш баланс успешно пополнен на {amount} р."
                         f"\n\n"
                         f"Текущий баланс: {user.balance} р")


async def send_payment(chat_id, amount, bot):
    await bot.send_invoice(chat_id=chat_id, title="Пополнение баланса",
                           description=f"Пополнение баланса бота {BOT_NAME}, после оплаты на ваш баланс будут начислены деньги.",
                           payload="refill_balance", provider_token=YOOTOKEN, currency="RUB",
                           start_parameter="refill_balance_user", prices=[{"label": "Руб", "amount": amount}])
