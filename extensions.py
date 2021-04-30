import json
import requests
from config import exchanges , API_access_key, website

class APIException(Exception):
    pass


class Convertor():
    @staticmethod
    def get_price(values):
        if len(values) != 3 :
            raise APIException('Неверное количество параметров!')
        quote, base, amount  = values
        if quote == base:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}!')
        try:
            base_key = exchanges[base]
        except KeyError:
            raise APIException(f"Валюта {base} не найдена!")
        try:
            quote_key = exchanges[quote]
        except KeyError:
            raise APIException(f"Валюта {quote} не найдена!")
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}!')
        r = requests.get(
            f'{website}?access_key={API_access_key}&symbols={base_key},{quote_key}')

        resp = json.loads(r.content)
        new_price = resp['rates'][quote_key.upper()] /  resp['rates'][base_key.upper()]  * amount
        new_price = round(new_price, 3)
        message =  f"Цена {amount} {base} в {quote} : {new_price}"
        return message
