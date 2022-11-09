from aiogram import types, Dispatcher
from create_bot import dp, bot, con
from keyboards import kb_client, hobby_client
from aiogram.dispatcher.filters import Command
from text.index import unknown_command, code_format, invalid_code, start_message
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

class Hobby(StatesGroup):
    hobby1 = State()
    hobby2 = State()

# Команда /start
async def command_start(message : types.Message):
    # Проверяем зарегистрирован ли пользователь
    with con.cursor() as cur:
        cur.execute(f"SELECT * FROM `user` WHERE ID={message.from_user.id}")
        rows = cur.fetchall()

        # Если нет, регистрируем его
        if not rows:
            await message.answer(start_message)
            
        # Иначе получает список команд
        else:
            await message.answer(unknown_command, reply_markup=kb_client)


# Команда /code [code]
async def cmd_code(message: types.Message, command: Command):
    # Проверяем на пустоту значения
    if command.args:
        # Проверяем не ввёл ли пользователь 'NULL'
        if command.args == 'NULL':
            await message.answer(code_format)
        else:
            # Проверяем зарегистрирован ли такой код
            with con.cursor() as cur:
                cur.execute(f"SELECT * FROM `user` WHERE `code`='{command.args}'")
                rows = cur.fetchall()
                
                # Если нет, то выводи сообщение о несуществующем коде
                if not rows:
                    message.answer(invalid_code)
                else:
                    # Записываем id пользователя и код
                    cur.execute(f"UPDATE `user` SET ID={message.from_user.id}, code = NULL WHERE code ='{command.args}'")
                    con.commit()
                    await message.answer(unknown_command, reply_markup=kb_client)

    # Выводим пример ввода кода
    else:
        await message.answer(code_format)

async def settings(message: types.Message):
    with con.cursor() as cur:
        cur.execute(f"SELECT * FROM `hobby` WHERE ID={message.from_user.id}")
        rows = cur.fetchall()
        if not rows:
            await message.answer('Заполните информацию о себе. Выберите ваши интересы', reply_markup=hobby_client)





def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(command_start, commands=['start'])
    dp.register_message_handler(cmd_code, commands=['code'])
    dp.register_message_handler(settings, commands=['Настройки'])
