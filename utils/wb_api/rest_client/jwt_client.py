import requests

TEST_TOKEN_FBS = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjAxYzU4NDhjLTg0MzAtNDIyZS1iMWIzLTc5MmM3ODE1ZDBkMiJ9.aIfhgRA5jaGxeCgAX8j1WSdEV6nsYl6gCAoBwcft0XA'

class JWTApiClient:
    """Get Marketplace Statistics."""

    def __init__(self, new_api_key: str):
        self.token = new_api_key
        self.base = "https://statistics-api.wildberries.ru/api/v1/supplier/"

    def build_headers(self):
        return {
            "Authorization": self.token,
            "accept": "application/json",
            "Content-Type": "application/json",
        }

    def get_stock(self):
        url = f"https://statistics-api.wildberries.ru/api/v1/supplier/stocks"

        offset = 200

        def get_page(skip=0):
            get_params = {
                "skip": skip,
                "take": offset,
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
        url = "https://statistics-api.wildberries.ru/api/v1/supplier/orders"

        offset = 200

        def get_page(skip=0):
            get_params = {
                "skip": skip,
                "take": offset,
                "date_start": date_from,
            }
            return requests.get(url, get_params, headers=self.build_headers())

        response = get_page()
        if response.status_code != 200:
            return []

        orders = []
        batch = response.json()
        total = int(batch.get("total"))
        attempt = 1

        orders += batch["orders"]
        while total > offset * attempt:
            orders += get_page(offset * attempt).json()["orders"]
            attempt += 1
        return orders

    def check_token(self):
        url = self.base + "v1/info"
        return requests.get(url, headers=self.build_headers())
