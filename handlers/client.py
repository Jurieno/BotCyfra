from aiogram import types, Dispatcher
from create_bot import dp, bot, con
from keyboards import kb_price, cancel_kb, cancel_ready_kb, kb_settings, hobby_client, hobbys, reset_kb
from handlers import valid
from aiogram.dispatcher.filters import Command
from text.index import unknown_command, code_format, invalid_code, start_message
from aiogram.utils.markdown import hide_link
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text

# --------------------------------------------------- FSMprice ---------------------------------------------------------

class FSMprice(StatesGroup):
    trial_period = State()
    name_company = State()
    num_employs = State()
    communication = State()
    data_veryfi = State()
# --------------------------------------------------- FSMprice ---------------------------------------------------------
# --------------------------------------------------- КОНЕЦ ---------------------------------------------------------


# --------------------------------------------------- FSMsettings ---------------------------------------------------------

class FSMsettings(StatesGroup):
    select_settings = State()
# --------------------------------------------------- FSMsettings ---------------------------------------------------------
# ---------------------------------------------------   КОНЕЦ     ---------------------------------------------------------



# --------------------------------------------------- FSMsettings ---------------------------------------------------------

class FSMsearch(StatesGroup):
    search = State()
# --------------------------------------------------- FSMsettings ---------------------------------------------------------
# ---------------------------------------------------   КОНЕЦ     ---------------------------------------------------------



# --------------------------------------------------- FSMuser ---------------------------------------------------------

class FSMuser(StatesGroup):
    name = State()
    photo = State()
    hobby = State()

class FSMwait_update_user(StatesGroup):
    wait = State()

class FSMupdate_user(StatesGroup):
    name = State()
    photo = State()
    hobby = State()
# --------------------------------------------------- FSMuser ---------------------------------------------------------
# ---------------------------------------------------   КОНЕЦ     ---------------------------------------------------------




# --------------------------------------------------- /start ---------------------------------------------------------
async def command_start(message : types.Message):
    if message.chat.type == "private":
        if await valid.check_user(message.from_user.id):
            await message.answer(unknown_command, reply_markup=types.ReplyKeyboardRemove())
        else:
            await message.answer(start_message, reply_markup=types.ReplyKeyboardRemove())
        
# --------------------------------------------------- /start ---------------------------------------------------------
# ---------------------------------------------------  КОНЕЦ ---------------------------------------------------------




# --------------------------------------------------- /settings ---------------------------------------------------------
async def cancel_settings(message: types.Message, state: FSMContext):
    if message.chat.type == "private":
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        if await valid.check_user(message.from_user.id):
            await message.answer(unknown_command, reply_markup=types.ReplyKeyboardRemove())
        else:
            await message.answer(start_message, reply_markup=types.ReplyKeyboardRemove())

async def settings(message : types.Message):
    if message.chat.type == "private":
        if await valid.check_user(message.from_user.id):
            await FSMsettings.select_settings.set()
            await message.answer("Выберите дальнейшие действия.", reply_markup=kb_settings)
        else:
            await message.answer(start_message, reply_markup=types.ReplyKeyboardRemove())
    else:
        await message.reply("Команда может использоваться только в личных сообщениях.")
    

async def cancel_profile(message: types.Message, state: FSMContext):
    if message.chat.type == "private":
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        if await valid.check_user(message.from_user.id):
            await check_profile(message)
        else:
            await message.answer(start_message, reply_markup=types.ReplyKeyboardRemove())


async def profile(message: types.Message, row_user=None):
    if row_user == None:
       row_user = await con("SELECT `name`, `photo`, `hobby` FROM `users` RIGHT OUTER JOIN `hobbys` ON `id` = `id_user` WHERE `id` = {}".format(message.from_user.id))
    await bot.send_photo(chat_id=message.from_user.id, 
                        photo=row_user[0][1],
                        caption='Имя: {0}\n\nХобби: \n{1}'.format(row_user[0][0], ', '.join([hobby[2] for hobby in row_user])),
                        reply_markup=reset_kb)
    await FSMwait_update_user.wait.set()

