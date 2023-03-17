import asyncio
import time
import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

from state import StateGroup
import buttons as bs
import strings as ss
import generator

loop = asyncio.get_event_loop()
TOKEN = "6272833831:AAGTNvQPUeoX_bPRNvt9CR5kc8EwztbCr2g"
CHANNEL_ID = 1

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot, loop=loop, storage=MemoryStorage())


@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    user_full_name = message.from_user.full_name
    logging.info(f'{user_id} {user_full_name} {time.asctime()}')
    await message.answer(ss.start, reply_markup=bs.mainMenu)
    await StateGroup.wait_for_choice.set()


@dp.message_handler(state=StateGroup.wait_for_choice)
async def choice_handler(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if message.text == 'Правила':
        await bot.send_message(message.from_user.id, ss.rules)
    if message.text == 'Выбор темы':
        generator.start()
        await message.answer(text='Выбирайте...', reply_markup=bs.themeMenu)
        await StateGroup.wait_for_themes.set()


@dp.message_handler(state=StateGroup.wait_for_themes)
async def themes_handler(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if message.text == 'Тема 1':
        await message.answer(text='Начнем!', reply_markup=bs.gameMenu)
        generator.start()
        await bot.send_photo(user_id, open('photo/temp.png', 'rb'))
        await message.answer(ss.questions1)
        await StateGroup.wait_for_answer.set()
    elif message.text == 'Тема 2':
        await message.answer(text='Начнем!', reply_markup=bs.gameMenu)
        generator.start()
        await bot.send_photo(user_id, open('photo/temp.png', 'rb'))
        await message.answer(ss.questions1)
        await StateGroup.wait_for_answer.set()
    elif message.text == 'Тема 3':
        await message.answer(text='Начнем!', reply_markup=bs.gameMenu)
        generator.start()
        await bot.send_photo(user_id, open('photo/temp.png', 'rb'))
        await message.answer(ss.questions1)
        await StateGroup.wait_for_answer.set()
    elif message.text == 'Тема 4':
        await message.answer(text='Начнем!', reply_markup=bs.gameMenu)
        generator.start()
        await bot.send_photo(user_id, open('photo/temp.png', 'rb'))
        await message.answer(ss.questions1)
        await StateGroup.wait_for_answer.set()
    elif message.text == 'Тема 5':
        await message.answer(text='Начнем!', reply_markup=bs.gameMenu)
        generator.start()
        await bot.send_photo(user_id, open('photo/temp.png', 'rb'))
        await message.answer(ss.questions1)
        await StateGroup.wait_for_answer.set()
    elif message.text == 'Назад':
        await StateGroup.wait_for_choice.set()
        await message.answer(text='Возвращаемся назад...', reply_markup=bs.mainMenu)


@dp.message_handler(state=StateGroup.wait_for_answer)
async def game_handler(message: types.Message, state: FSMContext):
    if message.text == 'Правила':
        await bot.send_message(message.from_user.id, ss.rules)
    elif message.text == 'Назад':
        await StateGroup.wait_for_themes.set()
        await message.answer(text='Возвращаемся назад...', reply_markup=bs.themeMenu)
    user_id = message.from_user.id
    for i in ss.answers1:
        if message.text == i:
            ss.counting += 1
            await message.answer(text='Верно!')
            f = int(message.text.split()[0][:-1]) - 1
            ss.answers1.remove(i)
            generator.paste(ss.cs[0][f][0], ss.cs[0][f][1], ss.cs[0][f][2], ss.cs[0][f][3])
            await bot.send_photo(user_id, open('photo/temp.png', 'rb'))
    if ss.counting == len(ss.cs[0]):
        await message.answer(text='Поздравляю! Вы прошли кроссворд!', reply_markup=bs.mainMenu)
        await StateGroup.wait_for_choice.set()


if __name__ == '__main__':
    executor.start_polling(dp)
