# -*- coding: utf-8 -*-

from urllib.request import urlopen
from urllib.error import HTTPError
import random
from bs4 import BeautifulSoup


def get_course(url):
    try:
        html = urlopen(url)
    except HTTPError:
        print("This web-page: " + url + " is not defined.")
        return None
    try:
        soup = BeautifulSoup(html.read(), "html.parser")
        text = soup.find("div", {"class": "birzha_info_head_rates"}).getText()
        text = text.replace('\n', '')
        text = text.replace('\t', '')
        text = text.replace('$', '')
        text = text.replace('RUB', '')
        bitcoin_value = float(text)
    except AttributeError:
        print("Tag was not found")
        return None
    return bitcoin_value


def get_random_int():
    integer = random.randint(10000, 99999)
    return integer


def convert_bitcoin_to_rub(bitcoin):
    rub_for_one_bitcoin = get_course("https://myfin.by/crypto-rates/bitcoin-rub")
    result = rub_for_one_bitcoin * bitcoin
    return result
