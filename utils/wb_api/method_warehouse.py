import asyncio
import time

from utils.db_api.quick_commands.product_inquiries import select_sales_by_seller_id, select_stocks_by_seller_id, \
    select_ordered_by_seller_id, select_stocks
from utils.wb_api.rest_client.jwt_client import JWTApiClient
from utils.wb_api.rest_client.x64_client import X64ApiClient, RETRY_DELAY
from utils.wb_api.sorting import SortingSales, SortingParameterSales, SortingOrders, SortingParameterOrders


async def get_full_report(seller_id):
    """
        Возвращает отчет по товарам  (сегодня, вчера, за 7 дней, за 30 дней):
        amount_payment - Количество выкупов
        amount_refund - Количество возвратов
        count_payment - Сумма со всех выкупов
        count_refund - Сумма на которую вернули товар
        amount_orders - Сумма со всех заказов
        count_orders - Количество заказов
    """
    result = {}
    sort_sales = SortingSales(seller_id)
    sort_orders = SortingOrders(seller_id)
    keys = ["today", "yesterday", "in_7_days", "in_30_days"]
    for key in keys:
        if key == "today":
            amount_payment, amount_refund, count_payment, count_refund, _ = await sort_sales.sorting_today()
            amount_orders, count_orders, _ = await sort_orders.sorting_today()
        elif key == "yesterday":
            amount_payment, amount_refund, count_payment, count_refund, _ = await sort_sales.sorting_yesterday()
            amount_orders, count_orders, _ = await sort_orders.sorting_yesterday()
        elif key == "in_7_days":
            amount_payment, amount_refund, count_payment, count_refund, _ = await sort_sales.sorting_in_7_days()
            amount_orders, count_orders, _ = await sort_orders.sorting_in_7_days()
        else:
            amount_payment, amount_refund, count_payment, count_refund, _ = await sort_sales.sorting_in_30_days()
            amount_orders, count_orders, _ = await sort_orders.sorting_in_30_days()
        result.update(
            {key: {"amount_payment": amount_payment, "amount_refund": amount_refund,
                   "count_payment": count_payment,
                   "count_refund": count_refund, "amount_orders": amount_orders, "count_orders": count_orders}})
    return result


async def sorting_category(seller_id, period):
    """
        Возвращает статистику по категориям:
        period - период за который вернуть статистику (сегодня - today, вчера - yesterday,
         за 7 дней - in_7_days, за 30 дней - in_30_days)
        count_back - Количество возвратов
        count_bought - Количество заказов
        sum_payment - Чистая выручка со всех заказов
        sum_back - Сумма на которую вернули товар
    """
    sort_sales = SortingSales(seller_id)
    sort_orders = SortingOrders(seller_id)
    if period == "today":
        _, _, _, _, sort_sales = await sort_sales.sorting_today(with_search=True)
        _, _, sort_orders = await sort_orders.sorting_today(with_search=True)
    elif period == "yesterday":
        _, _, _, _, sort_sales = await sort_sales.sorting_yesterday(with_search=True)
        _, _, sort_orders = await sort_orders.sorting_yesterday(with_search=True)
    elif period == "in_7_days":
        _, _, _, _, sort_sales = await sort_sales.sorting_in_7_days(with_search=True)
        _, _, sort_orders = await sort_orders.sorting_in_7_days(with_search=True)
    elif period == "in_30_days":
        _, _, _, _, sort_sales = await sort_sales.sorting_in_30_days(with_search=True)
        _, _, sort_orders = await sort_orders.sorting_in_30_days(with_search=True)
    else:
        _, _, _, _, sort_sales = await sort_sales.sorting_another_period(period)
        _, _, sort_orders = await sort_orders.sorting_another_period(period)
    result = {}
    sort_sales_parameter = SortingParameterSales(sort_sales)
    sort_list_sales, sales_region = sort_sales_parameter.sorting_for_category()
    sort_orders_parameter = SortingParameterOrders(sort_orders)
    sort_list_orders, orders_region = sort_orders_parameter.sorting_for_category()
    unique_orders_region = set(sales_region + orders_region)
    for region in unique_orders_region:
        if region in sort_list_sales and region in sort_list_orders:
            result.update({region: {"amount_payment": sort_list_sales[region]['amount_payment'],
                                    "amount_refund": sort_list_sales[region]['amount_refund'],
                                    "count_payment": sort_list_sales[region]['count_payment'],
                                    "count_refund": sort_list_sales[region]['count_refund'],
                                    "subject": sort_list_sales[region]['subject'],
                                    "supplierArticle": sort_list_sales[region]['supplierArticle'],
                                    "brand": sort_list_sales[region]['brand'],
                                    "amount_orders": sort_list_orders[region]['amount'],
                                    "count_orders": sort_list_orders[region]['count'],

                                    }})
        elif region in sort_list_sales:
            result.update({region: {"amount_payment": sort_list_sales[region]['amount_payment'],
                                    "amount_refund": sort_list_sales[region]['amount_refund'],
                                    "count_payment": sort_list_sales[region]['count_payment'],
                                    "count_refund": sort_list_sales[region]['count_refund'],
                                    "subject": sort_list_sales[region]['subject'],
                                    "supplierArticle": sort_list_sales[region]['supplierArticle'],
                                    "brand": sort_list_sales[region]['brand'],
                                    "amount_orders": 0,
                                    "count_orders": 0,
                                    }})
        elif region in sort_list_orders:
            result.update({region: {"amount_payment": 0,
                                    "amount_refund": 0,
                                    "count_payment": 0,
                                    "count_refund": 0,
                                    "subject": sort_list_orders[region]['subject'],
                                    "supplierArticle": sort_list_orders[region]['supplierArticle'],
                                    "brand": sort_list_orders[region]['brand'],
                                    "amount_orders": sort_list_orders[region]['amount'],
                                    "count_orders": sort_list_orders[region]['count'],
                                    }})
    return result


