from gigachat import GigaChat
import requests
import uuid
from dialog import CreateQuestForLMM
from pprint import pprint
import json


class GigaClient:

    def __init__(
            self,
            credentials: str,
            scope: str = 'GIGACHAT_API_PERS',
            model: str = 'GigaChat'
    ) -> None:
        self.credentials=credentials,
        self.scope=scope,
        self.model=model
        self.token_access = self.request_key()

    def request_key(self) -> str:
        """Метод для POST запроса для получения токена доступа"""
        url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

        payload = {'scope': self.scope}
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json',
            'RqUID': str(uuid.uuid4()),
            'Authorization': f'Bearer {self.credentials[0]}'
        }
        response = requests.request("POST", url, headers=headers, data=payload)

        if response.status_code == 200:
            access_token = response.json().get('access_token')
            return access_token

    def request_llm(self, user_quest: str) -> str:
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
        response = requests.request("POST", url, headers=headers, data=payload)

        if response.status_code == 200:
            return json.loads(response.text)['choices'][0]['message']['content']


if __name__ == '__main__':
    from config_data.config import API_GIGACHAT

    gig = GigaClient(credentials=API_GIGACHAT)
    quest_for_llm = CreateQuestForLMM(query_user='Какие есть проекты для промышленной безопасности?')
    quest = quest_for_llm.build_query()

    response = gig.request_llm(user_quest=quest)
    print(f'Ответ LLM: {response}')
