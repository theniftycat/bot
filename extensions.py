import requests
from config import keys

class ConvertionException (Exception):
    pass

class CurrencyExchange:
    @staticmethod
    def Convert (base: str, quote: str, amount: str):
        if quote == base:
            raise ConvertionException("Невозможно конвертировать валюту в нее же. Пожалуйста, введите запрос заново.")
        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f"Не удалось обработать валюту {quote}, введите запрос заново.")
        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f"Не удалось обработать валюту {base}, введите запрос заново.")
        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f"Не удалось обработать количество {amount}, введите запрос заново.")

        url = f"https://api.apilayer.com/exchangerates_data/convert?to={keys[quote]}&from={keys[base]}&amount={amount}"
        payload = {}
        headers = {
            "apikey": "SHwmFLCVhkdzLckoNTp34ROneCcE4fwt"
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        status_code = response.status_code
        result = response.text
        res = result.split("\n")
        r = res[-3].split(" ")
        a = float(r[-1])
        return a