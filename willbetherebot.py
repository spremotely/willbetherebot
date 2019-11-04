import yaml
import telebot

from data.alchemycontext import AlchemyContext
from data.alchemystaterepo import AlchemyStateRepo

with open("config.yml", 'r') as config_file:
    config = yaml.load(config_file, Loader=yaml.Loader)

bot = telebot.TeleBot(config['bot']['token'])
context = AlchemyContext(
    f"mysql+mysqlconnector://{config['db']['username']}:{config['db']['password']}@{config['db']['host']}/{config['db']['name']}")
state_repo = AlchemyStateRepo(context)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(
        message.chat.id,
        "Этот бот сохраняет места для будущего посещения")


@bot.message_handler(commands=['add'])
def add_message(message):
    state = state_repo.get_state(message.chat.id, message.from_user.id)

    if not state:
        process_location()


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


def process_location():
    pass


bot.polling()
