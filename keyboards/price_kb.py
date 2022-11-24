from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

buttons = ['Получить пробный период', 'Отмена']

kb_price = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

for i in buttons:
    kb_price.add(i)

cancel_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
cancel_kb.add('Отмена')

cancel_ready_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
cancel_ready_kb.add('Завершить отправку').add('Отмена')
