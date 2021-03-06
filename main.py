import config
import pymongo
import aiogram
import time
import timer
from quiz import Quiz
from config import dp, db, menu1, bot
from aiogram.dispatcher.filters import Command, Text
from aiogram import executor, types
from pymongo import CursorType

chatQuizes = {}

@dp.message_handler(commands=['start'])
async def welcome(message: types.Message):
    await message.answer(text='Привет, герои! Времени осталось совсем мало. Поэтому, подъезжайте к первому павильону. Остановитесь напротив звезды и дайте мне знать нажав «Начинаем! ✅».', reply_markup=menu1)

@dp.message_handler(text="Начинаем! ✅")
async def first(message: types.Message):
    quiz = Quiz(db, bot, message.chat.id)
    quiz.start()
    chatQuizes[message.chat.id] = quiz


@dp.message_handler(text="Таймер ⏳")
async def timer(message: types.Message):
    if message.chat.id in chatQuizes:
        timeLeft = chatQuizes[message.chat.id].timer.getTimeLeft()
        minutes = timeLeft / 60
        hours = int(minutes / 60)
        minutes = int(minutes % 60)
        seconds = int(timeLeft % 60)
        await message.answer("До окончания квеста: " + str(hours) + ":" + str(minutes) + ":" + str(seconds))

@dp.message_handler(content_types=types.ContentTypes.ANY)
async def all_other_messages(message: types.Message):
     if message.chat.id in chatQuizes:
         chatQuizes[message.chat.id].answer(message.text)
     else:
         await message.answer("Нажмите \"Начинаем!\" ✅ чтобы начать.")


if __name__ == '__main__':
    executor.start_polling(dp)
