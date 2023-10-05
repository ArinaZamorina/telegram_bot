from telebot import types
import telebot
from loader import bot
from configdata.config import CONTEXT
from handlers.destination_info_handlers.show_photo import show_photo


def get_photo(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_yes = types.InlineKeyboardButton('Да')
    button_no = types.InlineKeyboardButton('Нет')
    markup.add(button_yes, button_no)
    msg = bot.send_message(message.chat.id, 'Показать фото?', reply_markup=markup)
    bot.register_next_step_handler(msg, count_photo)


@bot.message_handler(content_types=['Да'])
@bot.message_handler(content_types=['Нет'])
def count_photo(message):
    if message.text == 'Да':
        msg = bot.send_message(message.chat.id, 'Сколько фото показать?', reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, show_hotel)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_yes = types.InlineKeyboardButton('/history')
        markup.add(button_yes)
        bot.send_message(message.chat.id, "Можете посмотреть историю диалога 😊", reply_markup=markup)

def show_hotel(message):
    print(CONTEXT)
    name_hotel_keys = CONTEXT[message.chat.id]["HOTELS_DICT"].keys()
    result_photo = show_photo(message, name_hotel_keys)
    for hotel in result_photo:
        hotel_photos = [result_photo[hotel].get(i) for i in range(1, int(CONTEXT[message.chat.id]["PHOTO_COUNT"]) + 1)]
        bot.send_media_group(message.chat.id,
                             [telebot.types.InputMediaPhoto(photo, caption=hotel) for photo in hotel_photos])
