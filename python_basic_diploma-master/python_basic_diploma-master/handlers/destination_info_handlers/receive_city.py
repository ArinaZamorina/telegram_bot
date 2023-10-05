from configdata.config import CONTEXT

from loader import bot
from handlers.destination_info_handlers.get_range_and_distance import get_range
from handlers.destination_info_handlers.get_hotels_count import get_hotels_count


def receive_city(message):
    bot.send_message(message.chat.id, f"Выбран город {message.text}")
    CONTEXT[message.chat.id]['CITY'] = message.text
    msg = bot.send_message(message.chat.id, "Сколько отелей показать?")
    if CONTEXT[message.chat.id]['COMMAND'] == 'best deal':
        bot.register_next_step_handler(msg, get_range)
    else:
        bot.register_next_step_handler(msg, get_hotels_count)