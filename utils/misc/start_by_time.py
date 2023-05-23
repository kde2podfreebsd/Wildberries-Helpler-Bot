import asyncio
import datetime
import requests

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.markdown import hbold, hcode
from loguru import logger

from data.config import AMOUNT_TARIFF
from loader import dp
from utils.db_api.db_gino import ProductsOrders, ProductsStocks, ProductsBought
from utils.db_api.quick_commands.product_inquiries import update_sales_products, update_stocks_products, \
    update_ordered_products, get_order_by_number, deleting_items, get_sale_by_number
from utils.db_api.quick_commands.seller_inquiries import update_last_scan_sales, \
    update_last_scan_orders, select_all_sellers_enable, select_seller, overdue_tariff, update_trail, overdue_free_trail, \
    returns_unsubscribed_sellers, for_notification_tariff
from utils.db_api.quick_commands.user_inquiries import select_user_by_seller, update_balance
from utils.wb_api.method_warehouse import get_sales_products, get_stock_products, get_ordered_products, \
    get_ordered_products_fbc
from utils.wb_api.sorting import SortingOrders
from utils.wb_api.tools import get_date, date_search, get_normal_number


async def update_all_bought(wait_for):
    """ Обновление заказов и выкупов
        :param wait_for: время в минутах
     """
    while True:
        await asyncio.sleep(wait_for * 10)
        sellers = await select_all_sellers_enable()
        for seller in sellers:
            last_scan_orders = get_date(days=1)
            if seller.api_x64:
                if seller.last_scan_sales is None:
                    last_scan_sales = get_date(days=90)
                else:
                    last_scan_sales = get_date(days=1)

                sales = await get_sales_products(seller.api_x64, last_scan_sales)
                orders = await get_ordered_products(seller.api_x64, last_scan_orders)
                date = datetime.datetime.today()
                if seller.last_scan_sales is None:
                    if sales:
                        for sale in sales:
                            await update_sales_products(seller.id, sale)
                        await update_last_scan_sales(seller.id, date)
                else:
                    if sales:
                        await send_new_sales(sales=sales, seller_id=seller.id)
                        await update_last_scan_sales(seller.id, date)
                        print('Обновил продажи')
                if orders:
                    if orders:
                        pass
                        await send_new_orders(orders, seller_id=seller.id)
                    await update_last_scan_orders(seller.id, date)
                    print('Обновил заказы')
            if seller.api_fbs:
                orders_fbs = get_ordered_products_fbc(seller.api_fbs, last_scan_orders)
                if orders_fbs:
                    await send_new_orders_fbs(orders_fbs, seller.id)


async def update_stocks(wait_for):
    """ Обновление товаров в стоке
        :param wait_for: время в часах
     """
    while True:
        await asyncio.sleep(wait_for * 10)
        sellers = await select_all_sellers_enable()
        for seller in sellers:

            stocks = await get_stock_products(seller.api_x64)

            if stocks:
                await update_stocks_products(seller_id=seller.id, data=stocks)
                print('Обновил товары в стоке')


async def deleting_all_items(wait_for):
    """ Удаление товаров которым больше 90 дней
            :param wait_for: время в часах
         """
    while True:
        await asyncio.sleep(wait_for * 3600)
        await deleting_items()
        logger.info(
            f"Произвел чистку товаров/заказов которым больше 90 дней")


async def first_scan(seller_id, token):
    """ Первое сканирование при добавлении пользователя """
    date_from = get_date(days=90)
    date = datetime.datetime.today()
    sales = await get_sales_products(token, date_from)
    stocks = await get_stock_products(token)
    orders = await get_ordered_products(token, date_from)
    if sales is not None:
        for sale in sales:
            await update_sales_products(seller_id=seller_id, sale=sale)
            await update_last_scan_sales(seller_id, date)

    if stocks is not None:
        await update_stocks_products(seller_id=seller_id, data=stocks)

    if orders is not None:
        for order in orders:
            if order["isCancel"] is False:
                product = await get_order_by_number(order['gNumber'], seller_id)
                if not product:
                    await update_ordered_products(seller_id=seller_id, order=order)
        await update_last_scan_orders(seller_id, date)
    logger.info(f"Произвел первое сканирование для {seller_id}")