async def sorting_subject(seller_id, period):
    """
        Возвращает статистику по предметам:
        period - период за который вернуть статистику (сегодня - today, вчера - yesterday,
         за 7 дней - in_7_days, за 30 дней - in_30_days)
        count_back - Количество возвратов
        count_bought - Количество заказов
        sum_payment - Чистая выручка со всех заказов
        sum_back - Сумма на которую вернули товар
    """
    sort_sales = SortingSales(seller_id)
    sort_orders = SortingOrders(seller_id)
    if period == "today":
        _, _, _, _, sort_sales = await sort_sales.sorting_today(with_search=True)
        _, _, sort_orders = await sort_orders.sorting_today(with_search=True)
    elif period == "yesterday":
        _, _, _, _, sort_sales = await sort_sales.sorting_yesterday(with_search=True)
        _, _, sort_orders = await sort_orders.sorting_yesterday(with_search=True)
    elif period == "in_7_days":
        _, _, _, _, sort_sales = await sort_sales.sorting_in_7_days(with_search=True)
        _, _, sort_orders = await sort_orders.sorting_in_7_days(with_search=True)
    elif period == "in_30_days":
        _, _, _, _, sort_sales = await sort_sales.sorting_in_30_days(with_search=True)
        _, _, sort_orders = await sort_orders.sorting_in_30_days(with_search=True)
    else:
        _, _, _, _, sort_sales = await sort_sales.sorting_another_period(period)
        _, _, sort_orders = await sort_orders.sorting_another_period(period)
    result = {}
    sort_sales_parameter = SortingParameterSales(sort_sales)
    sort_list_sales, sales_region = sort_sales_parameter.sorting_for_subject()
    sort_orders_parameter = SortingParameterOrders(sort_orders)
    sort_list_orders, orders_region = sort_orders_parameter.sorting_for_subject()
    unique_orders_region = set(sales_region + orders_region)
    for region in unique_orders_region:
        if region in sort_list_sales and region in sort_list_orders:
            result.update({region: {"amount_payment": sort_list_sales[region]['amount_payment'],
                                    "amount_refund": sort_list_sales[region]['amount_refund'],
                                    "count_payment": sort_list_sales[region]['count_payment'],
                                    "count_refund": sort_list_sales[region]['count_refund'],
                                    "subject": sort_list_sales[region]['subject'],
                                    "supplierArticle": sort_list_sales[region]['supplierArticle'],
                                    "brand": sort_list_sales[region]['brand'],
                                    "amount_orders": sort_list_orders[region]['amount'],
                                    "count_orders": sort_list_orders[region]['count'],

                                    }})
        elif region in sort_list_sales:
            result.update({region: {"amount_payment": sort_list_sales[region]['amount_payment'],
                                    "amount_refund": sort_list_sales[region]['amount_refund'],
                                    "count_payment": sort_list_sales[region]['count_payment'],
                                    "count_refund": sort_list_sales[region]['count_refund'],
                                    "subject": sort_list_sales[region]['subject'],
                                    "supplierArticle": sort_list_sales[region]['supplierArticle'],
                                    "brand": sort_list_sales[region]['brand'],
                                    "amount_orders": 0,
                                    "count_orders": 0,
                                    }})
        elif region in sort_list_orders:
            result.update({region: {"amount_payment": 0,
                                    "amount_refund": 0,
                                    "count_payment": 0,
                                    "count_refund": 0,
                                    "subject": sort_list_orders[region]['subject'],
                                    "supplierArticle": sort_list_orders[region]['supplierArticle'],
                                    "brand": sort_list_orders[region]['brand'],
                                    "amount_orders": sort_list_orders[region]['amount'],
                                    "count_orders": sort_list_orders[region]['count'],
                                    }})
    return result


