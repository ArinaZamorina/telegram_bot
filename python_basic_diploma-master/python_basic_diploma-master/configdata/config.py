import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit('Переменные окружения не загружены, так как отсутствует файл .env')
else:
    load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
RAPID_API_KEY = os.getenv('RAPID_API_KEY')

URL = "https://hotels4.p.rapidapi.com/"
HEADER = {
    "X-RapidAPI-Key": RAPID_API_KEY,
    "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
}

QUERY_STRING = {"locale": "en_US", "currency": "USD"}

DEFAULT_COMMANDS = (
    ('/history', "Вывести справку"),
    ('/bestdeal', "Вывести лучшие предложения"),
    ('/lowprice', "Вывести дешевые предложения"),
    ('/highprice', "Вывести дорогие предложения")
)
CONTEXT = {}