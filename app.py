import telebot
from config import cryptocurrency, TOKEN
from extensions import APIException, CryptoConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start_help(message):
    instruction = (f"Для работы бота вводим через пробел:\n"
                   f"<имя валюты, цену которой надо узнать>"
                   f"<имя валюты, в которой надо узнать цену первой валюты>"
                   f"<количество первой валюты>\n"
                   f"Пример: биткоин рубль 1\n"
                   f"Отображение списка криптовалют: /values")
    bot.reply_to(message, instruction)


@bot.message_handler(commands=['values'])
def show_cryptocurrency(message):
    text = 'Доступные криптовалюты/валюты:'
    for key in cryptocurrency.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert_work(message):
    try:
        user_message = message.text.lower().split(" ")

        if len(user_message) != 3:
            raise APIException(f'Неверное количество параметров\n'
                               f'Инструкция:  /help')

        qoute, base, amount = user_message

        total = CryptoConverter.get_price(qoute, base, amount)

    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя:\n{e}')

    except Exception as e:
        bot.reply_to(message, f'Ошибка в обработке:\n{e}')

    else:

        text = f'Цена {amount} {qoute} в {base} = {total * float(amount)}'

        bot.send_message(message.chat.id, text)


if __name__ == '__main__':
    bot.polling(none_stop=True)
