from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.markdown import hbold

from keyboards.inline.callback_datas import set_command_seller_id
from keyboards.inline.profile_keyboard.add_delete_seller import delete_seller_keyboard
from loader import dp
from utils.db_api.quick_commands.seller_inquiries import select_seller, delete_seller


@dp.callback_query_handler(set_command_seller_id.filter(command_name="delete_seller_keyboard"))
async def seller_settings(call: types.CallbackQuery, callback_data: dict):
    seller_id = callback_data.get("seller_id")
    seller = await select_seller(seller_id=int(seller_id))
    await call.message.edit_text("\n".join(
        [
            f'🗑 {hbold("Удаление")}\n',
            f'При выполнении этой команды из бота будет удален поставщик:',
            f'👤 {seller.name}',
        ]
    ), reply_markup=delete_seller_keyboard(seller_id)
    )


@dp.callback_query_handler(set_command_seller_id.filter(command_name="delete_seller_confirm"))
async def seller_settings(call: types.CallbackQuery, callback_data: dict):
    seller_id = callback_data.get("seller_id")
    await delete_seller(seller_id=int(seller_id))
    back_keyboard = InlineKeyboardMarkup(row_width=1)
    back_button = InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_profile")
    back_keyboard.insert(back_button)
    await call.message.edit_text("\n".join(
        [
            f'🗑 {hbold("Удаление")}\n',
            f'✅ API-ключ и поставщик успешно удалены',
        ]
    ), reply_markup=back_keyboard
    )