async def sorting_vendor_code(seller_id, period):
    """
        Возвращает статистику по Артиклам:
        period - период за который вернуть статистику (сегодня - today, вчера - yesterday,
         за 7 дней - in_7_days, за 30 дней - in_30_days)
        count_back - Количество возвратов
        count_bought - Количество заказов
        sum_payment - Чистая выручка со всех заказов
        sum_back - Сумма на которую вернули товар
        subject - предмет
    """
    sort_sales = SortingSales(seller_id)
    sort_orders = SortingOrders(seller_id)
    if period == "today":
        _, _, _, _, sort_sales = await sort_sales.sorting_today(with_search=True)
        _, _, sort_orders = await sort_orders.sorting_today(with_search=True)
    elif period == "yesterday":
        _, _, _, _, sort_sales = await sort_sales.sorting_yesterday(with_search=True)
        _, _, sort_orders = await sort_orders.sorting_yesterday(with_search=True)
    elif period == "in_7_days":
        _, _, _, _, sort_sales = await sort_sales.sorting_in_7_days(with_search=True)
        _, _, sort_orders = await sort_orders.sorting_in_7_days(with_search=True)
    elif period == "in_30_days":
        _, _, _, _, sort_sales = await sort_sales.sorting_in_30_days(with_search=True)
        _, _, sort_orders = await sort_orders.sorting_in_30_days(with_search=True)
    else:
        _, _, _, _, sort_sales = await sort_sales.sorting_another_period(period)
        _, _, sort_orders = await sort_orders.sorting_another_period(period)
    result = {}
    sort_sales_parameter = SortingParameterSales(sort_sales)
    sort_list_sales, sales_region = sort_sales_parameter.sorting_for_vendor_code()
    sort_orders_parameter = SortingParameterOrders(sort_orders)
    sort_list_orders, orders_region = sort_orders_parameter.sorting_for_vendor_code()
    unique_orders_region = set(sales_region + orders_region)
    for region in unique_orders_region:
        if region in sort_list_sales and region in sort_list_orders:
            result.update({region: {"amount_payment": sort_list_sales[region]['amount_payment'],
                                    "amount_refund": sort_list_sales[region]['amount_refund'],
                                    "count_payment": sort_list_sales[region]['count_payment'],
                                    "count_refund": sort_list_sales[region]['count_refund'],
                                    "subject": sort_list_sales[region]['subject'],
                                    "supplierArticle": sort_list_sales[region]['supplierArticle'],
                                    "brand": sort_list_sales[region]['brand'],
                                    "amount_orders": sort_list_orders[region]['amount'],
                                    "count_orders": sort_list_orders[region]['count'],

                                    }})
        elif region in sort_list_sales:
            result.update({region: {"amount_payment": sort_list_sales[region]['amount_payment'],
                                    "amount_refund": sort_list_sales[region]['amount_refund'],
                                    "count_payment": sort_list_sales[region]['count_payment'],
                                    "count_refund": sort_list_sales[region]['count_refund'],
                                    "subject": sort_list_sales[region]['subject'],
                                    "supplierArticle": sort_list_sales[region]['supplierArticle'],
                                    "brand": sort_list_sales[region]['brand'],
                                    "amount_orders": 0,
                                    "count_orders": 0,
                                    }})
        elif region in sort_list_orders:
            result.update({region: {"amount_payment": 0,
                                    "amount_refund": 0,
                                    "count_payment": 0,
                                    "count_refund": 0,
                                    "subject": sort_list_orders[region]['subject'],
                                    "supplierArticle": sort_list_orders[region]['supplierArticle'],
                                    "brand": sort_list_orders[region]['brand'],
                                    "amount_orders": sort_list_orders[region]['amount'],
                                    "count_orders": sort_list_orders[region]['count'],
                                    }})
    return result


