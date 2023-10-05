from telebot import types
from configdata.config import CONTEXT, QUERY_STRING
from loader import bot
from handlers.destination_info_handlers.get_name_hotel import get_name_hotel
from handlers.destination_info_handlers.get_photo import get_photo
from handlers.destination_info_handlers.formatted_text import formatted_text


def get_check_in(message):
    CONTEXT[message.chat.id]["CHECK_IN"] = message.text
    msg = bot.send_message(message.chat.id, 'Введите дату выезда(2020-01-01): ')
    bot.register_next_step_handler(msg, get_check_out)


def get_check_out(message):
    CONTEXT[message.chat.id]["CHECK_OUT"] = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.InlineKeyboardButton('Отлично!')
    markup.add(button)
    result_hotel = get_name_hotel(message, QUERY_STRING)
    msg = bot.send_message(message.chat.id, "\n\n".join(formatted_text(message, result_hotel)), reply_markup=markup)
    bot.register_next_step_handler(msg, get_photo)
