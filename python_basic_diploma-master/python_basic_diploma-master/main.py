from loader import bot
from telebot.types import BotCommand
from dal.database import DB, migrate
from handlers.default_handlers import *


if __name__ == '__main__':
    migrate()
    bot.set_my_commands([BotCommand("/start", "Начать")])
    bot.infinity_polling()
