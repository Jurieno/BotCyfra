from aiogram import types, Dispatcher
import json, string 
from create_bot import dp, bot, con
from text.index import unknown_command, start_message
from keyboards.client_kb import kb_client


# Реагирование на любые сообщения
async def echo_send(message : types.Message):

    # Проверка на мат
    if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.text.split(' ')}.intersection(set(json.load(open('fil.json')))) != set():
        await message.reply('Маты запрещены')
        await message.delete()

    # Если сообщение не мат, то проверяем зарегистрирован ли пользователь
    else:
        with con.cursor() as cur:

            cur.execute(f"SELECT * FROM `user` WHERE ID={message.from_user.id}")
            rows = cur.fetchall()

            # Если нет, предлагаем зарегистрироваться
            if not rows:
                print(start_message)

            # Иначе получает список команд
            else:
                await message.answer(unknown_command, reply_markup=kb_client)



def register_handlers_other(dp : Dispatcher):
    dp.register_message_handler(echo_send)  