from aiogram.types import ReplyKeyboardMarkup

hobbys = ['Чтение', 'Общение', 'Спорт', 'Компьютерные игры', 'Музыка', 
          'Авто/мото', 'Психология', 'Дизайн', 'Кулинария', 'Танцы']

hobby_client = ReplyKeyboardMarkup()           
for i in hobbys:
    hobby_client.add(i)