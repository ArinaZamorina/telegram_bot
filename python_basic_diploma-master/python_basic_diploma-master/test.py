import json
import re
from datetime import datetime

import requests
import telebot
from telebot import types

bot = telebot.TeleBot('Telebot')
CONTEXT = {}


@bot.message_handler(commands=['start'])
def main(message):
    CONTEXT[message.chat.id] = None
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    first_button = types.InlineKeyboardButton("/lowprice")
    second_button = types.InlineKeyboardButton("/highprice")
    third_button = types.InlineKeyboardButton("/bestdeal")
    fourth_button = types.InlineKeyboardButton("/history")
    markup.add(first_button, second_button, third_button, fourth_button)
    bot.send_message(message.chat.id, text="Выберите принцип сортировки отелей", reply_markup=markup)


@bot.message_handler(commands=['text'])
def common_func(message):
    if message.text == "/lowprice":
        bot.register_next_step_handler(message, low_price_step)
    elif message.text == "/highprice":
        bot.register_next_step_handler(message, high_price_step)
    elif message.text == "/bestdeal":
        bot.register_next_step_handler(message, best_deal_step)
    elif message.text == "/history":
        bot.register_next_step_handler(message, history_step)


def create_hotel_list(message, id_city):
    url = "https://hotels4.p.rapidapi.com/properties/list"
    sort_order = str()
    mini = None
    maxi = None
    if CONTEXT[message.chat.id]['command'] == 'low price':
        sort_order = "PRICE"
    elif CONTEXT[message.chat.id]['command'] == 'high price':
        sort_order = 'PRICE_HIGHEST_FIRST'
    elif CONTEXT[message.chat.id]['command'] == 'best deal':
        sort_order = "BEST_SELLER"
        mini = CONTEXT[message.chat.id]['MIN']
        maxi = CONTEXT[message.chat.id]['MAX']
    querystring = {"destinationId": id_city, "pageNumber": "1", "pageSize": CONTEXT[message.chat.id]["HOTEL_COUNT"],
                   "checkIn": CONTEXT[message.chat.id]['CHECK_IN'],
                   "checkOut": CONTEXT[message.chat.id]['CHECK_OUT'], "adults1": "1", "priceMin": mini,
                   "priceMax": maxi,
                   "sortOrder": sort_order, "locale": "en_US", "currency": "USD"}

    headers = {
        "X-RapidAPI-Key": "93840eb20bmsh569344d792332a5p11cccbjsn8ef099c66717",
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    data = json.loads(response.text)
    result_hotel = {}
    ind = 0
    for _ in range(CONTEXT[message.chat.id]["HOTEL_COUNT"]):
        new_dict = data["data"]["body"]["searchResults"].get("results")

        for tools in new_dict[ind]:
            if CONTEXT[message.chat.id].get('command') == 'best deal':
                if tools == 'ratePlan':
                    result = data["data"]["body"]["searchResults"]["results"][ind]["landmarks"][
                        0].get("label")
                    if result == 'City center':
                        distance = data["data"]["body"]["searchResults"]["results"][
                            ind]["landmarks"][0].get("distance")
                        numb = re.sub(' miles', '', distance)
                        if float(numb) <= float(CONTEXT[message.chat.id]['DISTANCE']):
                            if tools == "ratePlan":
                                result_hotel[
                                    data["data"]["body"]["searchResults"]["results"][ind][
                                        "name"]] \
                                    = {
                                    'cost':
                                        data["data"]["body"]["searchResults"]["results"][ind][
                                            "ratePlan"]["price"][
                                            "current"],
                                    'id': data["data"]["body"]["searchResults"]["results"][ind][
                                        'id'],
                                    'distance':
                                        data["data"]["body"]["searchResults"]["results"][
                                            ind]["landmarks"][0]['distance']}
                                ind += 1
            else:
                if tools == "ratePlan":
                    result_hotel[data["data"]["body"]["searchResults"]["results"][ind]["name"]] \
                        = {
                        'cost':
                            data["data"]["body"]["searchResults"]["results"][ind]["ratePlan"][
                                "price"][
                                "current"],
                        'id': data["data"]["body"]["searchResults"]["results"][ind]['id']}
                    ind += 1

        print(result_hotel)

    CONTEXT[message.chat.id]["HOTELS_DICT"] = result_hotel
    return result_hotel


def get_name_hotel(message, url, header, query_string):
    response = requests.request("GET", url + "locations/v2/search", headers=header, params=query_string)
    data = json.loads(response.text)
    print(data)
    id_city = str()

    for suggestion in data['suggestions']:
        if suggestion['group'] == "CITY_GROUP":
            id_city = suggestion['entities'][0]['destinationId']
            print(id_city)

    result_hotels = create_hotel_list(message, id_city)
    return result_hotels


def formatted_text(message, hotel_dict: dict):
    strings_for_print = str()

    if CONTEXT[message.chat.id]["command"] == 'low price' or CONTEXT[message.chat.id]["command"] == 'high price':
        strings_for_print = [f'{hotel.center(len(hotel) + 10, "*")}\n\n Цена: {hotel_dict[hotel].get("cost")}\n' for
                             hotel in hotel_dict]

    elif CONTEXT[message.chat.id]["command"] == 'best deal':
        strings_for_print = [f'{hotel.center(len(hotel) + 10, "*")}\n\n Цена: {hotel_dict[hotel].get("cost")}\n' \
                             f' Расстояние до центра города:' f'{hotel_dict[hotel].get("distance")}' for hotel in
                             hotel_dict]

    return strings_for_print


def print_history(command_dict):
    string_for_print = [
        f'Команда: {command_dict.get("command")}\n\nВремя вызова команды: {command_dict.get("TIME")}\n\n'
        f"Отели: " + ', '.join(command_dict["HOTELS_DICT"].keys())]

    return string_for_print


def show_photo(message, hotels):
    photo = dict()
    CONTEXT[message.chat.id]["PHOTO_COUNT"] = message.text

    url = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"

    headers = {
        "X-RapidAPI-Key": "93840eb20bmsh569344d792332a5p11cccbjsn8ef099c66717",
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }

    for hotel in hotels:
        querystring = {"id": CONTEXT[message.chat.id]["HOTELS_DICT"][hotel]['id']}

        response = requests.request("GET", url, headers=headers, params=querystring)
        data = json.loads(response.text)
        photo[hotel] = dict()
        for i in range(1, int(message.text) + 1):
            for img in data["hotelImages"][i]:
                if img == 'baseUrl':
                    url_photo = data["hotelImages"][i][img].format(size='w')
                    print(url_photo)

                    photo[hotel][i] = url_photo

    return photo


@bot.message_handler(commands=['lowprice'])  # для ответа на команды пользователя используются хендлеры
def low_price_step(message):
    CONTEXT[message.chat.id] = {'command': 'low price'}
    CONTEXT[message.chat.id]['TIME'] = datetime.now().time()
    msg = bot.send_message(message.chat.id, "Введите город")
    bot.register_next_step_handler(msg, receive_city)


@bot.message_handler(commands=['highprice'])
def high_price_step(message):
    CONTEXT[message.chat.id] = {'command': 'high price'}
    msg = bot.send_message(message.chat.id, "Введите город")
    bot.register_next_step_handler(msg, receive_city)


@bot.message_handler(commands=['bestdeal'])
def best_deal_step(message):
    CONTEXT[message.chat.id] = {'command': 'best deal'}
    msg = bot.send_message(message.chat.id, "Введите город")
    bot.register_next_step_handler(msg, receive_city)


@bot.message_handler(commands=['history'])
def history_step(message):
    history_dict = {i: CONTEXT[message.chat.id].get(i) for i in CONTEXT[message.chat.id] if i == 'TIME' or
                    i == 'command' or i == 'HOTELS_DICT'}
    while len(history_dict) != 3:
        if 'TIME' not in history_dict:
            history_dict['TIME'] = None
        if 'command' not in history_dict:
            history_dict['command'] = None
        if 'HOTELS_DICT' not in history_dict:
            history_dict['HOTELS_DICT'] = None

    result = print_history(history_dict)
    bot.send_message(message.chat.id, result)


def receive_city(message):
    bot.send_message(message.chat.id, f"Выбран город {message.text}")
    CONTEXT[message.chat.id]['CITY'] = message.text
    msg = bot.send_message(message.chat.id, "Сколько отелей показать?")
    if CONTEXT[message.chat.id]['command'] == 'best deal':
        bot.register_next_step_handler(msg, get_range)
    else:
        bot.register_next_step_handler(msg, get_hotels_count)


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


def get_hotels_count(message):
    CONTEXT[message.chat.id]['DISTANCE'] = message.text
    if CONTEXT[message.chat.id]['command'] == 'low price' or CONTEXT[message.chat.id]['command'] == 'high price':
        CONTEXT[message.chat.id]["HOTEL_COUNT"] = int(message.text)
    count = CONTEXT[message.chat.id]["HOTEL_COUNT"]
    bot.send_message(message.chat.id, f"Количество отелей {count}")
    query_string = QUERY_STRING
    query_string["query"] = CONTEXT[message.chat.id]["CITY"].lower()
    msg = bot.send_message(message.chat.id, 'Введите дату заезда(2020-01-01): ')
    bot.register_next_step_handler(msg, get_check_in)


def get_check_in(message):
    CONTEXT[message.chat.id]["CHECK_IN"] = message.text
    msg = bot.send_message(message.chat.id, 'Введите дату выезда(2020-01-01): ')
    bot.register_next_step_handler(msg, get_check_out)


def get_check_out(message):
    CONTEXT[message.chat.id]["CHECK_OUT"] = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.InlineKeyboardButton('Отлично!')
    markup.add(button)
    result_hotel = get_name_hotel(message, URL, HEADER, QUERY_STRING)
    msg = bot.send_message(message.chat.id, "\n\n".join(formatted_text(message, result_hotel)), reply_markup=markup)
    bot.register_next_step_handler(msg, get_photo)


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
        msg = bot.send_message(message.chat.id, 'Сколько фото показать?')
        bot.register_next_step_handler(msg, show_hotel)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_yes = types.InlineKeyboardButton('/history')
        markup.add(button_yes)
        bot.send_message(message.chat.id, "Можете посмотреть историю диалога c:", reply_markup=markup)


def show_hotel(message):
    print(CONTEXT)
    name_hotel_keys = CONTEXT[message.chat.id]["HOTELS_DICT"].keys()
    result_photo = show_photo(message, name_hotel_keys)
    for hotel in result_photo:
        bot.send_message(message.chat.id, f'{hotel}')
        for i in range(1, int(CONTEXT[message.chat.id]["PHOTO_COUNT"]) + 1):
            bot.send_message(message.chat.id, result_photo[hotel].get(i))


URL = "https://hotels4.p.rapidapi.com/"
HEADER = {
    "X-RapidAPI-Key": "3ff5cb1c1fmshed352f49f8e08f1p1fda5cjsn70abad276ada",
    "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
}

QUERY_STRING = {"locale": "en_US", "currency": "USD"}

bot.infinity_polling()
