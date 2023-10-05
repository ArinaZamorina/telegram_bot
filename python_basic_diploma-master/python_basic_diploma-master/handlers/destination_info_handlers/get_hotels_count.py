from configdata.config import CONTEXT, QUERY_STRING
from loader import bot
from handlers.destination_info_handlers.get_check_in_out import get_check_in


def get_hotels_count(message):
    CONTEXT[message.chat.id]['DISTANCE'] = message.text
    if CONTEXT[message.chat.id]["COMMAND"] == 'low price' or CONTEXT[message.chat.id]["COMMAND"] == 'high price':
        CONTEXT[message.chat.id]["HOTEL_COUNT"] = int(message.text)
    count = CONTEXT[message.chat.id]["HOTEL_COUNT"]
    bot.send_message(message.chat.id, f"Количество отелей {count}")
    query_string = QUERY_STRING
    query_string["query"] = CONTEXT[message.chat.id]["CITY"].lower()
    msg = bot.send_message(message.chat.id, 'Введите дату заезда(2020-01-01): ')
    bot.register_next_step_handler(msg, get_check_in)