async def check_profile(message: types.Message):
    row_user = await con("SELECT `name`, `photo`, `hobby` FROM `users` LEFT JOIN `hobbys` ON `id_user` = `id` WHERE `id` = {}".format(message.from_user.id))
    
    if not row_user:
        await message.answer('ОШИБКА: О неисправности сообщите Администратору!')
    else:
        if row_user[0][0] == None:
            
            await FSMuser.name.set()
            await message.answer('Введите ваше имя.', reply_markup=cancel_kb)

        elif row_user[0][1] == None:
            await FSMuser.photo.set()
            await message.answer('Загрузите фото для вашего профиля.', reply_markup=cancel_kb)
            
        elif row_user[0][2] == None:
            await FSMuser.hobby.set()
            await message.answer("Выберите хобби:", reply_markup=hobby_client)
            await message.answer('\n'.join(f'{x+1}. {hobbys[x]}' for x in range(len(hobbys) - 1)))
        
        else:
            await profile(message, row_user=row_user)


async def select_settings(message: types.Message, state: FSMContext):
    if message.text == 'Профиль':
        await state.finish()
        await check_profile(message=message)
    elif  message.text == 'Мои мероприятия':
        await message.answer('Функция в разработке.', reply_markup=types.ReplyKeyboardRemove())
        await message.answer(unknown_command)
    else:
        await state.finish()
        await message.answer('Действие прервано.', reply_markup=types.ReplyKeyboardRemove())
        await message.answer(unknown_command)


# --------------------------------------------------- /settings ---------------------------------------------------------
# ---------------------------------------------------    КОНЕЦ  ---------------------------------------------------------





# --------------------------------------------------- Профиль ------------------------------------------------------------


async def name_user(message: types.Message):
    await FSMuser.next()
    await con("UPDATE `users` SET `name`='{0}' WHERE `id`={1}".format(message.text, message.from_user.id), "update")
    await message.answer("Загрузите фото для вашего профиля.", reply_markup=cancel_kb)

async def photo_user(message: types.Message):
    await FSMuser.next()
    await con("UPDATE `users` SET `photo`='{0}' WHERE `id`={1}".format(message.photo[0].file_id, message.from_user.id), "update")
    await message.answer("Выберите хобби:", reply_markup=hobby_client)
    await message.answer('\n'.join(f'{x+1}. {hobbys[x]}' for x in range(len(hobbys) - 1)))
    
    

async def hobby_user(message: types.Message):
    try:
        rows = await con("SELECT `id_user`, `hobby` FROM `hobbys` WHERE `id_user`={0} AND `hobby`='{1}'".format(message.from_user.id, hobbys[int(message.text)-1]))
        if not rows:
            await con("INSERT INTO `hobbys`(`id_user`, `hobby`) VALUES ({0},'{1}')".format(message.from_user.id, hobbys[int(message.text)-1]),"insert")
            await message.answer('✅ Хобби {} добавлено'.format(hobbys[int(message.text)-1]))
        else:
            await con("DELETE FROM `hobbys` WHERE `id_user`={0} AND `hobby`='{1}'".format(message.from_user.id, hobbys[int(message.text)-1]),"insert")
            await message.answer('❌ Хобби {} удалено'.format(hobbys[int(message.text)-1]))
    except Exception as ex:
        print(ex)

async def wait_update(message: types.Message, state: FSMContext):
    await state.finish()
    if message.text == 'Изменить данные':
        await FSMuser.name.set()
        await message.answer('Введите ваше имя.', reply_markup=cancel_kb)
    else:
        await message.answer('Действие прервано', reply_markup=types.ReplyKeyboardRemove())
        await message.answer(unknown_command)


# --------------------------------------------------- Профиль ------------------------------------------------------------
# ---------------------------------------------------  КОНЕЦ  ------------------------------------------------------------


# --------------------------------------------------- /code ---------------------------------------------------------

async def cmd_code(message: types.Message, command: Command):
    if message.chat.type == "private":
        if command.args:
            if command.args == 'NULL':
                await message.answer(code_format)
            else:
                # True: пользователь зарегистрирован
                if await valid.check_user(message.from_user.id):
                    await message.answer(unknown_command, reply_markup=types.ReplyKeyboardRemove())
                else:
                    rows = await con(f"SELECT * FROM `codes` WHERE `code`='{command.args}'")

                    if not rows:
                        await message.answer(invalid_code)
                    else:
                        await con(f"DELETE FROM `codes` WHERE `code`='{command.args}'","delete")
                        await con(f"INSERT INTO `users`(`id`, `id_role`, `id_company`, `activate`) VALUES ({message.from_user.id},3,{rows[0][1]},true)","insert")
                        await message.answer("Заполните профиль введя команду /settings", reply_markup=types.ReplyKeyboardRemove())
        else:
            await message.answer(code_format)
    else:
        await message.reply("Команда может использоваться только в личных сообщениях.")
    

