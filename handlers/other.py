from aiogram import types, Dispatcher
import json, string 
from create_bot import dp, bot, con
from handlers import valid
from text.index import unknown_command, start_message
from aiogram.utils.markdown import hide_link


# Реагирование на любые сообщения
async def echo_send(message : types.Message):

    # Проверка на мат
    # if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.text.split(' ')}.intersection(set(json.load(open('fil.json')))) != set():
    #     await message.reply('Маты запрещены')
    #     await message.delete()
    if await valid.check_user(message.from_user.id):
        await message.answer(unknown_command, reply_markup=types.ReplyKeyboardRemove())
    else:
        await bot.send_message(message.from_user.id, start_message)



def register_handlers_other(dp : Dispatcher):
    dp.register_message_handler(echo_send)  