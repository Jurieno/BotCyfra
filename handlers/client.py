from aiogram import types, Dispatcher
from create_bot import dp, bot, con
from keyboards import kb_client, price_kb
from handlers import valid
from aiogram.dispatcher.filters import Command
from text.index import unknown_command, code_format, invalid_code, start_message
from aiogram.utils.markdown import hide_link
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StateGroup

class FSMAdmin(StateGroup):
    trial_period = State()

# Команда /start
async def command_start(message : types.Message):
    if await valid.check_user(message.from_user.id):
        await message.answer(unknown_command, reply_markup=kb_client)
    else:
        await message.answer(start_message)
        


# Команда /code [code]
async def cmd_code(message: types.Message, command: Command):
    # Проверяем на пустоту значения
    if command.args:
        # Проверяем не ввёл ли пользователь 'NULL'
        if command.args == 'NULL':
            await message.answer(code_format)
        else:
            with con.cursor() as cur:
                # True: пользователь зарегистрирован
                if await valid.check_user(message.from_user.id):
                    await message.answer(unknown_command, reply_markup=kb_client)
                else:
                    cur.execute(f"SELECT * FROM `codes` WHERE `code`='{command.args}'")
                    rows = cur.fetchall()

                    if not rows:
                        await message.answer(invalid_code)
                    else:
                        cur.execute(f"DELETE FROM `codes` WHERE `code`='{command.args}'")
                        cur.execute(f"INSERT INTO `users`(`id`, `id_role`, `id_company`, `activate`) VALUES ({message.from_user.id},3,{rows[0]['id_company']},true)")
                        con.commit()
                        await message.answer(unknown_command, reply_markup=kb_client)
    else:
        await message.answer(code_format)

async def price(message: types.Message):
    await FSMAdmin.trial_period.set()
    photo = open('./src/price.png', 'rb')
    await bot.send_photo(message.from_user.id, photo, reply_markup=price_kb)

async def hand_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        tt = 1
    await FSMAdmin





def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(command_start, commands=['start'])
    dp.register_message_handler(cmd_code, commands=['code'])
    dp.register_message_handler(price, commands=['price'], state=None)
    dp.register_message_handler(hand_price, state=FSMAdmin.name)
