import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hbold

from keyboards.inline.profile_keyboard.add_delete_seller import fail_add_seller_keyboard, seller_added_keyboard
from loader import dp
from states import States
from utils.db_api.quick_commands.seller_inquiries import select_seller_by_api_x64, add_seller, update_trail_fail
from utils.db_api.quick_commands.user_inquiries import update_user_seller
from utils.misc.start_by_time import first_scan
from utils.wb_api.method_warehouse import valid_token


@dp.message_handler(state=States.CONNECTING_API)
async def connection_api_x64(message: types.Message, state: FSMContext):
    status = await valid_token(message.text)
    if status == 200:
        await state.finish()
        api_x64 = message.text
        seller = await select_seller_by_api_x64(api_x64)
        if seller:
            await update_user_seller(seller=seller, user_id=message.from_user.id)
        else:
            seller = await add_seller(api_x64=api_x64, reserve=14, export=True, bot_enable=False,
                                      name=message.from_user.full_name, tarif=False)
            await update_user_seller(seller=seller, user_id=message.from_user.id)
            await first_scan(seller.id, seller.api_x64)
            await update_trail_fail(seller_id=seller.id)
        await message.answer(
            "\n".join(
                [
                    f'👤 {hbold("Добавление продавца")}\n',
                    f'✅ Поздравляем, {hbold("API-ключ x64")} добавлен успешно!\n',
                    f'🚙 Если вы работаете по схеме {hbold("FBS")} (продажа со склада поставщика), используйте дополнительный API-ключ, '
                    f'чтобы бот мог отслеживать новые заказы.\n'
                ]
            ), reply_markup=seller_added_keyboard(seller.id)
        )
    elif status == 400 or status == 500:
        await message.answer(
            "\n".join(
                [
                    f'👤 {hbold("Добавление продавца")}',
                    f'⏱ {datetime.datetime.now().time().strftime("%H:%M:%S")}\n',
                    f'❌{hbold("Ошибка!")}API-ключ (x64) некорректен!\n',
                    f'Отправьте правильный ключ заново в этом сообщении:',

                ]
            ), reply_markup=fail_add_seller_keyboard
        )
    else:
        await message.answer(
            "\n".join(
                [
                    f'👤 {hbold("Добавление продавца")}',
                    f'⏱ {datetime.datetime.now().time().strftime("%H:%M:%S")}\n',
                    f'❌{hbold("Ошибка!")} К сожалению сервера Wildberries не отвечают, '
                    f'пожалуйста попробуйте позже!\n',

                ]
            ), reply_markup=fail_add_seller_keyboard
        )
