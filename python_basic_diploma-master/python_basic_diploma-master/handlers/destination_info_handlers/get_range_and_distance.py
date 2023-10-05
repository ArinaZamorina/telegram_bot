from configdata.config import CONTEXT
from loader import bot
from handlers.destination_info_handlers.get_hotels_count import get_hotels_count


def get_range(message):
    CONTEXT[message.chat.id]["HOTEL_COUNT"] = int(message.text)
    msg = bot.send_message(message.chat.id, "Введите диапазон цен(10-100)")
    bot.register_next_step_handler(msg, get_distance_to_hotel)


def get_distance_to_hotel(message):
    msg_list = message.text.split('-')
    CONTEXT[message.chat.id]['MIN'] = msg_list[0]
    CONTEXT[message.chat.id]['MAX'] = msg_list[1]
    msg = bot.send_message(message.chat.id, "Введите расстояние от отеля до центра города")
    bot.register_next_step_handler(msg, get_hotels_count)
