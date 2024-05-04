import datetime
import asyncio
import platform
import os


import logging
import aiofiles
from settings import RM
import calendar
import datetime
from keyboards import Users_input# кнопки
from keyboards.Calendar import create_calendar
import phrases
import settings
from settings import Token, Users_db, Groups_db
from aiogram import Bot, types, executor
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from text_parsing import text_parsing # мои технологии
from phrases import bot_error_pic, bot_error, memasiki, stikers #phrases это папка со всеми приколами, стикерами, фразами которыми отвечает бот
from search_rasp import main_rasp# мои технологии
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


import struct_checker
import logger as log

import random as rn
import pandas as pd
import tg_analytic # эта библиотека загруженна с интернета для небольшого совершенствования (недоделал) O_o
import re

struct_checker.check_paths(['Data',
                            'schedule_files',
                            'statistics',
                            'replacements',
                            'logs'])

sd = datetime.datetime.now()

print(sd.weekday())

try:
    Users = pd.read_csv(Users_db, dtype={
        'User': int,
        'Group': str,
        'RegisterTime': str,
        'info': str
    })
    print(Users)
except:
    Users = pd.DataFrame({'User': [0], 'Group':['TEST_GROUP'], 'RegisterTime': [f'{sd}'], 'Info': ['TEST_INFO']}, dtype={
        'User': int,
        'Group': str,
        'RegisterTime': str,
        'info': str
    })
    print(Users)
    Users.to_csv(Users_db, index=False)

try:
    Groups = pd.read_csv(Groups_db)
    print(Groups)
except:
    Groups = pd.DataFrame({'TG_Group': [-1], 'Group':['TEST_GROUP'], 'RegisterTime': [f'{sd}'], 'Info': ['TEST_INFO']})
    Groups.to_csv(Groups_db, index=False)
    print(Groups)


