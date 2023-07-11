import requests
import json
from config import cryptocurrency


class APIException(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def get_price(qoute: str, base: str, amount: str):
        if qoute == base:
            raise APIException(f'Одинаковые валюты - "{base}"\n'
                               f'Инструкция:  /help')
        try:
            qoute_ticker = cryptocurrency[qoute]
        except KeyError:
            raise APIException(f'Неверное написание криптовалюты - "{qoute}"\n'
                               f'Отображение списка криптовалют: /values')

        try:
            base_ticker = cryptocurrency[base]
        except KeyError:
            raise APIException(f'Неверное написание криптовалюты - "{base}"\n'
                               f'Отображение списка криптовалют: /values')
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Неверное написание количества - "{amount}"\n'
                               f'Инструкция:  /help')

        respone = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={qoute_ticker}&tsyms={base_ticker}')
        result = json.loads(respone.content)

        if 'error' in result:
            raise APIException(result['error'])
        else:
            result = json.loads(respone.content)[cryptocurrency[base]]

        return result