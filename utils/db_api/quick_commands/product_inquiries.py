import datetime

from utils.db_api.db_gino import ProductsBought, ProductsStocks, ProductsOrders
from utils.db_api.quick_commands.seller_inquiries import select_seller
from utils.wb_api.tools import format_date, date_search


async def update_sales_products(seller_id, sale):
    """ Обновляет продажи"""
    date = format_date(sale['date'])
    product = ProductsBought(seller_id=seller_id, date=date, category=sale['category'],
                             subject=sale['subject'], nmId=sale['nmId'],
                             regionName=sale['regionName'], brand=sale['brand'], saleID=sale['saleID'],
                             forPay=sale['forPay'], supplierArticle=sale['supplierArticle'], techSize=sale['techSize'],
                             number=sale['gNumber'])

    await product.create()


async def update_stocks_products(seller_id, data):
    """ Обновляет товары в стоке"""
    await ProductsStocks.delete.where(ProductsStocks.seller_id == seller_id).gino.status()
    for i in data:
        product = ProductsStocks(seller_id=seller_id, category=i['category'], subject=i['subject'], nmId=i['nmId'],
                                 brand=i['brand'], techSize=i['techSize'], supplierArticle=i['supplierArticle'],
                                 quantityFull=i['quantityFull'],
                                 inWayToClient=0, inWayFromClient=0,
                                 quantity=i['quantity'], warehouseName=i['warehouseName'])

        await product.create()


async def update_ordered_products(seller_id, order):
    """ Обновляет заказы"""
    date = format_date(order['date'])
    price = int(order["totalPrice"] * (1 - order["discountPercent"] / 100))
    product = ProductsOrders(seller_id=seller_id, date=date, category=order['category'], subject=order['subject'],
                             nmId=order['nmId'], brand=order['brand'], techSize=order['techSize'],
                             supplierArticle=order['supplierArticle'], price=price, oblast=order['oblast'],
                             number=order['gNumber'])

    await product.create()


async def get_order_by_number(number, seller_id):
    """ Возврощает заказы по их номеру"""
    return await ProductsOrders.query.where(ProductsOrders.seller_id == seller_id).where(
        ProductsOrders.number == number).gino.all()


async def get_sale_by_number(number, seller_id):
    """ Возврощает заказы по их номеру"""
    return await ProductsBought.query.where(ProductsBought.seller_id == seller_id).where(
        ProductsBought.number == number).gino.all()


async def select_stocks_by_seller_id(seller_id):
    """ Возвращает все тоовары которые привязаны к продавцу"""
    seller = await select_seller(seller_id)
    if seller.search is not None:
        if seller.search.isdigit():
            return await ProductsStocks.query.where(ProductsStocks.seller_id == seller_id).where(
                ProductsStocks.nmId == int(seller.search)).gino.all()
        else:
            result = await ProductsStocks.query.where(ProductsStocks.seller_id == seller_id).where(
                ProductsStocks.subject == seller.search).gino.all()
            if not result:
                result = await ProductsStocks.query.where(ProductsStocks.seller_id == seller_id).where(
                    ProductsStocks.brand == seller.search).gino.all()
            if not result:
                result = await ProductsStocks.query.where(ProductsStocks.seller_id == seller_id).where(
                    ProductsStocks.supplierArticle == seller.search).gino.all()
            return result
    return await ProductsStocks.query.where(ProductsStocks.seller_id == seller_id).gino.all()


async def select_sales_by_seller_id(seller_id):
    """ Возвращает все продажи которые привязаны к продавцу"""
    seller = await select_seller(seller_id)
    if seller.search is not None:
        if seller.search.isdigit():
            return await ProductsBought.query.where(ProductsBought.seller_id == seller_id).where(
                ProductsBought.nmId == int(seller.search)).gino.all()
        else:
            result = await ProductsBought.query.where(ProductsBought.seller_id == seller_id).where(
                ProductsBought.subject == seller.search).gino.all()
            if not result:
                result = await ProductsBought.query.where(ProductsBought.seller_id == seller_id).where(
                    ProductsBought.brand == seller.search).gino.all()
            if not result:
                result = await ProductsBought.query.where(ProductsBought.seller_id == seller_id).where(
                    ProductsBought.supplierArticle == seller.search).gino.all()
            return result
    return await ProductsBought.query.where(ProductsBought.seller_id == seller_id).gino.all()


async def select_ordered_by_seller_id(seller_id):
    """ Возвращает все заказы которые привязаны к продавцу"""
    seller = await select_seller(seller_id)
    if seller.search is not None:
        if seller.search.isdigit():
            return await ProductsOrders.query.where(ProductsOrders.seller_id == seller_id).where(
                ProductsOrders.nmId == int(seller.search)).gino.all()
        else:
            result = await ProductsOrders.query.where(ProductsOrders.seller_id == seller_id).where(
                ProductsOrders.subject == seller.search).gino.all()
            if not result:
                result = await ProductsOrders.query.where(ProductsOrders.seller_id == seller_id).where(
                    ProductsOrders.brand == seller.search).gino.all()
            if not result:
                result = await ProductsOrders.query.where(ProductsOrders.seller_id == seller_id).where(
                    ProductsOrders.supplierArticle == seller.search).gino.all()
            return result
    return await ProductsOrders.query.where(ProductsOrders.seller_id == seller_id).gino.all()


async def select_stocks(seller_id):
    """ Возвращает все товары на складе кторые относятся к продавцу"""
    return await ProductsStocks.query.where(ProductsStocks.seller_id == seller_id).gino.all()


async def deleting_items():
    """ Удаление товаров которым больше 90 дней """
    in_90_days = date_search("in_90_days")
    await ProductsBought.delete.where(ProductsBought.date < in_90_days).gino.status()
    await ProductsOrders.delete.where(ProductsOrders.date < in_90_days).gino.status()


async def count_mouth_order(seller_id):
    date = date_search("in_30_days")
    return await ProductsOrders.query.where(ProductsOrders.seller_id == seller_id).where(
        ProductsOrders.date > date).gino.all()


async def get_days_stats(seller_id, days):
    if days == "7":
        date = date_search("in_7_days")
    elif days == "14":
        date = datetime.datetime.now() - datetime.timedelta(days=14)
        date = date.replace(hour=0, minute=0, second=0, microsecond=0)
    elif days == "30":
        date = date_search("in_30_days")
    else:
        date = date_search("in_90_days")
    orders = await ProductsOrders.query.where(ProductsOrders.seller_id == seller_id).where(
        ProductsOrders.date > date).gino.all()
    sales = await ProductsBought.query.where(ProductsBought.seller_id == seller_id).where(
        ProductsBought.date > date).gino.all()
    stocks = await ProductsStocks.query.where(ProductsStocks.seller_id == seller_id).gino.all()
    return orders, sales, stocks
