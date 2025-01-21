from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import Command, CommandStart

router = Router()

@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await message.answer("Привет! Я бот для предоставления информации о проектах компании Eora, введите ваш вопрос, для "
                         "получения информации о проектах")
    await state.set_state("StatesBot:START")

@router.message(Command("help"))
async def start(message: Message, state: FSMContext):
    await message.reply(
        "Команды бота:\n/start - начать работу с ботом\n/help - получить справку"
    )
