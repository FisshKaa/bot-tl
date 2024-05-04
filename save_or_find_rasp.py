import pandas as pd
import os
import aiohttp
import asyncio
import datetime

from io import StringIO

from phrases import web_rasp
from settings import put, header



cortech = (
    (1, "yanvar"),
    (2, "fevral"),
    (3, "mart"),
    (4, "aprel"),
    (5, "maj"),
    (6, "iyun"),
    (7, "July"),
    (8, "avgust"),
    (9, "sentyabr"),
    (10, "oktyabr"),
    (11, "noyabr"),
    (12, "decabr")
)


async def find_rasp(name):
    today = datetime.datetime.now()
    rasp_month_path = put + 'rasp_month.txt'
    try:
        rasp_month = int(open(rasp_month_path, 'r').read())
    except:
        rasp_month = today.month
        open(rasp_month_path, 'w').write(str(rasp_month))
    if rasp_month != today.month:
        del_rasp_files()
        print("[*] Schedule update")

    # Get the month name from the tuple based on the current month
    month_name = cortech[today.month - 1][1]

    # Create the link using the user input and the month name
    link = f"{name}-{month_name.lower()}"

    try:
        pd_rasp = pd.read_csv(put + name + '.csv', encoding='UTF-8')
        return pd_rasp
    except:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(web_rasp + link + '/', headers=header, ssl=False) as response:
                    html = await response.text()
        except aiohttp.ClientError:
            # Обработка ошибки при выполнении запроса
            print("Error: Failed to retrieve data from the website")
            return pd.DataFrame()

        try:
            pd_rasp = pd.read_html(StringIO(html))[0]
        except:
            pd_rasp = pd.DataFrame()
        pd_rasp.columns = [column.upper() for column in pd_rasp.columns]
        await save_rasp(name, pd_rasp)
        return pd_rasp

async def find_rasp_with_retry(name):
    for i in range(3):
        try:
            pd_rasp = await find_rasp(name)
            if not pd_rasp.empty:
                return pd_rasp
            else:
                pass
        except:
            pass
        name_parts = name.split('-')
        if len(name_parts) >= 5:
            last_digit = name_parts[-1]
            number_is_out = name_parts[-2]
            if number_is_out != '01' or number_is_out == '01':
                name_parts[-2] = '01'
                name = '-'.join(name_parts)
                await asyncio.sleep(5)
                pd_rasp = await find_rasp(name)
                if not pd_rasp.empty:
                    return pd_rasp
                else:
                    for k in range(1, 7):
                        name_parts[-1] = str(int(last_digit) + k).rjust(2, '0')
                        name = '-'.join(name_parts)
                        pd_rasp = await find_rasp(name)
                        if not pd_rasp.empty:
                            return pd_rasp
                        else:
                            continue
                    if not pd_rasp.empty:
                        return pd_rasp


async def save_rasp(name, pd_rasp):
    if not os.path.exists(put):
        os.mkdir(put)
    file_put = put + name + '.csv'
    if not pd_rasp.empty:
        pd_rasp.to_csv(file_put, index=False)

def del_rasp_files():
    try:
        for item in os.listdir(put):
            if 'csv' in item:
                print(put + item)
                os.remove(put + item)
    except:
        print('[!] Error during removing old schedule')

def check_actual():
    now = datetime.datetime.now()
    delta = datetime.timedelta(hours=6)
    time = []

    try:
        raw_time = open(put + 'rasp_time.txt', 'r').readlines()
    except:
        raw_time = []

    if len(raw_time) == 0:
        raw_time = [
            str(now.day),
            str(now.month),
            str(now.year),
            str(now.hour),
            str(now.minute)
        ]
        open(put + 'rasp_time.txt', 'w').write('\n'.join(raw_time))

    for i in range(0, len(raw_time)):
        time.append(int(raw_time[i]))
    rasp_time = datetime.datetime(day=time[0],
                                   month=time[1],
                                   year=time[2],
                                   hour=time[3],
                                   minute=time[4])
    if(now > (rasp_time + delta)):
        del_rasp_files()
        now_time = [
            str(now.day),
            str(now.month),
            str(now.year),
            str(now.hour),
            str(now.minute)
        ]
        open(put + 'rasp_time.txt', 'w').write('\n'.join(now_time))