async def send_new_sales(sales, seller_id):
    users = await select_user_by_seller(seller_id)
    seller = await select_seller(seller_id)
    count_successful = 0
    for sale in sales:
        if sale['saleID'].startswith('R') or sale['saleID'].startswith('S'):
            product = await get_sale_by_number(sale['gNumber'], seller_id)
            if not product:
                if len(sales) > 5:
                    await asyncio.sleep(1)
                await update_sales_products(seller_id, sale)
                count_successful += 1
                *info, = await info_on_sale(sale['nmId'], seller_id, sale['saleID'])
                in_sale = info[7]
                in_transit = info[4]
                if info[6] != 0 and in_sale != 0 and info[9] != 0:
                    if info[9] > 0:
                        enough_for = 90 / float(info[9]) * in_sale
                    else:
                        enough_for = 90 * in_sale

                    if enough_for > 90:
                        enough_for = 90
                else:
                    enough_for = 0
                photo_url = await get_photo_url(sale['nmId'])
                price = int(sale["finishedPrice"])
                date = datetime.datetime.strptime(sale["date"], "%Y-%m-%dT%H:%M:%S")
                date = date.strftime("%d.%m.%Y %H:%M")
                if sale['saleID'].startswith('S'):
                    type_sale = "Выкуп"
                else:
                    type_sale = "Возврат"
                string = [
                    hcode(date),
                    f'{hbold(f"{type_sale}: {await get_normal_number(price)} ₽")}\n',
                    f'📁 {sale["subject"]} ∙ {sale["techSize"]}',
                    f'{sale["brand"]}  ∙ {hcode(sale["nmId"])}',
                    f'✅ Сегодня : {info[2]} на {await get_normal_number(info[3])} ₽',
                    f'💰 Купили: {hbold(info[0])} на {hbold(await get_normal_number(info[1]))} ₽\n',
                    f'🛣 {sale["warehouseName"]} → {sale["regionName"]}',
                    f'💼 Комиссия (базовая): {hbold("15%")}',
                    f'💎 Выкуп за 3 мес: {hbold(f"{info[9]} шт")}',
                    f'🚀 В пути до клиента: {hbold(in_transit)}',
                    f'🚚 В пути обратно на склад (возврат): {hbold(info[5])}',
                    f'🛒 В продаже: {hbold(in_sale)}',
                ]
                if enough_for < seller.reserve:
                    string.append(f'📦 {hbold(f"{in_sale} шт")} хватит на ⚠️ {hbold(f"{int(enough_for)} дн.")}')
                else:
                    string.append(f'📦 {hbold(f"{in_sale} шт")} хватит на {hbold(f"{int(enough_for)} дн.")}')
                if info[6] != 0 or in_sale > 0:
                    if enough_for < seller.reserve:
                        if info[9] > 0:
                            replenish_on = round(seller.reserve / (90 / info[9]))
                            replenish_on = replenish_on - in_sale
                            string.append(f'🚗 Пополните склад на {hbold(f"{replenish_on} шт.")}')
                keyboard = InlineKeyboardMarkup(row_width=1)
                button = InlineKeyboardButton(text=f"👉🏻Карточка {sale['nmId']}",
                                              url=f"https://www.wildberries.ru/catalog/{sale['nmId']}/detail.aspx")
                keyboard.insert(button)
                for user in users:
                    await dp.bot.send_photo(chat_id=user.chat_id, caption="\n".join(string), reply_markup=keyboard,
                                            photo=photo_url)
        if count_successful > 0:
            logger.info(
                f"Сохранил и уведомил пользователя {seller.name} о {count_successful} заказах")


