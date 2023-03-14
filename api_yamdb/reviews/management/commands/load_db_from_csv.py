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
        models = {
            User: 'raw_data',
            Genre: 'raw_data',
            Category: 'raw_data',
            Titles: 'titles',
            Review: 'review',
            Genre_Title: 'genre_title',
            Comment: 'comment',
        }

        file_path = [path for path in data_folder.iterdir()]
        
        try:
            for model, type_data in models.items():
                name_model = model.objects.model._meta.db_table.lstrip('reviews_')
                for path in file_path:
                    if name_model == str(path.name).rstrip('.csv'):
                        self.load_data(path, model, type_data)
                        print('puc')
        except Exception as r:
            print(r)
            raise CommandError("Ошибка загрузки данных")

    def load_data(self, path, model, type_data):
        with open(path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            temp_instances = []
            if type_data == 'raw_data':
                self.load_raw_data(model, reader, temp_instances)
            elif type_data == 'titles':
                print(model, reader, temp_instances)
                self.load_titles(model, reader, temp_instances)
            elif type_data == 'review':
                self.load_review(model, reader, temp_instances)
            elif type_data == 'genre_title':
                self.load_genre_title(model, reader, temp_instances)
            elif type_data == 'comment':
                self.load_comment(model, reader, temp_instances)

            if temp_instances:
                model.objects.bulk_create(temp_instances)

    def load_raw_data(self, model, reader, temp_instances):
        for row in reader:
            temp_instances.append(
                model(**row)
            )

    def load_titles(self, model, reader, temp_instances):
        Titles.objects.bulk_create(objs=[
            Titles(
                id=row['id'],
                name=row['name'],
                year=row['year'],
                category=Category.objects.get_or_create(
                    id=row['category']
                )[0],
            )
            for row in reader
        ])

    def load_review(self, model, reader, temp_instances):
        for row in reader:
            temp_instances.append(
                model(
                    id=row['id'],
                    title=Titles.objects.get_or_create(
                        id=row['title_id']
                    ),
                    text=row['text'],
                    author=User.objects.get_or_create(
                        id=row['author']
                    ),
                    score=row['score'],
                    pub_date=row['pub_date'],
                )
            )

    def load_genre_title(self, model, reader, temp_instances):
        for row in reader:
            title, created = Titles.objects.get_or_create(
                id=row['title_id']
            )
            genre, created = Genre.objects.get_or_create(
                id=row['genre_id']
            )
            title.genre.add(genre)
            title.save()

    def load_comment(self, model, reader, temp_instances):
        for row in reader:
            temp_instances.append(
                model(
                    review=Review.objects.get_or_create(
                        id=row['review_id']
                    ),
                    text=row['text'],
                    author=User.objects.get_or_create(
                        id=row['author']
                    ),
                    pub_date=row['pub_date']
                )
            )
