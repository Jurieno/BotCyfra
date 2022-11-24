from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

b1 = KeyboardButton('Изменить данные')
b2 = KeyboardButton('Отмена')

reset_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

reset_kb.row(b1, b2)