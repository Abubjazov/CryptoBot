"""Получение данных по курсам криптовалют с сайта https://global.bittrex.com/
описание запросов взято отсюда https://bittrex.github.io/api/v1-1
"""
import requests


class BittrexClient(object):

    def __init__(self):
        self.base_url = 'https://api.bittrex.com/api/v1.1'

    def __request(self, method, params):
        url = self.base_url + method
        r = requests.get(url=url, params=params)
        result = r.json()
        return result

    def get_ticker(self, pair):
        params = {'market': pair}
        return self.__request(method='/public/getticker', params=params)

    def get_last_price(self, pair):
        res = self.get_ticker(pair=pair)
        return res['result']['Last']