async def sorting_region(seller_id, period):
    """
        Возвращает статистику по регионам:
        period - период за который вернуть статистику (сегодня - today, вчера - yesterday,
         за 7 дней - in_7_days, за 30 дней - in_30_days)
        count_back - Количество возвратов
        count_bought - Количество заказов
        sum_payment - Чистая выручка со всех заказов
        sum_back - Сумма на которую вернули товар
    """
    sort_sales = SortingSales(seller_id)
    sort_orders = SortingOrders(seller_id)
    if period == "today":
        _, _, _, _, sort_sales = await sort_sales.sorting_today(with_search=True)
        _, _, sort_orders = await sort_orders.sorting_today(with_search=True)
    elif period == "yesterday":
        _, _, _, _, sort_sales = await sort_sales.sorting_yesterday(with_search=True)
        _, _, sort_orders = await sort_orders.sorting_yesterday(with_search=True)
    elif period == "in_7_days":
        _, _, _, _, sort_sales = await sort_sales.sorting_in_7_days(with_search=True)
        _, _, sort_orders = await sort_orders.sorting_in_7_days(with_search=True)
    elif period == "in_30_days":
        _, _, _, _, sort_sales = await sort_sales.sorting_in_30_days(with_search=True)
        _, _, sort_orders = await sort_orders.sorting_in_30_days(with_search=True)
    else:
        _, _, _, _, sort_sales = await sort_sales.sorting_another_period(period)
        _, _, sort_orders = await sort_orders.sorting_another_period(period)
    result = {}
    sort_sales_parameter = SortingParameterSales(sort_sales)
    sort_list_sales, sales_region = sort_sales_parameter.sorting_for_region()
    sort_orders_parameter = SortingParameterOrders(sort_orders)
    sort_list_orders, orders_region = sort_orders_parameter.sorting_for_region()
    unique_orders_region = set(sales_region + orders_region)
    for region in unique_orders_region:
        if region in sort_list_sales and region in sort_list_orders:
            result.update({region: {"amount_payment": sort_list_sales[region]['amount_payment'],
                                    "amount_refund": sort_list_sales[region]['amount_refund'],
                                    "count_payment": sort_list_sales[region]['count_payment'],
                                    "count_refund": sort_list_sales[region]['count_refund'],
                                    "subject": sort_list_sales[region]['subject'],
                                    "supplierArticle": sort_list_sales[region]['supplierArticle'],
                                    "brand": sort_list_sales[region]['brand'],
                                    "amount_orders": sort_list_orders[region]['amount'],
                                    "count_orders": sort_list_orders[region]['count'],

                                    }})
        elif region in sort_list_sales:
            result.update({region: {"amount_payment": sort_list_sales[region]['amount_payment'],
                                    "amount_refund": sort_list_sales[region]['amount_refund'],
                                    "count_payment": sort_list_sales[region]['count_payment'],
                                    "count_refund": sort_list_sales[region]['count_refund'],
                                    "subject": sort_list_sales[region]['subject'],
                                    "supplierArticle": sort_list_sales[region]['supplierArticle'],
                                    "brand": sort_list_sales[region]['brand'],
                                    "amount_orders": 0,
                                    "count_orders": 0,
                                    }})
        elif region in sort_list_orders:
            result.update({region: {"amount_payment": 0,
                                    "amount_refund": 0,
                                    "count_payment": 0,
                                    "count_refund": 0,
                                    "subject": sort_list_orders[region]['subject'],
                                    "supplierArticle": sort_list_orders[region]['supplierArticle'],
                                    "brand": sort_list_orders[region]['brand'],
                                    "amount_orders": sort_list_orders[region]['amount'],
                                    "count_orders": sort_list_orders[region]['count'],
                                    }})
    return result


