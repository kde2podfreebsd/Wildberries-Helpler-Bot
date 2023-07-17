import requests
import datetime
import json

TEST_TOKEN_FBS = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjAxYzU4NDhjLTg0MzAtNDIyZS1iMWIzLTc5MmM3ODE1ZDBkMiJ9.aIfhgRA5jaGxeCgAX8j1WSdEV6nsYl6gCAoBwcft0XA'

class JWTApiClient:
    """Get Marketplace Statistics."""

    def __init__(self, new_api_key: str):
        self.token = new_api_key
        self.base = "https://suppliers-api.wildberries.ru/api/v3/supplies"

    def build_headers(self):
        return {
            "Authorization": self.token,
            "accept": "application/json",
            "Content-Type": "application/json",
        }

    def get_stock(self):
        url = f"https://statistics-api.wildberries.ru/api/v1/supplier/stocks"

        offset = 1000

        def get_page(skip=0):
            get_params = {
                "next": skip,
                "limit": offset,
            }
            return requests.get(url, get_params, headers=self.build_headers())

        response = get_page()
        if response.status_code != 200:
            return []

        stock = []
        batch = response.json()
        total = int(batch.get("total"))
        attempt = 1

        stock += batch["stocks"]
        while total > offset * attempt:
            stock += get_page(offset * attempt).json()["stocks"]
            attempt += 1
        return stock

    def get_orders(self, date_from):
        url = "https://suppliers-api.wildberries.ru/api/v3/orders"

        date_from = datetime.datetime.strptime(date_from, '%Y-%m-%dT%H:%M:%S')
        date_from = int(date_from.timestamp())
        offset = 1000

        def get_page(skip=0):
            get_params = {
                "next": skip,
                "limit": offset,
                "dateFrom": date_from,
            }
            return requests.get(url=url, params=get_params, headers=self.build_headers())

        response = get_page()
        if response.status_code != 200:
            return []

        orders = []
        batch = response.json()
        # print(batch)
        total = len(batch['orders'])
        attempt = 1
        # print(total)

        orders += batch["orders"]
        while total > offset * attempt:
            orders += get_page(offset * attempt).json()["orders"]
            attempt += 1
        return orders

    def check_token(self):
        url = self.base
        params = {
            "limit": "1000",
            "next": "0"
        }
        return requests.get(url, headers=self.build_headers(), params=params)