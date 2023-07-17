# from loader import db
import asyncio

from data.config import UPDATE_SALES_AND_ORDERS, UPDATE_STOCKS, TARIFF_ACTIVATION, DEVIATING_TARIFFS, ALERT_TARIFF, \
    DELETING_ITEM
from utils.db_api import db_gino
from utils.misc.logging import configure_logger
from utils.misc.start_by_time import update_all_bought, update_stocks, enable_tariff, shutdown_bot, \
    notification_of_tariff, deleting_all_items
from utils.set_bot_commands import set_default_commands

from utils.wb_api.method_warehouse import get_full_report

async def on_startup(dp):
    import filters
    import middlewares
    filters.setup(dp)
    middlewares.setup(dp)
    configure_logger(True)
    from utils.notify_admins import on_startup_notify
    await db_gino.on_startup(dp)
    await on_startup_notify(dp)
    await set_default_commands(dp)


if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    loop = asyncio.get_event_loop()
    # Обновляет статистику у всех пользователей
    loop.create_task(update_all_bought(UPDATE_SALES_AND_ORDERS))
    loop.create_task(update_stocks(UPDATE_STOCKS))
    loop.create_task(enable_tariff(TARIFF_ACTIVATION))
    loop.create_task(shutdown_bot(DEVIATING_TARIFFS))
    loop.create_task(notification_of_tariff(ALERT_TARIFF))
    loop.create_task(deleting_all_items(DELETING_ITEM))
    executor.start_polling(dp, on_startup=on_startup)
