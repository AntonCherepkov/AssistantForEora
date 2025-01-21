from api_methods.custom_requests import GigaClient
from config_data.config import API_GIGACHAT, TELEGRAM_API_TOKEN
from aiogram import Bot, Dispatcher
from middlewar.file_check import FileCheckMiddleware
from aiogram.fsm.storage.memory import MemoryStorage


g_client = GigaClient(credentials=API_GIGACHAT)
bot = Bot(token=TELEGRAM_API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
