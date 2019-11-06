import yaml
import telebot

import scenario
from data.alchemychatrepo import AlchemyChatRepo
from data.alchemycontext import AlchemyContext
from data.alchemystaterepo import AlchemyStateRepo
from data.alchemyuserrepo import AlchemyUserRepo
from scenario.start.welcome import Welcome
from scenario.add.welcome import Welcome
from scenario.add.photo import Photo

with open("config.yml", 'r') as config_file:
    config = yaml.load(config_file, Loader=yaml.Loader)

bot = telebot.TeleBot(config['bot']['token'])
context = AlchemyContext(
    f"mysql+mysqlconnector://{config['db']['username']}:{config['db']['password']}@{config['db']['host']}/{config['db']['name']}")
state_repo = AlchemyStateRepo(context)
user_repo = AlchemyUserRepo(context)
chat_repo = AlchemyChatRepo(context)


@bot.message_handler(content_types=['text', 'photo', 'location'])
def any_message(message):
    chat, user = process_chat_user(message)
    result = process_scenario(chat, user, message)

    if result:
        bot.send_message(chat_id=message.chat.id, text=result)


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


def process_scenario(chat, user, message):
    state = state_repo.get_state(chat.id, user.id)
    scn = scenario.start.welcome.Welcome(
        context, state_repo, scenario.add.welcome.Welcome(
            context, state_repo, scenario.add.photo.Photo(
                context, state_repo)))
    return scn.handle(chat, user, state, message)


bot.polling()
