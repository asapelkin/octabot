from oct2py import Oct2Py
import telebot
import config

bot = telebot.TeleBot(config.token)

oct_sess_dict = dict()   # здесь будут хранится открытые сессии octave

def get_oct_session(id):   #
    oc = oct_sess_dict.get(id)
    if not oc:
        print("create new octave shell for chat № " + str(id))
        oc = Oct2Py()
        oct_sess_dict[id] = oc

    return oc

@bot.message_handler(content_types=["text"])
def text_handler(message): # обработчик текстовых сообщений
    oc = get_oct_session(message.chat.id)
    try:
        output = oc.eval(message.text, return_both=True)[0]
    except BaseException:
        output = "Error"
    print(output)
    if output:
        bot.send_message(message.chat.id, output)


@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    bot.send_message(message.chat.id, "@todo")


if __name__ == '__main__':
     bot.polling(none_stop=True)


