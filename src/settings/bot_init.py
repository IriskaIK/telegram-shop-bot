from dotenv import load_dotenv
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os

load_dotenv()


bot = Bot(token=os.environ.get('bot_token'))
dp = Dispatcher(bot, storage=MemoryStorage())