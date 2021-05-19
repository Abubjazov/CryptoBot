"""Инлайн клавиатуры"""
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

"""Инлайн кнопки"""
CALLBACK_BTC = 'BTC'
CALLBACK_LTC = 'LTC'
CALLBACK_ETH = 'ETH'


def get_inline_keyboard() -> InlineKeyboardMarkup:
    """Инлайн клавиатура"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='BTC', callback_data=CALLBACK_BTC),
                InlineKeyboardButton(text='LTC', callback_data=CALLBACK_LTC),
                InlineKeyboardButton(text='ETH', callback_data=CALLBACK_ETH)
            ]
        ]
    )
