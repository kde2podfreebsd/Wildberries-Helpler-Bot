import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hbold

from handlers.users.reports.reports import show_reports_subject, show_reports_vendor_code, show_reports_category, \
    show_reports_brand, show_reports_region, show_reports_no_grouping
from keyboards.inline.callback_datas import set_another_period_callback
from keyboards.inline.reports_keyboard.reports_keyboard import back_to_reports
from loader import dp
from states import States


@dp.callback_query_handler(set_another_period_callback.filter(filter="another_period"))
async def show_set_another_period(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    seller_id = callback_data.get("seller_id")
    command_name = callback_data.get("command_name")
    await States.ANOTHER_PERIOD.set()
    await state.update_data(seller_id=seller_id)
    await state.update_data(command_name=command_name)
    await state.update_data(call=call)
    await call.message.edit_text("\n".join(
        [
            f'📝 Введите дату или диапазон дат в этом сообщении:\n',
            f'{hbold("Пример 1:")} 23.05.2022',
            f'{hbold("Пример 2:")} 09.05.2022 - 16.05.2022',
        ]
    ), reply_markup=back_to_reports(seller_id))


@dp.message_handler(state=States.ANOTHER_PERIOD)
async def set_search(message: types.Message, state: FSMContext):
    data = await state.get_data()
    seller_id = data.get("seller_id")
    command_name = data.get("command_name")
    call = data.get("call")
    date = message.text
    if len(date) <= 10:
        try:
            datetime.datetime.strptime(date, "%d.%m.%Y")
            await state.finish()
            callback_data = {"method": f"{date}", "command_name": command_name, "seller_id": seller_id,
                             "start": 0,
                             "end": 9}
            await message.delete()
            await show_another_period(call, callback_data, state)
        except Exception:
            print("Ошибка")
    else:
        try:
            date = date.split('-')
            date1 = date[0].strip()
            date2 = date[1].strip()
            datetime.datetime.strptime(date1, "%d.%m.%Y")
            datetime.datetime.strptime(date2, "%d.%m.%Y")
            await state.finish()
            callback_data = {"method": f"{date1}-{date2}", "command_name": command_name, "seller_id": seller_id,
                             "start": 0,
                             "end": 9}
            await message.delete()
            await show_another_period(call, callback_data, state)
        except Exception:
            print("Ошибка")


async def show_another_period(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    command_name = callback_data.get("command_name")
    if command_name == "subject":
        await show_reports_subject(call, callback_data, state)
    elif command_name == "vendor_code":
        await show_reports_vendor_code(call, callback_data, state)
    elif command_name == "category":
        await show_reports_category(call, callback_data, state)
    elif command_name == "brand":
        await show_reports_brand(call, callback_data, state)
    elif command_name == "region":
        await show_reports_region(call, callback_data, state)
    elif command_name == "grouping":
        await show_reports_no_grouping(call, callback_data, state)
