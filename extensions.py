import requests
from bs4 import BeautifulSoup

# Функция для получения данных о курсе валют с помощью API CoinGecko
def get_currency_price(currency):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={currency}&vs_currencies=usd"
    response = requests.get(url)
    data = response.json()
    if data.get(currency):
        return data[currency]["usd"]
    else:
        raise Exception("Invalid currency")

# Функция для получения текущих данных о валютах
def get_currency_rates():
    url = "https://www.x-rates.com"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    currency_table = soup.find("table", class_="tablesorter ratesTable")

    currency_rates = {}
    rows = currency_table.find_all("tr")
    for row in rows:
        columns = row.find_all("td")
        if len(columns) == 3:
            currency_name = columns[0].text
            currency_rate = columns[1].text
            currency_rates[currency_name] = currency_rate

    return currency_rates

# Пример использования
try:

    usd_price = get_currency_price("usd")
    print(f"Курс доллара: {usd_price} USD")

    eur_price = get_currency_price("eur")
    print(f"Курс евро: {eur_price} USD")

    currency_rates = get_currency_rates()
    print("Текущие курсы валют:")
    for currency, rate in currency_rates.items():
        print(f"{currency}: {rate}")
except Exception as e:
    print(f"Произошла ошибка: {str(e)}")


    # Большое спасибо курс Фэктори что тратите свое время на таких как я ))))