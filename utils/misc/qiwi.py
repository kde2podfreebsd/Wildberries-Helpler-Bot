import datetime
import random
from dataclasses import dataclass

import pyqiwi

from data.config import QIWI_TOKEN, WALLET_QIWI, QIWI_PUBKEY

wallet = pyqiwi.Wallet(token=QIWI_TOKEN, number=WALLET_QIWI)


class NotEnoughMoney(Exception):
    pass


class NoPaymentFound(Exception):
    pass


@dataclass
class Payment:
    amount: int
    id: str = None

    def create(self):
        self.id = str(round(random.uniform(1000000, 9999999)))

    def check_payment(self):
        start_date = datetime.datetime.now() - datetime.timedelta(days=2)
        transactions = wallet.history(start_date=start_date).get("transactions")
        for transactions in transactions:
            if transactions.comment:
                if str(self.id) in transactions.comment:
                    if float(transactions.total.amount) >= float(self.amount):
                        return True
                    else:
                        raise NotEnoughMoney
        else:
            raise NoPaymentFound

    @property
    def invoice(self):
        link = "https://oplata.qiwi.com/create?publicKey={pubkey}&amount={amount}&comment={comment}"
        return link.format(pubkey=QIWI_PUBKEY, amount=self.amount, comment=self.id)


@dataclass()
class Accept:
    amount: int
    nomer: str

    def send_payment(self):
        wallet.send(pid=str(99), amount=self.amount, recipient=self.nomer)


@dataclass()
class Balance:

    def balance(self):
        wallet.balance()
        return wallet.balance()
