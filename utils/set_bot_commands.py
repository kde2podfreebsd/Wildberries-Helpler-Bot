from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("my", "🐲 Личный кабинет"),
        types.BotCommand("stock", "📦 Товары и остатки"),
        types.BotCommand("reports", "📊 Отчеты"),
        types.BotCommand("tarif", "💰 Тарифы"),

    ])