async def sorting_brand(seller_id, period):
    """
        Возвращает статистику по брендам:
        period - период за который вернуть статистику (сегодня - today, вчера - yesterday,
         за 7 дней - in_7_days, за 30 дней - in_30_days)
        count_back - Количество возвратов
        count_bought - Количество заказов
        sum_payment - Чистая выручка со всех заказов
        sum_back - Сумма на которую вернули товар
    """
    sort_sales = SortingSales(seller_id)
    sort_orders = SortingOrders(seller_id)
    if period == "today":
        _, _, _, _, sort_sales = await sort_sales.sorting_today(with_search=True)
        _, _, sort_orders = await sort_orders.sorting_today(with_search=True)
    elif period == "yesterday":
        _, _, _, _, sort_sales = await sort_sales.sorting_yesterday(with_search=True)
        _, _, sort_orders = await sort_orders.sorting_yesterday(with_search=True)
    elif period == "in_7_days":
        _, _, _, _, sort_sales = await sort_sales.sorting_in_7_days(with_search=True)
        _, _, sort_orders = await sort_orders.sorting_in_7_days(with_search=True)
    elif period == "in_30_days":
        _, _, _, _, sort_sales = await sort_sales.sorting_in_30_days(with_search=True)
        _, _, sort_orders = await sort_orders.sorting_in_30_days(with_search=True)
    else:
        _, _, _, _, sort_sales = await sort_sales.sorting_another_period(period)
        _, _, sort_orders = await sort_orders.sorting_another_period(period)
    result = {}
    sort_sales_parameter = SortingParameterSales(sort_sales)
    sort_list_sales, sales_region = sort_sales_parameter.sorting_for_brand()
    sort_orders_parameter = SortingParameterOrders(sort_orders)
    sort_list_orders, orders_region = sort_orders_parameter.sorting_for_brand()
    unique_orders_region = set(sales_region + orders_region)
    for region in unique_orders_region:
        if region in sort_list_sales and region in sort_list_orders:
            result.update({region: {"amount_payment": sort_list_sales[region]['amount_payment'],
                                    "amount_refund": sort_list_sales[region]['amount_refund'],
                                    "count_payment": sort_list_sales[region]['count_payment'],
                                    "count_refund": sort_list_sales[region]['count_refund'],
                                    "subject": sort_list_sales[region]['subject'],
                                    "supplierArticle": sort_list_sales[region]['supplierArticle'],
                                    "brand": sort_list_sales[region]['brand'],
                                    "amount_orders": sort_list_orders[region]['amount'],
                                    "count_orders": sort_list_orders[region]['count'],

                                    }})
        elif region in sort_list_sales:
            result.update({region: {"amount_payment": sort_list_sales[region]['amount_payment'],
                                    "amount_refund": sort_list_sales[region]['amount_refund'],
                                    "count_payment": sort_list_sales[region]['count_payment'],
                                    "count_refund": sort_list_sales[region]['count_refund'],
                                    "subject": sort_list_sales[region]['subject'],
                                    "supplierArticle": sort_list_sales[region]['supplierArticle'],
                                    "brand": sort_list_sales[region]['brand'],
                                    "amount_orders": 0,
                                    "count_orders": 0,
                                    }})
        elif region in sort_list_orders:
            result.update({region: {"amount_payment": 0,
                                    "amount_refund": 0,
                                    "count_payment": 0,
                                    "count_refund": 0,
                                    "subject": sort_list_orders[region]['subject'],
                                    "supplierArticle": sort_list_orders[region]['supplierArticle'],
                                    "brand": sort_list_orders[region]['brand'],
                                    "amount_orders": sort_list_orders[region]['amount'],
                                    "count_orders": sort_list_orders[region]['count'],
                                    }})
    return result


