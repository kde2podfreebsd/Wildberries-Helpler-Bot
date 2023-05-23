from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hbold, hlink, hitalic

from handlers.users.reports.tools import get_button_next_back
from keyboards.inline.callback_datas import order_or_returns_callback
from keyboards.inline.reports_keyboard.orders_dynamic import report_dynamic_order_keyboard
from loader import dp
from utils.db_api.quick_commands.seller_inquiries import update_filter_orders, select_seller

from utils.wb_api.method_warehouse import sorting_sales_no_grouping, sorting_by_days, \
    sorting_returns_no_grouping, sorting_by_month, sorting_orders_no_grouping
from utils.wb_api.tools import array_slice, get_normal_number


@dp.callback_query_handler(order_or_returns_callback.filter(method="sales"), state='*')
async def show_sales(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await state.finish()
    command_name = callback_data.get("command_name")
    seller_id = callback_data.get("seller_id")
    seller = await select_seller(int(seller_id))
    method = callback_data.get("method")
    string = [hbold("Выкупы"), '']
    is_search = False
    if seller.search is not None:
        string = [hbold("Выкупы"), f'{hbold("Поиск:")} 🔍 "{seller.search}"\n']
        is_search = True
    if command_name == "no_grouping":
        await update_filter_orders(int(seller_id), command_name)
        data = await sorting_sales_no_grouping(int(seller_id))
        await show_sales_no_grouping(call, callback_data, data, string, is_search)
    elif command_name == "by_days":
        await update_filter_orders(int(seller_id), command_name)
        data = await sorting_by_days(int(seller_id), method)
        await show_by_days(call, callback_data, data, string, is_search)
    elif command_name == "by_month":
        await update_filter_orders(int(seller_id), command_name)
        data = await sorting_by_month(int(seller_id), method)
        await show_by_month(call, callback_data, data, string, is_search)


@dp.callback_query_handler(order_or_returns_callback.filter(method="orders"), state='*')
async def show_orders(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await state.finish()
    command_name = callback_data.get("command_name")
    seller_id = callback_data.get("seller_id")
    seller = await select_seller(int(seller_id))
    method = callback_data.get("method")
    string = [hbold("Заказы"), '']
    is_search = False
    if seller.search is not None:
        string = [hbold("Заказы"), f'{hbold("Поиск:")} 🔍 "{seller.search}"\n']
        is_search = True
    if command_name == "no_grouping":
        await update_filter_orders(int(seller_id), command_name)
        data = await sorting_orders_no_grouping(int(seller_id))
        await show_orders_no_grouping(call, callback_data, data, string, is_search)
    elif command_name == "by_days":
        await update_filter_orders(int(seller_id), command_name)
        data = await sorting_by_days(int(seller_id), method)
        await show_by_days(call, callback_data, data, string, is_search)
    elif command_name == "by_month":
        await update_filter_orders(int(seller_id), command_name)
        data = await sorting_by_month(int(seller_id), method)
        await show_by_month(call, callback_data, data, string, is_search)


@dp.callback_query_handler(order_or_returns_callback.filter(method="returns"), state='*')
async def show_returns(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await state.finish()
    command_name = callback_data.get("command_name")
    seller_id = callback_data.get("seller_id")
    seller = await select_seller(int(seller_id))
    method = callback_data.get("method")
    string = [hbold("Возвраты"), '']
    is_search = False
    if seller.search is not None:
        string = [hbold("Возвраты"), f'{hbold("Поиск:")} 🔍 "{seller.search}"\n']
        is_search = True
    if command_name == "no_grouping":
        await update_filter_orders(int(seller_id), command_name)
        data = await sorting_returns_no_grouping(int(seller_id))
        await show_returns_no_grouping(call, callback_data, data, string, is_search)
    elif command_name == "by_days":
        await update_filter_orders(int(seller_id), command_name)
        data = await sorting_by_days(int(seller_id), method)
        await show_returns_by_days(call, callback_data, data, string, is_search)
    elif command_name == "by_month":
        await update_filter_orders(int(seller_id), command_name)
        data = await sorting_by_month(int(seller_id), method)
        await show_returns_by_month(call, callback_data, data, string, is_search)


async def show_orders_no_grouping(call: types.CallbackQuery, callback_data: dict, data, string, is_search):
    seller_id = callback_data.get("seller_id")
    command_name = callback_data.get("command_name")
    start = callback_data.get("start")
    end = callback_data.get("end")
    method = callback_data.get("method")
    start, end = int(start), int(end)
    next, back = await get_button_next_back(len(data), end, start)
    sorting_orders = data[start:end]

    if sorting_orders:
        for order in sorting_orders:
            string.append(hitalic(order.date.strftime("%Y.%m.%d %H:%M")))
            string.append(f'🛒 {await get_normal_number(int(order.price))} ₽')
            string.append(
                f'🆔 Артикул WB: {hlink(str(order.nmId), f"https://www.wildberries.ru/catalog/{order.nmId}/detail.aspx")}')
            string.append(f'📁 {order.subject} / {order.techSize}')
            string.append(
                f'🏷 {order.brand} / {hlink(str(order.supplierArticle), f"https://www.wildberries.ru/catalog/{order.nmId}/detail.aspx")}')
            if order.oblast:
                string.append(f'🌐 {order.oblast}')

            string.append('')
    else:
        string.append(f"Ничего не найдено!")
    await call.message.edit_text(
        "\n".join(string),
        reply_markup=report_dynamic_order_keyboard(seller_id=seller_id, command_name=command_name, method=method,
                                                   end=end + 10, start=start + 10, next=next, back=back,
                                                   is_search=is_search))


async def show_sales_no_grouping(call: types.CallbackQuery, callback_data: dict, data, string, is_search):
    seller_id = callback_data.get("seller_id")
    command_name = callback_data.get("command_name")
    start = callback_data.get("start")
    end = callback_data.get("end")
    method = callback_data.get("method")
    start, end = int(start), int(end)
    next, back = await get_button_next_back(len(data), end, start)
    sorting_orders = data[start:end]

    if sorting_orders:
        for order in sorting_orders:
            string.append(hitalic(order.date.strftime("%Y.%m.%d %H:%M")))
            string.append(f'🛒 {await get_normal_number(int(order.forPay))} ₽')
            string.append(
                f'🆔 Артикул WB: {hlink(str(order.nmId), f"https://www.wildberries.ru/catalog/{order.nmId}/detail.aspx")}')
            string.append(f'📁 {order.subject} / {order.techSize}')
            string.append(
                f'🏷 {order.brand} / {hlink(str(order.supplierArticle), f"https://www.wildberries.ru/catalog/{order.nmId}/detail.aspx")}')
            if order.regionName:
                string.append(f'🌐 {order.regionName}')

            string.append('')
    else:
        string.append(f"Ничего не найдено!")
    await call.message.edit_text(
        "\n".join(string),
        reply_markup=report_dynamic_order_keyboard(seller_id=seller_id, command_name=command_name, method=method,
                                                   end=end + 10, start=start + 10, next=next, back=back,
                                                   is_search=is_search))


async def show_by_days(call: types.CallbackQuery, callback_data: dict, data, string, is_search):
    seller_id = callback_data.get("seller_id")
    command_name = callback_data.get("command_name")
    start = callback_data.get("start")
    end = callback_data.get("end")
    method = callback_data.get("method")
    start, end = int(start), int(end)
    next, back = await get_button_next_back(len(data), end, start)
    paginator = array_slice(data, start, end)
    if paginator:
        for i in paginator:
            count = paginator[i]["count"]
            amount = paginator[i]["amount"]
            nmId = paginator[i]["nmId"]
            subject = paginator[i]["subject"]
            techSize = paginator[i]["techSize"]
            brand = paginator[i]["brand"]
            supplierArticle = paginator[i]["supplierArticle"]
            string.append(hitalic(i.split()[0]))
            string.append(f'🛒 {hbold(f"Всего: {count}")} на {hbold(f"{await get_normal_number(count * int(amount))} ₽")}')
            string.append(
                f'🆔 Артикул WB: {hlink(str(nmId), f"https://www.wildberries.ru/catalog/{nmId}/detail.aspx")}')
            string.append(f'📁 {subject} / {techSize}')
            string.append(
                f'🏷 {brand} / {hlink(str(supplierArticle), f"https://www.wildberries.ru/catalog/{nmId}/detail.aspx")}')
            string.append(f'💰 Цена: {hbold(f"{int(amount)}₽")} (средняя)\n')
    else:
        string.append(f"Ничего не найдено!")
    await call.message.edit_text(
        "\n".join(string),
        reply_markup=report_dynamic_order_keyboard(seller_id=seller_id, command_name=command_name, method=method,
                                                   end=end + 10, start=start + 10, next=next, back=back,
                                                   is_search=is_search))


async def show_by_month(call: types.CallbackQuery, callback_data: dict, data, string, is_search):
    seller_id = callback_data.get("seller_id")
    command_name = callback_data.get("command_name")
    start = callback_data.get("start")
    end = callback_data.get("end")
    method = callback_data.get("method")
    start, end = int(start), int(end)
    next, back = await get_button_next_back(len(data), end, start)
    paginator = array_slice(data, start, end)
    if paginator:
        for i in paginator:
            count = paginator[i]["count"]
            amount = paginator[i]["amount"]
            nmId = paginator[i]["nmId"]
            subject = paginator[i]["subject"]
            techSize = paginator[i]["techSize"]
            brand = paginator[i]["brand"]
            supplierArticle = paginator[i]["supplierArticle"]
            string.append(hitalic(i.split()[0]))
            string.append(f'🛒 {hbold(f"Всего: {count}")} на {hbold(f"{await get_normal_number(count * int(amount))} ₽")}')
            string.append(
                f'🆔 Артикул WB: {hlink(str(nmId), f"https://www.wildberries.ru/catalog/{nmId}/detail.aspx")}')
            string.append(f'📁 {subject} / {techSize}')
            string.append(
                f'🏷 {brand} / {hlink(str(supplierArticle), f"https://www.wildberries.ru/catalog/{nmId}/detail.aspx")}')
            string.append(f'💰 Цена: {hbold(f"{int(amount)}₽")} (средняя)\n')
    else:
        string.append(f"Ничего не найдено!")
    await call.message.edit_text(
        "\n".join(string),
        reply_markup=report_dynamic_order_keyboard(seller_id=seller_id, command_name=command_name, method=method,
                                                   end=end + 10, start=start + 10, next=next, back=back,
                                                   is_search=is_search))


async def show_returns_by_days(call: types.CallbackQuery, callback_data: dict, data, string, is_search):
    seller_id = callback_data.get("seller_id")
    command_name = callback_data.get("command_name")
    start = callback_data.get("start")
    end = callback_data.get("end")
    method = callback_data.get("method")
    start, end = int(start), int(end)
    next, back = await get_button_next_back(len(data), end, start)
    paginator = array_slice(data, start, end)
    if paginator:
        for i in paginator:
            count = paginator[i]["count"]
            amount = paginator[i]["amount"]
            nmId = paginator[i]["nmId"]
            subject = paginator[i]["subject"]
            techSize = paginator[i]["techSize"]
            brand = paginator[i]["brand"]
            supplierArticle = paginator[i]["supplierArticle"]
            string.append(hitalic(i.split()[0]))
            string.append(f'🛒 {hbold(f"Всего: {count}")} на {hbold(f"{await get_normal_number(-count * int(amount))} ₽")}')
            string.append(
                f'🆔 Артикул WB: {hlink(str(nmId), f"https://www.wildberries.ru/catalog/{nmId}/detail.aspx")}')
            string.append(f'📁 {subject} / {techSize}')
            string.append(
                f'🏷 {brand} / {hlink(str(supplierArticle), f"https://www.wildberries.ru/catalog/{nmId}/detail.aspx")}')
            string.append(f'🚚 → Склад WB: {hbold(f"{count * 33}")}\n')
    else:
        string.append(f"Ничего не найдено!")
    await call.message.edit_text(
        "\n".join(string),
        reply_markup=report_dynamic_order_keyboard(seller_id=seller_id, command_name=command_name, method=method,
                                                   end=end + 10, start=start + 10, next=next, back=back,
                                                   is_search=is_search))


async def show_returns_by_month(call: types.CallbackQuery, callback_data: dict, data, string, is_search):
    seller_id = callback_data.get("seller_id")
    command_name = callback_data.get("command_name")
    start = callback_data.get("start")
    end = callback_data.get("end")
    method = callback_data.get("method")
    start, end = int(start), int(end)
    next, back = await get_button_next_back(len(data), end, start)
    paginator = array_slice(data, start, end)
    if paginator:
        for i in paginator:
            count = paginator[i]["count"]
            amount = paginator[i]["amount"]
            nmId = paginator[i]["nmId"]
            subject = paginator[i]["subject"]
            techSize = paginator[i]["techSize"]
            brand = paginator[i]["brand"]
            supplierArticle = paginator[i]["supplierArticle"]
            string.append(hitalic(i.split()[0]))
            string.append(f'🛒 {hbold(f"Всего: {count}")} на {hbold(f"{await get_normal_number(-count * int(amount))} ₽")}')
            string.append(
                f'🆔 Артикул WB: {hlink(str(nmId), f"https://www.wildberries.ru/catalog/{nmId}/detail.aspx")}')
            string.append(f'📁 {subject} / {techSize}')
            string.append(
                f'🏷 {brand} / {hlink(str(supplierArticle), f"https://www.wildberries.ru/catalog/{nmId}/detail.aspx")}')
            string.append(f'🚚 → Склад WB: {hbold(f"{count * 33}")}\n')
    else:
        string.append(f"Ничего не найдено!")
    await call.message.edit_text(
        "\n".join(string),
        reply_markup=report_dynamic_order_keyboard(seller_id=seller_id, command_name=command_name, method=method,
                                                   end=end + 10, start=start + 10, next=next, back=back,
                                                   is_search=is_search))


async def show_returns_no_grouping(call: types.CallbackQuery, callback_data: dict, data, string, is_search):
    seller_id = callback_data.get("seller_id")
    command_name = callback_data.get("command_name")
    start = callback_data.get("start")
    end = callback_data.get("end")
    method = callback_data.get("method")
    start, end = int(start), int(end)
    next, back = await get_button_next_back(len(data), end, start)
    sorting_orders = data[start:end]

    if sorting_orders:
        for order in sorting_orders:
            string.append(hitalic(order.date.strftime("%Y.%m.%d %H:%M")))
            string.append(f'🛒 {await get_normal_number(int(order.forPay) * -1)} ₽')
            string.append(
                f'🆔 Артикул WB: {hlink(str(order.nmId), f"https://www.wildberries.ru/catalog/{order.nmId}/detail.aspx")}')
            string.append(f'📁 {order.subject} / {order.techSize}')
            string.append(
                f'🏷 {order.brand} / {hlink(str(order.supplierArticle), f"https://www.wildberries.ru/catalog/{order.nmId}/detail.aspx")}')
            if order.regionName:
                string.append(f'🚚 {order.regionName} → Склад WB: 33₽')

            string.append('')
    else:
        string.append(f"Ничего не найдено!")
    await call.message.edit_text(
        "\n".join(string),
        reply_markup=report_dynamic_order_keyboard(seller_id=seller_id, command_name=command_name, method=method,
                                                   end=end + 10, start=start + 10, next=next, back=back,
                                                   is_search=is_search))
