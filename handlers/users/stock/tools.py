async def get_headline(command_name):
    headline = ''
    if command_name == "in_stock":
        headline = 'остатки по возрастанию ↗️'
    elif command_name == "reverse_in_stock":
        headline = 'остатки по убыванию ↘️'
    elif command_name == "to_client":
        headline = 'в пути по возрастанию ↗️'
    elif command_name == "revers_to_client":
        headline = 'в пути по убыванию ↘️'
    elif command_name == "from_client":
        headline = 'от клиента по возрастанию ↗️'
    elif command_name == "revers_from_client":
        headline = 'от клиента по убыванию ↘️'
    elif command_name == "on_sale":
        headline = 'на продаже по возрастанию ↗️'
    elif command_name == "revers_on_sale":
        headline = 'на продаже по убыванию ↘️'
    return headline
