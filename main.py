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
    # user_name = message.from_user.first_name
    user_full_name = message.from_user.full_name
    logging.info(f'{user_id} {user_full_name} {time.asctime()}')
    await message.answer(ss.start, reply_markup=bs.mainMenu)
    await StateGroup.wait_for_choice.set()


@dp.message_handler(state=StateGroup.wait_for_choice)
async def choice_handler(message: types.Message):
    if message.text == 'Правила':
        await bot.send_message(message.from_user.id, ss.rules)
    if message.text == 'Выбор темы':
        await message.answer(text='Выбирайте...', reply_markup=bs.themeMenu)
        await message.answer(ss.themes)
        await StateGroup.wait_for_themes.set()


@dp.message_handler(state=StateGroup.wait_for_themes)
async def themes_handler(message: types.Message):
    user_id = message.from_user.id
    ss.counting = 0
    if message.text == 'Тема 1':
        ss.theme = 1
        await message.answer(text='Начнем!', reply_markup=bs.gameMenu)
        generator.start(user_id)
        await bot.send_photo(user_id, open('{}/temp.png'.format(user_id), 'rb'))
        await message.answer(ss.questions1)
        await StateGroup.wait_for_answer.set()
    elif message.text == 'Тема 2':
        ss.theme = 2
        await message.answer(text='Начнем!', reply_markup=bs.gameMenu)
        generator.start(user_id)
        await bot.send_photo(user_id, open('{}/temp.png'.format(user_id), 'rb'))
        await message.answer(ss.questions2)
        await StateGroup.wait_for_answer.set()
    elif message.text == 'Тема 3':
        ss.theme = 3
        await message.answer(text='Начнем!', reply_markup=bs.gameMenu)
        generator.start(user_id)
        await bot.send_photo(user_id, open('{}/temp.png'.format(user_id), 'rb'))
        await message.answer(ss.questions3)
        await StateGroup.wait_for_answer.set()
    elif message.text == 'Тема 4':
        ss.theme = 4
        await message.answer(text='Начнем!', reply_markup=bs.gameMenu)
        generator.start(user_id)
        await bot.send_photo(user_id, open('{}/temp.png'.format(user_id), 'rb'))
        await message.answer(ss.questions4)
        await StateGroup.wait_for_answer.set()
    elif message.text == 'Тема 5':
        ss.theme = 5
        await message.answer(text='Начнем!', reply_markup=bs.gameMenu)
        generator.start(user_id)
        await bot.send_photo(user_id, open('{}/temp.png'.format(user_id), 'rb'))
        await message.answer(ss.questions5)
        await StateGroup.wait_for_answer.set()
    elif message.text == 'Назад':
        await StateGroup.wait_for_choice.set()
        await message.answer(text='Возвращаемся назад...', reply_markup=bs.mainMenu)


@dp.message_handler(state=StateGroup.wait_for_exitin)
async def exit_handler(message: types.Message):
    if message.text == 'Подтвердить':
        await message.answer(text='Возвращаемся назад...', reply_markup=bs.themeMenu)
        await StateGroup.wait_for_themes.set()
    if message.text == 'Назад к решению':
        await message.answer(text='Возвращаемся назад...', reply_markup=bs.gameMenu)
        await StateGroup.wait_for_answer.set()


@dp.message_handler(state=StateGroup.wait_for_answer)
async def game_handler(message: types.Message):
    user_id = message.from_user.id
    th = ss.theme - 1
    ss.temp_ans = ss.answers[th].copy()
    if message.text == 'Правила':
        await bot.send_message(user_id, ss.rules)
    elif message.text == 'Назад':
        await StateGroup.wait_for_exitin.set()
        await message.answer(text='Внимание: если вы вернетесь к выбору темы, ваш прогресс будет сброшен',
                             reply_markup=bs.confMenu)
    elif message.text == 'Повтор вопросов':
        await bot.send_photo(user_id, open('{}/temp.png'.format(user_id), 'rb'))
        await bot.send_message(user_id, ss.questions[th])
    for i in ss.temp_ans:
        if message.text == i:
            ss.counting += 1
            await message.answer(text='Верно!')
            f = int(message.text.split()[0][:-1]) - 1
            ss.temp_ans.remove(i)
            generator.paste(ss.cs[th][f][0], ss.cs[th][f][1], ss.cs[th][f][2], ss.cs[th][f][3], user_id)
            await bot.send_photo(user_id, open('{}/temp.png'.format(user_id), 'rb'))
    if ss.counting == len(ss.cs[th]):
        await message.answer(text='Поздравляю! Вы прошли кроссворд!', reply_markup=bs.mainMenu)
        await StateGroup.wait_for_choice.set()


if __name__ == '__main__':
    executor.start_polling(dp)
