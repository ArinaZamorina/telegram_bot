from telebot.types import Message

from configdata.config import CONTEXT
from loader import bot
from handlers.destination_info_handlers.receive_city import receive_city


@bot.message_handler(commands=['bestdeal'])
def best_deal_step(message: Message):
    CONTEXT[message.chat.id] = {"COMMAND": 'best deal'}
    msg = bot.send_message(message.chat.id, "Введите город")
    bot.register_next_step_handler(msg, receive_city)
