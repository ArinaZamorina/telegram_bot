from telebot.types import Message

from loader import bot
from dal.database import Person
from utils.set_bot_commands import set_default_commands


@bot.message_handler(commands=['start'])  # для ответа на команды пользователя используются хендлеры
def start_handler(message: Message):
    existing_person = Person.select().where(Person.chat_id == message.chat.id)
    person_name = message.chat.first_name
    if len(existing_person.model) == 0:
        Person.create(chat_id=message.chat.id, name=person_name)
        bot.send_message(message.chat.id, f"Hello, {person_name}")
    else:
        bot.send_message(message.chat.id, f"Hello again, {person_name}")

    set_default_commands(bot)
