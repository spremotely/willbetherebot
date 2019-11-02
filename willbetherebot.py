import yaml
import telebot

with open("config.yml", 'r') as config_file:
    config = yaml.load(config_file, Loader=yaml.Loader)

bot = telebot.TeleBot(config['bot']['token'])


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Этот бот сохраняет места для будущего посещения")


@bot.message_handler(commands=['add'])
def add_message(message):
    pass


@bot.message_handler
def text_message(message):
    pass


@bot.message_handler(content_types=['photo'])
def image_message(message):
    print(message)
    pass


@bot.message_handler(content_types=['location'])
def location_message(message):
    print(message)
    pass


bot.polling()

