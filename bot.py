from oct2py import Oct2Py
import telebot
import config

bot = telebot.TeleBot(config.token)

oct_sess_dict = dict()   # здесь будут хранится открытые сессии octave

def get_oct_session(id):   # получение существующей сессии или создание новой
    oc = oct_sess_dict.get(id)
    if not oc:
        print("create new octave shell for chat № " + str(id))
        oc = Oct2Py()
        oct_sess_dict[id] = oc
    return oc

@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    bot.send_message(message.chat.id, "@todo")


@bot.message_handler(content_types=["text"])
def text_handler(message): # обработчик текстовых сообщений
    command = message.text
    chat_id = message.chat.id
    plot_flag = False
    oc = get_oct_session(chat_id)

    if "plot" in command:
        command = "figure(1, 'visible', 'off'); \n" + command + "\n  print -djpg '/tmp/output_img.jpg' "
        plot_flag = True

    try:
        output = oc.eval(command, return_both=True)[0]
    except BaseException:
        output = "Unknow error"

    print(output) # only for debug
    if output:
        bot.send_message(message.chat.id, output)
        if plot_flag:
            photo = open('/tmp/output_img.jpg', 'rb')
            bot.send_photo(chat_id, photo)
            photo.close()



if __name__ == '__main__':
     bot.polling(none_stop=True)


