from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import calendar

# Функция для создания клавиатуры с календарем
def create_calendar(year, month):
    inline_keyboard = InlineKeyboardMarkup(row_width=7)

    # Кнопки для дней недели
    days_of_week = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
    for day in days_of_week:
        inline_keyboard.insert(InlineKeyboardButton(day, callback_data='#'))

    # Получаем первый день месяца и количество дней в месяце
    first_day, num_days = calendar.monthrange(year, month)

    # Получаем сдвиг для первого дня месяца
    shift = first_day

    # Создаем клавиатуру с днями месяца
    for _ in range(shift):
        inline_keyboard.insert(InlineKeyboardButton(' ', callback_data='#'))

    for day in range(1, num_days+1):
        inline_keyboard.insert(InlineKeyboardButton(str(day), callback_data='day_' + str(day)))

    # Получаем сдвиг для последнего дня месяца
    last_day = (shift + num_days) % 7

    # Добавляем пустые кнопки после последнего дня месяца
    for _ in range(7 - last_day):
        inline_keyboard.insert(InlineKeyboardButton(' ', callback_data='#'))

    return inline_keyboard