from configdata.config import CONTEXT, HEADER, URL
import json
import requests
import re
from dal.database import History


def create_hotel_list(message, id_city):
    url = "https://hotels4.p.rapidapi.com/properties/list"
    sort_order = str()
    mini = None
    maxi = None
    if CONTEXT[message.chat.id]["COMMAND"] == 'low price':
        sort_order = "PRICE"
    elif CONTEXT[message.chat.id]["COMMAND"] == 'high price':
        sort_order = 'PRICE_HIGHEST_FIRST'
    elif CONTEXT[message.chat.id]["COMMAND"] == 'best deal':
        sort_order = "BEST_SELLER"
        mini = CONTEXT[message.chat.id]['MIN']
        maxi = CONTEXT[message.chat.id]['MAX']
    querystring = {"destinationId": id_city, "pageNumber": "1", "pageSize": CONTEXT[message.chat.id]["HOTEL_COUNT"],
                   "checkIn": CONTEXT[message.chat.id]['CHECK_IN'],
                   "checkOut": CONTEXT[message.chat.id]['CHECK_OUT'], "adults1": "1", "priceMin": mini,
                   "priceMax": maxi,
                   "sortOrder": sort_order, "locale": "en_US", "currency": "USD"}

    bot.send_message(message.chat.id, "Падажжи, ща найду")
    response = requests.request("GET", url, headers=HEADER, params=querystring)
    data = json.loads(response.text)
    result_hotel = {}
    ind = 0
    for _ in range(CONTEXT[message.chat.id]["HOTEL_COUNT"]):
        new_dict = data["data"]["body"]["searchResults"].get("results")

        for tools in new_dict[ind]:
            if CONTEXT[message.chat.id].get("COMMAND") == 'best deal':
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
    value = CONTEXT[message.chat.id]
    person = History.create(chat_id=message.chat.id, command=value['COMMAND'], time=value['TIME'], hotels=value['HOTELS_DICT'])

    return result_hotel


def get_name_hotel(message, query_string):
    response = requests.request("GET", URL + "locations/v2/search", headers=HEADER, params=query_string)
    data = json.loads(response.text)
    print(data)
    id_city = str()

    for suggestion in data['suggestions']:
        if suggestion['group'] == "CITY_GROUP":
            id_city = suggestion['entities'][0]['destinationId']
            print(id_city)

    result_hotels = create_hotel_list(message, id_city)
    return result_hotels



