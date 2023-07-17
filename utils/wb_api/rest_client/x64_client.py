import aiohttp
import requests

from utils.wb_api.tools import get_date

RETRY_DELAY = 0.1
TEST_TOKEN = 'MmNkMzU2MzUtMGI5Yy00NjljLWE5NGYtNWZkMWJkNTY3ZTkx'


class X64ApiClient:
    """Класс для работы с WB API X64."""

    def __init__(self, token):
        self.token = token
        self.base_url = "https://statistics-api.wildberries.ru/api/v1/supplier/"

    @staticmethod
    async def connect(client, params, headers, server):
        # print(server)
        # redis_client.get_date
        async with client.get(url=server, headers=headers, params=params) as resp:
            return resp.status

    @staticmethod
    async def response(params, headers, server):
        response = requests.get(url=server, params=params, headers=headers)
        return response

    async def get_stock(self):
        params = {
            "dateFrom": get_date(days=90),
            "key": self.token,
        }
        headers = {
            "Authorization": self.token
        }
        return await self.response(params, headers, self.base_url + "stocks")

    async def get_ordered(self, url, date_from, flag=1):
        params = {
            "dateFrom": date_from,
            "flag": flag,
        }
        headers = {
            "Authorization": self.token
        }
        return await self.response(params, headers, self.base_url + url)

    async def check_token(self):
        params = {
            "dateFrom": "2023-01-27",
        }
        headers = {
            "Authorization":self.token
        }
        async with aiohttp.ClientSession() as client:
            return await self.connect(client, params, headers, self.base_url + "incomes")