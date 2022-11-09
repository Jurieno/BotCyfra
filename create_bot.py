from aiogram import Bot, types  #Сможем писать анотации типов
from aiogram.dispatcher import Dispatcher #Улавливает события отправки
import pymysql

import os

bot = Bot(token=os.getenv('TOKEN')) #Получаем токен из start.bat
dp = Dispatcher(bot) #Инициализируем бота

con = pymysql.connect(host=os.getenv('host'),
                        user=os.getenv('user'),
                        password=os.getenv('password'),
                        database=os.getenv('database'),
                        charset='utf8mb4',
                        cursorclass=pymysql.cursors.DictCursor)