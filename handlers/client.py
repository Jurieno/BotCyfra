from aiogram import types, Dispatcher
from create_bot import dp, bot, con
from keyboards import kb_price, cancel_kb, cancel_ready_kb, kb_settings, hobby_client, hobbys, reset_kb
from keyboards import kb_search, kb_ankets
from handlers import valid
from aiogram.dispatcher.filters import Command
from text.index import unknown_command, code_format, invalid_code, start_message
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from magic_filter import F

import datetime

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
    check_profile = State()
# --------------------------------------------------- FSMsettings ---------------------------------------------------------
# ---------------------------------------------------   КОНЕЦ     ---------------------------------------------------------


# --------------------------------------------------- FSMsearch ---------------------------------------------------------

class FSMsearch(StatesGroup):
    search = State()


class FSMwaitankets(StatesGroup):
    wait = State()


class FSM_refresh_ankets(StatesGroup):
    refresh = State()
# --------------------------------------------------- FSMsearch ---------------------------------------------------------
# ---------------------------------------------------   КОНЕЦ   ---------------------------------------------------------


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
# ---------------------------------------------------  КОНЕЦ  ---------------------------------------------------------


# --------------------------------------------------- /start ---------------------------------------------------------
async def command_start(message: types.Message):
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
        if await state.get_state() is None:
            return
        await state.finish()

        if await valid.check_user(message.from_user.id):
            await message.answer(unknown_command, reply_markup=types.ReplyKeyboardRemove())
        else:
            await message.answer(start_message, reply_markup=types.ReplyKeyboardRemove())


async def settings(message: types.Message):
    if message.chat.type == "private":
        if await valid.check_user(message.from_user.id):
            await FSMsettings.check_profile.set()
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
            await check_profile(message, state)
        else:
            await message.answer(start_message, reply_markup=types.ReplyKeyboardRemove())


async def profile(message: types.Message, state: FSMContext, row_user=None):
    async with state.proxy() as data:
        data['row_user'] = row_user
        if data['row_user'] == None:
            data['row_user'] = await con("SELECT `name`, `photo`, `hobby` FROM `users` RIGHT OUTER JOIN `hobbys` ON `id` = `id_user` WHERE `id` = {}".format(message.from_user.id))
        await bot.send_photo(chat_id=message.from_user.id,
                             photo=data['row_user'][0][1],
                             caption='Имя: {0}\n\nХобби: \n{1}'.format(
                                 data['row_user'][0][0], ', '.join([hobby[2] for hobby in data['row_user']])),
                             reply_markup=reset_kb)
        await FSMwait_update_user.wait.set()


async def check_profile(message: types.Message, state: FSMContext):
    await state.finish()
    async with state.proxy() as data:
        data['row_user'] = await con("SELECT `name`, `photo`, `hobby` FROM `users` LEFT JOIN `hobbys` ON `id_user` = `id` WHERE `id` = {}".format(message.from_user.id))
        if not data['row_user']:
            await message.answer('ОШИБКА: О неисправности сообщите Администратору!')
        else:
            if data['row_user'][0][0] == None:

                await FSMuser.name.set()
                await message.answer('Введите ваше имя.', reply_markup=cancel_kb)

            elif data['row_user'][0][1] == None:
                await FSMuser.photo.set()
                await message.answer('Загрузите фото для вашего профиля.', reply_markup=cancel_kb)

            elif data['row_user'][0][2] == None:
                await FSMuser.hobby.set()
                await message.answer("Выберите хобби:", reply_markup=hobby_client)
                await message.answer('\n'.join(f'{x+1}. {hobbys[x]}' for x in range(len(hobbys) - 1)))

            else:
                await profile(message, state, row_user=data['row_user'])

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


