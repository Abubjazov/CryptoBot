"""Модуль обработки Callback'ов"""
import datetime
import pytz
from telegram import Update, ParseMode
from telegram.ext import CallbackContext

import inline_keyboards
from coins_api import BittrexClient


client = BittrexClient()

def get_now_formatted() -> str:
    """Возвращает текущие дату и время строкой"""
    return get_now_datetime().strftime("%Y-%m-%d %H:%M:%S")


def get_now_datetime() -> datetime.datetime:
    """Возвращает текущий datetime с учётом времненной зоны Мск."""
    tz = pytz.timezone("Europe/Moscow")
    now = datetime.datetime.now(tz)
    return now


def callback_handler(update: Update, context: CallbackContext):
    """Обработка Callback'ов"""
    callback_data = update.callback_query.data

    if callback_data in (inline_keyboards.CALLBACK_BTC, inline_keyboards.CALLBACK_LTC, inline_keyboards.CALLBACK_ETH):
        pair = {
            inline_keyboards.CALLBACK_BTC: 'USD-BTC',
            inline_keyboards.CALLBACK_LTC: 'USD-LTC',
            inline_keyboards.CALLBACK_ETH: 'USD-ETH'
        }[callback_data]

        current_price = client.get_last_price(pair=pair)
        now = get_now_formatted()
        text = f'Пара {pair}\n\n на данный момент торгуется по цене \n\n {current_price} USD \n\n{now}'

        update.effective_message.edit_text(  # редактируем текущее сообщение и добавляем инлайн клавиатуру
            text=text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=inline_keyboards.get_inline_keyboard()
        )