async def send_new_orders(orders, seller_id):
    """ Проверяет если заказ новый то отправлет уведомление о нем """
    users = await select_user_by_seller(seller_id)
    seller = await select_seller(seller_id)
    count_successful = 0
    for order in orders:
        if order["isCancel"] is False:
            product = await get_order_by_number(order['gNumber'], seller_id)
            if not product:
                if len(orders) > 5:
                    await asyncio.sleep(1)
                await update_ordered_products(seller_id, order)
                count_successful += 1
                *info, = await info_on_order(order['nmId'], seller_id)
                date = datetime.datetime.strptime(order["date"], "%Y-%m-%dT%H:%M:%S")
                date = date.strftime("%d.%m.%Y %H:%M")
                photo_url = await get_photo_url(order['nmId'])
                price = int(order["totalPrice"] * (1 - order["discountPercent"] / 100))
                in_sale = info[7]
                in_transit = info[4]
                if info[6] != 0 and in_sale != 0 and info[9] != 0:
                    if info[9] > 0:
                        enough_for = 90 / info[9] * in_sale
                    else:
                        enough_for = 90 * in_sale

                    if enough_for > 90:
                        enough_for = 90
                else:
                    enough_for = 0
                string = [
                    hcode(date),
                    f'{hbold(f"Заказ: {await get_normal_number(price)} ₽")}\n',
                    f'📁 {order["subject"]} ∙ {order["techSize"]}',
                    f'{order["brand"]}  ∙ {hcode(order["nmId"])}',
                    f'✅ Сегодня : {info[0]} на {await get_normal_number(info[1])} ₽',
                    f'💰 Купили: {hbold(info[2])} на {hbold(await get_normal_number(info[3]))} ₽\n',
                    f'🛣 {info[8]} → {order["oblast"]}',
                    f'💼 Комиссия (базовая): {hbold("15%")}',
                    f'💎 Выкуп за 3 мес: {hbold(f"{info[9]} шт")}',
                    f'🚀 В пути до клиента: {hbold(in_transit)}',
                    f'🚚 В пути обратно на склад (возврат): {hbold(info[5])}',
                    f'🛒 В продаже: {hbold(in_sale)}',
                ]
                if enough_for < seller.reserve:
                    string.append(f'📦 {hbold(f"{in_sale} шт")} хватит на ⚠️ {hbold(f"{int(enough_for)} дн.")}')
                else:
                    string.append(f'📦 {hbold(f"{in_sale} шт")} хватит на {hbold(f"{int(enough_for)} дн.")}')
                if info[6] != 0 or in_sale > 0:
                    if enough_for < seller.reserve:
                        if info[9] > 0:
                            replenish_on = round(seller.reserve / (90 / info[9]))
                            replenish_on = replenish_on - in_sale
                            string.append(f'🚗 Пополните склад на {hbold(f"{replenish_on} шт.")}')
                keyboard = InlineKeyboardMarkup(row_width=1)
                button = InlineKeyboardButton(text=f"👉🏻Карточка {order['nmId']}",
                                              url=f"https://www.wildberries.ru/catalog/{order['nmId']}/detail.aspx")
                keyboard.insert(button)
                for user in users:
                    await dp.bot.send_photo(chat_id=user.chat_id, caption="\n".join(string), reply_markup=keyboard,
                                            photo=photo_url)
    if count_successful > 0:
        logger.info(
            f"Сохранил и уведомил пользователя {seller.name} о {count_successful} заказах")


async def send_new_orders_fbs(orders, seller_id):
    users = await select_user_by_seller(seller_id)
    count_order = len(orders)
    seller = await select_seller(seller_id)
    for order in orders:
        count_order -= 1
        in_way_to_client, in_way_from_client, in_stock, in_order, from_stock, count_bought = await info_on_order_fbs(
            order['wbWhId'], seller_id)
        date = datetime.datetime.strptime(order['dateCreated'].split(".")[0], "%Y-%m-%dT%H:%M:%S")
        date = date.strftime("%d.%m.%Y %H:%M")
        photo_url = await get_photo_url(order['wbWhId'])
        price = int(order["totalPrice"])
        if count_bought > 0:
            enough_for = 90 / count_bought * in_stock
        else:
            enough_for = 90 * in_stock

        if enough_for > 90:
            enough_for = 90
        string = [
            hbold("Заказ со склада поставщика"),
            date,
            f'{hbold(f"🛒 Заказ : {await get_normal_number(price)}₽")}',
            f'💼 Комиссия (базовая): {hbold("15%")}',
            f'💎 Выкуп за 3 мес: {hbold(f"{count_bought} шт")}',
            f'🌐 {from_stock} → {order["oblast"]}',
            f'🚛 В пути до клиента: {in_way_to_client}',
            f'🚚 В пути возвраты: {in_way_from_client}',
            f'🗂 В продаже: {in_order}',
        ]
        if enough_for < seller.reserve:
            string.append(f'📦 {hbold(f"{in_stock} шт")} хватит на ⚠️ {hbold(f"{int(enough_for)} дн.")}')
        else:
            string.append(f'📦 {hbold(f"{in_stock} шт")} хватит на {hbold(f"{int(enough_for)} дн.")}')
        if enough_for < seller.reserve:
            replenish_on = round(seller.reserve / (90 / count_bought))
            replenish_on = replenish_on - in_stock
            string.append(f'🚗 Пополните склад на {hbold(f"{replenish_on} шт.")}')
        keyboard = InlineKeyboardMarkup(row_width=1)
        button = InlineKeyboardButton(text=f"👉🏻Карточка {order['wbWhId']}",
                                      url=f"https://www.wildberries.ru/catalog/{order['wbWhId']}/detail.aspx")
        keyboard.insert(button)
        for user in users:
            await dp.bot.send_photo(chat_id=user.chat_id, caption="\n".join(string), reply_markup=keyboard,
                                    photo=photo_url)


