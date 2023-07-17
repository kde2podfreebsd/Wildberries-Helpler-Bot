from utils.wb_api.method_warehouse import sorting_region, sorting_subject, sorting_vendor_code, sorting_category, \
    sorting_brand, sorting_no_grouping


async def get_data_by_period(period, seller_id, command_name):
    operations = {

        'subject': lambda seller_id, period: sorting_subject(int(seller_id), period),

        'vendor_code': lambda seller_id, period: sorting_vendor_code(int(seller_id), period),

        'category': lambda seller_id, period: sorting_category(int(seller_id), period),

        'brand': lambda seller_id, period: sorting_brand(int(seller_id), period),

        'region': lambda seller_id, period: sorting_region(int(seller_id), period),

        'grouping': lambda seller_id, period: sorting_no_grouping(int(seller_id), period),

    }

    if period == "today":
        data = await operations[command_name](seller_id, period)
        name_tag = "СТАТИСТИКА ЗА СЕГОДНЯ"
    elif period == "yesterday":
        data = await operations[command_name](seller_id, period)
        name_tag = "СТАТИСТИКА ЗА ВЧЕРА"
    elif period == "in_7_days":
        name_tag = "СТАТИСТИКА ЗА 7 ДНЕЙ"
        data = await operations[command_name](seller_id, period)
    elif period == "in_30_days":
        name_tag = "СТАТИСТИКА ЗА 30 ДНЕЙ"
        data = await operations[command_name](seller_id, period)
    else:
        name_tag = f"СТАТИСТИКА ЗА {period}"
        data = await operations[command_name](seller_id, period)
    return data, name_tag


async def get_button_next_back(number_position, end, start):
    if number_position <= 10:
        next, back = False, False
    elif end < number_position and start > 0:
        next, back = True, True
    elif start == 0:
        next, back = True, False
    elif end >= number_position:
        next, back = False, True
    else:
        print("Возникло исключение в кнопках вперед/назад")

    return next, back
