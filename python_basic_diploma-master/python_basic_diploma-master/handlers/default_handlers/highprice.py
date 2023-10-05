from telebot.types import Message

from loader import bot
from configdata.config import CONTEXT
from handlers.destination_info_handlers.receive_city import receive_city


@bot.message_handler(commands=['highprice'])
def high_price_step(message: Message):
    CONTEXT[message.chat.id] = {"COMMAND": 'high price'}
    msg = bot.send_message(message.chat.id, "Введите город")
    bot.register_next_step_handler(msg, receive_city)


