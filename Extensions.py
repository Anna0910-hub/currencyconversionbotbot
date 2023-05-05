import requests
import json
from config_sketch import exchanges


class APIException(Exception):
    pass


class Converter:
    @staticmethod
    def get_price(quote, base, amount):
        if quote == base:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}.')

        try:
            quote_ticker = exchanges[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту "{quote}"')

        try:
            base_ticker = exchanges[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту "{base}"')

        try:
            amount = float(amount.replace(",", "."))
        except ValueError:
            raise APIException(f'Не удалось обработать количество "{amount}"')

        url = f'https://api.apilayer.com/exchangerates_data/convert?to={base_ticker}&from={quote_ticker}&amount={amount}'
        headers = {
            'apikey': 'HxkK7QOeaLxjGvVLXivUtszo5ufvBxxT'
        }

        r = requests.get(url, headers=headers)
        response = json.loads(r.content)
        total_base = response['result']
        return round(total_base, 2)