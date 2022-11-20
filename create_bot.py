from aiogram import Bot, types  #Сможем писать анотации типов
from aiogram.dispatcher import Dispatcher #Улавливает события отправки
import pymysql
import configparser
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import os

storage = MemoryStorage()

config = configparser.ConfigParser()
config.read('config.ini')

bot = Bot(token=config['bot']['TOKEN']) #Получаем токен из config.ini
dp = Dispatcher(bot, storage=storage) #Инициализируем бота

con = pymysql.connect(host=config['database']['host'],
                        user=config['database']['user'],
                        password=config['database']['password'],
                        database=config['database']['db'],
                        charset='utf8mb4',
                        cursorclass=pymysql.cursors.DictCursor)