async def info_on_order(nmId, seller_id):
    """ Получает информцию о новом заказе:
        :param nmId: код товара WB
        :param user_id: id продовца
        :return count_yesterday: количество таких же заказов вчера
        :return amount_yesterday: сумма таких же заказов вчера
        :return count_today: количество таких же заказов сегодрня
        :return amount_today: сумма таких же заказов сегодня
        :return count_today_all: количество заказов вчера
        :return amount_today_all: сумма заказов сегодня
        :return in_way_to_client: количество заказов которое едет к клиенту
        :return in_way_from_client: количество заказов которое едет от клиента
        :return in_stock: количество заказов на складе
        :return in_order: количество заказов в продаже
        :return from_stock: название склада откуда идет доставка
        :return count_bought: количество такихже заказов за 90 дней
     """
    date_now = date_search("today")
    today_order = await ProductsOrders.query.where(ProductsOrders.seller_id == seller_id).where(
        ProductsOrders.date > date_now).where(
        ProductsOrders.nmId == int(nmId)).gino.all()
    today_sale = await ProductsBought.query.where(ProductsBought.seller_id == seller_id).where(
        ProductsBought.date > date_now).where(
        ProductsBought.nmId == int(nmId)).gino.all()
    all_sales_today_amount = int(sum([item.forPay for item in today_sale]))
    all_order_today_amount = int(sum([item.price for item in today_order]))
    stock = await ProductsStocks.query.where(ProductsStocks.seller_id == seller_id).where(
        ProductsStocks.nmId == int(nmId)).gino.first()
    if stock:
        in_way_to_client = stock.inWayToClient
        in_way_from_client = stock.inWayFromClient
        in_stock = stock.quantityFull
        in_order = stock.quantity
        from_stock = stock.warehouseName
    else:
        in_way_to_client = 0
        in_way_from_client = 0
        in_stock = 0
        in_order = 0
        from_stock = 0
    count_orders_today = len(today_order)
    count_sales_today = len(today_sale)
    in_90_days = date_search("in_90_days")
    products = await ProductsBought.query.where(ProductsBought.seller_id == seller_id).where(
        ProductsBought.date > in_90_days).where(
        ProductsBought.nmId == int(nmId)).gino.all()
    count_bought = len(products)

    return count_orders_today, all_order_today_amount, count_sales_today, all_sales_today_amount,\
           in_way_to_client, in_way_from_client, in_stock, in_order, from_stock, count_bought


async def info_on_sale(nmId, seller_id, sale_id):
    date_now = date_search("today")
    today_order = await ProductsOrders.query.where(ProductsOrders.seller_id == seller_id).where(
        ProductsOrders.date > date_now).where(
        ProductsOrders.nmId == int(nmId)).gino.all()
    today_sale = await ProductsBought.query.where(ProductsBought.seller_id == seller_id).where(
        ProductsBought.date > date_now).where(
        ProductsBought.nmId == int(nmId)).gino.all()
    if sale_id.startswith('S'):
        all_sales_today = [i for i in today_sale if i.saleID.startswith('S')]
        all_sales_today_amount = int(sum([item.forPay for item in all_sales_today]))
        all_order_today_amount = int(sum([item.price for item in today_order]))
    else:
        all_sales_today = [i for i in today_sale if i.saleID.startswith('R')]
        all_sales_today_amount = int(sum([item.forPay for item in all_sales_today]))
        all_order_today_amount = int(sum([item.price for item in today_order]))
    stock = await ProductsStocks.query.where(ProductsStocks.seller_id == seller_id).where(
        ProductsStocks.nmId == int(nmId)).gino.first()
    if stock:
        in_way_to_client = stock.inWayToClient
        in_way_from_client = stock.inWayFromClient
        in_stock = stock.quantityFull
        in_order = stock.quantity
        from_stock = stock.warehouseName
    else:
        in_way_to_client = 0
        in_way_from_client = 0
        in_stock = 0
        in_order = 0
        from_stock = 0
    count_today_sale = len(all_sales_today)
    count_today_order = len(today_order)
    in_90_days = date_search("in_90_days")
    products = await ProductsBought.query.where(ProductsBought.seller_id == seller_id).where(
        ProductsBought.date > in_90_days).where(
        ProductsBought.nmId == int(nmId)).gino.all()
    count_bought = len(products)

    return count_today_sale, all_sales_today_amount, count_today_order, all_order_today_amount, in_way_to_client, \
           in_way_from_client, in_stock, in_order, from_stock, count_bought


