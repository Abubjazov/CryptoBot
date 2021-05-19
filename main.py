"""Сервер Telegram бота, запускаемый непосредственно"""
from telegram import Bot, Update

from telegram.ext import Updater, CallbackContext
from telegram.ext import MessageHandler
from telegram.ext import CommandHandler
from telegram.ext import Filters
from telegram.utils.request import Request

from bot_config import TOKEN


def start_command_handler(update: Update, context: CallbackContext):
    """Обработка команд от пользователя"""
    user = update.effective_user  # извлекаем юзернейм
    if user:
        name = user.first_name
    else:
        name = 'Аноним'

    reply_text = f'Привет, {name}!\n\n'  # формируем сообщение

    update.message.reply_text(  # отправляем сообщение
        text=reply_text
    )


def message_handler(update: Update, context: CallbackContext):
    """Обработка входящих сообщений"""
    user = update.effective_user  # извлекаем юзернейм
    if user:
        name = user.first_name
    else:
        name = 'Аноним'

    reply_text = f'Привет, {name}!\n\n'  # формируем сообщение

    update.message.reply_text(  # отправляем сообщение
        text=reply_text
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

    """Проверка корректного подключения к Telegram API"""
    info = bot.get_me()
    print(info)

    """Обработчики команд и сообщений от пользователя"""
    updater.dispatcher.add_handler(CommandHandler('start', start_command_handler))
    updater.dispatcher.add_handler(MessageHandler(Filters.all, message_handler))

    """Запуск обработки входящих сообщений боту"""
    updater.start_polling()
    updater.idle()

    print('Stop bot')


if __name__ == '__main__':
    main()
