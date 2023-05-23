import datetime

from utils.db_api.db_gino import ProductsBought, ProductsOrders
from utils.db_api.quick_commands.seller_inquiries import select_seller
from utils.wb_api.tools import date_search


class SortingSales:
    """Класс для сортировки продаж по ромежутку времени
        sorting_today - Выбирает продажи из базы данных за сегодня
        sorting_yesterday - Выбирает продажи из базы данных за вчера
        sorting_in_7_days - Выбирает продажи из базы данных за 7 дней
        sorting_in_30_days - Выбирает продажи из базы данных за 30 дней
        sorting_another_period - Выбирает продажи из базы данных за выбраный период
        sorting_result - Возвращает полную статистику в виде списка [today, yesterday, in_7_days, in_30_days]
    """

    def __init__(self, seller_id):
        self.seller_id = seller_id

    @staticmethod
    def sorting(sort_list):
        sort_payment = [product for product in sort_list if product.saleID.startswith('S')]
        sort_refund = [product for product in sort_list if product.saleID.startswith('R')]
        amount_payment = int(sum(product.forPay for product in sort_payment))
        amount_refund = int(sum(product.forPay for product in sort_refund)) * -1
        count_payment = len(sort_payment)
        count_refund = len(sort_refund)
        return amount_payment, amount_refund, count_payment, count_refund, sort_list

    async def sorting_today(self, with_search=None):
        date = date_search("today")
        if with_search is None:
            sort_list = await ProductsBought.query.where(ProductsBought.seller_id == self.seller_id).where(
                ProductsBought.date > date).gino.all()
        else:
            seller = await select_seller(self.seller_id)
            if seller.search is not None:
                if seller.search.isdigit():
                    sort_list = await ProductsBought.query.where(ProductsBought.seller_id == self.seller_id).where(
                        ProductsBought.date > date).where(
                        ProductsBought.nmId == int(seller.search)).gino.all()
                else:
                    sort_list = await ProductsBought.query.where(ProductsBought.seller_id == self.seller_id).where(
                        ProductsBought.date > date).where(
                        ProductsBought.subject == seller.search).gino.all()
                    if not sort_list:
                        sort_list = await ProductsBought.query.where(ProductsBought.seller_id == self.seller_id).where(
                            ProductsBought.date > date).where(
                            ProductsBought.brand == seller.search).gino.all()
                    if not sort_list:
                        sort_list = await ProductsBought.query.where(ProductsBought.seller_id == self.seller_id).where(
                            ProductsBought.date > date).where(
                            ProductsBought.supplierArticle == seller.search).gino.all()
            else:
                sort_list = await ProductsBought.query.where(ProductsBought.seller_id == self.seller_id).where(
                    ProductsBought.date > date).gino.all()
        return self.sorting(sort_list)

    async def sorting_yesterday(self, with_search=None):
        date = date_search("yesterday")
        date_now = date_search("today")
        if with_search is None:
            sort_list = await ProductsBought.query.where(ProductsBought.seller_id == self.seller_id).where(
                ProductsBought.date > date).where(ProductsBought.date < date_now).gino.all()
        else:
            seller = await select_seller(self.seller_id)
            if seller.search is not None:
                if seller.search.isdigit():
                    sort_list = await ProductsBought.query.where(ProductsBought.seller_id == self.seller_id).where(
                        ProductsBought.date > date).where(ProductsBought.date < date_now).where(
                        ProductsBought.nmId == int(seller.search)).gino.all()
                else:
                    sort_list = await ProductsBought.query.where(ProductsBought.seller_id == self.seller_id).where(
                        ProductsBought.date > date).where(ProductsBought.date < date_now).where(
                        ProductsBought.subject == seller.search).gino.all()
                    if not sort_list:
                        sort_list = await ProductsBought.query.where(ProductsBought.seller_id == self.seller_id).where(
                            ProductsBought.date > date).where(ProductsBought.date < date_now).where(
                            ProductsBought.brand == seller.search).gino.all()
                    if not sort_list:
                        sort_list = await ProductsBought.query.where(ProductsBought.seller_id == self.seller_id).where(
                            ProductsBought.date > date).where(ProductsBought.date < date_now).where(
                            ProductsBought.supplierArticle == seller.search).gino.all()
            else:
                sort_list = await ProductsBought.query.where(ProductsBought.seller_id == self.seller_id).where(
                    ProductsBought.date > date).where(ProductsBought.date < date_now).gino.all()
        return self.sorting(sort_list)

    async def sorting_in_7_days(self, with_search=None):
        date = date_search("in_7_days")
        if with_search is None:
            sort_list = await ProductsBought.query.where(ProductsBought.seller_id == self.seller_id).where(
                ProductsBought.date > date).gino.all()
        else:
            seller = await select_seller(self.seller_id)
            if seller.search is not None:
                if seller.search.isdigit():
                    sort_list = await ProductsBought.query.where(ProductsBought.seller_id == self.seller_id).where(
                        ProductsBought.date > date).where(
                        ProductsBought.nmId == int(seller.search)).gino.all()
                else:
                    sort_list = await ProductsBought.query.where(ProductsBought.seller_id == self.seller_id).where(
                        ProductsBought.date > date).where(
                        ProductsBought.subject == seller.search).gino.all()
                    if not sort_list:
                        sort_list = await ProductsBought.query.where(ProductsBought.seller_id == self.seller_id).where(
                            ProductsBought.date > date).where(
                            ProductsBought.brand == seller.search).gino.all()
                    if not sort_list:
                        sort_list = await ProductsBought.query.where(ProductsBought.seller_id == self.seller_id).where(
                            ProductsBought.date > date).where(
                            ProductsBought.supplierArticle == seller.search).gino.all()
            else:
                sort_list = await ProductsBought.query.where(ProductsBought.seller_id == self.seller_id).where(
                    ProductsBought.date > date).gino.all()
        return self.sorting(sort_list)

    async def sorting_in_30_days(self, with_search=None):
        date = date_search("in_30_days")
        if with_search is None:
            sort_list = await ProductsBought.query.where(ProductsBought.seller_id == self.seller_id).where(
                ProductsBought.date > date).gino.all()
        else:
            seller = await select_seller(self.seller_id)
            if seller.search is not None:
                if seller.search.isdigit():
                    sort_list = await ProductsBought.query.where(ProductsBought.seller_id == self.seller_id).where(
                        ProductsBought.date > date).where(
                        ProductsBought.nmId == int(seller.search)).gino.all()
                else:
                    sort_list = await ProductsBought.query.where(ProductsBought.seller_id == self.seller_id).where(
                        ProductsBought.date > date).where(
                        ProductsBought.subject == seller.search).gino.all()
                    if not sort_list:
                        sort_list = await ProductsBought.query.where(ProductsBought.seller_id == self.seller_id).where(
                            ProductsBought.date > date).where(
                            ProductsBought.brand == seller.search).gino.all()
                    if not sort_list:
                        sort_list = await ProductsBought.query.where(ProductsBought.seller_id == self.seller_id).where(
                            ProductsBought.date > date).where(
                            ProductsBought.supplierArticle == seller.search).gino.all()
            else:
                sort_list = await ProductsBought.query.where(ProductsBought.seller_id == self.seller_id).where(
                    ProductsBought.date > date).gino.all()
        return self.sorting(sort_list)

    async def sorting_another_period(self, date):
        seller = await select_seller(self.seller_id)
        if len(date) == 10:
            days = int(date.split(".")[0])
            mouth = int(date.split(".")[1])
            year = int(date.split(".")[2])
            date = datetime.datetime(year, mouth, days, 0, 0, 0)
            date_from = date - datetime.timedelta(days=1)
            if seller.search is not None:
                if seller.search.isdigit():
                    sort_list = await ProductsBought.query.where(ProductsBought.seller_id == self.seller_id).where(
                        ProductsBought.date > date_from).where(ProductsBought.date < date).where(
                        ProductsBought.nmId == int(seller.search)).gino.all()
                else:
                    sort_list = await ProductsBought.query.where(ProductsBought.seller_id == self.seller_id).where(
                        ProductsBought.date > date_from).where(ProductsBought.date < date).where(
                        ProductsBought.subject == seller.search).gino.all()
                    if not sort_list:
                        sort_list = await ProductsBought.query.where(ProductsBought.seller_id == self.seller_id).where(
                            ProductsBought.date > date_from).where(ProductsBought.date < date).where(
                            ProductsBought.brand == seller.search).gino.all()
                    if not sort_list:
                        sort_list = await ProductsBought.query.where(ProductsBought.seller_id == self.seller_id).where(
                            ProductsBought.date > date_from).where(ProductsBought.date < date).where(
                            ProductsBought.supplierArticle == seller.search).gino.all()
            else:
                sort_list = await ProductsBought.query.where(ProductsBought.seller_id == self.seller_id).where(
                    ProductsBought.date > date_from).where(ProductsBought.date < date).gino.all()
        else:
            date1 = date.split('-')[0]
            date2 = date.split('-')[1]
            days1 = int(date1.split(".")[0])
            mouth1 = int(date1.split(".")[1])
            year1 = int(date1.split(".")[2])
            date_from = datetime.datetime(year1, mouth1, days1, 0, 0, 0)
            days2 = int(date2.split(".")[0])
            mouth2 = int(date2.split(".")[1])
            year2 = int(date2.split(".")[2])
            date_to = datetime.datetime(year2, mouth2, days2, 0, 0, 0)
            if seller.search is not None:
                if seller.search.isdigit():
                    sort_list = await ProductsBought.query.where(ProductsBought.seller_id == self.seller_id).where(
                        ProductsBought.date > date_from).where(ProductsBought.date < date_to).where(
                        ProductsBought.nmId == int(seller.search)).gino.all()
                else:
                    sort_list = await ProductsBought.query.where(ProductsBought.seller_id == self.seller_id).where(
                        ProductsBought.date > date_from).where(ProductsBought.date < date_to).where(
                        ProductsBought.subject == seller.search).gino.all()
                    if not sort_list:
                        sort_list = await ProductsBought.query.where(ProductsBought.seller_id == self.seller_id).where(
                            ProductsBought.date > date_from).where(ProductsBought.date < date_to).where(
                            ProductsBought.brand == seller.search).gino.all()
                    if not sort_list:
                        sort_list = await ProductsBought.query.where(ProductsBought.seller_id == self.seller_id).where(
                            ProductsBought.date > date_from).where(ProductsBought.date < date_to).where(
                            ProductsBought.supplierArticle == seller.search).gino.all()
            else:
                sort_list = await ProductsBought.query.where(ProductsBought.seller_id == self.seller_id).where(
                    ProductsBought.date > date_from).where(ProductsBought.date < date_to).gino.all()
        return self.sorting(sort_list)

    async def sorting_result(self):
        _, _, _, _, today = await self.sorting_today()
        _, _, _, _, yesterday = await self.sorting_yesterday()
        _, _, _, _, in_7_days = await self.sorting_in_7_days()
        _, _, _, _, in_30_days = await self.sorting_in_30_days()
        return [today, yesterday, in_7_days, in_30_days]


