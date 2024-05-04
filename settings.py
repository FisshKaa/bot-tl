import os

# Token = '' # Геншин мем парадайз
# Token = '' # Колян
# Token = '' # ОСНОВА
translate_spec = {'би': 'bi', 'мн': 'mn', 'эк': 'ek', 'гд': 'gd', 'тур': 'tur', 'юф': 'ur', 'ек': 'ek'}
Token = '' # ТЕСТ
# Token = '' # Основа 2

admins = [760095030, 999962779]

test = ['би 03 21 04']
tur = 'тур-3-22-01'
test2 = ['мн 3 19 3 4', 'мн-3-19-03-04', 'БИ-03-21-03-04','би 03 21 03', 'би 03 21 04', 'эк 3 22 1']

put = os.curdir + '/schedule_files/' # Адаптивный путь
replacements = os.curdir + '/replacements/replacements.txt' # Замены
Users_db = os.curdir + '/Data/Users_db.csv'
Groups_db = os.curdir + '/Data/Groups_db.csv'
RM = os.curdir + '/schedule_files/rasp_month.txt'

# Заголовок для запроса, чтобы как будто чел в браузере смотрит, а не бот
header = {
    'Host': 'spb.ranepa.ru',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
    'Accept': '*/*',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'X-Requested-With': 'XMLHttpRequest',
    'Content-Type': 'application/x-protobuffer',
    # 'Content-Length': '6988',
    'Origin': 'https://techblog.willshouse.com',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Referer': 'https://www.spb.ranepa.ru',
    # 'Cookie': '__cf_bm=Q7IQqJmok4nvASfNI63UBaXjXLBjwjd7nGFyMWDbifs-1670242984-0-AY6EU82sMeE+vCrTxWz0ROSANqWgLAy3i51NP7c8aSeY5UrtMVrbFx7YGvVUw7BspP8UHz0YXEbeWYycyUm42w4muqiTy3KS+Xg9AyKA3i9SJKmB1kVHh7/oyRAmth1EukxlkAE0AU2Yh4fZ+c2cs6Q=',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-GPC': '1',
    'TE': 'trailers',
}