async def sorting_no_grouping(seller_id, period):
    """ Сортировка без группы """
    sort_sales = SortingSales(seller_id)
    sort_orders = SortingOrders(seller_id)
    if period == "today":
        amount_payment, amount_refund, count_payment, count_refund, _ = await sort_sales.sorting_today(with_search=True)
        amount_orders, count_orders, _ = await sort_orders.sorting_today(with_search=True)
    elif period == "yesterday":
        amount_payment, amount_refund, count_payment, count_refund, _ = await sort_sales.sorting_yesterday(
            with_search=True)
        amount_orders, count_orders, _ = await sort_orders.sorting_yesterday(with_search=True)
    elif period == "in_7_days":
        amount_payment, amount_refund, count_payment, count_refund, _ = await sort_sales.sorting_in_7_days(
            with_search=True)
        amount_orders, count_orders, _ = await sort_orders.sorting_in_7_days(with_search=True)
    elif period == "in_30_days":
        amount_payment, amount_refund, count_payment, count_refund, _ = await sort_sales.sorting_in_30_days(
            with_search=True)
        amount_orders, count_orders, _ = await sort_orders.sorting_in_30_days(with_search=True)
    else:
        amount_payment, amount_refund, count_payment, count_refund, _ = await sort_sales.sorting_another_period(period)
        amount_orders, count_orders, _ = await sort_orders.sorting_another_period(period)

    return {"amount_payment": amount_payment, "amount_refund": amount_refund,
            "count_payment": count_payment,
            "count_refund": count_refund, "amount_orders": amount_orders, "count_orders": count_orders}


async def sorting_orders_no_grouping(seller_id):
    """ Без группы заказы """
    data = await select_ordered_by_seller_id(seller_id)
    sorting_orders = sorted(data, key=lambda x: x.date, reverse=True)
    return sorting_orders


async def sorting_returns_no_grouping(seller_id):
    """ Без группы  возвтраы """
    data = await select_sales_by_seller_id(seller_id)
    sorting_orders = [product for product in data if product.saleID.startswith('R')]
    sorting_orders = sorted(sorting_orders, key=lambda x: x.date, reverse=True)
    return sorting_orders


async def sorting_sales_no_grouping(seller_id):
    """ Без группы  продажи  """
    data = await select_sales_by_seller_id(seller_id)
    sorting_orders = [product for product in data if product.saleID.startswith('S')]
    sorting_orders = sorted(sorting_orders, key=lambda x: x.date, reverse=True)
    return sorting_orders


async def sorting_by_days(seller_id, method):
    """ Сортировка по дням """
    substring = ''
    if method == 'sales':
        substring = 'S'
    elif method == 'returns':
        substring = 'R'
    if substring:
        data = await select_sales_by_seller_id(seller_id)
        sorting_orders = [product for product in data if product.saleID.startswith(substring)]
    else:
        sorting_orders = await select_ordered_by_seller_id(seller_id)
    sorting_orders = sorted(sorting_orders, key=lambda x: x.date, reverse=True)
    unique_date = []
    unique_nmId = []
    for order in sorting_orders:
        date = order.date.strftime("%Y-%m-%d")
        if date not in unique_date:
            unique_date.append(date)
        if order.nmId not in unique_nmId:
            unique_nmId.append(order.nmId)

    result = {}
    for date in unique_date:
        for nmId in unique_nmId:
            count, brand, return_nmId, amount, return_date, subject, supplierArticle, techSize = 0, 0, 0, 0, 0, 0, 0, 0
            for order in sorting_orders:
                order_date = order.date.strftime("%Y-%m-%d")
                if date == order_date and nmId == order.nmId:
                    count += 1
                    brand = order.brand
                    return_nmId = order.nmId
                    return_date = order.date.strftime("%Y.%m.%d %H:%M:%S")
                    subject = order.subject
                    if substring:
                        amount = order.forPay
                    else:
                        amount = order.price
                    supplierArticle = order.supplierArticle
                    techSize = order.techSize
            if count > 0:
                result.update({return_date: {"count": count, "brand": brand, "nmId": return_nmId,
                                             "subject": subject, "amount": amount, "supplierArticle": supplierArticle,
                                             "techSize": techSize}})
    return result