class SortingOrders:
    """
        Класс для сортировки заказов по промежутку времени
        sorting_today - Выбирает заказы из базы данных за сегодня
        sorting_yesterday - Выбирает заказы из базы данных за вчера
        sorting_in_7_days - Выбирает заказы из базы данных за 7 дней
        sorting_in_30_days - Выбирает заказы из базы данных за 30 дней
        sorting_another_period - Выбирает заказы из базы данных за выбраный период
        sorting_result - Возвращает полную статистику в виде списка [today, yesterday, in_7_days, in_30_days]
    """

    def __init__(self, seller_id):
        self.seller_id = seller_id

    @staticmethod
    def sorting(sort_list):
        amount = sum(product.price for product in sort_list)
        count = len(sort_list)
        return amount, count, sort_list

    async def sorting_today(self, with_search=None):
        date = date_search("today")
        if with_search is None:
            sort_list = await ProductsOrders.query.where(ProductsOrders.seller_id == self.seller_id).where(
                ProductsOrders.date > date).gino.all()
        else:
            seller = await select_seller(self.seller_id)
            if seller.search is not None:
                if seller.search.isdigit():
                    sort_list = await ProductsOrders.query.where(ProductsOrders.seller_id == self.seller_id).where(
                        ProductsOrders.date > date).where(
                        ProductsOrders.nmId == int(seller.search)).gino.all()
                else:
                    sort_list = await ProductsOrders.query.where(ProductsOrders.seller_id == self.seller_id).where(
                        ProductsOrders.date > date).where(
                        ProductsOrders.subject == seller.search).gino.all()
                    if not sort_list:
                        sort_list = await ProductsOrders.query.where(ProductsOrders.seller_id == self.seller_id).where(
                            ProductsOrders.date > date).where(
                            ProductsOrders.brand == seller.search).gino.all()
                    if not sort_list:
                        sort_list = await ProductsOrders.query.where(ProductsOrders.seller_id == self.seller_id).where(
                            ProductsOrders.date > date).where(
                            ProductsOrders.supplierArticle == seller.search).gino.all()
            else:
                sort_list = await ProductsOrders.query.where(ProductsOrders.seller_id == self.seller_id).where(
                    ProductsOrders.date > date).gino.all()

        return self.sorting(sort_list)

    async def sorting_yesterday(self, with_search=None):
        date = date_search("yesterday")
        date_now = date_search("today")
        if with_search is None:
            sort_list = await ProductsOrders.query.where(ProductsOrders.seller_id == self.seller_id).where(
                ProductsOrders.date > date).where(ProductsOrders.date < date_now).gino.all()
        else:
            seller = await select_seller(self.seller_id)
            if seller.search is not None:
                if seller.search.isdigit():
                    sort_list = await ProductsOrders.query.where(ProductsOrders.seller_id == self.seller_id).where(
                        ProductsOrders.date > date).where(ProductsOrders.date < date_now).where(
                        ProductsOrders.nmId == int(seller.search)).gino.all()
                else:
                    sort_list = await ProductsOrders.query.where(ProductsOrders.seller_id == self.seller_id).where(
                        ProductsOrders.date > date).where(ProductsOrders.date < date_now).where(
                        ProductsOrders.subject == seller.search).gino.all()
                    if not sort_list:
                        sort_list = await ProductsOrders.query.where(ProductsOrders.seller_id == self.seller_id).where(
                            ProductsOrders.date > date).where(ProductsOrders.date < date_now).where(
                            ProductsOrders.brand == seller.search).gino.all()
                    if not sort_list:
                        sort_list = await ProductsOrders.query.where(ProductsOrders.seller_id == self.seller_id).where(
                            ProductsOrders.date > date).where(ProductsOrders.date < date_now).where(
                            ProductsOrders.supplierArticle == seller.search).gino.all()
            else:
                sort_list = await ProductsOrders.query.where(ProductsOrders.seller_id == self.seller_id).where(
                    ProductsOrders.date > date).where(ProductsOrders.date < date_now).gino.all()
        return self.sorting(sort_list)

    async def sorting_in_7_days(self, with_search=None):
        date = date_search("in_7_days")
        if with_search is None:
            sort_list = await ProductsOrders.query.where(ProductsOrders.seller_id == self.seller_id).where(
                ProductsOrders.date > date).gino.all()
        else:
            seller = await select_seller(self.seller_id)
            if seller.search is not None:
                if seller.search.isdigit():
                    sort_list = await ProductsOrders.query.where(ProductsOrders.seller_id == self.seller_id).where(
                        ProductsOrders.date > date).where(
                        ProductsOrders.nmId == int(seller.search)).gino.all()
                else:
                    sort_list = await ProductsOrders.query.where(ProductsOrders.seller_id == self.seller_id).where(
                        ProductsOrders.date > date).where(
                        ProductsOrders.subject == seller.search).gino.all()
                    if not sort_list:
                        sort_list = await ProductsOrders.query.where(ProductsOrders.seller_id == self.seller_id).where(
                            ProductsOrders.date > date).where(
                            ProductsOrders.brand == seller.search).gino.all()
                    if not sort_list:
                        sort_list = await ProductsOrders.query.where(ProductsOrders.seller_id == self.seller_id).where(
                            ProductsOrders.date > date).where(
                            ProductsOrders.supplierArticle == seller.search).gino.all()
            else:
                sort_list = await ProductsOrders.query.where(ProductsOrders.seller_id == self.seller_id).where(
                    ProductsOrders.date > date).gino.all()
        return self.sorting(sort_list)

    async def sorting_in_30_days(self, with_search=None):
        date = date_search("in_30_days")
        if with_search is None:
            sort_list = await ProductsOrders.query.where(ProductsOrders.seller_id == self.seller_id).where(
                ProductsOrders.date > date).gino.all()
        else:
            seller = await select_seller(self.seller_id)
            if seller.search is not None:
                if seller.search.isdigit():
                    sort_list = await ProductsOrders.query.where(ProductsOrders.seller_id == self.seller_id).where(
                        ProductsOrders.date > date).where(
                        ProductsOrders.nmId == int(seller.search)).gino.all()
                else:
                    sort_list = await ProductsOrders.query.where(ProductsOrders.seller_id == self.seller_id).where(
                        ProductsOrders.date > date).where(
                        ProductsOrders.subject == seller.search).gino.all()
                    if not sort_list:
                        sort_list = await ProductsOrders.query.where(ProductsOrders.seller_id == self.seller_id).where(
                            ProductsOrders.date > date).where(
                            ProductsOrders.brand == seller.search).gino.all()
                    if not sort_list:
                        sort_list = await ProductsOrders.query.where(ProductsOrders.seller_id == self.seller_id).where(
                            ProductsOrders.date > date).where(
                            ProductsOrders.supplierArticle == seller.search).gino.all()
            else:
                sort_list = await ProductsOrders.query.where(ProductsOrders.seller_id == self.seller_id).where(
                    ProductsOrders.date > date).gino.all()
        return self.sorting(sort_list)

    async def sorting_another_period(self, date):
        seller = await select_seller(self.seller_id)
        if len(date) == 10:
            days = int(date.split(".")[0])
            mouth = int(date.split(".")[1])
            year = int(date.split(".")[2])
            date = datetime.datetime(year, mouth, days, 0, 0, 0)
            date_from = date - datetime.timedelta(days=1)
            if seller.search is not None:
                if seller.search.isdigit():
                    sort_list = await ProductsOrders.query.where(ProductsOrders.seller_id == self.seller_id).where(
                        ProductsOrders.date > date_from).where(ProductsOrders.date < date).where(
                        ProductsOrders.nmId == int(seller.search)).gino.all()
                else:
                    sort_list = await ProductsOrders.query.where(ProductsOrders.seller_id == self.seller_id).where(
                        ProductsOrders.date > date_from).where(ProductsOrders.date < date).where(
                        ProductsOrders.subject == seller.search).gino.all()
                    if not sort_list:
                        sort_list = await ProductsOrders.query.where(ProductsOrders.seller_id == self.seller_id).where(
                            ProductsOrders.date > date_from).where(ProductsOrders.date < date).where(
                            ProductsOrders.brand == seller.search).gino.all()
                    if not sort_list:
                        sort_list = await ProductsOrders.query.where(ProductsOrders.seller_id == self.seller_id).where(
                            ProductsOrders.date > date_from).where(ProductsOrders.date < date).where(
                            ProductsOrders.supplierArticle == seller.search).gino.all()
            else:
                sort_list = await ProductsOrders.query.where(ProductsOrders.seller_id == self.seller_id).where(
                    ProductsOrders.date > date_from).where(ProductsOrders.date < date).gino.all()
        else:
            date1 = date.split('-')[0]
            date2 = date.split('-')[1]
            days1 = int(date1.split(".")[0])
            mouth1 = int(date1.split(".")[1])
            year1 = int(date1.split(".")[2])
            date_from = datetime.datetime(year1, mouth1, days1, 0, 0, 0)
            days2 = int(date2.split(".")[0])
            mouth2 = int(date2.split(".")[1])
            year2 = int(date2.split(".")[2])
            date_to = datetime.datetime(year2, mouth2, days2, 0, 0, 0)
            if seller.search is not None:
                if seller.search.isdigit():
                    sort_list = await ProductsOrders.query.where(ProductsOrders.seller_id == self.seller_id).where(
                        ProductsOrders.date > date_from).where(ProductsOrders.date < date_to).where(
                        ProductsOrders.nmId == int(seller.search)).gino.all()
                else:
                    sort_list = await ProductsOrders.query.where(ProductsOrders.seller_id == self.seller_id).where(
                        ProductsOrders.date > date_from).where(ProductsOrders.date < date_to).where(
                        ProductsOrders.subject == seller.search).gino.all()
                    if not sort_list:
                        sort_list = await ProductsOrders.query.where(ProductsOrders.seller_id == self.seller_id).where(
                            ProductsOrders.date > date_from).where(ProductsOrders.date < date_to).where(
                            ProductsOrders.brand == seller.search).gino.all()
                    if not sort_list:
                        sort_list = await ProductsOrders.query.where(ProductsOrders.seller_id == self.seller_id).where(
                            ProductsOrders.date > date_from).where(ProductsOrders.date < date_to).where(
                            ProductsOrders.supplierArticle == seller.search).gino.all()
            else:
                sort_list = await ProductsOrders.query.where(ProductsOrders.seller_id == self.seller_id).where(
                    ProductsOrders.date > date_from).where(ProductsOrders.date < date_to).gino.all()
        return self.sorting(sort_list)

    async def sorting_result(self):
        _, _, today = await self.sorting_today()
        _, _, yesterday = await self.sorting_yesterday()
        _, _, in_7_days = await self.sorting_in_7_days()
        _, _, in_30_days = await self.sorting_in_30_days()
        return [today, yesterday, in_7_days, in_30_days]


