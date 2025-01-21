from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
import asyncio


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Начать работу с ботом"),
        BotCommand(command="help", description="Получить справку")
    ]
    await bot.set_my_commands(commands)
