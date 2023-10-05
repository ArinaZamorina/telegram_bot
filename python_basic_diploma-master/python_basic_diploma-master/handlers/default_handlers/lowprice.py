from telebot.types import Message

from loader import bot
from configdata.config import CONTEXT
from datetime import datetime
from handlers.destination_info_handlers.receive_city import receive_city


@bot.message_handler(commands=['lowprice'])  # для ответа на команды пользователя используются хендлеры
def low_price_step(message: Message):
    CONTEXT[message.chat.id] = {'COMMAND': 'low price'}
    CONTEXT[message.chat.id]['TIME'] = datetime.now().time()
    msg = bot.send_message(message.chat.id, "Введите город")
    bot.register_next_step_handler(msg, receive_city)
