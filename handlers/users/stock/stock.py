from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.utils.markdown import hbold, hlink

from handlers.users.reports.tools import get_button_next_back
from handlers.users.stock.tools import get_headline
from keyboards.inline.callback_datas import set_command_seller_id, order_or_returns_callback
from keyboards.inline.stock_keyboard.stock_dynamic import stock_dynamic_keyboard
from keyboards.inline.stock_keyboard.stock_keyboard import stocks_by_seller_keyboard, show_info_stock
from loader import dp

from utils.db_api.quick_commands.seller_inquiries import count_seller_by_user, select_seller_by_user, select_seller, \
    update_filter_stocks
from utils.wb_api.method_warehouse import get_info_stocks_product, get_in_stock_stocks_product, \
    get_to_client_stocks_product, get_from_client_stocks_product, get_on_sale_stocks_product


@dp.message_handler(Command("stock"), state='*')
async def show_stocks(message: types.Message, state: FSMContext):
    await message.delete()
    await state.finish()
    user_id = message.from_user.id
    count_sellers = await count_seller_by_user(user_id=user_id)
    if count_sellers == 1:
        sellers = await select_seller_by_user(user_id)
        for i in sellers:
            seller_id = i.id
            filter_stocks = i.filter_stocks
        in_stock, to_client, from_client, on_sale = await get_info_stocks_product(seller_id)
        await message.answer("\n".join(
            [
                f'{hbold("ТОВАРЫ И ОСТАТКИ")}\n',
                f'📦 Остатки всего: {hbold(in_stock)}',
                f'🗂 Артикулы в продаже: {on_sale}',
            ]
        ), reply_markup=show_info_stock(seller_id, filter_stocks))
    elif count_sellers == 0:
        await message.answer("После поступления нового заказа от Wildberries, этот раздел станет доступен ⏳")
    else:
        sellers = await select_seller_by_user(user_id)
        await message.answer("\n".join(
            [
                f'📝 Выберите продавца для формирования отчета:',
            ]
        ), reply_markup=stocks_by_seller_keyboard(sellers))


@dp.callback_query_handler(text="back_to_stocks_by_seller")
async def back_to_show_stocks(call: types.CallbackQuery):
    user_id = call.message.chat.id
    sellers = await select_seller_by_user(user_id)
    await call.message.edit_text("\n".join(
        [
            f'📝 Выберите продавца для формирования отчета:',
        ]
    ), reply_markup=stocks_by_seller_keyboard(sellers))


@dp.callback_query_handler(set_command_seller_id.filter(command_name="stocks_by_seller"))
async def show_by_seller_stocks(call: types.CallbackQuery, callback_data: dict):
    seller_id = callback_data.get("seller_id")
    user_id = call.message.chat.id
    count_sellers = await count_seller_by_user(user_id=user_id)
    in_stock, to_client, from_client, on_sale = await get_info_stocks_product(int(seller_id))
    seller = await select_seller(int(seller_id))
    back = False
    if count_sellers > 1:
        back = True

    await call.message.edit_text("\n".join(
        [
            f'{hbold("ТОВАРЫ И ОСТАТКИ")}\n',
            f'📦 Остатки всего: {hbold(in_stock)}',
            f'🚛 В пути до клиента: {to_client}',
            f'🚚 В пути возвраты: {from_client}',
            f'🗂 Артикулы в продаже: {on_sale}',
        ]
    ), reply_markup=show_info_stock(seller_id, seller.filter_stocks, back=back))


@dp.callback_query_handler(order_or_returns_callback.filter(method="stocks"), state='*')
async def show_stocks_by_filter(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await state.finish()
    seller_id = callback_data.get("seller_id")
    seller = await select_seller(int(seller_id))
    command_name = callback_data.get("command_name")
    start = callback_data.get("start")
    end = callback_data.get("end")
    method = callback_data.get("method")
    if command_name == "in_stock":
        products = await get_in_stock_stocks_product(int(seller_id))
    elif command_name == "reverse_in_stock":
        products = await get_in_stock_stocks_product(int(seller_id))
        products = products[::-1]
    elif command_name == "to_client":
        products = await get_to_client_stocks_product(int(seller_id))
    elif command_name == "revers_to_client":
        products = await get_to_client_stocks_product(int(seller_id))
        products = products[::-1]
    elif command_name == "from_client":
        products = await get_from_client_stocks_product(int(seller_id))
    elif command_name == "revers_from_client":
        products = await get_from_client_stocks_product(int(seller_id))
        products = products[::-1]
    elif command_name == "on_sale":
        products = await get_on_sale_stocks_product(int(seller_id))
    elif command_name == "revers_on_sale":
        products = await get_on_sale_stocks_product(int(seller_id))
        products = products[::-1]
    start, end = int(start), int(end)
    next, back = await get_button_next_back(len(products), end, start)
    sorting_products = products[start:end]
    headline = await get_headline(command_name)
    string = [hbold("Мои товары:"), f'',
              f'{hbold("Сортировка:")} {headline}\n']
    is_search = False
    if seller.search is not None:
        is_search = True
        string = [hbold("Мои товары:"), f'{hbold("Поиск:")} 🔍 "{seller.search}"\n']
    await update_filter_stocks(int(seller_id), command_name)
    if sorting_products:
        for product in sorting_products:
            string.append(
                f'🆔 Артикул WB: {hlink(str(product.nmId), f"https://www.wildberries.ru/catalog/{product.nmId}/detail.aspx")}')
            string.append(f'📁 {product.subject} / {product.techSize}')
            string.append(
                f'🏷 {product.brand} / {hlink(str(product.supplierArticle), f"https://www.wildberries.ru/catalog/{product.nmId}/detail.aspx")}')
            string.append(f'🚛 В пути до клиента: {product.inWayToClient}')
            string.append(f'🚚 В пути возвраты: {product.inWayFromClient}')
            string.append(f'📊 Сейчас в продаже: {product.quantity}')
            string.append(f'📦 На складе: {product.quantityFull}\n')
    else:
        string.append(f"Ничего не найдено!")

    await call.message.edit_text(
        "\n".join(string),
        reply_markup=stock_dynamic_keyboard(seller_id=seller_id, command_name=command_name, method=method,
                                            end=end + 10, start=start + 10, next=next, back=back,is_search=is_search))
