from aiogram import Bot, types  #Сможем писать анотации типов
from aiogram.dispatcher import Dispatcher #Улавливает события отправки
import aiomysql
import asyncio
import configparser
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import os

async def select(loop, sql, pool):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(sql)
            return await cur.fetchone()


async def insert(loop, sql, pool):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(sql)
            await conn.commit()


async def main(loop):
    pool = await aiomysql.create_pool(
        host=config['database']['host'],
        user=config['database']['user'],
        password=config['database']['password'],
        db=config['database']['db'],
        loop=loop)

    c1 = select(loop=loop, sql='select * from minifw limit 1', pool=pool)
    c2 = insert(loop=loop, sql="insert into minifw (name) values ('hello')", pool=pool)

    tasks = [asyncio.ensure_future(c1), asyncio.ensure_future(c2)]
    return await asyncio.gather(*tasks)


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



cur_loop = asyncio.get_event_loop()
cur_loop.run_until_complete(main(cur_loop))

storage = MemoryStorage()

config = configparser.ConfigParser()
config.read('config.ini')

bot = Bot(token=config['bot']['TOKEN']) #Получаем токен из config.ini
dp = Dispatcher(bot, storage=storage) #Инициализируем бота

loop = asyncio.get_event_loop()