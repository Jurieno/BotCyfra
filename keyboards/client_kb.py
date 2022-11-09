from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

button_assign = ''
b1 = KeyboardButton('/Добавить_в_беседу')
b2 = KeyboardButton('/Найти_интересное_мероприятие')
b3 = KeyboardButton('/Создать_событие')
b4 = KeyboardButton('/Поиск_друзей')
b5 = KeyboardButton('/Настройки')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

kb_client.add(b1).add(b2).add(b3).add(b4).add(b5)