from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

b = ['Получить пробный период', 'Назад']

kb_price = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

kb_price.add(b)