# -*- coding: utf-8 -*-

import config
import telebot
import time
import random
import string
import logging
from utils import get_course, get_random_int, convert_bitcoin_to_rub

bot = telebot.TeleBot(config.token)


# if user send command /start
@bot.message_handler(commands=['start'])
def first_messages(message):
    txt = """Здравствуйте! Меня зовут Bitcoin Bot.
    Вы можете использовать следующие комманды: 
        /rate (я скажу вам актуальный курс Биткойна)
        /buy (Я помогу вам купить Биткойны) """
    bot.send_message(message.chat.id, txt)


# if user send command /rate
@bot.message_handler(commands=['rate'])
def handle_rate(message):
    usd = get_course("https://myfin.by/crypto-rates/bitcoin-usd")
    rub = get_course("https://myfin.by/crypto-rates/bitcoin-rub")
    txt = """Актуальный курс Биткойна:
        {} USD;
        {} RUB;
    """.format(usd, rub)
    bot.send_message(message.chat.id, txt)


# if user send command /buy
@bot.message_handler(commands=['buy'])
def handle_buy(message):
    first_message = """ 
    Пожалуйста, скажите мне: сколько биткоинов вы бы хотели купить?
    Это должно быть значение менее  чем 100 000 и более чем 0.
    Вы можете ввести дробное число. 
    Введите сумму биткоинов:
    """
    bot.send_message(message.chat.id, first_message)


@bot.message_handler(content_types=["text"])
def buy_bitcoin_messages(message):
    global bitcoin_value

    letters = [letter for letter in string.ascii_letters]
    errors = []

    for letter in letters:
        if letter in message.text:
            errors.append(letter)
        else:
            pass

    if not errors and len(message.text) != 19 and "-" not in message.text:
        try:
            bitcoin_value = float(message.text)
        except ValueError:
            txt = "Прошу прощения, но вы ввели неверное значение. Повторите попытку."
            bitcoin_value = 0
            bot.send_message(message.chat.id, txt)

        if 0 < bitcoin_value < 100000:
            txt = """Отлично! Я успешно получил вашу сумму Биткоинов. 
            
            Теперь, пожалуйста скажите мне номер карты куда я должен выслать Биткоины
            (формат xxxx-xxxx-xxxx-xxxx  - замените символы 'хххх' на цифры)
            Введите номер карты:
            """
            bot.send_message(message.chat.id, txt)
        else:
            txt = """Вы ввели неверное значение суммы Биткоинов.
            Это должно быть значение менее  чем 100 000 и более чем 0. Повторите попытку."""
            bot.send_message(message.chat.id, txt)

    if len(message.text) == 19 and "-" in message.text:
        address = message.text
        txt = "Принял! Спасибо!"
        bot.send_message(message.chat.id, txt)
        rub = convert_bitcoin_to_rub(bitcoin_value)
        comment = get_random_int()
        text = """Чтобы купить Биткойны -
        перечислите {} рублей на кошелек QIWI '{}' с комментарием {}""".format(rub, config.QIWI_PURSE, comment)
        bot.send_message(message.chat.id, text)


if __name__ == '__main__':
    while True:
        try:
            random.seed()
            bot.polling(none_stop=True)
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.error(e)
            time.sleep(15)
