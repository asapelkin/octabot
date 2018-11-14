from oct2py import Oct2Py
import telebot
import config
import os.path

bot = telebot.TeleBot(config.token)

oct_sess_dict = dict()   # здесь будут хранится открытые сессии octave

def get_oct_session(id):   # получение существующей сессии или создание новой
    octave_session = oct_sess_dict.get(id)
    if not octave_session:
        print("create new octave shell for chat # " + str(id))
        octave_session = Oct2Py()
        octave_session.eval("set(0, 'defaultfigurevisible', 'off');")
        oct_sess_dict[id] = octave_session
    return octave_session

@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    bot.send_message(message.chat.id, "@todo")

@bot.message_handler(content_types=["text"])
def text_handler(message): # обработчик текстовых сообщений
    command = message.text
    chat_id = message.chat.id
    plot_flag = False
    octave_session = get_oct_session(chat_id)

    if "plot" in command or "mesh" in command:
        user_path = "/tmp/octabot/"+ str(chat_id)
        if not os.path.exists(user_path):
            os.mkdir(user_path)
        command = "figure(1, 'visible', 'off'); \n" + command + "\n  print -djpg  '"+ user_path +"/output_img.jpg'; close(gcf)"
        plot_flag = True
    try:
        output = octave_session.eval(command, return_both=True, timeout=10)[0]
    except BaseException:
        output = "Syntax error"

    print("output = " + output) # only for debug
    if output:
        bot.send_message(message.chat.id, output)
    if plot_flag:
        photo = open('/tmp/octabot/'+ str(chat_id) +'/output_img.jpg', 'rb')
        bot.send_photo(chat_id, photo)
        photo.close()
        plot_flag = False
        os.remove('/tmp/octabot/'+ str(chat_id) +'/output_img.jpg')

if __name__ == '__main__':
     bot.polling(none_stop=True)


