from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.utils.markdown import hbold, hlink

from handlers.users.reports.tools import get_data_by_period, get_button_next_back
from keyboards.inline.callback_datas import set_report_callback, set_command_seller_id
from keyboards.inline.reports_keyboard.report_dynamic import report_dynamic_keyboard
from keyboards.inline.reports_keyboard.reports_keyboard import reports_keyboard, report_by_seller_keyboard
from loader import dp
from utils.db_api.quick_commands.seller_inquiries import count_seller_by_user, select_seller_by_user, select_seller, \
    update_filter_bought
from utils.wb_api.method_warehouse import get_full_report
from utils.wb_api.tools import array_slice, get_normal_number


@dp.message_handler(Command("reports"), state='*')
async def show_reports(message: types.Message, state: FSMContext):
    await message.delete()
    await state.finish()
    user_id = message.from_user.id
    count_sellers = await count_seller_by_user(user_id=user_id)
    if count_sellers == 1:
        sellers = await select_seller_by_user(user_id)
        for i in sellers:
            seller_id = i.id
            filter_bought = i.filter_bought
            filter_orders = i.filter_orders
        sorting_list = await get_full_report(seller_id)
        string = [f'{hbold("Сводка")}\n']
        for i in sorting_list:
            if i == "today":
                name_sorting = "Сегодня"
            elif i == "yesterday":
                name_sorting = "Вчера"
            elif i == "in_7_days":
                name_sorting = "ЗА 7 ДНЕЙ"
            else:
                name_sorting = "ЗА 30 ДНЕЙ"
            string.append(hbold(name_sorting))
            string.append(
                f'🛒 Заказы:        {sorting_list[i]["count_orders"]} на {await get_normal_number(sorting_list[i]["amount_orders"])} ₽')
            string.append(
                f'💳 Выкупы:        {sorting_list[i]["count_payment"]} на {await get_normal_number(sorting_list[i]["amount_payment"])} ₽')
            string.append(
                f'🚚 Возвраты:      {sorting_list[i]["count_refund"]} на {await get_normal_number(sorting_list[i]["amount_refund"])} ₽\n')
        string.append(f'ℹ️ Фактические данные могут отличаться.')
        await message.answer(
            "\n".join(string), reply_markup=reports_keyboard(seller_id, filter_bought, filter_orders))
    elif count_sellers == 0:
        await message.answer("После поступления нового заказа от Wildberries, этот раздел станет доступен ⏳")
    else:
        sellers = await select_seller_by_user(user_id)
        await message.answer("\n".join(
            [
                f'📝 Выберите продавца для формирования отчета:',
            ]
        ), reply_markup=report_by_seller_keyboard(sellers))


@dp.callback_query_handler(text="back_to_report_by_seller")
async def back_to_show_reports(call: types.CallbackQuery):
    user_id = call.message.chat.id
    sellers = await select_seller_by_user(user_id)
    await call.message.edit_text("\n".join(
        [
            f'📝 Выберите продавца для формирования отчета:',
        ]
    ), reply_markup=report_by_seller_keyboard(sellers))


