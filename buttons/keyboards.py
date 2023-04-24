from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardButton, InlineKeyboardMarkup
from data.texts import create_group_text, join_group_text
from db import db_funcs

# -------------------------------------------start keyboard---------------------------------------------------
# Стартовые кнопки
create_group_button = KeyboardButton(create_group_text)
join_group_button = KeyboardButton(join_group_text)

# Стартовая клавиатура
start_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
start_keyboard.add(create_group_button)
start_keyboard.add(join_group_button)
# ------------------------------------------------------------------------------------------------------------

back_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
back_button = KeyboardButton('Вернуться')
back_keyboard.add(back_button)

# -------------------------------------------------in group keyboard-------------------------------------------------
# Кнопки
exit_inline_button = InlineKeyboardButton(text='Выйти из группы',
                                          callback_data='leave_from_group')
lists = InlineKeyboardButton(text='Актуальные листы',
                             callback_data='show_all_lists')
get_code = InlineKeyboardButton(text='Код группы', callback_data='group_code')

# Клавиатура
group_keyboard = InlineKeyboardMarkup()
group_keyboard.add(exit_inline_button)
group_keyboard.add(lists)
group_keyboard.add(get_code)

# ---------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------actual list-------------------------------------------------------------
def generate_actual_lists_keyboard(lists):
    add_list = InlineKeyboardButton(text='Добавить новый лист',
                                    callback_data='add_new_list')
    back = InlineKeyboardButton(text='Вернутсья',
                                callback_data='back_to_groups')
    list_keyboard = InlineKeyboardMarkup()

    for list in lists:
        list_keyboard.add(
            InlineKeyboardButton(text=list.name, callback_data=list.id))

    list_keyboard.add(add_list)
    list_keyboard.add(back)
    return list_keyboard

# --------------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------list keyboard---------------------------------------------------
def generate_main_list_keyboard(sales):
    back = InlineKeyboardButton(text='Вернуться',
                                callback_data='back_to_actual_lists')
    add_new_item = InlineKeyboardButton(text='Добавить новый продукт',
                                        callback_data='add_new_item')
    delete = InlineKeyboardButton(text='Удалить лист',
                                  callback_data='delete_list')

    keyboard = InlineKeyboardMarkup()
    for sale in sales:
        if sale.state:
            keyboard.add(InlineKeyboardButton(text=f'{sale.item.name} ✅',
                            callback_data=sale.item.id))
        else:
            keyboard.add(InlineKeyboardButton(text=f'{sale.item.name} 🕛',
                            callback_data=sale.item.id))
    keyboard.add(add_new_item)
    keyboard.add(delete)
    keyboard.add(back)

    return keyboard
# --------------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------add item keyboard-----------------------------------------------------
def generate_back_button():
    back = KeyboardButton(text='Вернуться')

    back_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    back_keyboard.add(back)

    return back_keyboard
# ------------------------------------------------------------------------------------------------------------