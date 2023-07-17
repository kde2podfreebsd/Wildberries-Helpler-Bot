from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data.config import SUPPORT_LINK
from keyboards.inline.callback_datas import paid_callback

go_to_paid = InlineKeyboardMarkup(row_width=1)

paid = InlineKeyboardButton(text="💳 Перейти к оплате", callback_data="balance_and_paid")

go_to_paid.insert(paid)


def paid_keyboard():
    # keyboard = InlineKeyboardMarkup(row_width=2,
    #                                 inline_keyboard=[
    #                                     [
    #                                         InlineKeyboardButton(text="Ввести сумму", callback_data="other_amount"),
    #                                     ],
    #
    #                                     [
    #                                         InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_profile"),
    #                                         InlineKeyboardButton(text="👨🏻‍💻 Поддержка", url=SUPPORT_LINK),
    #                                     ]
    #                                 ])
    keyboard = InlineKeyboardMarkup(row_width=2,
                                    inline_keyboard=[
                                        [
                                            InlineKeyboardButton(text="+490 руб",
                                                                 callback_data="other_amount#490")
                                        ],
                                        [
                                            InlineKeyboardButton(text="+1 000 руб (скидка 1%)",
                                                                 callback_data="other_amount#1000")
                                        ],
                                        [
                                            InlineKeyboardButton(text="+3 000 руб (скидка 3%)",
                                                                 callback_data="other_amount#3000")
                                        ],
                                        [
                                            InlineKeyboardButton(text="+5 000 руб (скидка 5%)",
                                                                 callback_data="other_amount#5000")
                                        ],
                                        [
                                            InlineKeyboardButton(text="+10 000 руб (скидка 10%)",
                                                                 callback_data="other_amount#10000")
                                        ],
                                        [
                                            InlineKeyboardButton(text="Пополнения", callback_data="replenishment"),
                                            InlineKeyboardButton(text="Списания", callback_data="withdrawal")
                                        ],
                                        [
                                            InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_profile"),
                                            InlineKeyboardButton(text="👨🏻‍💻 Поддержка", url=SUPPORT_LINK),
                                        ]
                                    ])
    return keyboard