class SortingParameterSales:
    """
            Класс для сортировки продаж по фильтру
            sorting_for_category - Сортирует полученые продажи по категориям
            sorting_for_subject - Сортирует полученые продажи по предметам
            sorting_for_vendor_code - Сортирует полученые продажи по Артиклу
            sorting_for_region - Сортирует полученые продажи по региону
            sorting_for_brand -  Сортирует полученые продажи по бренду
            get_orders - Возвращает все заказы
            get_returns - Возвращает заказы которые отправили лбратно
    """

    def __init__(self, list_bought: list):
        self.list_bought = list_bought

    def sorting(self, lambda_func):
        temp_list = []
        for product in self.list_bought:
            if lambda_func(product) not in temp_list:
                temp_list.append(lambda_func(product))

        result = {}
        for parameter in temp_list:
            amount_payment, amount_refund, count_payment, count_refund = 0, 0, 0, 0
            subject = ''
            supplierArticle = ''
            brand = ''
            for product in self.list_bought:
                if parameter == lambda_func(product):
                    if product.saleID.startswith('S'):
                        count_payment += 1
                        amount_payment += product.forPay
                        subject = product.subject
                        supplierArticle = product.supplierArticle
                        brand = product.brand
                    elif product.saleID.startswith('R'):
                        count_refund += 1
                        amount_refund += product.forPay

            result.update({parameter: {"amount_payment": int(amount_payment), "amount_refund": int(amount_refund) * -1,
                                       "count_payment": count_payment,
                                       "count_refund": count_refund, "subject": subject,
                                       "supplierArticle": supplierArticle, "brand": brand}})
        return result, temp_list

    def sorting_for_category(self):
        return self.sorting(lambda product: product.category)

    def sorting_for_subject(self):
        return self.sorting(lambda product: product.subject)

    def sorting_for_vendor_code(self):
        return self.sorting(lambda product: product.nmId)

    def sorting_for_region(self):
        return self.sorting(lambda product: product.regionName)

    def sorting_for_brand(self):
        return self.sorting(lambda product: product.brand)

    def get_orders(self):
        result = []
        for i in self.list_bought:
            if i.saleID.startswith('S'):
                result.append(i)
        return result

    def get_returns(self):
        result = []
        for i in self.list_bought:
            if i.saleID.startswith('R'):
                result.append(i)
        return result


