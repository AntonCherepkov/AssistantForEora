from api_methods.dialog import CreateQuestForLMM
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from errors.errors import ProjectSearchError
from loader import g_client
from aiogram import Router

router = Router()

@router.message()
async def dialogue_with_assistant(message: Message, state: FSMContext):
    await message.answer("Пожалуйста, подождите, идет обработка запроса...")
    await state.set_state("StatesBot:DIALOG")
    user_question = message.text
    await message.reply("\u231B Думаю над ответом...")

    try:
        question_for_llm = CreateQuestForLMM(query_user=user_question)
        await g_client.initialize()
        quest = question_for_llm.build_query()
        response = await g_client.request_llm(user_quest=quest)
        await message.reply(f'{response}')

    except ProjectSearchError as e_1:
        await message.reply(f'Проекты по вашему запросу не найдены. Попробуйте перефразировать вопрос.')
