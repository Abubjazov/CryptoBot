"""Сервер Telegram бота, запускаемый непосредственно"""
import datetime
import pytz
import inline_keyboards

from telegram import Bot, Update, ParseMode

from telegram.ext import Updater, CallbackContext, CallbackQueryHandler
from telegram.ext import MessageHandler
from telegram.ext import CommandHandler
from telegram.ext import Filters
from telegram.utils.request import Request

from bot_config import TOKEN
from coins_api import BittrexClient

hello_msg = 'Я простой телеграм бот который знает\nкурсы основных криптовалют на данный момент.' \
            f'\n\nЧто бы увидеть текущий курс интересующей тебя валюты нажми на нужную кнопку. 😃'

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
        reply_markup=inline_keyboards.get_inline_keyboard()
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
        reply_markup=inline_keyboards.get_inline_keyboard()
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
