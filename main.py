import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher.webhook import DeleteMessage

from db import db_funcs
from data import db_session
from buttons.keyboards import *
from data.texts import *
from utils import UserState
from TOKEN import TOKEN

# Настройка бота
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())


# Стартовая функция
@dp.message_handler(commands=['start'], state='*')
async def start(message: types.Message):
    username = message.from_user.first_name
    tg_user_id = message.from_user.id
    chat_id = message.chat.id
    db_funcs.add_user_to_db_table_user(username, tg_user_id, chat_id)
    await message.answer(text=start_text, reply_markup=start_keyboard)


# Запрос имя новый группы
@dp.message_handler(lambda message: message.text == create_group_text)
async def start_create_group(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    await state.set_state('create_group_state')  # UserState.CREATE_GROUP_STATE
    await message.answer(text=offer_to_write_text)


# Создание новой группы
@dp.message_handler(state=UserState.CREATE_GROUP_STATE)
async def create_group(message: types.Message):
    admin_id = message.from_user.id
    name = message.text
    state = dp.current_state(user=message.from_user.id)
    db_funcs.create_new_group(admin_id, name)
    await state.set_state('in_group_state')  # UserState.IN_GROUP_STATE
    await message.answer(text=main_group_text(message.from_user.id),
                         reply_markup=group_keyboard)


# Запрос на код группы
@dp.message_handler(lambda message: message.text == join_group_text)
async def start_join_group(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    await state.set_state('join_group_state')  # UserState.JOIN_GROUP_STATE
    await message.answer(text=offer_to_send_code_text)


# Присоеднинение к группе
@dp.message_handler(state=UserState.JOIN_GROUP_STATE)
async def join_group(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    code = message.text
    user_id = message.from_user.id
    res = db_funcs.join_to_group(code, user_id)
    if db_funcs.join_to_group(code, user_id):
        if res == 2:
            await message.answer(text=already_in_group_text)
            await state.reset_state()
        else:
            await message.answer(text=f'{success_join_text} {res}')
            await message.answer(
                text=f'{main_group_text(message.from_user.id)}',
                reply_markup=group_keyboard)
            await state.set_state('in_group_state')  # UserState.IN_GROUP_STATE
    else:
        await message.answer(text=group_doesnt_exist_text)
        await state.reset_state()


# Выход из группы
@dp.callback_query_handler(
    lambda inline_query: inline_query.data == 'leave_from_group',
    state=UserState.IN_GROUP_STATE)
async def delete_group(callback_query: types.CallbackQuery):
    state = dp.current_state(user=callback_query.from_user.id)
    db_funcs.leave_from_group(callback_query.from_user.id)
    await state.reset_state()
    await bot.delete_message(chat_id=callback_query.message.chat.id,
                             message_id=callback_query.message.message_id)
    await callback_query.answer(text='Вы вышли из группы')


# Ожидание названия листа
@dp.message_handler(state=UserState.WAITING_LIST_NAME)
async def add_new_list(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    group_id = db_funcs.get_group_by_user_id(message.from_user.id)
    db_funcs.create_new_list(group_id, message.text)
    lists = db_funcs.get_actual_lists(group_id)
    keyboard = generate_actual_lists_keyboard(lists)
    await state.set_state('waiting_to_open_list')
    await message.answer(text=actual_lists_text(message.from_user.id),
                         reply_markup=keyboard)


# Добавить новый лист
@dp.callback_query_handler(
    lambda inline_query: inline_query.data == 'add_new_list',
    state=UserState.WAITING_TO_OPEN_LIST)
async def add_new_list(callback_query: types.CallbackQuery):
    state = dp.current_state(user=callback_query.from_user.id)
    await state.set_state('waiting_list_name')
    await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                message_id=callback_query.message.message_id,
                                text='Введите название нового листа')


@dp.callback_query_handler(
    lambda inline_query: inline_query.data == 'back_to_groups',
    state=UserState.WAITING_TO_OPEN_LIST)
async def back_to_groups(callback_query: types.CallbackQuery):
    state = dp.current_state(user=callback_query.from_user.id)
    user_id = callback_query.from_user.id
    chat_id = db_funcs.get_chat_id_by_user_id(user_id)
    group = db_funcs.get_group_by_user_id(user_id)
    await state.set_state('in_group_state')
    await bot.delete_message(chat_id=chat_id,
                             message_id=callback_query.message.message_id)
    await bot.send_message(chat_id=chat_id, text=main_group_text(user_id),
                           reply_markup=group_keyboard)


# Показать все листы
@dp.callback_query_handler(
    lambda inline_query: inline_query.data == 'show_all_lists',
    state=UserState.IN_GROUP_STATE)
async def show_all_lists(callback_query: types.CallbackQuery):
    state = dp.current_state(user=callback_query.from_user.id)
    group_id = db_funcs.get_group_by_user_id(callback_query.from_user.id)
    lists = db_funcs.get_actual_lists(group_id)
    keyboard = generate_actual_lists_keyboard(lists)
    await state.set_state('waiting_to_open_list')
    await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                message_id=callback_query.message.message_id,
                                text=actual_lists_text(
                                    callback_query.from_user.id),
                                reply_markup=keyboard)


@dp.callback_query_handler(state=UserState.WAITING_TO_OPEN_LIST)
async def open_list(callback_query: types.CallbackQuery):
    state = dp.current_state(user=callback_query.from_user.id)
    user_id = callback_query.from_user.id
    chat_id = db_funcs.get_chat_id_by_user_id(user_id)
    list_id = callback_query.data
    name = db_funcs.get_name_list_by_list_id(list_id)
    await state.set_data(
        {'curr_list': list_id}
    )
    await state.set_state('in_list')
    await bot.delete_message(chat_id=chat_id,
                             message_id=callback_query.message.message_id)
    await bot.send_message(chat_id=chat_id,
                           text=f'Продукты листа {name}',
                           reply_markup=generate_main_list_keyboard())


@dp.callback_query_handler(
    lambda inline_query: inline_query.data == 'add_new_item',
    state=UserState.IN_LIST)
async def add_new_product(callback_query: types.CallbackQuery):
    state = dp.current_state(user=callback_query.from_user.id)
    chat_id = db_funcs.get_chat_id_by_user_id(callback_query.from_user.id)
    await state.set_state('add_new_product')
    await bot.delete_message(chat_id=chat_id,
                             message_id=callback_query.message.message_id)
    await bot.send_message(chat_id=chat_id, text='Введите название продукта')


@dp.message_handler(state=UserState.ADD_NEW_PRODUCT)
async def set_name_for_new_product(message: types.Message):
    pass


@dp.callback_query_handler(
    lambda inline_query: inline_query.data == 'back_to_actual_lists',
    state=UserState.IN_LIST)
async def back_to_actual_list(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    chat_id = db_funcs.get_chat_id_by_user_id(user_id)
    state = dp.current_state(user=user_id)
    group_id = db_funcs.get_group_by_user_id(user_id)
    lists = db_funcs.get_actual_lists(group_id)
    keyboard = generate_actual_lists_keyboard(lists)
    await state.set_state('waiting_to_open_list')
    await bot.edit_message_text(chat_id=chat_id,
                                message_id=callback_query.message.message_id,
                                text=actual_lists_text(user_id),
                                reply_markup=keyboard)


if __name__ == '__main__':
    db_session.global_init('db/database.db')
    executor.start_polling(dp, skip_updates=True)
