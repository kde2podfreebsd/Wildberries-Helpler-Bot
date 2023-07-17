import datetime
from typing import List

import sqlalchemy as sa
from aiogram import Dispatcher
from gino import Gino
from sqlalchemy import Column, DateTime, BigInteger, String, sql, ForeignKey, UniqueConstraint

from data import config

db = Gino()


class BaseModel(db.Model):
    __abstract__ = True

    def __str__(self):
        model = self.__class__.__name__
        table: sa.Table = sa.inspect(self.__class__)
        primary_key_columns: List[sa.Column] = table.primary_key.columns
        values = {
            column.name: getattr(self, self._column_name_map[column.name])
            for column in primary_key_columns
        }
        values_str = " ".join(f"{name}={value!r}" for name, value in values.items())
        return f"<{model} {values_str}>"


class TimeBaseModel(BaseModel):
    __abstract__ = True

    created_at = Column(DateTime(True), server_default=db.func.now())
    updated_at = Column(DateTime(True),
                        default=datetime.datetime.utcnow,
                        onupdate=datetime.datetime.utcnow,
                        server_default=db.func.now())


class Association(BaseModel):
    __tablename__ = 'association'
    user_id = Column(ForeignKey('user.id'), primary_key=True)
    seller_id = Column(ForeignKey('seller.id'), primary_key=True)
    __table_args__ = (UniqueConstraint('user_id', 'seller_id', name='_user_seller_uc'),
                      )

    query: sql.Select


class Seller(TimeBaseModel):
    __tablename__ = 'seller'
    id = Column(BigInteger, primary_key=True)
    name = Column(String(250))
    api_x64 = Column(String(250), unique=True)
    api_fbs = Column(String(250), unique=True)
    reserve = Column(db.Integer)
    bot_enable = Column(db.Boolean, default=False)
    export = Column(db.Boolean, default=False)
    tarif = Column(db.Boolean, default=False)
    starting_tarif = Column(DateTime(), default=None)
    filter_bought = Column(String(50), default=None)
    filter_stocks = Column(String(50), default=None)
    filter_orders = Column(String(50), default=None)
    last_scan_sales = Column(DateTime(), default=None)
    last_scan_orders = Column(DateTime(), default=None)
    search = Column(String(250), default=None)

    query: sql.Select


class ProductsBought(BaseModel):
    __tablename__ = 'products_bought'
    id = Column(BigInteger, primary_key=True)
    number = Column(String())
    seller_id = Column(ForeignKey('seller.id'))
    date = Column(DateTime())
    category = Column(String())
    subject = Column(String(50))
    nmId = Column(db.Integer)
    regionName = Column(String(50))
    brand = Column(String(50))
    techSize = Column(String(50))
    supplierArticle = Column(String(100))
    saleID = Column(String(50))
    forPay = Column(db.Float)
    query: sql.Select


class ProductsStocks(BaseModel):
    __tablename__ = 'products_stocks'
    id = Column(BigInteger, primary_key=True)
    seller_id = Column(ForeignKey('seller.id'))
    category = Column(String())
    subject = Column(String(50))
    nmId = Column(db.Integer)
    brand = Column(String(50))
    techSize = Column(String(50))
    supplierArticle = Column(String(100))
    quantity = Column(db.Integer)
    quantityFull = Column(db.Integer)
    inWayToClient = Column(db.Integer)
    inWayFromClient = Column(db.Integer)
    warehouseName = Column(String(50))
    query: sql.Select


class ProductsOrders(BaseModel):
    __tablename__ = 'products_orders'
    id = Column(BigInteger, primary_key=True)
    number = Column(String())
    seller_id = Column(ForeignKey('seller.id'))
    date = Column(DateTime())
    category = Column(String())
    subject = Column(String(50))
    nmId = Column(db.Integer)
    brand = Column(String(50))
    techSize = Column(String(50))
    supplierArticle = Column(String(100))
    price = Column(db.Integer)
    oblast = Column(String(100))
    query: sql.Select

class ProductsOrderedFBS(BaseModel):
    __tablename__ = 'products_ordered_fbs'
    id = Column(BigInteger, primary_key=True)
    createdAt = Column(DateTime())
    nmId = Column(db.Integer)
    price = Column(db.Integer)
    seller_id = Column(ForeignKey('seller.id'))
    warehouseId = Column(db.Integer)

    query: sql.Select

class User(TimeBaseModel):
    __tablename__ = 'user'
    id = Column(BigInteger, primary_key=True)
    name = Column(String(100))
    chat_id = Column(BigInteger, unique=True)
    balance = Column(db.Integer)
    discount = Column(db.Integer, default=0)
    current_seller = Column(db.Integer)

    query: sql.Select


class FreeTrail(TimeBaseModel):
    __tablename__ = 'free_trail'

    user_id = Column(ForeignKey('user.id'), primary_key=True)
    seller_api = Column(String(250), unique=True)
    __table_args__ = (UniqueConstraint('user_id', 'seller_api', name='_user_seller_api_uc'),)

    query: sql.Select


async def on_startup(dispatcher: Dispatcher):
    print("Установка связи с PostgreSQL")
    await db.set_bind(config.POSTGRES_URL)
    print("Готово")
    print("Создаем таблицу")
    await db.gino.create_all()
    print("Готово")
