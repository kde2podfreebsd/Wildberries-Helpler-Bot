import datetime

from asyncpg import UniqueViolationError

from utils.db_api.db_gino import Seller, Association, ProductsBought, ProductsStocks, ProductsOrders, FreeTrail, User,\
    ProductsOrderedFBS
from utils.wb_api.tools import date_search


async def add_seller(api_x64: str, reserve: int, export: bool, bot_enable: bool, name: str, tarif: bool):
    """ Добавление продавца в БД"""
    try:
        seller = Seller(api_x64=api_x64, reserve=reserve, export=export, bot_enable=bot_enable,
                        name=name, tarif=tarif)

        await seller.create()
        return seller
    except UniqueViolationError:
        pass


async def select_seller(seller_id: int):
    """ Выбор продавца по seller_id"""
    return await Seller.query.where(Seller.id == seller_id).gino.first()


async def select_seller_by_user(user_id: int):
    """ Выбор всех продавцов у пользователя """
    founding_sellers = await Association.query.where(Association.user_id == user_id).gino.all()
    sellers_list = []
    for i in founding_sellers:
        seller = await Seller.query.where(Seller.id == i.seller_id).gino.first()
        sellers_list.append(seller)
    return sellers_list


async def count_seller_by_user(user_id: int):
    """ Подщет продавцов у пользователя """
    founding_sellers = await Association.query.where(Association.user_id == user_id).gino.all()
    return len(founding_sellers)


async def select_all_users():
    return await User.query.gino.all()


async def select_seller_by_api_x64(api_x64):
    """ Возвращает селлера по api_x64 """
    return await Seller.query.where(Seller.api_x64 == api_x64).gino.first()


async def select_all_sellers_enable():
    """ Возвращает всех продавцов у которых в настроqках включен бот"""
    return await Seller.query.where(Seller.bot_enable == True).gino.all()


async def select_all_sellers():
    """ Возвращает всех продавцов"""
    return await Seller.query.gino.all()


async def update_seller_settings(seller_id, reserve: int = None, bot_enable: bool = None, export: bool = None):
    """ Обновление настроек продавца"""
    seller = await Seller.get(seller_id)
    if reserve is not None:
        await seller.update(reserve=reserve).apply()
    if bot_enable is not None:
        await seller.update(bot_enable=bot_enable).apply()
    if export is not None:
        await seller.update(export=export).apply()
    return seller


async def update_filter_bought(seller_id, method):
    """ Обновляет фильтр поиска отчетов"""
    seller = await Seller.get(seller_id)
    await seller.update(filter_bought=method).apply()


async def update_api64(seller_id, api):
    """ Обновляет api64 у продавца по seller_id"""
    seller = await Seller.get(seller_id)
    await seller.update(api_x64=api).apply()


async def update_fbs_api(seller_id, api):
    """ Обновляет fbs api у продавца по seller_id"""
    seller = await Seller.get(seller_id)
    await seller.update(api_fbs=api).apply()


async def update_filter_stocks(seller_id, method):
    """ Обновляет фильтр поиска по моим товарам """
    seller = await Seller.get(seller_id)
    await seller.update(filter_stocks=method).apply()


async def update_filter_orders(seller_id, method):
    """ Обновляет фильтр поиска по заказам """
    seller = await Seller.get(seller_id)
    await seller.update(filter_orders=method).apply()


async def update_last_scan_sales(seller_id, date):
    """ Обновляет последнюю дату сканирования продаж """
    seller = await Seller.get(seller_id)
    await seller.update(last_scan_sales=date).apply()


async def update_last_scan_orders(seller_id, date):
    """ Обновляет последнюю дату сканирования заказов """
    seller = await Seller.get(seller_id)
    await seller.update(last_scan_orders=date).apply()


async def update_set_search(seller_id, search):
    """ Обновляет фильтр поиска """
    seller = await Seller.get(seller_id)
    await seller.update(search=search).apply()


async def delete_set_search(seller_id):
    """ Удаляет фильтр поиска """
    seller = await Seller.get(seller_id)
    await seller.update(search=None).apply()


async def delete_seller(seller_id):
    """ Удаляет продовца """
    await ProductsBought.delete.where(ProductsBought.seller_id == seller_id).gino.status()
    await ProductsStocks.delete.where(ProductsStocks.seller_id == seller_id).gino.status()
    await ProductsOrders.delete.where(ProductsOrders.seller_id == seller_id).gino.status()
    await ProductsOrderedFBS.delete.where(ProductsOrderedFBS.seller_id == seller_id).gino.status()
    await Association.delete.where(Association.seller_id == seller_id).gino.status()
    await Seller.delete.where(Seller.id == seller_id).gino.status()


