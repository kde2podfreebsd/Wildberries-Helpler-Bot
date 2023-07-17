from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery

from loader import dp


@dp.callback_query_handler(text="not_working", state='*')
async def show_connection_menu(call: CallbackQuery):
    await call.message.answer("😞 К сожалению эта функция пока не работает")


@dp.message_handler(Command("dragon"), state='*')
async def show_stock_by_seller(message: types.Message):
    await message.answer("😞 К сожалению эта функция пока не работает")


@dp.message_handler(Command("export"), state='*')
async def show_stock_by_seller(message: types.Message):
    await message.answer("😞 К сожалению эта функция пока не работает")
