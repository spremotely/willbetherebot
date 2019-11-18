import yaml
import telebot

import scenario
from data.alchemy.alchemychatrepo import AlchemyChatRepo
from data.alchemy.alchemycontext import AlchemyContext
from data.alchemy.alchemychatstaterepo import AlchemyChatStateRepo
from data.alchemy.alchemyentityrepo import AlchemyEntityRepo
from data.alchemy.alchemylocationrepo import AlchemyLocationRepo
from data.alchemy.alchemyphotorepo import AlchemyPhotoRepo
from data.alchemy.alchemyuserrepo import AlchemyUserRepo
from scenario.start.welcome import Welcome
from scenario.add.welcome import Welcome
from scenario.add.photo import Photo
from scenario.add.location import Location
from scenario.list.listall import ListAll
from scenario.list.welcome import Welcome
from scenario.list.list import List
from scenario.default.default import Default

with open("config.yml", 'r') as config_file:
    config = yaml.load(config_file, Loader=yaml.Loader)

bot = telebot.TeleBot(config['bot']['token'])
context = AlchemyContext(
    f"mysql+mysqlconnector://{config['db']['username']}:{config['db']['password']}@{config['db']['host']}/{config['db']['name']}")
state_repo = AlchemyChatStateRepo(context)
user_repo = AlchemyUserRepo(context)
chat_repo = AlchemyChatRepo(context)
photo_repo = AlchemyPhotoRepo(context)
location_repo = AlchemyLocationRepo(context)
entity_repo = AlchemyEntityRepo(context)


@bot.message_handler(content_types=['text', 'photo', 'location'])
def any_message(message):
    chat, user = process_chat_user(message)
    ans_type, ans = process_scenario(chat, user, message)

    if not ans:
        return

    if ans_type == "message":
        bot.send_message(chat_id=message.chat.id, text=ans)

    if ans_type == "locations":
        for location in ans:
            bot.send_photo(chat_id=message.chat.id, photo=location.photo.uri)
            bot.send_location(chat_id=message.chat.id, latitude=location.latitude, longitude=location.longitude)


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
    default_scenario = scenario.default.default.Default()
    list_scenario = scenario.list.list.List(context, state_repo, location_repo, default_scenario)
    list_welcome_scenario = scenario.list.welcome.Welcome(context, state_repo, list_scenario)
    list_all_scenario = scenario.list.listall.ListAll(location_repo, list_welcome_scenario)
    add_location_scenario = scenario.add.location.Location(
        context, state_repo, photo_repo, location_repo, list_all_scenario)
    add_photo_scenario = scenario.add.photo.Photo(
        context, state_repo, photo_repo, entity_repo, add_location_scenario)
    add_welcome_scenario = scenario.add.welcome.Welcome(
        context, state_repo, add_photo_scenario)
    start_welcome_scenario = scenario.start.welcome.Welcome(
        context, state_repo, add_welcome_scenario)
    return start_welcome_scenario.handle(chat, user, state, message)


bot.polling()
