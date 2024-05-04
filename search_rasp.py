import datetime
import re


import pandas as pd
import aiofiles
import asyncio
import datetime
import re
import phrases
import save_or_find_rasp

from save_or_find_rasp import find_rasp_with_retry
from settings import translate_spec, test, put
from save_or_find_rasp import find_rasp
from settings import replacements
#голова кода находиться в низу, оттуда все начинается
# процесс преобразования и создания ссылки на расписание
def editing_requests(text, izn_n):
    spl = ' '
    if '-' in text:
        spl = '-'
    number = text.split(spl)
    izn_n = izn_n.split(spl)
    if len(number[1]) != len(str(int(number[1]))):  # в случае если написано би-03-21-04, сайту нужно би-3-21-03
        number[1] = number[1][1]
        izn_n[1] = izn_n[1][1]
    if len(number) == 4:
        if int(number[-1]) % 2 == 1:
            number = number + [str(int(number[-1]) + 1), ]
        else:
            number = number[:-1] + [str(int(number[-1]) - 1), number[-1]]
    for n in range(-2, 0, 1):
        number[n] = number[n].rjust(2, '0')
    return '-'.join(number), '-'.join(izn_n)

def obr_rasp(text):
    text=text.lower()
    izn_n = text.upper()
    if text[:2] in translate_spec:
        text = translate_spec[text[:2]] + text[2:]
    # не помню для чего я делал расписания для тур, наверно там также составлялась ссылка
    else:
        if 'тур' in text:
            text = translate_spec['тур'] + text[3:]
    number, izn_n = editing_requests(text, izn_n)
    return number, izn_n

async def search_raspis(text):
    loop = asyncio.get_event_loop()
    rasp, izn_n = await loop.run_in_executor(None, obr_rasp, text)
    # raspisanie = await loop.run_in_executor(None, find_rasp, rasp)
    raspisanie = await find_rasp_with_retry(rasp)
    return izn_n, raspisanie

# тут происходит так называемый отбор по дням и нужным колонкам
async def sort_rasp(izn_n, raspisanie, day):
    today = datetime.datetime.now()
    month = today.month
    num_columns = len(raspisanie.columns)
    if num_columns >= 2:
        first_column_name = raspisanie.columns[0]
    second_column_name = raspisanie.columns[1]
    if first_column_name != 'day':
        raspisanie = raspisanie.rename(columns={first_column_name: 'day'})
    if second_column_name != 'month':
        raspisanie = raspisanie.rename(columns={second_column_name: 'month'})
    filtered_rasp = raspisanie.query(f"day == {day} and month == {month}")
    raw_entries = filtered_rasp.values.tolist()
    if len(raw_entries) == 0:
        return phrases.day_rasp_empty
    rasp_readable = ''
    for item in raw_entries:
        rasp_groups = group_split(item[6])[3:]
        group = group_split(izn_n)[3]
        if (group not in rasp_groups) and is_group_in_range(group, rasp_groups):
            continue
        rasp_readable += f"<b>--- </b> <b>{item[3].replace('.', ':')}</b> <b> ---</b>\n" \
                         f"<b>Группы:</b> <i>{str(item[6]).replace('[', '').replace(']', '')}</i>\n" \
                         f"<b>Тип:</b> <i>{item[5]}</i>\n" \
                         f"<b>Предмет:</b> <i>{item[7]}</i>\n" \
                         f"<b>Препод:</b> <i>{item[9]}</i>\n" \
                         f"<b>Аудитория:</b> <i>{item[10]}</i>\n\n".replace("'", "")

    if rasp_readable == '':
        return phrases.day_rasp_empty

    rasp_readable = f'<b>Расписание на {day if day >= 10 else f"0{day}"}.{month if month >= 10 else f"0{month}"} ({raw_entries[0][2]}): \n\n</b>' + rasp_readable
    async with aiofiles.open(replacements, mode='r', encoding='UTF-8') as f:
        contents = await f.read()
    replace = eval(contents)
    for r in replace:
        if len(r) < 2:
            continue
        rasp_readable = re.sub(rf" {r[0]} ", rf"{r[1]}", rasp_readable)
    return rasp_readable


def is_group_in_range(group, rasp_groups):
    if len(rasp_groups) == 1:
        return True

    if len(rasp_groups) > 2:
        return True

    first_arg = int(rasp_groups[0])
    second_arg = int(rasp_groups[1])

    if first_arg < second_arg:
        for i in range(second_arg, first_arg):
            if i == group:
                return True
    else:
        return False
    return False

def convert_text(text):
    parts = text.lower().replace(' ', '-',).split('-')
    if len(parts) == 4 and parts[0] in translate_spec:
        if len(parts[1]) == 2 and parts[1].isdigit():
            parts[1] = str(int(parts[1]))
        if len(parts[3]) == 1 and parts[3].isdigit():
            parts[3] = '0' + parts[3]
        return '-'.join([translate_spec[parts[0]], parts[1], parts[2], parts[3]])
    return None


def convert_text_error(text):
    parts = text.lower().replace(' ', '-',).split('-')
    if len(parts) == 4 and parts[0]:
        if len(parts[1]) == 2 and parts[1].isdigit():
            parts[1] = str(int(parts[1]))
        if len(parts[3]) == 1 and parts[3].isdigit():
            parts[3] = '0' + parts[3]
        return '-'.join([parts[0], parts[1], parts[2], parts[3]])
    return None

async def main_rasp(group, phr):
    if group is None or phr is None:
        return None
    save_or_find_rasp.check_actual()
    day = int(phr)
    text = convert_text_error(group)
    converted_text = convert_text(text)
    if len(converted_text.lower().split('-')) == 4:
        raspisanie = await find_rasp(converted_text)
        if not raspisanie.empty:
            izn_n = converted_text
        else:
            otvet = await search_raspis(text)
            izn_n = otvet[0]
            raspisanie = otvet[1]
    rasp = await sort_rasp(izn_n, raspisanie, day)
    return rasp
    # except:
    #     return phrases.group_not_find_err


def group_split(group = str()):
    return group.split('-')