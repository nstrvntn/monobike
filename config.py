from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils.helper import  Helper, HelperMode, ListItem
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from pymongo import MongoClient

#get telegram token from config.py
TOKEN =  'BOT TOKEN'
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

#conect to db
connect = MongoClient('localhost', 27017)
db = connect["monobike"]

#keyboard
helpButton = KeyboardButton("Помощь ❓")
timerButton = KeyboardButton("Таймер ⏳")
nextButton = KeyboardButton("Дальше ➡")
startButton = KeyboardButton("Начинаем! ✅")
menu1 = ReplyKeyboardMarkup(resize_keyboard=True).row(startButton)
