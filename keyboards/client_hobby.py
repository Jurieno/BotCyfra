from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

h1  = 'Чтение'
h2  = 'Общение'
h3  = 'Спорт'
h4  = 'Компьютерные игры'
h5  = 'Музыка'
h6  = 'Авто/мото'
h7  = 'Психология'
h8  = 'Дизайн'
h9  = 'Кулинария'
h10 = 'Танцы'
h11 = 'Иностранные языки'
h12 = 'Музыка'
h13 = 'Кино'
end = 'Закончить'

hobbys = []
hobbys.append(h1)
hobbys.append(h2)
hobbys.append(h3)
hobbys.append(h4)
hobbys.append(h5)
hobbys.append(h6)
hobbys.append(h7)
hobbys.append(h8)
hobbys.append(h9)
hobbys.append(h10)
hobbys.append(h11)
hobbys.append(h12)
hobbys.append(h13)
hobbys.append(end)


hobby_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=4)           
hobby_client.add('1','2','3','4','5','6','7','8','9','10','11','12','13').add('Завершить')