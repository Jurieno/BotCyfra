from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

buttons = ['👍', '❌']

kb_ankets = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

kb_ankets.add(buttons[0],buttons[1])