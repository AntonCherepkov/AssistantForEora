from typing import Callable, Dict, Any
from aiogram import types
from aiogram import BaseMiddleware
from utils.run_parsing import run_spider
import os, time


class FileCheckMiddleware(BaseMiddleware):
    def __init__(self):
        super().__init__()

    async def __call__(self, handler: Callable, event: types, data: Dict[str, Any]) -> Callable:
        """Проверка файла c данными о проектах на актуальность"""

        if event.message:
            message: types.Message = event.message

            file_path = "result.json"
            if not os.path.exists(file_path) or self.is_file_outdated(file_path):
                await message.answer(
                    "Файл данных устарел или отсутствует. Пожалуйста, подождите, запускаю процесс обновления..."
                )
                await run_spider()
                await message.answer("Процесс обновления завершен, информация актуальна.")

        return await handler(event, data)

    def is_file_outdated(self, file_path):
        """Проверка актуальности файла с данными о проектах по времени создания (сутки)"""
        file_mod_time = os.path.getmtime(file_path)
        current_time = time.time()
        file_age = current_time - file_mod_time

        if file_age > 86400:
            return True
        return False
