from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.users.reports.reports import show_reports_subject, show_reports_vendor_code, show_reports_category, \
    show_reports_brand, show_reports_region, show_reports_no_grouping
from handlers.users.reports.sorting_by_orders import show_sales, show_orders, show_returns
from handlers.users.stock.stock import show_stocks_by_filter
from keyboards.inline.callback_datas import set_search_callback
from keyboards.inline.reports_keyboard.set_search_keyboard import from_report_dynamic_keyboard, \
    from_report_orders_keyboard
from loader import dp
from states import States
from utils.db_api.quick_commands.seller_inquiries import update_set_search, delete_set_search


@dp.callback_query_handler(set_search_callback.filter(from_keyboard="report_dynamic"))
async def show_set_search_report(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    period = callback_data.get("method")
    seller_id = callback_data.get("seller_id")
    command_name = callback_data.get("command_name")
    start = callback_data.get("start")
    end = callback_data.get("end")
    start, end = int(start), int(end)
    await States.SET_SEARCH.set()
    await state.update_data(method=period)
    await state.update_data(call=call)
    await state.update_data(seller_id=seller_id)
    await state.update_data(callback_data=callback_data)
    await state.update_data(command_name=command_name)
    await call.message.edit_text("\n".join(
        [
            f'🔍 Искать можно по артикулу WB, артикулу поставщика,  '
            f'бренду или названию предмета.\n',
            f'Введите поисковый запрос в этом сообщении: 👇🏻',
        ]
    ), reply_markup=from_report_dynamic_keyboard(seller_id, command_name, period, end, start))


@dp.callback_query_handler(set_search_callback.filter(from_keyboard="report_orders"))
async def show_set_search_orders(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    method = callback_data.get("method")
    seller_id = callback_data.get("seller_id")
    command_name = callback_data.get("command_name")
    start = callback_data.get("start")
    end = callback_data.get("end")
    start, end = int(start), int(end)
    await States.SET_SEARCH.set()
    await state.update_data(method=method)
    await state.update_data(call=call)
    await state.update_data(seller_id=seller_id)
    await state.update_data(callback_data=callback_data)
    await state.update_data(command_name=command_name)
    await call.message.edit_text("\n".join(
        [
            f'🔍 Искать можно по артикулу WB, артикулу поставщика,  '
            f'бренду или названию предмета.\n',
            f'Введите поисковый запрос в этом сообщении: 👇🏻',
        ]
    ), reply_markup=from_report_orders_keyboard(seller_id, command_name, method, end, start))


@dp.callback_query_handler(set_search_callback.filter(from_keyboard="report_stocks"))
async def show_set_search_stocks(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    method = callback_data.get("method")
    seller_id = callback_data.get("seller_id")
    command_name = callback_data.get("command_name")
    start = callback_data.get("start")
    end = callback_data.get("end")
    start, end = int(start), int(end)
    await States.SET_SEARCH.set()
    await state.update_data(method=method)
    await state.update_data(seller_id=seller_id)
    await state.update_data(call=call)
    await state.update_data(callback_data=callback_data)
    await state.update_data(command_name=command_name)
    await call.message.edit_text("\n".join(
        [
            f'🔍 Искать можно по артикулу WB, артикулу поставщика,  '
            f'бренду или названию предмета.\n',
            f'Введите поисковый запрос в этом сообщении: 👇🏻',
        ]
    ), reply_markup=from_report_orders_keyboard(seller_id, command_name, method, end, start))


@dp.message_handler(state=States.SET_SEARCH)
async def set_search(message: types.Message, state: FSMContext):
    data = await state.get_data()
    seller_id = data.get("seller_id")
    await update_set_search(int(seller_id), message.text)
    await message.delete()
    method = data.get("method")
    call = data.get("call")
    callback_data = data.get("callback_data")
    command_name = data.get("command_name")
    if method == "stocks":
        await show_stocks_by_filter(call, callback_data, state)
    elif method == "sales":
        await show_sales(call, callback_data, state)
    elif method == "orders":
        await show_orders(call, callback_data, state)
    elif method == "returns":
        await show_returns(call, callback_data, state)

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


@dp.callback_query_handler(set_search_callback.filter(from_keyboard="delete_search"))
async def delete_search(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    method = callback_data.get("method")
    seller_id = callback_data.get("seller_id")
    await delete_set_search(int(seller_id))
    command_name = callback_data.get("command_name")
    if method == "stocks":
        await show_stocks_by_filter(call, callback_data, state)
    elif method == "sales":
        await show_sales(call, callback_data, state)
    elif method == "orders":
        await show_orders(call, callback_data, state)
    elif method == "returns":
        await show_returns(call, callback_data, state)

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