@dp.callback_query_handler(set_command_seller_id.filter(command_name="report_by_seller"), state='*')
async def show_by_seller_reports(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await state.finish()
    seller_id = callback_data.get("seller_id")
    user_id = call.message.chat.id
    seller = await select_seller(seller_id=int(seller_id))
    sorting_list = await get_full_report(seller.id)
    count_sellers = await count_seller_by_user(user_id=user_id)
    back = True
    if count_sellers < 2:
        back = False
    string = [f'{hbold("Сводка")}\n']
    for i in sorting_list:
        if i == "today":
            name_sorting = "Сегодня"
        elif i == "yesterday":
            name_sorting = "Вчера"
        elif i == "in_7_days":
            name_sorting = "ЗА 7 ДНЕЙ"
        else:
            name_sorting = "ЗА 30 ДНЕЙ"
        string.append(hbold(name_sorting))
        string.append(
            f'🛒 Заказы:        {sorting_list[i]["count_orders"]} на {await get_normal_number(sorting_list[i]["amount_orders"])} ₽')
        string.append(
            f'💳 Выкупы:        {sorting_list[i]["count_payment"]} на {await get_normal_number(sorting_list[i]["amount_payment"])} ₽')
        string.append(
            f'🚚 Возвраты:      {sorting_list[i]["count_refund"]} на {await get_normal_number(sorting_list[i]["amount_refund"])} ₽\n')
    string.append(f'ℹ️ Фактические данные могут отличаться.')
    await call.message.edit_text(
        "\n".join(string),
        reply_markup=reports_keyboard(seller_id, seller.filter_bought, seller.filter_orders, back=back))


@dp.callback_query_handler(set_report_callback.filter(command_name="subject"), state='*')
async def show_reports_subject(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    period = callback_data.get("method")
    await state.finish()
    seller_id = callback_data.get("seller_id")
    seller = await select_seller(int(seller_id))
    command_name = callback_data.get("command_name")
    start = callback_data.get("start")
    end = callback_data.get("end")
    start, end = int(start), int(end)
    data, name_tag = await get_data_by_period(period, seller_id, command_name)
    next, back = await get_button_next_back(len(data), end, start)
    await update_filter_bought(int(seller_id), command_name)
    string = [hbold(name_tag), '']
    is_search = False
    if seller.search is not None:
        string = [hbold(name_tag), f'{hbold("Поиск:")} 🔍 "{seller.search}"\n']
        is_search = True
    paginator = array_slice(data, start, end)
    if paginator:
        for i in paginator:
            string.append(hbold(i))
            string.append(
                f'🛒 Заказы:        {paginator[i]["count_orders"]} на {await get_normal_number(paginator[i]["amount_orders"])} ₽')
            string.append(
                f'💳 Выкупы:        {paginator[i]["count_payment"]} на {await get_normal_number(paginator[i]["amount_payment"])} ₽')
            string.append(
                f'🚚 Возвраты:      {paginator[i]["count_refund"]} на {await get_normal_number(paginator[i]["amount_refund"])} ₽\n')
    else:
        string.append(f"Ничего не найдено!")
    await call.message.edit_text(
        "\n".join(string),
        reply_markup=report_dynamic_keyboard(seller_id=seller_id, command_name=command_name, period=period,
                                             end=end + 10, start=start + 10, next=next, back=back, is_search=is_search))


@dp.callback_query_handler(set_report_callback.filter(command_name="vendor_code"), state='*')
async def show_reports_vendor_code(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    period = callback_data.get("method")
    await state.finish()
    seller_id = callback_data.get("seller_id")
    seller = await select_seller(int(seller_id))
    command_name = callback_data.get("command_name")
    start = callback_data.get("start")
    end = callback_data.get("end")
    start, end = int(start), int(end)
    data, name_tag = await get_data_by_period(period, seller_id, command_name)
    next, back = await get_button_next_back(len(data), end, start)
    string = [hbold(name_tag), '']
    is_search = False
    if seller.search is not None:
        string = [hbold(name_tag), f'{hbold("Поиск:")} 🔍 "{seller.search}"\n']
        is_search = True
    await update_filter_bought(int(seller_id), command_name)
    paginator = array_slice(data, start, end)
    if paginator:
        for i in paginator:
            string.append(hlink(str(i), f'https://www.wildberries.ru/catalog/{i}/detail.aspx'))
            string.append(
                f'🛒 Заказы:        {paginator[i]["count_orders"]} на {await get_normal_number(paginator[i]["amount_orders"])} ₽')
            string.append(
                f'💳 Выкупы:        {paginator[i]["count_payment"]} на {await get_normal_number(paginator[i]["amount_payment"])} ₽')
            string.append(
                f'🚚 Возвраты:      {paginator[i]["count_refund"]} на {await get_normal_number(paginator[i]["amount_refund"])} ₽\n')
            string.append(f'📁 {paginator[i]["subject"]}')
            string.append(f'🏷 {paginator[i]["brand"]} / {paginator[i]["supplierArticle"]}\n')
    else:
        string.append(f"Ничего не найдено!")
    await call.message.edit_text(
        "\n".join(string),
        reply_markup=report_dynamic_keyboard(seller_id=seller_id, command_name=command_name, period=period,
                                             end=end + 10, start=start + 10, next=next, back=back, is_search=is_search))


@dp.callback_query_handler(set_report_callback.filter(command_name="category"), state='*')
async def show_reports_category(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    period = callback_data.get("method")
    await state.finish()
    seller_id = callback_data.get("seller_id")
    seller = await select_seller(int(seller_id))
    command_name = callback_data.get("command_name")
    start = callback_data.get("start")
    end = callback_data.get("end")
    start, end = int(start), int(end)
    data, name_tag = await get_data_by_period(period, seller_id, command_name)
    next, back = await get_button_next_back(len(data), end, start)
    await update_filter_bought(int(seller_id), command_name)
    string = [hbold(name_tag), '']
    is_search = False
    if seller.search is not None:
        string = [hbold(name_tag), f'{hbold("Поиск:")} 🔍 "{seller.search}"\n']
        is_search = True
    paginator = array_slice(data, start, end)
    if paginator:
        for i in paginator:
            string.append(hbold(i))
            string.append(
                f'🛒 Заказы:        {paginator[i]["count_orders"]} на {await get_normal_number(paginator[i]["amount_orders"])} ₽')
            string.append(
                f'💳 Выкупы:        {paginator[i]["count_payment"]} на {await get_normal_number(paginator[i]["amount_payment"])} ₽')
            string.append(
                f'🚚 Возвраты:      {paginator[i]["count_refund"]} на {await get_normal_number(paginator[i]["amount_refund"])} ₽\n')
    else:
        string.append(f"Ничего не найдено!")
    await call.message.edit_text(
        "\n".join(string),
        reply_markup=report_dynamic_keyboard(seller_id=seller_id, command_name=command_name, period=period,
                                             end=end + 10, start=start + 10, next=next, back=back, is_search=is_search))


@dp.callback_query_handler(set_report_callback.filter(command_name="brand"), state='*')
async def show_reports_brand(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    period = callback_data.get("method")
    await state.finish()
    seller_id = callback_data.get("seller_id")
    seller = await select_seller(int(seller_id))
    command_name = callback_data.get("command_name")
    start = callback_data.get("start")
    end = callback_data.get("end")
    start, end = int(start), int(end)
    data, name_tag = await get_data_by_period(period, seller_id, command_name)
    next, back = await get_button_next_back(len(data), end, start)
    await update_filter_bought(int(seller_id), command_name)
    string = [hbold(name_tag), '']
    is_search = False
    if seller.search is not None:
        string = [hbold(name_tag), f'{hbold("Поиск:")} 🔍 "{seller.search}"\n']
        is_search = True
    paginator = array_slice(data, start, end)
    if paginator:
        for i in paginator:
            string.append(hbold(i))
            string.append(
                f'🛒 Заказы:        {paginator[i]["count_orders"]} на {await get_normal_number(paginator[i]["amount_orders"])} ₽')
            string.append(
                f'💳 Выкупы:        {paginator[i]["count_payment"]} на {await get_normal_number(paginator[i]["amount_payment"])} ₽')
            string.append(
                f'🚚 Возвраты:      {paginator[i]["count_refund"]} на {await get_normal_number(paginator[i]["amount_refund"])} ₽\n')
    else:
        string.append(f"Ничего не найдено!")
    await call.message.edit_text(
        "\n".join(string),
        reply_markup=report_dynamic_keyboard(seller_id=seller_id, command_name=command_name, period=period,
                                             end=end + 10, start=start + 10, next=next, back=back, is_search=is_search))


@dp.callback_query_handler(set_report_callback.filter(command_name="region"), state='*')
async def show_reports_region(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    period = callback_data.get("method")
    await state.finish()
    seller_id = callback_data.get("seller_id")
    seller = await select_seller(int(seller_id))
    command_name = callback_data.get("command_name")
    start = callback_data.get("start")
    end = callback_data.get("end")
    start, end = int(start), int(end)
    data, name_tag = await get_data_by_period(period, seller_id, command_name)
    next, back = await get_button_next_back(len(data), end, start)
    await update_filter_bought(int(seller_id), command_name)
    string = [hbold(name_tag), '']
    is_search = False
    if seller.search is not None:
        string = [hbold(name_tag), f'{hbold("Поиск:")} 🔍 "{seller.search}"\n']
        is_search = True
    paginator = array_slice(data, start, end)
    if paginator:
        for i in paginator:
            name = i
            if not name:
                name = "Неизвестно"
            string.append(hbold(name))
            string.append(
                f'🛒 Заказы:        {paginator[i]["count_orders"]} на {await get_normal_number(paginator[i]["amount_orders"])} ₽')
            string.append(
                f'💳 Выкупы:        {paginator[i]["count_payment"]} на {await get_normal_number(paginator[i]["amount_payment"])} ₽')
            string.append(
                f'🚚 Возвраты:      {paginator[i]["count_refund"]} на {await get_normal_number(paginator[i]["amount_refund"])} ₽\n')
    else:
        string.append(f"Ничего не найдено!")
    await call.message.edit_text(
        "\n".join(string),
        reply_markup=report_dynamic_keyboard(seller_id=seller_id, command_name=command_name, period=period,
                                             end=end + 10, start=start + 10, next=next, back=back, is_search=is_search))


@dp.callback_query_handler(set_report_callback.filter(command_name="grouping"), state='*')
async def show_reports_no_grouping(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    period = callback_data.get("method")
    await state.finish()
    seller_id = callback_data.get("seller_id")
    seller = await select_seller(int(seller_id))
    command_name = callback_data.get("command_name")
    start = callback_data.get("start")
    end = callback_data.get("end")
    start, end = int(start), int(end)
    data, name_tag = await get_data_by_period(period, seller_id, command_name)
    await update_filter_bought(int(seller_id), command_name)
    string = [hbold(name_tag), '']
    is_search = False
    if seller.search is not None:
        string = [hbold(name_tag), f'{hbold("Поиск:")} 🔍 "{seller.search}"\n']
        is_search = True
    if data:
        string.append(f'🛒 Заказы:        {data["count_orders"]} на {await get_normal_number(data["amount_orders"])} ₽')
        string.append(
            f'💳 Выкупы:        {data["count_payment"]} на {await get_normal_number(data["amount_payment"])} ₽')
        string.append(
            f'🚚 Возвраты:      {data["count_refund"]} на {await get_normal_number(data["amount_refund"])} ₽\n')
    else:
        string.append(f"Ничего не найдено!")
    await call.message.edit_text(
        "\n".join(string),
        reply_markup=report_dynamic_keyboard(seller_id=seller_id, command_name=command_name, period=period,
                                             end=end + 10, start=start + 10, next=False, back=False,
                                             is_search=is_search))
