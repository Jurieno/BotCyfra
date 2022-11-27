from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

buttons = ['Профиль', 'Отмена'] # Добавить мои мероприятия сюда

kb_settings = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

for i in buttons:
    kb_settings.add(i)