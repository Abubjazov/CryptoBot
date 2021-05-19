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

    if callback_data in (inline_keyboards.CALLBACK_BTC, inline_keyboards.CALLBACK_LTC, inline_keyboards.CALLBACK_ETH,
                         inline_keyboards.CALLBACK_DOGE, inline_keyboards.CALLBACK_ADA, inline_keyboards.CALLBACK_BCH):
        pair = {
            inline_keyboards.CALLBACK_BTC: 'USD-BTC',
            inline_keyboards.CALLBACK_LTC: 'USD-LTC',
            inline_keyboards.CALLBACK_ETH: 'USD-ETH',
            inline_keyboards.CALLBACK_DOGE: 'USD-DOGE',
            inline_keyboards.CALLBACK_ADA: 'USD-ADA',
            inline_keyboards.CALLBACK_BCH: 'USD-BCH'
        }[callback_data]  # выбираем пару

        current_price = client.get_last_price(pair=pair)  # узнаём текущий курс пары
        now = get_now_formatted()  # узнаём текущие дату и время
        text = f'Пара {pair}\n\n на данный момент торгуется по цене \n\n {current_price} USD \n\n{now}'

        if callback_data in (inline_keyboards.CALLBACK_BTC, inline_keyboards.CALLBACK_LTC, inline_keyboards.CALLBACK_ETH):
            update.effective_message.edit_text(
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=inline_keyboards.get_inline_keyboard_1()  # добавляем инлайн клавиатуру №1
                                                                       # если была нажата кнопка из её состава
            )

        else:
            update.effective_message.edit_text(
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=inline_keyboards.get_inline_keyboard_2()  # добавляем инлайн клавиатуру №2
                                                                       # если была нажата кнопка из её состава
            )

    elif callback_data == inline_keyboards.CALLBACK_MORE:  # замена клавиатуры №1 на клавиатуру №2
        text = update.effective_message.text
        update.effective_message.edit_text(
            text=text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=inline_keyboards.get_inline_keyboard_2()
        )

    elif callback_data == inline_keyboards.CALLBACK_BACK:  # замена клавиатуры №2 на клавиатуру №1
        text = update.effective_message.text
        update.effective_message.edit_text(
            text=text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=inline_keyboards.get_inline_keyboard_1()
        )

    else:
        update.effective_message.edit_text(                 # если вдруг прилетит что то неизвестное
            text='Похоже что то пошло не по плану... 😅\n\nПопробуйте ещё раз',
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=inline_keyboards.get_inline_keyboard_1()
        )
