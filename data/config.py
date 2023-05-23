import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))
DATABASE = str(os.getenv("DATABASE"))
PGUSER = str(os.getenv("PGUSER"))
PGPASSWORD = str(os.getenv("PGPASSWORD"))
SUPPORT_LINK = str(os.getenv("SUPPORT_LINK"))
BOT_NAME = str(os.getenv("BOT_NAME"))
UPDATE_SALES_AND_ORDERS = int(os.getenv("UPDATE_SALES_AND_ORDERS"))
UPDATE_STOCKS = int(os.getenv("UPDATE_STOCKS"))
AMOUNT_TARIFF = int(os.getenv("AMOUNT_TARIFF"))
TARIFF_ACTIVATION = int(os.getenv("TARIFF_ACTIVATION"))
DEVIATING_TARIFFS = int(os.getenv("DEVIATING_TARIFFS"))
ALERT_TARIFF = int(os.getenv("ALERT_TARIFF"))
DELETING_ITEM = int(os.getenv("DELETING_ITEM"))
YOOTOKEN = str(os.getenv("YOOTOKEN"))

admins = [
    479516545,
]

ip = os.getenv("IP")

aiogram_redis = {
    'host': ip,
}

redis = {
    'address': (ip, 6379),
    'encoding': 'utf8'
}

POSTGRES_URL = f"postgresql://{PGUSER}:{PGPASSWORD}@{ip}/{DATABASE}"