async def sorting_by_month(seller_id, method):
    """ Сортировка по месяцу """
    substring = ''
    if method == 'sales':
        substring = 'S'
    elif method == 'returns':
        substring = 'R'
    if substring:
        data = await select_sales_by_seller_id(seller_id)
        sorting_orders = [product for product in data if product.saleID.startswith(substring)]
    else:
        sorting_orders = await select_ordered_by_seller_id(seller_id)
    sorting_orders = sorted(sorting_orders, key=lambda x: x.date, reverse=True)
    unique_date = []
    unique_nmId = []
    for order in sorting_orders:
        date = order.date.strftime("%Y-%m")
        if date not in unique_date:
            unique_date.append(date)
        if order.nmId not in unique_nmId:
            unique_nmId.append(order.nmId)

    date_list = []
    result = {}
    for date in unique_date:
        nmId_dict = []
        for nmId in unique_nmId:
            nmId_list = []
            count, brand, return_nmId, amount, return_date, subject, supplierArticle, techSize = 0, 0, 0, 0, 0, 0, 0, 0
            for order in sorting_orders:
                order_date = order.date.strftime("%Y-%m")
                if date == order_date and nmId == order.nmId:
                    nmId_list.append(order)
                    count += 1
                    brand = order.brand
                    return_nmId = order.nmId
                    return_date = order.date.strftime("%Y.%m %d %H:%M:%S")
                    subject = order.subject
                    if substring:
                        amount = order.forPay
                    else:
                        amount = order.price
                    supplierArticle = order.supplierArticle
                    techSize = order.techSize
            if nmId_list:
                nmId_dict.append(nmId_list)
            if count > 0:
                result.update({return_date: {"count": count, "brand": brand, "nmId": return_nmId,
                                             "subject": subject, "amount": amount, "supplierArticle": supplierArticle,
                                             "techSize": techSize}})
        if nmId_dict:
            date_list.append(nmId_dict)
    return result


async def get_info_stocks_product(seller_id):
    """ Статистика по складу """
    products = await select_stocks(seller_id)
    in_stock, to_client, from_client, on_sale = 0, 0, 0, 0
    unique_nmId = []
    for product in products:
        if product.nmId not in unique_nmId:
            unique_nmId.append(product.nmId)
            in_stock += product.quantityFull
            to_client += product.inWayToClient
            from_client += product.inWayFromClient
            if product.quantity >= 1:
                on_sale += 1
    return in_stock, to_client, from_client, on_sale


async def get_in_stock_stocks_product(seller_id):
    """ Сортирует товары по остаткам """
    products = await select_stocks_by_seller_id(seller_id)
    sorting_products = []
    unique_nmId = set()
    # unique_techSize = []
    # unique_warehouse = []
    for product in products:
        if (product.nmId, product.techSize) not in unique_nmId:
            unique_nmId.add((product.nmId,product.techSize))
            sorting_products.append(product)
        else:
            for i in sorting_products:
                if i.nmId == product.nmId and i.techSize == product.techSize:
                    i.quantityFull += product.quantityFull
                    i.quantity += product.quantity


    sorting_products = sorted(sorting_products, key=lambda x: x.quantityFull)
    return sorting_products


async def get_to_client_stocks_product(seller_id):
    """ Сортирует товары которые в доставке """
    products = await select_stocks_by_seller_id(seller_id)
    sorting_products = []
    unique_nmId = set()
    # unique_techSize = []
    # unique_warehouse = []
    for product in products:
        if (product.nmId, product.techSize) not in unique_nmId:
            unique_nmId.add((product.nmId, product.techSize))
            sorting_products.append(product)
        else:
            for i in sorting_products:
                if i.nmId == product.nmId and i.techSize == product.techSize:
                    i.quantityFull += product.quantityFull
                    i.quantity += product.quantity
    sorting_products = sorted(sorting_products, key=lambda x: x.inWayToClient)
    return sorting_products


