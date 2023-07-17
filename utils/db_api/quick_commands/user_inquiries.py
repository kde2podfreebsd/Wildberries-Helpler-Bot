from asyncpg import UniqueViolationError

from utils.db_api.db_gino import User, Association, Seller


async def add_user(id: int, name: str, chat_id: int, balance: int):
    """ Добавление пользователя в БД"""
    try:
        user = User(id=id, name=name, chat_id=chat_id, balance=balance)

        await user.create()

    except UniqueViolationError:
        pass


async def update_user_seller(seller: Seller, user_id: int):
    """ Связь пользователь + продавец многие ко многим"""
    try:
        user = await User.query.where(User.id == user_id).gino.first()
        user_seller = Association(seller_id=seller.id, user_id=user.id)
        await user_seller.create()
    except UniqueViolationError:
        pass


async def select_user(user_id: int):
    """ Выбор пользователя """
    return await User.query.where(User.id == user_id).gino.first()


async def select_user_by_seller(seller_id: int):
    """ Выбор всех пользователе у продавцов """
    founding_users = await Association.query.where(Association.seller_id == seller_id).gino.all()
    users_list = []
    for i in founding_users:
        user = await User.query.where(User.id == i.user_id).gino.first()
        users_list.append(user)
    return users_list


async def update_balance(id: int, summ):
    user = await User.get(id)
    await user.update(balance=user.balance + summ).apply()
    return user

async def update_discount(id: int, discount: int):
    user = await User.get(id)
    await user.update(discount=discount).apply()
    # return user