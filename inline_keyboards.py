"""Инлайн клавиатуры"""
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

"""Инлайн кнопки"""
CALLBACK_BTC = 'BTC'
CALLBACK_LTC = 'LTC'
CALLBACK_ETH = 'ETH'
CALLBACK_DOGE = 'DOGE'
CALLBACK_ADA = 'ADA'
CALLBACK_BCH = 'BCH'
CALLBACK_MORE = 'more'
CALLBACK_BACK = 'back'


def get_inline_keyboard_1():
    """Инлайн клавиатура"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='BTC', callback_data=CALLBACK_BTC),
                InlineKeyboardButton(text='LTC', callback_data=CALLBACK_LTC),
                InlineKeyboardButton(text='ETH', callback_data=CALLBACK_ETH)
            ],
            [
                InlineKeyboardButton(text='Ещё', callback_data=CALLBACK_MORE)
            ]
        ]
    )


def get_inline_keyboard_2():
    """Инлайн клавиатура"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='DOGE', callback_data=CALLBACK_DOGE),
                InlineKeyboardButton(text='ADA', callback_data=CALLBACK_ADA),
                InlineKeyboardButton(text='BCH', callback_data=CALLBACK_BCH)
            ],
            [
                InlineKeyboardButton(text='Назад', callback_data=CALLBACK_BACK)
            ]
        ]
    )