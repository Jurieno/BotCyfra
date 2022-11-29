from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

buttons = ['👍', '❌', '💤'] # Добавить мои мероприятия сюда

kb_search = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

kb_search.add(buttons[0],buttons[1],buttons[2])