from aiogram.utils.callback_data import CallbackData

set_command_seller_id = CallbackData("set", "command_name", "seller_id")
set_report_callback = CallbackData("set", "method", "command_name", "seller_id", "start", "end")
change_sellers_callback = CallbackData("set", "group", "command_name", "seller_id")
order_or_returns_callback = CallbackData("set", "method", "command_name", "seller_id", "start", "end")
change_api_callback = CallbackData("set", "method", "version_api", "seller_id")
set_search_callback = CallbackData("set", "method", "command_name", "seller_id", "start", "end", "from_keyboard")
set_another_period_callback = CallbackData("set", "method", "command_name", "seller_id", "start", "end", "filter")
paid_callback = CallbackData("set", "amount", "command_name", "user_id")
set_paid = CallbackData("set", "text_name")
choice_date_xlsx_callback = CallbackData("set", "command_name", "seller_id", "days")