async def get_from_client_stocks_product(seller_id):
    """ Сортирует товары которые в возврате """
    products = await select_stocks_by_seller_id(seller_id)
    sorting_products = []
    unique_nmId = set()
    # unique_techSize = []
    # unique_warehouse = []
    for product in products:
        if (product.nmId, product.techSize) not in unique_nmId:
            unique_nmId.add((product.nmId, product.techSize))
            sorting_products.append(product)
        else:
            for i in sorting_products:
                if i.nmId == product.nmId and i.techSize == product.techSize:
                    i.quantityFull += product.quantityFull
                    i.quantity += product.quantity
    sorting_products = sorted(sorting_products, key=lambda x: x.inWayFromClient)
    return sorting_products


async def get_on_sale_stocks_product(seller_id):
    """ Сортирует товары которые на продаже """
    products = await select_stocks_by_seller_id(seller_id)
    sorting_products = []
    unique_nmId = set()
    # unique_techSize = []
    # unique_warehouse = []
    for product in products:
        if (product.nmId, product.techSize) not in unique_nmId:
            unique_nmId.add((product.nmId, product.techSize))
            sorting_products.append(product)
        else:
            for i in sorting_products:
                if i.nmId == product.nmId and i.techSize == product.techSize:
                    i.quantityFull += product.quantityFull
                    i.quantity += product.quantity
    sorting_products = sorted(sorting_products, key=lambda x: x.quantity)
    return sorting_products


# def get_ordered_sum(token):
#     data = get_ordered_products(token)
#     if data:
#         return int(
#             sum((x["totalPrice"] * (1 - x["discountPercent"] / 100)) for x in data)
#         )
#     return 0
#
#
# def get_weekly_payment(token):
#     data = get_sales_products(token, week=True, flag=0)
#     if data:
#         payment = sum((x["forPay"]) for x in data)
#         return int(payment)
#     return 0
#
#
async def get_stock_products(token):
    """Getting products in stock."""
    client = X64ApiClient(token)
    data = await client.get_stock()
    attempt = 0
    while data.status_code != 200:
        attempt += 1
        if attempt > 10:
            return None
        time.sleep(RETRY_DELAY)
        data = await client.get_stock()
    return data.json()


async def get_ordered_products(token, date_from, flag=0):
    """ Возвращает заказ:
                        flag = 0 возвращает закзы за days дней
                        flag = 1 возвращает заказы за days определенный день
                    """
    client = X64ApiClient(token)
    data = await client.get_ordered(url="orders", flag=flag, date_from=date_from)
    attempt = 0
    while data.status_code != 200:
        attempt += 1
        if attempt > 10:
            return None
        data = await client.get_ordered(url="orders", flag=flag, date_from=date_from)
    return data.json()


async def get_sales_products(token, date_from):
    """ Возвращает выкупы:
                    flag = 0 возвращает закзы за days дней
                    flag = 1 возвращает заказы за days определенный день
                """
    client = X64ApiClient(token)
    data = await client.get_ordered(url="sales", flag=0, date_from=date_from)
    attempt = 0
    while data.status_code != 200:
        attempt += 1
        if attempt > 10:
            return None
        data = await client.get_ordered(url="sales", flag=0, date_from=date_from)
    return data.json()


async def valid_token(token):
    """ Проверка токена на валидность
    """
    client = X64ApiClient(token)
    data = await client.check_token()
    attempt = 0
    while data != 200:
        attempt += 1
        if attempt > 10:
            return data
        data = await client.check_token()
    return 200


def get_ordered_products_fbc(token, date_from):
    """ Возвращает заказ:"""
    client = JWTApiClient(token)
    data = client.get_orders(date_from=date_from)
    return data


def valid_token_fbs(token):
    """ Проверка фбс токена на валидность
        """
    client = JWTApiClient(token)
    data = client.check_token()
    # print(data.text)
    attempt = 0
    while data.status_code != 200:
        attempt += 1
        if attempt > 10:
            return data.status_code
        data = client.check_token()
    return data.status_code
