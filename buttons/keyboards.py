from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from data.texts import create_group_text, join_group_text


# -------------------------------------------start keyboard---------------------------------------------------
# Стартовые кнопки
create_group_button = KeyboardButton(create_group_text)
join_group_button = KeyboardButton(join_group_text)

#Стартовая клавиатура
start_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
start_keyboard.add(create_group_button)
start_keyboard.add(join_group_button)
# ------------------------------------------------------------------------------------------------------------



# -------------------------------------------------in group keyboard-------------------------------------------------
# Кнопки
exit_inline_button = InlineKeyboardButton(text='Выйти из группы', callback_data='leave_from_group')
lists = InlineKeyboardButton(text='Актуальные листы', callback_data='show_all_lists')

# Клавиатура
group_keyboard = InlineKeyboardMarkup()
group_keyboard.add(exit_inline_button)
group_keyboard.add(lists)
#---------------------------------------------------------------------------------------------------------------------



# ----------------------------------------------------actual list-------------------------------------------------------------
# кнопки
def generate_lists_keyboard(lists):
    add_list = InlineKeyboardButton(text='Добавить новый лист', callback_data='add_new_list')
    back = InlineKeyboardButton(text='Вернутсья', callback_data='back_to_groups')
    list_keyboard = InlineKeyboardMarkup()

    for list in lists:
        list_keyboard.add(InlineKeyboardButton(text=list.name, callback_data=list.id))

    list_keyboard.add(add_list)
    list_keyboard.add(back)
    return list_keyboard

#Клавиатура


# ------------------------------------------------------------------------------------------