async def info_on_order_fbs(nmId, user_id):
    """ Получает информцию о новом заказе:
        :param nmId: код товара WB
        :param user_id: id продовца
        :return in_way_to_client: количество заказов которое едет к клиенту
        :return in_way_from_client: количество заказов которое едет от клиента
        :return in_stock: количество заказов на складе
        :return in_order: количество заказов в продаже
        :return from_stock: название склада откуда идет доставка
        :return count_bought: количество такихже заказов за 90 дней
     """
    stock = await ProductsStocks.query.where(ProductsStocks.user_id == user_id).where(
        ProductsStocks.nmId == int(nmId)).gino.first()
    in_way_to_client, in_way_from_client, in_stock, in_order = 0, 0, 0, 0
    from_stock = "Неизвестно"
    if stock:
        in_way_to_client = stock.inWayToClient
        in_way_from_client = stock.inWayFromClient
        in_stock = stock.quantityFull
        in_order = stock.quantity
        from_stock = stock.warehouseName
    in_90_days = date_search("in_90_days")
    products = await ProductsBought.query.where(ProductsBought.user_id == user_id).where(
        ProductsBought.date > in_90_days).where(
        ProductsBought.nmId == int(nmId)).gino.all()
    count_bought = 0
    if products:
        count_bought = len(products)

    return in_way_to_client, in_way_from_client, in_stock, in_order, from_stock, count_bought


async def get_photo_url(nmId):
    """ Возвращает ссылку на фото по nmId заказа"""
    nmId = str(nmId)
    for i in range(1, 11):
        if i == 10:
            url = f"https://basket-{i}.wb.ru/vol{nmId[:-5]}/part{nmId[:-3]}/{nmId}/images/big/1.jpg"
        else:
            url = f"https://basket-0{i}.wb.ru/vol{nmId[:-5]}/part{nmId[:-3]}/{nmId}/images/big/1.jpg"
        res = requests.get(url=url)
        if res.status_code == 200:
            return url



async def shutdown_bot(wait_for):
    """ 1)отключение подписки если скро вышел и на балансе нет денег
        2)отлючение бесплатной подписки если на балансе нет денег и платный период не начался
    """
    while True:
        await asyncio.sleep(wait_for * 3600)
        sellers = await overdue_tariff()
        for seller in sellers:
            users = await select_user_by_seller(seller.id)
            paid = False
            for user in users:
                if user.balance >= AMOUNT_TARIFF:
                    paid = True
                    await update_balance(user.id, -AMOUNT_TARIFF)
                    await update_trail("paid", seller.id)
                    break
            if paid is False:
                await update_trail("no_paid", seller.id)

        fre_trail_sellers = await overdue_free_trail()
        for seller in fre_trail_sellers:
            users = await select_user_by_seller(seller.id)
            paid = False
            if seller.starting_tarif is None:
                for user in users:
                    if user.balance >= AMOUNT_TARIFF:
                        paid = True
                        await update_balance(user.id, -AMOUNT_TARIFF)
                        await update_trail("paid", seller.id)
                        break
                if paid is False:
                    await update_trail("no_paid", seller.id)
            else:
                await update_trail("no_paid", seller.id)


async def enable_tariff(wait_for):
    """  Автосписание денег у всех пользователей чей баланс позволяет оплатить подписку"""
    while True:
        await asyncio.sleep(wait_for * 3600)
        sellers = await returns_unsubscribed_sellers()
        for seller in sellers:
            await update_trail("no_paid", seller.id)


async def notification_of_tariff(wait_for):
    """  Оповещение пользователь об оканчании подписки за день """
    while True:
        await asyncio.sleep(wait_for * 3600)
        tariff = await for_notification_tariff()
        for seller in tariff:
            bot_name = await dp.bot.get_me()
            text = [
                f'💳 {hbold(f"Оплата для {seller.name}")}\n',
                f'Уважаемый поставщик, чтобы @{bot_name.username} продолжил работу, '
                f'необходимо {hbold("пополнить баланс.")}\n',
                f'🔒 Деньги сами по себе не списываются и вы пополняете баланс только по своему желанию. \n',
                f'🛡 Мы не списываем деньги в автоматическом режиме и не привязываем ваши карты.',
            ]
            users = await select_user_by_seller(seller.id)
            for user in users:
                if user.balance < AMOUNT_TARIFF:
                    await dp.bot.send_message(chat_id=user.chat_id, text="\n".join(text))