async def current_seller(user_id):
    return await User.query.where(User.id == user_id).gino.first()


async def rename_seller(seller_id, name):
    seller = await Seller.get(seller_id)
    await seller.update(name=name).apply()


async def update_current_seller(user_id, seller_id):
    user = await User.query.where(User.id == user_id).gino.first()
    await user.update(current_seller=seller_id).apply()


async def check_free_trail(user_id, api_x64):
    user = await FreeTrail.query.where(FreeTrail.user_id == user_id).gino.first()
    api = await FreeTrail.query.where(FreeTrail.seller_api == api_x64).gino.first()
    if user or api:
        return False
    return True


async def append_free_trail(user_id, api_x64):
    try:
        free_trail = FreeTrail(user_id=user_id, seller_api=api_x64)

        await free_trail.create()
    except UniqueViolationError:
        pass


async def overdue_tariff():
    """  Возвращает продавцов у которых прошел день после истечения подписки"""
    date = date_search("in_30_days")
    now = datetime.datetime.now().date() - datetime.timedelta(days=31)
    now = now.strftime("%Y-%m-%d")
    year = int(now.split("-")[0])
    mouth = int(now.split("-")[1])
    days = int(now.split("-")[2])
    last_date = datetime.datetime(year, mouth, days, 0, 0, 0)
    return await Seller.query.where(Seller.starting_tarif < date).where(Seller.starting_tarif > last_date).gino.all()


async def overdue_free_trail():
    """  Возвращает продавцов у которых прошел день после истечения бесплатной подписки"""
    date = date_search("in_7_days")
    now = datetime.datetime.now().date() - datetime.timedelta(days=8)
    now = now.strftime("%Y-%m-%d")
    year = int(now.split("-")[0])
    mouth = int(now.split("-")[1])
    days = int(now.split("-")[2])
    last_date = datetime.datetime(year, mouth, days, 0, 0, 0)
    free_trail = await FreeTrail.query.where(FreeTrail.created_at < date).where(
        FreeTrail.created_at > last_date).gino.all()
    seller = []
    for i in free_trail:
        seller.append(await select_seller_by_api_x64(i.seller_api))
    return seller


async def for_notification_free_trail():
    last_date = date_search("in_7_days")
    now = datetime.datetime.now().date() - datetime.timedelta(days=5)
    now = now.strftime("%Y-%m-%d")
    year = int(now.split("-")[0])
    mouth = int(now.split("-")[1])
    days = int(now.split("-")[2])
    date = datetime.datetime(year, mouth, days, 0, 0, 0)
    free_trail = await FreeTrail.query.where(FreeTrail.created_at < date).where(
        FreeTrail.created_at > last_date).gino.all()
    seller = []
    for i in free_trail:
        seller.append(await select_seller_by_api_x64(i.seller_api))
    return seller


async def for_notification_tariff():
    last_date = date_search("in_30_days")
    now = datetime.datetime.now().date() - datetime.timedelta(days=28)
    now = now.strftime("%Y-%m-%d")
    year = int(now.split("-")[0])
    mouth = int(now.split("-")[1])
    days = int(now.split("-")[2])
    date = datetime.datetime(year, mouth, days, 0, 0, 0)
    return await Seller.query.where(Seller.starting_tarif < date).where(Seller.starting_tarif > last_date).gino.all()


async def update_trail(method, seller_id):
    """  Обновляет подписку при успешной оплате - paid
         Завершает подписку при неудачное оплате - no_paid
     """
    now = datetime.datetime.now()
    seller = await Seller.get(seller_id)
    if method == "paid":
        await seller.update(starting_tarif=now, tarif=True, bot_enable=True).apply()
    elif method == "no_paid":
        await seller.update(tarif=False, bot_enable=False).apply()


async def returns_unsubscribed_sellers():
    """  Возвращает продавцов у которых истекла подписка более чем 30 дней назад """
    date = date_search("in_30_days")
    return await Seller.query.where(Seller.starting_tarif < date).gino.all()


async def update_trail_fail(seller_id):
    """  Обновляет подписку при успешной оплате - paid
         Завершает подписку при неудачное оплате - no_paid
     """
    now = datetime.datetime.now() - datetime.timedelta(days=40)
    seller = await Seller.get(seller_id)
    await seller.update(starting_tarif=now, tarif=False, bot_enable=False).apply()
