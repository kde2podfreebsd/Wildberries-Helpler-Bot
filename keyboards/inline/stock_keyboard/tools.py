def button_name_by_stock(command_name):
    if command_name == "in_stock":
        in_stock_button = "💠 Остатки А-Я"
    else:
        in_stock_button = "Остатки А-Я"

    if command_name == "to_client":
        to_client_button = "💠 Едут к клиенту А-Я"
    else:
        to_client_button = "Едут к клиенту А-Я"

    if command_name == "from_client":
        from_client_button = "💠 Возвраты А-Я"
    else:
        from_client_button = "Возвраты А-Я"

    if command_name == "on_sale":
        on_sale_button = "💠 В продаже А-Я"
    else:
        on_sale_button = "В продаже А-Я"

    if command_name == "reverse_in_stock":
        reverse_in_stock_button = "💠 Остатки Я-А"
    else:
        reverse_in_stock_button = "Остатки Я-А"

    if command_name == "revers_to_client":
        revers_to_client_button = "💠 Eдут к клиенту Я-А"
    else:
        revers_to_client_button = "Eдут к клиенту Я-А"

    if command_name == "revers_from_client":
        revers_from_client_button = "💠 Возвраты Я-А"
    else:
        revers_from_client_button = "Возвраты Я-А"

    if command_name == "revers_on_sale":
        revers_on_sale_button = "💠 В продаже Я-А"
    else:
        revers_on_sale_button = "В продаже Я-А"

    return in_stock_button, to_client_button, from_client_button, on_sale_button, reverse_in_stock_button, revers_to_client_button, revers_from_client_button, revers_on_sale_button