# --------------------------------------------------- /code ---------------------------------------------------------
# --------------------------------------------------- КОНЕЦ ---------------------------------------------------------




# --------------------------------------------------- /search ---------------------------------------------------------

async def search(message: types.Message):
    if message.chat.type == "private":
        if await valid.check_user(message.from_user.id):

            row_user = await con(
                '''SELECT `id` FROM `users` JOIN `hobbys` ON `id` = `id_user` WHERE `id_company` = (SELECT `id_company` FROM `users` WHERE `id` = 1026555793) AND `id` != 1026555793 AND `id` != (SELECT `id_prosmotr` FROM `ankets` WHERE `id_smotr` = 1026555793)  AND `hobby` = "Спорт"'''.format(message.from_user.id))
            print(row_user)

        else:
            await message.answer(start_message)
    

async def handle_search(message: types.Message):
    pass

# --------------------------------------------------- /search ---------------------------------------------------------
# --------------------------------------------------- КОНЕЦ ---------------------------------------------------------







# --------------------------------------------------- /price ---------------------------------------------------------

async def price(message: types.Message):
    if message.chat.type == "private":
        await FSMprice.trial_period.set()
        photo = open('./src/price.png', 'rb')
        await bot.send_photo(message.from_user.id, photo, reply_markup=kb_price)
    else:
        await message.reply("Команда может использоваться только в личных сообщениях.")
    
    
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply(start_message)

async def hand_price(message: types.Message):
    await FSMprice.next()
    await message.reply("Введите название компании.", reply_markup=cancel_kb)
        

async def company(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name_company'] = message.text
    await FSMprice.next()
    await message.reply("Введите количество сотрудников в вашей компании.", reply_markup=cancel_kb)

async def num_employs(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['num_employs'] = int(message.text)
        await FSMprice.next()
        await message.reply("Укажите способ связи с вами.\nПример: Whatsapp +7800*****66", reply_markup=cancel_kb)
    except Exception:
        await message.reply('Введите количество сотрудников.')

async def communication(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['communication'] = message.text
        await bot.send_message(message.from_user.id, f"Проверьте введённые данные:\n\nКомпания: {data['name_company']}\nСотрудники: {data['num_employs']}\nСвязь: "+
                               f"{data['communication']}\n\nЕсли что-то введено неверно, нажмите кнопку: ОТМЕНА", reply_markup=cancel_ready_kb)
        await FSMprice.next()


async def data_veryfi(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        await con("INSERT INTO `company`(`am_employs`, `name`, `communication`) VALUES ({0},'{1}','{2}')".format(data['num_employs'],data['name_company'],data['communication']),"insert")
    await bot.send_message(message.from_user.id, 'Данные сохранены, ожидайте, Администрация с вами свяжется')

    await state.finish()

# --------------------------------------------------- /price ---------------------------------------------------------
# ---------------------------------------------------  КОНЕЦ ---------------------------------------------------------




def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(command_start, commands=['start'])

    dp.register_message_handler(cmd_code, commands=['code'])

    dp.register_message_handler(settings, commands=['settings'], state=None)
    dp.register_message_handler(cancel_settings, state="*", commands='отмена')
    dp.register_message_handler(cancel_settings, Text(equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(select_settings, state=FSMsettings.select_settings)

    dp.register_message_handler(cancel_profile, Text(equals='завершить', ignore_case=True), state="*")
    dp.register_message_handler(name_user,  state=FSMuser.name)
    dp.register_message_handler(photo_user, content_types=['photo'], state=FSMuser.photo)
    dp.register_message_handler(hobby_user, state=FSMuser.hobby)

    dp.register_message_handler(wait_update, state=FSMwait_update_user.wait)

    dp.register_message_handler(price, commands=['price'], state=None)
    dp.register_message_handler(hand_price, state=FSMprice.trial_period)
    dp.register_message_handler(company, state=FSMprice.name_company)
    dp.register_message_handler(num_employs, state=FSMprice.num_employs)
    dp.register_message_handler(communication, state=FSMprice.communication)
    dp.register_message_handler(data_veryfi, state=FSMprice.data_veryfi)

    dp.register_message_handler(search, commands=['search'], state=None)
    dp.register_message_handler(handle_search, state=FSMsearch.search)

    dp.register_message_handler(command_start, commands=[''])
