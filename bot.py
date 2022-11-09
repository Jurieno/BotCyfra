from pydoc import cli
from aiogram.utils import executor #Для запуска бота в онлайн
from create_bot import dp, bot

import os

async def on_startup(_):
    await bot.send_message(os.getenv('idAdmin'), 'Бот запущен')

from handlers import client, admin, other

client.register_handlers_client(dp)
other.register_handlers_other(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

