from dotenv import load_dotenv, find_dotenv
import os

if not find_dotenv():
    exit('Переменные окружения не загружены, нет файла .env')
else:
    load_dotenv()

API_GIGACHAT = os.getenv('API_GIGACHAT')
ID_GIGACHAT = os.getenv('ID_GIGACHAT')
TELEGRAM_API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')
