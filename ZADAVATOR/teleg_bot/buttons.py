from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from teleg_bot.config import sigma

#стандартные кнопки 
def main_kb(user_telegram_id: int):
    kb_list = [
        [KeyboardButton(text='get_task')],
        [KeyboardButton(text='send_answer')],
        [KeyboardButton(text='kill_user')]
    ]
    if user_telegram_id in sigma:
        kb_list.append([KeyboardButton(text='stats')])
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True, is_persistent=True)
                                
    return keyboard

# ну хз нахуй кнопка это
def welcome_kb(user_telegram_id: int):
    kb_list = [
        [KeyboardButton(text='reg')],
        [KeyboardButton(text='Что умеет этот бот?')]
    ]
    if user_telegram_id in sigma:
        kb_list.append([KeyboardButton(text='stats')])
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True, is_persistent=True)
    return keyboard

# тоже по сути и по содержанию хуйня
def send_all_kb():
    kb_list = [
        [KeyboardButton(text='send_all')],
        [KeyboardButton(text='cancel')]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True, is_persistent=True)
    return keyboard