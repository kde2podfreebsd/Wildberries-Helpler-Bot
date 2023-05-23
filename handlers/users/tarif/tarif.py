from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.utils.markdown import hlink, hbold

from data.config import BOT_NAME, AMOUNT_TARIFF
from keyboards.inline.tarif_keyboard.tarif_keyboard import go_to_paid
from loader import dp


@dp.message_handler(Command("tarif"), state='*')
async def show_about_user(message: types.Message, state: FSMContext):
    await message.delete()
    await state.finish()
    await message.answer("\n".join(
        [
            f'💰 {hbold(f"Тарифы {BOT_NAME}")}\n',
            f'Минимальный период оплаты составляет {hbold("1 месяц")}.\n',
            f'Стоимость тарифа зависит от количества заказов за последние 30 дней. \n',
            f'1 - 500 заказов {hbold("340")} руб/ мес',
            f'501 - 1000 заказов {hbold("490")} руб/ мес',
            f'1001 - 3000 заказов {hbold("790")} руб/ мес',
            f'3001 - 10000 заказов {hbold("1040")} руб/ мес',
            f'10000 + заказов {hbold("1290")} руб/ мес\n',
            f'За дополнительных сотрудников, подключённых к вашим API-ключам, {hbold("оплата не взимается")}.\n',
            f'🔒 Оплата производится только по Вашему согласию.\n',
            f'🛡 Деньги с карты в автоматическом режиме не списываются.\n',
        ]
    ), reply_markup=go_to_paid, disable_web_page_preview=True)
