import telebot
from extensions import CurrencyConverter, APIException


TOKEN = "<6711984271:AAHmY7gB8x5b_WF5bdZc6yXFFwjhmT2cklQ>"
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start", "help"])
def send_instructions(message):
    instructions = """
    Привет! Я бот для получения цены на валюту.
    Чтобы воспользоваться мной, отправь мне сообщение в формате:
    <имя валюты, цену которой ты хочешь узнать> <имя валюты, в которой надо узнать цену первой валюты> <количество первой валюты>

    Например: USD RUB 10

    Для вывода информации о всех доступных валютах используй команду /values.
    """
    bot.reply_to(message, instructions)


@bot.message_handler(commands=["values"])
def send_currency_values(message):
    values = """
    Доступные валюты:
    - USD (Доллар США)
    - EUR (Евро)
    - RUB (Российский рубль)
    """
    bot.reply_to(message, values)


@bot.message_handler(func=lambda message: True)
def convert_currency(message):
    try:
        text = message.text.split()
        base = text[0].upper()
        quote = text[1].upper()
        amount = float(text[2])

        total = CurrencyConverter.get_price(base, quote, amount)
        result = f"Цена {amount} {base} в {quote} равна {total}"
        bot.reply_to(message, result)

    except (IndexError, ValueError):
        error = "Неправильный формат сообщения. Пожалуйста, введите данные в формате: <имя валюты> <имя валюты> <количество>"
        bot.reply_to(message, error)

    except APIException as e:
        bot.reply_to(message, str(e))


bot.polling()