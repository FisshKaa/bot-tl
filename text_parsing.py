from phrases import *
import re

def process_message_int(msg):
    match = re.search(r'\d+', msg)
    if match:
        return int(match.group())
    else:
        return None

def process_message(msg):
    text = [t[:4] for t in msg.lower().split()] # разбиваю фразу пользователя на слова, сост. из первых 4 букв
    phr = []    # и потом добавляем по ключевым словам то, что должен ответить бот
    if 'прив' in text or 'здра' in text:
        phr.append(hello_sms)
    if 'сайт' in text:
        phr.append(web_site)
    if 'груп' in text or 'сооб' in text:
        phr.append(web_vk)
    if 'спас' in text or 'спс' in text:
        phr = 'спасибо'
    return phr

def text_parsing(msg):
    phr = process_message_int(msg)
    if phr is not None:
        return phr
    else:
        return []