class SortingParameterOrders:
    """Класс для сортировки заказов по фильтру
            sorting_for_category - Сортирует полученые заказы по категориям
            sorting_for_subject - Сортирует полученые заказы по предметам
            sorting_for_vendor_code - Сортирует полученые заказы по Артиклу
            sorting_for_region - Сортирует полученые заказы по региону
            sorting_for_brand -  Сортирует полученые заказы по бренду
            get_orders - Возвращает все заказы
            get_returns - Возвращает заказы которые отправили лбратно
        """

    def __init__(self, list_bought: list):
        self.list_bought = list_bought

    def sorting(self, lambda_func):
        temp_list = []
        for product in self.list_bought:
            if lambda_func(product) not in temp_list:
                temp_list.append(lambda_func(product))

        result = {}
        for parameter in temp_list:
            amount, count = 0, 0
            subject = ''
            supplierArticle = ''
            brand = ''
            for product in self.list_bought:
                if parameter == lambda_func(product):
                    amount += product.price
                    count += 1
                    subject = product.subject
                    supplierArticle = product.supplierArticle
                    brand = product.brand

            result.update({parameter: {"amount": int(amount), "count": count, "subject": subject,
                                       "supplierArticle": supplierArticle, "brand": brand}})
        return result, temp_list

    def sorting_for_category(self):
        return self.sorting(lambda product: product.category)

    def sorting_for_subject(self):
        return self.sorting(lambda product: product.subject)

    def sorting_for_vendor_code(self):
        return self.sorting(lambda product: product.nmId)

    def sorting_for_region(self):
        return self.sorting(lambda product: product.oblast)

    def sorting_for_brand(self):
        return self.sorting(lambda product: product.brand)
