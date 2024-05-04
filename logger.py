from aiogram import types
import aiofiles
import datetime
import platform
import os
import getpass

import settings


async def user(msg: types.Message):
    now = datetime.datetime.now()

    text = msg.text
    id = msg.from_user.id

    date = now.strftime("%d.%m.%Y")
    time = now.strftime("%H.%M.%S")

    info = platform.platform()
    #user = os.getlogin()
    user = getpass.getuser()

    entry = f'{date},{time},{info},{user},{msg.chat.id},{msg.from_user.id},"{msg.text}"\n'

    filename = f"LOG-{user}-{date}.csv"

    async with aiofiles.open(os.curdir + '/logs/' + filename, mode="a", encoding="UTF-8") as file:
        await file.write(entry)


async def bot(msg: types.message, answer = str()):
    answer = answer.replace('\n', '<enter>')

    now = datetime.datetime.now()

    text = msg.text
    id = msg.from_user.id

    date = now.strftime("%d.%m.%Y")
    time = now.strftime("%H.%M.%S")

    info = platform.platform()
    #user = os.getlogin()
    user = getpass.getuser()


    entry = f'{date},{time},{info},{user},{msg.chat.id},{msg.from_user.id},BOT ANSWER: "{answer}"\n'

    filename = f"LOG-{user}-{date}.csv"

    async with aiofiles.open(os.curdir + '/logs/' + filename, mode="a", encoding="UTF-8") as file:
        await file.write(entry)
