from aiogram import types, Dispatcher
import json, string 
from create_bot import dp, bot, con
from text.index import unknown_command, start_message
from keyboards.client_kb import kb_client
from aiogram.utils.markdown import hide_link


# Реагирование на любые сообщения
async def echo_send(message : types.Message):

    # Проверка на мат
    # if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.text.split(' ')}.intersection(set(json.load(open('fil.json')))) != set():
    #     await message.reply('Маты запрещены')
    #     await message.delete()
    with con.cursor() as cur:

        cur.execute(f"SELECT * FROM `user` WHERE ID={message.from_user.id}")
        rows = cur.fetchall()

        # Если нет, предлагаем зарегистрироваться
        if not rows:
            await bot.send_message(message.from_user.id, start_message + f"{hide_link('./src/price.png')}")

        # Иначе получает список команд
        else:
            await message.answer(unknown_command, reply_markup=kb_client)



def register_handlers_other(dp : Dispatcher):
    dp.register_message_handler(echo_send)  