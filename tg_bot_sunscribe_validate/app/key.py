from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Проверить подписку')]
], resize_keyboard=True, one_time_keyboard=True, is_persistent=True)
