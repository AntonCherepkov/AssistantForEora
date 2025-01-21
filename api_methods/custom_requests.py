import uuid
from pprint import pprint
import json
import aiohttp
import asyncio


class GigaClient:
    """Класс для работы с API GigaChat"""
    def __init__(
            self,
            credentials: str,
            scope: str = 'GIGACHAT_API_PERS',
            model: str = 'GigaChat'
    ) -> None:
        self.credentials=credentials
        self.scope=scope
        self.model=model
        self.token_access = None

    async def initialize(self):
        """Асинхронная инициализация токена доступа"""
        self.token_access = await self.request_key()

    async def request_key(self) -> str:
        """Асинхронная функция для получения токена доступа"""
        url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

        payload = {'scope': self.scope}
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json',
            'RqUID': str(uuid.uuid4()),
            'Authorization': f'Bearer {self.credentials}'
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=payload) as response:
                print(response)
                if response.status == 200:
                    data = await response.json()
                    return data.get('access_token')

    async def request_llm(self, user_quest: str) -> str:
        """Асинхронный метод для отправки запроса к LLM"""
        url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

        payload = json.dumps(
            {
                'model': self.model,
                'stream': False,
                'update_interval': 0,
                'messages': user_quest,
                'repetition_penalty': 1
            }
        )
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.token_access}'
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=payload) as response:
                print('Ответ чистый от AI: ', response)
                if response.status == 200:
                    response_json = await response.json()
                    print(response_json, 'Тип ответа от AI: ', type(response_json))
                    return response_json['choices'][0]['message']['content']


if __name__ == '__main__':
    from config_data.config import API_GIGACHAT
    from api_methods.dialog import CreateQuestForLMM
    #
    # async def main():
    #     gig = GigaClient(credentials=API_GIGACHAT)
    #     await gig.initialize()
    #     quest_for_llm = CreateQuestForLMM(query_user='Какие есть проекты для промышленной безопасности?')
    #     quest = quest_for_llm.build_query()
    #     response = await gig.request_llm(user_quest=quest)
    #     pprint(response)
    #
    # asyncio.run(main())

    async def main():
        gig = GigaClient(credentials=API_GIGACHAT)
        await gig.initialize()
        content = [
            {
                'role': 'user',
                'content': f'Расскажи о себе'
            }
        ]
        response = await gig.request_llm(user_quest=content)
        print(f'Итоговый ответ API:\n{response}')

    asyncio.run(main())