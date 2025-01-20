# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface


class ParserPipeline:
    def process_item(self, item, spider):
        return item


class CustomJsonPipeline:
    """Класс, определяющий порядок сохранения информации во внешний json файл"""
    def open_spider(self, spider):
        """Данные, которые были запрошены для каждого из URL, будут храниться в списке"""
        self.data = []


    def close_spider(self, spider):
        """При завершении опроса всех URL, 'сваливаем' все данные в JSON файл для дальнейшей обработки"""
        combined_data = {}
        for item in self.data:
            for key, value in item.items():
                if value is not None:
                    combined_data[key] = value

        with open('result.json', 'w', encoding='utf-8') as f:
            import json
            json.dump(combined_data, f, ensure_ascii=False, indent=4)


    def process_item(self, item, spider):
        """В процессе получения данных от сервиса проверяем на валидность (не пустые) и добавляем в список"""
        item_dict = dict(item)
        cleaned_item = {k: v for k, v in item_dict.items() if v is not None}

        if cleaned_item:
            self.data.append(item_dict)
        return item
