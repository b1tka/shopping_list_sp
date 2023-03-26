import logging
import asyncio

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from db import db_funcs
from data import db_session
from buttons.buttons import keyboard
from data.texts import *
from utils import UserState
from TOKEN import TOKEN


logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())


@dp.message_handler(commands=['start'], state='*')
async def start(message: types.Message):
    username = message.from_user.first_name
    tg_user_id = message.from_user.id
    chat_id = message.chat.id
    print(username, tg_user_id, chat_id)
    db_funcs.add_user_to_db_table_user(username, tg_user_id, chat_id)
    await message.answer(text=start_text, reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == create_group_text, state='*')
async def start_create_group(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    await state.set_state(UserState.all()[0])
    await message.answer(text=offer_to_write_text)


@dp.message_handler(state=UserState.CREATE_GROUP_STATE)
async def create_group(message: types.Message):
    admin_id = message.from_user.id
    name = message.text
    state = dp.current_state(user=message.from_user.id)
    db_funcs.create_new_group(admin_id, name)
    await message.answer(text='123')
    await state.reset_state()


@dp.message_handler(lambda message: message.text == join_group_text, state='*')
async def start_join_group(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    await state.set_state(UserState.all()[1])
    await message.answer(text=offer_to_send_code_text)


@dp.message_handler(state=UserState.JOIN_GROUP_STATE)
async def join_group(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    code = message.text
    user_id = message.from_user.id
    res = db_funcs.join_to_group(code, user_id)
    if db_funcs.join_to_group(code, user_id):
        if res == 2:
            await message.answer(text=already_in_group_text)
        else:
            await message.answer(text=f'{success_join_text} {res}')
    else:
        await message.answer(text=group_doesnt_exist_text)
    await state.reset_state()


@dp.message_handler(lambda message: message.text == join_group_text, state='*')
async def join_group(message: types.Message):
    pass


if __name__ == '__main__':
    db_session.global_init('db/database.db')
    executor.start_polling(dp, skip_updates=True)