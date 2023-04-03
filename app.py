import telebot
from config import keys, TOKEN
from extensions import CurrencyExchange, ConvertionException

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start", "help"])
def help (message: telebot.types.Message):
    text = "Чтобы начать работу, введите команду боту в следующем формате: \n <имя валюты> \
<в какую валюту перевести> \
<количество переводимой валюты>\n Чтобы увидеть список доступных валют, введите команду /values"
    bot.reply_to(message, text)

@bot.message_handler(commands=["values"])
def values (message: telebot.types.Message):
    text = "Доступные валюты:"
    for key in keys.keys():
        text = "\n".join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=["text",])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(" ")
        if len(values) != 3:
            raise ConvertionException("Не удалось обработать данные. Пожалуйста, введите запрос заново.")
        base, quote, amount = values
        a = CurrencyExchange.Convert(quote,base,amount)
    except ConvertionException as e:
        bot.reply_to(message, f"Ошибка пользователя.\n{e}")
    except Exception as e:
        bot.reply_to(message, f"Не удалось обработать команду.\n{e}")
    else:
        text = f"Цена {amount} {base} в {quote} равна {a}"
        bot.send_message(message.chat.id, text)

bot.polling()