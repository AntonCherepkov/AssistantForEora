from data_proccessing.text_analizer import similarity_threshold
from errors.errors import ProjectSearchError
from typing import Dict, List


class CreateQuestForLMM:
    SYSTEM_MESSAGE = (
        "Ты - ассистент компании EORA. Твоя задача - предоставить краткую информацию по проектам компании, "
        "отвечать на вопросы пользователей о назначении, клиентах, и результатах проектов. "
        "Используй только предоставленные данные и формируй ответы коротко и по делу, добавляя ссылку на проект."
    )

    def __init__(self, query_user: str):
        self.query_user = query_user
        self.work_struct = self.get_work_struct(self.query_user)

    def build_query(self) -> List[Dict]:
        """Функция, формирующая итоговый запрос для Gigachat, с учетом """
        project_data = self.gen_project_data()

        return [
            {"role": "system", "content": self.SYSTEM_MESSAGE},
            {"role": "user", "content": f"Данные по проекту:\n{project_data}\nВопрос пользователя: {self.query_user}"}
        ]

    def get_work_struct(self, query_user: str) -> Dict[str,str]:
        """Функция для определения релевантных проектов, относительно вопроса пользователя"""
        relevant_projects = similarity_threshold(query=query_user)

        if relevant_projects is None:
            raise ProjectSearchError()
        else:
            return relevant_projects

    def gen_project_data(self):
        """Функция для генерации текста с информацией о проектах для LLM"""
        result = ''
        for project in self.work_struct.values():
            result = ' '.join(
                [
                    result,
                    f"ID проекта: {project['id']}. {project['description']}",
                    f"Тема проекта: {project['title']}.",
                    f"Ссылка проекта: {project['links']}"
                ]
            )
        return result


if __name__ == '__main__':
    # quest_1 = CreateQuestForLMM(query_user='Какие есть проекты для промышленной безопасности?')
    # result_1 = quest_1.build_query()
    # print(result_1)

    # Некорректный вопрос
    quest_2 = CreateQuestForLMM(query_user='Назови проекты для детей')
    result_2 = quest_2.build_query()
    print(result_2)
