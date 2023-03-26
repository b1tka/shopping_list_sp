from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from data.texts import create_group_text, join_group_text

test_button = KeyboardButton(create_group_text)
test_button_2 = KeyboardButton(join_group_text)
keyboard = ReplyKeyboardMarkup([[test_button, test_button_2]], resize_keyboard=True)