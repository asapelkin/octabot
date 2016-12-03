from oct2py import Oct2Py
import telebot
import config


bot = telebot.TeleBot(config.token)
oc = Oct2Py()

@bot.message_handler(content_types=["text"])
def text_handler(message): # обработчик текстовых сообщений
    try:
        output = oc.eval(message.text, return_both=True)
    except BaseException:
        output = "Error"

    print(output)
    bot.send_message(message.chat.id, output)

if __name__ == '__main__':
     bot.polling(none_stop=True)


