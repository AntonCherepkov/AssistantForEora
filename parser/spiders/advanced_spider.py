from typing import Iterable
import scrapy
from scrapy import Request
from ..items import ParserItem
import os
import re


try:
    path_file = os.path.abspath('urls.txt')
    if not os.path.exists(path_file):
        raise FileNotFoundError('Файл urls.txt не найден!')
except FileNotFoundError as e:
    print(f'Error: {e}')


class AdvancedSpider(scrapy.Spider):
    name = "advanced"

    def start_requests(self) -> Iterable[Request]:
        self.id_project = 1

        with open(path_file, 'r', encoding='utf-8') as f:
            urls = [line.strip() for line in f.readlines()]

        for url in urls:
            try:
                print(url)
                yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)
            except Exception as e:
                print(f"Ошибка при обработке URL: {url} - {e}")

    def parse(self, response, *args, **kwargs):
        """Метод для обработки данных"""
        if response.status != 200:
            self.logger.error(f"Ошибка: сервер вернул код {response.status} для {response.url}")
            return

        project_data = {
            'id': self.id_project,
            'title': response.css('title::text').get(),
            'description': response.css('meta[name="description"]::attr(content)').get(),
            'links': response.url
        }

        self.id_project += 1

        key = self.generate_key(response.url)
        if key:
            yield {key: project_data}

    def generate_key(self, url):
        """Генерируем ключ для каждого URL, на основе его уникальной части"""
        match = re.search(r'/cases/([a-z0-9-/]+)', url)
        if match:
            return match.group(1)
        return 'default-key'
