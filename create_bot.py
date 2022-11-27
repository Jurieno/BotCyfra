from aiogram import Bot, types  #Сможем писать анотации типов
from aiogram.dispatcher import Dispatcher #Улавливает события отправки
import aiomysql
import asyncio
import configparser
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import os

storage = MemoryStorage()

config = configparser.ConfigParser()
config.read('config.ini')

bot = Bot(token=config['bot']['TOKEN']) #Получаем токен из config.ini
dp = Dispatcher(bot, storage=storage) #Инициализируем бота

loop = asyncio.get_event_loop()

@staticmethod
async def con(request,task="select"):
    conn = await aiomysql.connect(host=config['database']['host'],
                            user=config['database']['user'],
                            password=config['database']['password'],
                            db=config['database']['db'],
                            loop=loop,
                            autocommit=False)
    async with conn.cursor() as cur:
        if task == "select":
            await cur.execute(request)
            return await cur.fetchall()
        else:
            await cur.execute(request)
            await conn.commit()