from configdata.config import CONTEXT


def formatted_text(message, hotel_dict: dict):
    strings_for_print = str()

    if CONTEXT[message.chat.id]["COMMAND"] == 'low price' or CONTEXT[message.chat.id]["COMMAND"] == 'high price':
        strings_for_print = [f'{hotel.center(len(hotel) + 10, "*")}\n\n Цена: {hotel_dict[hotel].get("cost")}\n' for
                             hotel in hotel_dict]

    elif CONTEXT[message.chat.id]["COMMAND"] == 'best deal':
        strings_for_print = [f'{hotel.center(len(hotel) + 10, "*")}\n\n Цена: {hotel_dict[hotel].get("cost")}\n' \
                             f' Расстояние до центра города:' f'{hotel_dict[hotel].get("distance")}' for hotel in
                             hotel_dict]

    return strings_for_print
