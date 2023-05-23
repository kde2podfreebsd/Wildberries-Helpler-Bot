import datetime


def get_date(days=None):
    """
        Возвращает дату в виде строки формата  %Y-%m-%dT00:00:00,
        за: (сегодняшнее число) - days
    """
    date = datetime.datetime.today() - datetime.timedelta(days=days)

    return date.strftime("%Y-%m-%dT00:00:00")


def array_slice(array, start, end):
    """
        Функция для среза словаря
        start - начало среза
        end - конец среза
    """
    new_array = {}
    for num, i in enumerate(array):
        if start <= num <= end:
            new_array.update({i: array[i]})
    return new_array


def format_date(date):
    """  Возвращает из строки формата  %Y-%m-%dT%H:%M:%S объект datetime """
    return datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")


def date_search(method):
    """  Возвращает дату с временем 00:00:00 """
    if method == "today":
        now = datetime.datetime.now().date().strftime("%Y-%m-%d")
        year = int(now.split("-")[0])
        mouth = int(now.split("-")[1])
        days = int(now.split("-")[2])
        date = datetime.datetime(year, mouth, days, 0, 0, 0)
    elif method == "yesterday":
        now = datetime.datetime.now().date() - datetime.timedelta(days=1)
        now = now.strftime("%Y-%m-%d")
        year = int(now.split("-")[0])
        mouth = int(now.split("-")[1])
        days = int(now.split("-")[2])
        date = datetime.datetime(year, mouth, days, 0, 0, 0)

    elif method == "in_7_days":
        now = datetime.datetime.now().date() - datetime.timedelta(days=7)
        now = now.strftime("%Y-%m-%d")
        year = int(now.split("-")[0])
        mouth = int(now.split("-")[1])
        days = int(now.split("-")[2])
        date = datetime.datetime(year, mouth, days, 0, 0, 0)

    elif method == "in_30_days":
        now = datetime.datetime.now().date() - datetime.timedelta(days=30)
        now = now.strftime("%Y-%m-%d")
        year = int(now.split("-")[0])
        mouth = int(now.split("-")[1])
        days = int(now.split("-")[2])
        date = datetime.datetime(year, mouth, days, 0, 0, 0)

    elif method == "in_90_days":
        now = datetime.datetime.now().date() - datetime.timedelta(days=90)
        now = now.strftime("%Y-%m-%d")
        year = int(now.split("-")[0])
        mouth = int(now.split("-")[1])
        days = int(now.split("-")[2])
        date = datetime.datetime(year, mouth, days, 0, 0, 0)

    return date


async def get_normal_number(number):
    return f'{number:,}'.replace(',', ' ')
