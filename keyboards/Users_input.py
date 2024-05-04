from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

button_tomorrow = KeyboardButton('на Завтра')
button_today = KeyboardButton('на Сегодня')
button_myrasp = KeyboardButton('Моё расписание на день/дни')
button_help = KeyboardButton('Помощь')
button_rasp = KeyboardButton('Поиск расписания любой группы')
button_group = KeyboardButton('Сохранить группу')


Users_input = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
Users_input.row(
    button_tomorrow, button_today, button_myrasp
).add(button_rasp).row(
    button_help, button_group
)



