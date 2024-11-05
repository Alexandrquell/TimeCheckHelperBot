import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import pandas as pd
from datetime import datetime

# Включение логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Словарь для хранения чисел по датам
data = {}

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет! Я бот для подсчета чисел. Отправь мне сообщения с числами!')

def count_numbers(update: Update, context: CallbackContext) -> None:
    global data
    message_date = update.message.date.date()  # Получаем дату сообщения
    numbers = list(map(int, filter(str.isdigit, update.message.text.split())))  # Извлекаем числа

    # Сохраняем числа по дате
    if message_date not in data:
        data[message_date] = []
    data[message_date].extend(numbers)

def show_count(update: Update, context: CallbackContext) -> None:
    global data
    if len(context.args) < 3:
        update.message.reply_text('Пожалуйста, укажите число, месяц и год в формате ЧЧ ММ ГГГГ.')
        return

    try:
        day = int(context.args[0])
        month = int(context.args[1])
        year = int(context.args[2])
    except ValueError:
        update.message.reply_text('Неверный формат даты. Используйте ЧЧ ММ ГГГГ.')
        return

    count = 0
    # Суммируем числа за указанное число, месяц и год
    for date, numbers in data.items():
        if date.day == day and date.month == month and date.year == year:
            count += sum(numbers)

    update.message.reply_text(f'Сумма чисел за {day}/{month}/{year}: {count}')

def main() -> None:
    # Вставьте ваш токен
    updater = Updater("7872907691:AAG1tBtZg2Db7n2WitLxjv24nr-fBXt35z8")

    # Получаем диспетчер для обработки команд
    dispatcher = updater.dispatcher

    # Определяем обработчики
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, count_numbers))
    dispatcher.add_handler(CommandHandler("count", show_count))

    # Запускаем бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