bot = Bot(token=Token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
# sost_rasp = 0 помять о Кирилле(пидр)
group_rasp = {}

class UserState(StatesGroup):
    waiting_for_group = State()
    waiting_for_month = State()
    waiting_for_input_group = State()

@dp.message_handler(commands=['send'])
async def send_msg_to_all(msg: types.Message):
    await log.user(msg)
    if msg.from_user.id in settings.admins:
        text = msg.text.replace('/send ', '')
        ids = Users.loc[:, 'User']
        for item in ids:
            print('[*]', item, end='  ')
            try:
                await bot.send_message(chat_id=item, text=text, disable_web_page_preview=True)
                print()
            except:
                print('ERROR')
        await log.bot(msg, "<НА ЭТУ КОМАНДУ ОТВЕТ НЕ ТРЕБУЕТСЯ>")

    else:
        await msg.answer('😛')
        await log.bot(msg, '😛')

@dp.message_handler(commands=['send-list'])
async def send_to_list(msg: types.Message):
    await log.user(msg)
    if msg.from_user.id in settings.admins:
        try:
            raw = msg.text.split(' ')
            ids = eval(f"[{raw[1]}]")
            text = ' '.join(raw[2:])
            print(raw)
            print(ids)
            print(text)
            id_err = []
            for id in ids:
                try:
                    print(f"[*] {id}  ", end='')
                    await bot.send_message(chat_id=id, text=text)
                    print()
                except:
                    print('ERROR')
                    id_err.append(id)
            if len(id_err) > 0:
                await msg.answer(f"Не удалось отправить сообщение следующим личностям: \n{id_err}")
                await log.bot(msg, f"Не удалось отправить сообщение следующим личностям: \n{id_err}")
        except:
            await msg.answer("Ошибка при вводе команды")
            await log.bot(msg, "Ошибка при вводе команды")
    else:
        await msg.answer('😛')
        await log.bot(msg, '😛')

@dp.message_handler(commands=['sticker'])
async def send_sticker_direct(msg: types.Message):
    await log.user(msg)
    if msg.from_user.id in settings.admins:
        raw = msg.text.split(' ')
        try:
            id = int(raw[1])
            sticker_id = raw[2]
            await bot.send_sticker(chat_id=id, sticker=sticker_id)
            await msg.answer(f"Стикер отправлен ID: {id}")
            await log.bot(msg, f"Стикер отправлен ID: {id}")
            await bot.send_sticker(chat_id=msg.from_user.id, sticker=sticker_id)
            await log.bot(msg, "<СТИКЕР>")
        except:
            await msg.answer("Ошибочка вышла")
            await log.bot(msg, "Ошибочка вышла")
    else:
        await msg.answer('😛')
        await log.bot(msg, '😛')

@dp.message_handler(commands=['msg'])
async def send_msg_to_admins(msg: types.Message):
    await log.user(msg)
    # raw = msg.text.split(':')
    try:
        text = msg.text.replace("/msg", "").strip() # удаляем "/msg" и удаляем пробелы в начале и конце текста
        if not text: # проверяем, что текст не пустой
            await msg.answer('Ваше сообщение пустое')
            await log.bot(msg, 'Ваше сообщение пустое')
            return
    except:
        await msg.answer('Вы не ввели сообщение')
        await log.bot(msg, 'Вы не ввели сообщение')
        return
    sended = False
    message = f"💌Сообщение от {msg.from_user.first_name}({msg.from_user.id}):\n{text}"
    for id in settings.admins:
        try:
            await bot.send_message(chat_id=id, text=message)
            sended = True
        except:
            await msg.answer(f'Ошибка отправки')
            await log.bot(msg, f'Ошибка отправки')
            print(f"Ошибка отправки: {msg.from_user.id}, {raw}")
    if sended == True:
        await msg.answer(f'Сообщение разработчикам отправлено💌')
        await log.bot(msg, f'Сообщение разработчикам отправлено💌')

@dp.message_handler(commands=['direct'])
async def direct(msg: types.Message):
    await log.user(msg)
    if msg.from_user.id in settings.admins:
        raw = msg.text.split(' ')
        try:
            id = int(raw[1])
            text = ' '.join(raw[2:])
            await bot.send_message(chat_id=id, text=text, disable_web_page_preview=True)
            await msg.answer(f'Сообщение отправлено ID: {id}')
            await log.bot(msg, f'Сообщение отправлено ID: {id}')
        except:
            print(msg.from_user.id, raw, 'ERROR')
    else:
        await msg.answer('😛')
        await log.bot(msg, '😛')

@dp.message_handler(commands=['start']) # команда старт
async def process_start_command(message: types.Message):
    td = datetime.datetime.now()
    global Users
    global Groups
    id = message.from_user.id
    chat_id = message.chat.id
    print(message.chat)
    # tg_analytic.statistics(id, 'start')
    await log.user(msg=message)

    if chat_id < 0:
        if Groups.loc[Groups['TG_Group'] == chat_id].empty:
            Groups = pd.concat([Groups, pd.DataFrame({'TG_Group': [chat_id], 'Group':['-'], 'RegisterTime': [f'{td}'], 'Info': [str(message.chat)]})])
            Groups.to_csv(Groups_db, index=False)
            await message.answer(phrases.hello_msg_1, parse_mode='html', reply_markup=Users_input)
            await log.bot(message, phrases.hello_msg_1)
            print(f'[*] New group: {chat_id}')
        else:
            await message.answer(phrases.hello_msg_2, parse_mode='html', reply_markup=Users_input)
            await log.bot(message, phrases.hello_msg_2)

        if Users.loc[Users['User'] == id].empty:
            Users = pd.concat([Users, pd.DataFrame({'User': [id], 'Group': '-', 'RegisterTime': [f'{td}'], 'Info': [str(message.from_user)]})])
            Users.to_csv(Users_db, index=False)
            print(f'[*] New user: {id}')

    else:
        if Users.loc[Users['User'] == id].empty:
            Users = pd.concat([Users, pd.DataFrame({'User': [id], 'Group': '-', 'RegisterTime': [f'{td}'], 'Info': [str(message.from_user)]})])
            await message.answer(phrases.hello_msg_1, parse_mode='html', reply_markup=Users_input)
            await log.bot(message, phrases.hello_msg_2)
            Users.to_csv(Users_db, index=False)
            print(f'[*] New user: {id}')
        else:
            await message.answer(phrases.hello_msg_2, parse_mode='html', reply_markup=Users_input)
            await log.bot(message, phrases.hello_msg_2)


#когда то здесь был кусок кода для мемов 😢

@dp.message_handler(regexp=re.compile(r'^Помощь$', re.IGNORECASE))   #ну тут понятно, помощь
async def process_help_command(message: types.Message):
    # tg_analytic.statistics(message.from_user.id, 'help')
    await log.user(msg=message)
    await message.answer(phrases.help, parse_mode='html', reply_markup=Users_input)
    await log.bot(msg=message, answer=phrases.help)

@dp.message_handler(regexp=re.compile(r'^Поиск расписания любой группы$', re.IGNORECASE))
async def process_help_command(message: types.Message, state: FSMContext):
    await log.user(msg=message)
    async with state.proxy() as data:
        data.clear()
        data['group'] = None
    await UserState.waiting_for_group.set()
    await bot.send_message(message.from_user.id, 'Введите свою группу', reply_markup=types.ReplyKeyboardRemove())
    await log.bot(msg=message, answer='Введите свою группу')


@dp.message_handler(state=UserState.waiting_for_group)
async def process_group(message: types.Message, state: FSMContext):
    await log.user(msg=message)
    async with state.proxy() as data:
        data['group'] = message.text
    await UserState.waiting_for_month.set()
    async with aiofiles.open(RM, mode='r', encoding='UTF-8') as f:
        month = await f.read()
    now = datetime.datetime.now()
    year = now.year
    month_number = int(month)
    if 1 <= month_number <= 12:
        calendar_keyboard = create_calendar(year, month_number)
        await bot.send_message(message.from_user.id, 'Выберите день(после нажатия на день, у вас будет ровно 5 секунд, чтобы выбрать остальные дни):', reply_markup=calendar_keyboard)
        await bot.send_message(message.from_user.id, 'После вашего нажатия обработка вашего расписания может варьироваться от 20 до 80 секунд. Пожалуйста, подождите...',)

# Обработчик нажатия кнопок календаря
@dp.callback_query_handler(lambda c: c.data.startswith('day_'), state=UserState.waiting_for_month)
async def process_day_selection(callback_query: types.CallbackQuery, state: FSMContext):
    await log.user(msg=callback_query.message)
    day = callback_query.data.split('_')[1]  # Извлекаем день из данных кнопки
    async with state.proxy() as data:
        data['day'] = day  # Сохраняем выбранный день в состоянии
    await sms_pasrsing(callback_query.message, state)  # Перенаправляем на функцию sms_pasrsing


@dp.message_handler(regexp=re.compile(r'^Сохранить группу$', re.IGNORECASE))
async def ask_user_group(msg: types.Message, state: FSMContext):
    await log.user(msg=msg)
    async with state.proxy() as data:
        data.clear()
        data['input_group'] = None
    await UserState.waiting_for_input_group.set()
    await bot.send_message(msg.from_user.id, 'Введите вашу группу:', reply_markup=types.ReplyKeyboardRemove())
    await log.bot(msg=msg, answer='Введите вашу группу:')

@dp.message_handler(state=UserState.waiting_for_input_group)
async def process_group_message(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['input_group'] = msg.text
    group = data['input_group']
    Users.loc[Users['User'] == msg.from_user.id, 'Group'] = group
    Users.to_csv(Users_db, index=False)
    await msg.answer('Группа сохранена: ' + group, reply_markup=Users_input)
    await log.bot(msg=msg, answer='Группа сохранена: ' + group)
    await state.finish()
    # Register the message handler for group input


@dp.message_handler(regexp=re.compile(r'^Моё расписание на день/дни$', re.IGNORECASE))
async def myrasp(msg: types.Message, state: FSMContext):
    await log.user(msg=msg)
    search = Users.loc[Users['User'] == msg.from_user.id, 'Group'].values
    if search == '-':
        await msg.answer(phrases.group_err_dlg, parse_mode='html')
        await log.bot(msg=msg, answer=phrases.group_err_dlg)
        return
    else:
        group = search[0]

    async with aiofiles.open(RM, mode='r', encoding='UTF-8') as f:
        month = await f.read()
    now = datetime.datetime.now()
    year = now.year
    month_number = int(month)
    if 1 <= month_number <= 12:
        calendar_keyboard = create_calendar(year, month_number)
        await bot.send_message(msg.from_user.id, 'Выберите день(после нажатия на день, у вас будет ровно 5 секунд, чтобы выбрать остальные дни):', reply_markup=calendar_keyboard)
        await bot.send_message(msg.from_user.id,
                               'После вашего нажатия обработка вашего расписания может варьироваться от 20 до 80 секунд. Пожалуйста, подождите...',
                               reply_markup=types.ReplyKeyboardRemove())
        await UserState.waiting_for_month.set()
        await state.update_data(group=group)  # Сохраняем группу в состоянии
    else:
        await msg.answer('Ошибка при загрузке календаря. Пожалуйста, попробуйте еще раз.')
        await log.bot(msg=msg, answer='Ошибка при загрузке календаря')

@dp.callback_query_handler(lambda c: c.data.startswith('day_'), state=UserState.waiting_for_month)
async def process_day_selection(callback_query: types.CallbackQuery, state: FSMContext):
    await log.user(msg=callback_query.message)
    day = callback_query.data.split('_')[1]  # Извлекаем день из данных кнопки
    async with state.proxy() as data:
        data['day'] = day  # Сохраняем выбранный день в состоянии
    await UserState.waiting_for_day.set()
    await state.update_data(day=day)  # Сохраняем выбранный день в состоянии
    await sms_parsing(callback_query.message, state)


@dp.message_handler(regexp=re.compile(r'^на Завтра$', re.IGNORECASE))
async def tomorrow_rasp(msg: types.Message):
    await log.user(msg=msg)
    today = datetime.datetime.now()
    try:
        search = Users.loc[Users['User'] == msg.from_user.id, 'Group'].values
        if search == '-':
            await msg.answer(phrases.group_err_dlg, parse_mode='html', reply_markup=Users_input)
            await log.bot(msg=msg, answer=phrases.group_err_dlg)
            return
        else:
            group = search[0]
        day = today.day + 1
        await bot.send_message(msg.from_user.id,
                               'Обработка вашего расписания, может варьироваться от 20 до 80 секунд. Пожалуйста, подождите...',
                               reply_markup=types.ReplyKeyboardRemove())
        rasp = await main_rasp(group, day)
        await msg.answer(rasp, parse_mode='html', reply_markup=Users_input)
        await log.bot(msg=msg, answer=rasp)
    except:
        await msg.answer('Ошибка поиска', reply_markup=Users_input)
        await log.bot(msg=msg, answer='Ошибка поиска')
        print('Ошибка поиска \n', msg.from_user)


@dp.message_handler(regexp=re.compile(r'^на Сегодня$', re.IGNORECASE))
async def tomorrow_rasp(msg: types.Message):
    await log.user(msg=msg)
    today = datetime.datetime.now()

    try:
        search = Users.loc[Users['User'] == msg.from_user.id, 'Group'].values
        if search == '-':
            await msg.answer(phrases.group_err_dlg, parse_mode='html', reply_markup=Users_input)
            await log.bot(msg=msg, answer=phrases.group_err_dlg)
            return
        else:
            group = search[0]
        day = today.day
        await bot.send_message(msg.from_user.id,
                               'Обработка вашего расписания, может варьироваться от 20 до 80 секунд. Пожалуйста, подождите...',
                               reply_markup=types.ReplyKeyboardRemove())
        rasp = await main_rasp(group, day)
        await msg.answer(rasp, parse_mode='html', reply_markup=Users_input)
        await log.bot(msg=msg, answer=rasp)

    except:
        await msg.answer('Ошибка поиска', reply_markup=Users_input)
        await log.bot(msg=msg, answer='Ошибка поиска')
        print('Ошибка поиска \n', msg.from_user)

# @dp.message_handler(commands=['statistics']) #это для той библиотеки из интернета
# async def process_stat(msg: types.Message):
#     message = tg_analytic.analysis(msg.text.split(), msg.from_user.id)
#     await bot.send_message(msg.from_user.id, message)
#     if search == '-':
#         await msg.answer(phrases.group_err_dlg, parse_mode='html')
#         return

@dp.message_handler(commands=['serverinfo'])
async def server_info(msg: types.Message):
    await log.user(msg=msg)
    if msg.from_user.id in settings.admins:
        info = platform.platform()
        user = os.getlogin()
        await msg.answer(f'{info}\n'
                         f'{user}\n')
        await log.bot(msg=msg, answer=(f'{info}\n'
                                    f'{user}\n'))


async def sms_pasrsing(msg: types.Message, state: FSMContext):
    await log.user(msg=msg)
    async with state.proxy() as data:
        group = data.get('group')
        phr = data.get('day')
        if group is not None and phr is not None:
            try:
                rasp = await main_rasp(group, phr)
                await msg.answer(rasp, parse_mode='html', reply_markup=Users_input)
                await log.bot(msg, rasp)
            except Exception as e:
                await msg.answer(phrases.group_not_find_err, parse_mode='html', reply_markup=Users_input)
                await log.bot(msg, f"{phrases.group_not_find_err}\nException: {str(e)}")
        else:
            await msg.answer(phrases.invalid_input_err, parse_mode='html', reply_markup=Users_input)
            await log.bot(msg, "<ЭТОТ БЛОК КОДА НЕ ДОЛЖЕН ВЫЗЫВАТЬСЯ>")
        await state.finish()


executor.start_polling(dp)  # чтобы бот работал всегда