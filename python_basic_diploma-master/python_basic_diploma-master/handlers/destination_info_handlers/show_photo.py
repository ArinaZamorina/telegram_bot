from configdata.config import CONTEXT
import json
import requests


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
