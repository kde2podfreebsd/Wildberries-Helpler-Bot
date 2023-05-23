def button_name_by_filter(command_name):
    if command_name == "subject":
        subject_button = "💠 Предметы"
    else:
        subject_button = "Предметы"

    if command_name == "category":
        category_button = "💠 Категории"
    else:
        category_button = "Категории"

    if command_name == "vendor_code":
        vendor_code_button = "💠 Артикулы"
    else:
        vendor_code_button = "Артикулы"

    if command_name == "brand":
        brand_button = "💠 Бренды"
    else:
        brand_button = "Бренды"

    if command_name == "region":
        region_button = "💠 Регионы"
    else:
        region_button = "Регионы"

    if command_name == "grouping":
        no_grouping_button = "💠 Без группировки"
    else:
        no_grouping_button = "Без группировки"

    return subject_button, vendor_code_button, category_button, brand_button, region_button, no_grouping_button


def button_name_by_order(command_name):
    if command_name == "by_days":
        days_button = "💠 По дням"
    else:
        days_button = "По дням"

    if command_name == "by_week":
        week_button = "💠 По неделям"
    else:
        week_button = "По неделям"

    if command_name == "by_month":
        month_button = "💠 По месяцам"
    else:
        month_button = "По месяцам"

    if command_name == "no_grouping":
        no_grouping_button = "💠 Без группировки"
    else:
        no_grouping_button = "Без группировки"

    return days_button, week_button, month_button, no_grouping_button
