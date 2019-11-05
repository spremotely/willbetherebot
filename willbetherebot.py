import yaml
import telebot

from data.alchemychatrepo import AlchemyChatRepo
from data.alchemycontext import AlchemyContext
from data.alchemystaterepo import AlchemyStateRepo
from data.alchemyuserrepo import AlchemyUserRepo

with open("config.yml", 'r') as config_file:
    config = yaml.load(config_file, Loader=yaml.Loader)

bot = telebot.TeleBot(config['bot']['token'])
context = AlchemyContext(
    f"mysql+mysqlconnector://{config['db']['username']}:{config['db']['password']}@{config['db']['host']}/{config['db']['name']}")
state_repo = AlchemyStateRepo(context)
user_repo = AlchemyUserRepo(context)
chat_repo = AlchemyChatRepo(context)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(
        message.chat.id,
        "Этот бот сохраняет места для будущего посещения")


@bot.message_handler(commands=['add'])
def add_message(message):
    chat, user = process_chat_user(message)
    process_add_command(chat, user, message.message_id)


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


def process_chat_user(message):
    user = user_repo.get_user(message.from_user.id)

    if not user:
        user = user_repo.create_user(
            message.from_user.id,
            message.from_user.username,
            message.from_user.first_name,
            message.from_user.last_name,
            message.from_user.is_bot)

    chat = chat_repo.get_chat(message.chat.id)

    if not chat:
        chat = chat_repo.create_chat(message.chat.id, message.chat.type)

    context.save_changes()
    return chat, user


def process_add_command(chat, user, message_id):
    state = state_repo.get_state(chat.id, user.id)

    if not state:
        state = state_repo.create_state(chat, user, message_id, "add", "init")

    context.save_changes()


bot.polling()
