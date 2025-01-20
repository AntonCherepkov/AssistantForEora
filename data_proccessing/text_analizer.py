from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import json
import os

import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
russian_stopwords = stopwords.words('russian')


def similarity_threshold(query: str):
    """
    Анализирует схожесть между пользовательским запросом и описаниями проектов из JSON-файла,
    определяя проекты, которые соответствуют заданному порогу схожести.

    :param query: Поисковый запрос, введённый пользователем.
    :type query: str

    :return: dict или None
        Возвращает словарь с релевантными проектами (ключи — идентификаторы проектов, значения — данные о проектах),
        если они соответствуют порогу схожести. Если релевантных проектов нет, возвращает None.

    :raises FileNotFoundError: Если файл `result.json` не найден в родительской директории.

    Логика работы:
        1. Открывает и читает JSON-файл (`result.json`), содержащий данные о проектах.
        2. Объединяет поля `title` и `description` каждого проекта в одну строку для анализа.
        3. Использует `TfidfVectorizer` из `sklearn.feature_extraction.text` для вычисления представления TF-IDF
           для запроса и описаний проектов.
        4. Вычисляет косинусное сходство между запросом и каждым описанием проекта.
        5. Отбирает проекты, у которых оценка схожести превышает заданный порог (по умолчанию 0.08).
        6. Возвращает идентификаторы и описание релевантных проектов, если они найдены. В противном случае возвращает None.

    Зависимости:
        - `os`: Для работы с путями к файлам.
        - `json`: Для чтения данных из JSON-файла.
        - `sklearn.feature_extraction.text.TfidfVectorizer`: Для вычисления представления TF-IDF.
        - `sklearn.metrics.pairwise.cosine_similarity`: Для вычисления оценок схожести.
        - `pandas` (подключается как `pd`): Для работы с оценками схожести и фильтрации релевантных проектов.
        - `russian_stopwords`: Предопределённый список стоп-слов на русском языке (должен быть импортирован или определён отдельно).

    Примечания:
        - JSON-файл `result.json` должен быть структурирован в виде словаря, где каждый ключ — это ID проекта,
          а значение — это другой словарь с полями `title` и `description`.
        - Переменная `russian_stopwords` должна быть определена в другом месте кода и содержать список
          распространённых стоп-слов для русского языка.
        - Порог схожести сейчас установлен на уровне 0.05, но его можно изменить при необходимости.
        - Если `relevant_projects` оказывается пустым, функция возвращает None.
    """
    try:
        with open(os.path.join('..', 'result.json'), 'r', encoding='utf-8') as file:
            data = json.load(file)

        document = [
            f"{project['title']} {project['description']}"
            for project in data.values()
        ]

        vectorizer = TfidfVectorizer(stop_words=russian_stopwords)
        tfidf_matrix = vectorizer.fit_transform([query] + document)
        similarity_scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
        # print("Сходства с проектами:", similarity_scores)

        project_scores = pd.DataFrame({
            'id': list(data.keys()),
            'similarity': similarity_scores
        })

        threshold = 0.05

        relevant_projects_ids = project_scores[project_scores['similarity'] >= threshold]['id']
        relevant_projects = {project_id: data[project_id] for project_id in relevant_projects_ids}

        if relevant_projects == {}:
            return None
        return relevant_projects

    except FileNotFoundError as e:
        print(f'Error: {e}')
        return


if __name__ == '__main__':
    # Тесты вопросов для определения релевантности того или иного проекта к

    result_1 = similarity_threshold('Какие есть проекты для промышленной безопасности?')
    print(f'Релевантная структура: {result_1}')

    result_2 = similarity_threshold('Какие есть проекты для оценки игроков по очкам')
    print(f'Релевантная структура: {result_2}')

    result_3 = similarity_threshold('Есть приложения для ТВ-приставок и колонок')
    print(f'Релевантная структура: {result_3}')

