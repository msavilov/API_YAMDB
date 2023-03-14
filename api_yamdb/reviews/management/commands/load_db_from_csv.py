import csv
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from reviews.models import (
    Category,
    Comment,
    Genre,
    Genre_Title,
    Review,
    Titles,
    User
)


class Command(BaseCommand):
    help = "Загрузка тестовых данных из csv"

    def handle(self, *args, **options):

        data_folder = Path('../api_yamdb/static/data/')
        models = [
            User,
            Genre,
            Titles,
            Category,
            Review,
            Genre_Title,
            Comment,
            
        ]

        print('files')
        for x in data_folder.iterdir():
            print(x)
            
        print(models)

        try:
            for model in models:
                # if model != User:
                name_model = model.objects.model._meta.db_table.lstrip('reviews_')
                # else:
                    # name_model = model.objects.model._meta.db_table.lstrip('auth_')
                print(name_model, 'Имя модели')
                for path in data_folder.iterdir():
                    print(path, 'путь')
                    # print(str(path.name).rstrip('.csv'))
                    print(str(path.name).rstrip('.csv'), name_model, ' сравнения имен1')
                    if name_model == str(path.name).rstrip('.csv'):
                        # print(str(path.name).rstrip('.csv'), name_model, ' сравнения имен')
                        self.load_categories(path, model)
                        print('puc')
        except Exception as r:
            print(r)
            raise CommandError("Ошибка загрузки данных")

    def load_categories(self, path, model):
        with open(path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            categories = []
            for row in reader:
                print(row, 'row')
                categories.append(
                    model(**row)
                )
            print('ok')
            model.objects.bulk_create(categories)