async def hobby_user(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data["hobby"] = await con("SELECT `id_user`, `hobby` FROM `hobbys` WHERE `id_user`={0} AND `hobby`='{1}'".format(message.from_user.id, hobbys[int(message.text)-1]))
            if not data["hobby"]:
                await con("INSERT INTO `hobbys`(`id_user`, `hobby`) VALUES ({0},'{1}')".format(message.from_user.id, hobbys[int(message.text)-1]), "insert")
                await message.answer('✅ Хобби {} добавлено'.format(hobbys[int(message.text)-1]))
            else:
                await con("DELETE FROM `hobbys` WHERE `id_user`={0} AND `hobby`='{1}'".format(message.from_user.id, hobbys[int(message.text)-1]), "insert")
                await message.answer('❌ Хобби {} удалено'.format(hobbys[int(message.text)-1]))
    except ValueError as ex:
        print(ex)


async def wait_update(message: types.Message, state: FSMContext):
    await state.finish()
    await FSMuser.name.set()
    await message.answer('Введите ваше имя.', reply_markup=cancel_kb)

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
                        await con(f"DELETE FROM `codes` WHERE `code`='{command.args}'", "delete")
                        await con(f"INSERT INTO `users`(`id`, `id_role`, `id_company`, `activate`) VALUES ({message.from_user.id},3,{rows[0][1]},true)", "insert")
                        await message.answer("Заполните профиль введя команду /settings", reply_markup=types.ReplyKeyboardRemove())
        else:
            await message.answer(code_format)
    else:
        await message.reply("Команда может использоваться только в личных сообщениях.")

# --------------------------------------------------- /code ---------------------------------------------------------
# --------------------------------------------------- КОНЕЦ ---------------------------------------------------------


# --------------------------------------------------- /search ---------------------------------------------------------

async def func_search(message: types.Message, state: FSMContext):
    timer = datetime.datetime.now()
    async with state.proxy() as data:
        data['my_hobby'] = await con("SELECT `hobby` FROM `hobbys` WHERE `id_user` = {}".format(message.from_user.id))

        data['query'] = f"SELECT `id` FROM `users` JOIN `hobbys` ON `id` = `id_user` WHERE `id_company` = (SELECT `id_company` FROM `users` WHERE `id` = {message.from_user.id}) AND `id` NOT IN (SELECT `id_prosmotr` FROM `ankets` WHERE `id_smotr` = {message.from_user.id}) AND (`hobby` IN ('"+"','".join([
            data['hobby'][0] for data['hobby'] in data['my_hobby']])+"')) ORDER BY RAND() LIMIT 1"
        data['id_searched'] = await con(data['query'])
        if data['id_searched']:
            data['row_user'] = await con("SELECT `name`, `photo`, `hobby` FROM `users` RIGHT OUTER JOIN `hobbys` ON `id` = `id_user` WHERE `id` = {}".format(data['id_searched'][0][0]))
        else:
            data[
                'query'] = f"SELECT `id` FROM `users` JOIN `hobbys` ON `id` = `id_user` WHERE `id_company` = (SELECT `id_company` FROM `users` WHERE `id` = {message.from_user.id}) AND `id` NOT IN (SELECT `id_prosmotr` FROM `ankets` WHERE `id_smotr` = {message.from_user.id}) ORDER BY RAND() LIMIT 1"
            data['id_searched'] = await con(data['query'])
            if not data['id_searched']:
                await state.finish()
                await FSM_refresh_ankets.refresh.set()
                await message.answer("К сожалению вы просмотрели все анкеты. Хотите просмотреть заново?")

        if data['id_searched']:
            data['row_user'] = await con("SELECT `name`, `photo`, `hobby` FROM `users` RIGHT OUTER JOIN `hobbys` ON `id` = `id_user` WHERE `id` = {}".format(data['id_searched'][0][0]))
            await bot.send_photo(chat_id=message.from_user.id,
                                 photo=data['row_user'][0][1],
                                 caption='Имя: {0}\n\nХобби: \n{1}'.format(
                                    data['row_user'][0][0], ', '.join([hobby[2] for hobby in data['row_user']])),
                                 reply_markup=kb_search)
            await con("INSERT INTO `ankets`(`id_smotr`, `id_prosmotr`, `date_at`,`checked`) VALUES ({0},{1},NOW(),0)".format(message.from_user.id, data['id_searched'][0][0]), "insert")

    print(datetime.datetime.now() - timer)


async def search(message: types.Message, state: FSMContext):
    if message.chat.type == "private":
        if await valid.check_user(message.from_user.id):

            async with state.proxy() as data:
                data['rows'] = await con("(SELECT `id_prosmotr` FROM `ankets` WHERE `id_smotr` = {} LIMIT 1)".format(message.from_user.id))
                if not data['rows']:
                    await con("INSERT INTO `ankets`(`id_smotr`, `id_prosmotr`, `date_at`,`checked`) VALUES ({0},{0},NOW(),1)".format(message.from_user.id), "insert")
                await FSMsearch.search.set()
                await func_search(message, state)

        else:
            await message.answer(start_message)


async def like_search(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['id_searched'] = await con(f"SELECT `id_prosmotr` FROM `ankets` WHERE `id_smotr` = {message.from_user.id} ORDER BY `date_at` LIMIT 1")
        await bot.send_message(data['id_searched'][0][0], "С вами хотят общаться, хотите проверить кто?", reply_markup=kb_ankets)
        await dp.current_state(user=data['id_searched'][0][0]).set_state(FSMwaitankets.wait)

    await func_search(message, state)


async def dislike_search(message: types.Message, state: FSMContext):
    await func_search(message, state)


async def zzz_search(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['current_state'] = await state.get_state()
        if data['current_state'] is None:
            return
        await state.finish()
        if await valid.check_user(message.from_user.id):
            await check_profile(message, state)
        else:
            await message.answer(start_message, reply_markup=types.ReplyKeyboardRemove())


async def wait_ankets_true(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Тут пока ничего нет)")


async def refreshing(message: types.Message, state: FSMContext):
    await state.finish()
    await con("DELETE FROM `ankets` WHERE `id_smotr` = {0} AND `id_prosmotr` != {0}".format(message.from_user.id), "delete")
    await func_search(message, state)

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
        await bot.send_message(message.from_user.id, f"Проверьте введённые данные:\n\nКомпания: {data['name_company']}\nСотрудники: {data['num_employs']}\nСвязь: " +
                               f"{data['communication']}\n\nЕсли что-то введено неверно, нажмите кнопку: ОТМЕНА", reply_markup=cancel_ready_kb)
        await FSMprice.next()


async def data_veryfi(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        await con("INSERT INTO `company`(`am_employs`, `name`, `communication`) VALUES ({0},'{1}','{2}')".format(data['num_employs'], data['name_company'], data['communication']), "insert")
    await bot.send_message(message.from_user.id, 'Данные сохранены, ожидайте, Администрация с вами свяжется')

    await state.finish()

# --------------------------------------------------- /price ---------------------------------------------------------
# ---------------------------------------------------  КОНЕЦ ---------------------------------------------------------


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start'])

    dp.register_message_handler(cmd_code, commands=['code'])

    dp.register_message_handler(settings, commands=['settings'], state=None)
    dp.register_message_handler(cancel_settings, Text(
        equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(check_profile, Text(
        equals='Профиль', ignore_case=True), state=FSMsettings.check_profile)
    dp.register_message_handler(cancel_profile, Text(
        equals='завершить', ignore_case=True), state="*")
    dp.register_message_handler(name_user,  state=FSMuser.name)
    dp.register_message_handler(photo_user, content_types=[
                                'photo'], state=FSMuser.photo)
    dp.register_message_handler(hobby_user, state=FSMuser.hobby)
    dp.register_message_handler(wait_update, Text(
        equals='Изменить данные', ignore_case=True), state=FSMwait_update_user.wait)

    dp.register_message_handler(price, commands=['price'], state=None)
    dp.register_message_handler(hand_price, state=FSMprice.trial_period)
    dp.register_message_handler(company, state=FSMprice.name_company)
    dp.register_message_handler(num_employs, state=FSMprice.num_employs)
    dp.register_message_handler(communication, state=FSMprice.communication)
    dp.register_message_handler(data_veryfi, state=FSMprice.data_veryfi)

    dp.register_message_handler(search, commands=['search'], state=None)
    dp.register_message_handler(wait_ankets_true, Text(
        equals='👍', ignore_case=True), state=FSMwaitankets.wait)
    dp.register_message_handler(cancel_settings, Text(
        equals='❌', ignore_case=True), state=FSMwaitankets.wait)
    dp.register_message_handler(like_search, Text(
        equals='👍', ignore_case=True), state=FSMsearch.search)
    dp.register_message_handler(dislike_search, Text(
        equals='❌', ignore_case=True), state=FSMsearch.search)
    dp.register_message_handler(zzz_search, Text(
        equals='💤', ignore_case=True), state=FSMsearch.search)

    dp.register_message_handler(cancel_settings, Text(
        equals='Нет', ignore_case=True), state=FSM_refresh_ankets.refresh)
    dp.register_message_handler(refreshing, Text(
        equals='Да', ignore_case=True), state=FSM_refresh_ankets.refresh)

    dp.register_message_handler(command_start, commands=[''])
