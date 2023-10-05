from telebot.types import Message

from loader import bot
from configdata.config import CONTEXT
from handlers.destination_info_handlers.print_history import print_history


@bot.message_handler(commands=['history'])
def history_step(message: Message):
    history_dict = {i: CONTEXT[message.chat.id].get(i) for i in CONTEXT[message.chat.id] if i == 'TIME' or
                    i == "COMMAND" or i == 'HOTELS_DICT'}
    while len(history_dict) != 3:
        if 'TIME' not in history_dict:
            history_dict['TIME'] = None
        if "COMMAND" not in history_dict:
            history_dict["COMMAND"] = None
        if 'HOTELS_DICT' not in history_dict:
            history_dict['HOTELS_DICT'] = None

    result = print_history(history_dict)
    bot.send_message(message.chat.id, result)