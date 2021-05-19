"""Сервер Telegram бота, запускаемый непосредственно"""
import datetime

import pytz
from telegram import Bot, Update, InlineKeyboardMarkup, InlineKeyboardButton, ParseMode

from telegram.ext import Updater, CallbackContext, CallbackQueryHandler
from telegram.ext import MessageHandler
from telegram.ext import CommandHandler
from telegram.ext import Filters
from telegram.utils.request import Request

from bot_config import TOKEN

hello_msg = 'Я простой телеграм бот который знает\nкурсы основных криптовалют на данный момент.' \
            f'\n\nЧто бы увидеть текущий курс интересующей тебя валюты нажми на нужную кнопку. 😃'

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
    callback_data = str(update.callback_query.data)
    update.effective_message.edit_text(  # редактируем текущее сообщение и добавляем инлайн клавиатуру
        text=get_now_formatted() + '\n' + callback_data,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=get_inline_keyboard()
    )


def start_command_handler(update: Update, context: CallbackContext):
    """Обработка команд от пользователя"""
    user = update.effective_user  # извлекаем юзернейм
    if user:
        name = user.first_name
    else:
        name = 'Аноним'

    reply_text = f'Привет, {name}!\n\n' + hello_msg  # формируем сообщение

    update.message.reply_text(  # отправляем сообщение и добавляем инлайн клавиатуру
        text=reply_text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=get_inline_keyboard()
    )


def message_handler(update: Update, context: CallbackContext):
    """Обработка входящих сообщений"""
    user = update.effective_user  # извлекаем юзернейм
    if user:
        name = user.first_name
    else:
        name = 'Аноним'

    reply_text = f'Привет, {name}!\n\n' + hello_msg  # формируем сообщение

    update.message.reply_text(  # отправляем сообщение и добавляем инлайн клавиатуру
        text=reply_text,
        reply_markup=get_inline_keyboard()
    )


def main():
    print('Start bot')
    """Создаём и настраиваем бота"""
    req = Request(
        con_pool_size=8,
        connect_timeout=0.5,
        read_timeout=1.0
    )

    bot = Bot(
        token=TOKEN,
        request=req,
        # base_url='https://telegg.ru/orig/bot'
    )

    updater = Updater(
        bot=bot,
        use_context=True
    )

    """Проверяем корректность подключения к Telegram API"""
    info = bot.get_me()
    print(info)

    """Регистрируем обработчики команд и сообщений от пользователя"""
    updater.dispatcher.add_handler(CommandHandler('start', start_command_handler))
    updater.dispatcher.add_handler(MessageHandler(Filters.all, message_handler))
    updater.dispatcher.add_handler(CallbackQueryHandler(callback_handler))

    """Запускаем обработку входящих сообщений боту"""
    updater.start_polling()
    updater.idle()

    print('Stop bot')


if __name__ == '__main__':
    main()
