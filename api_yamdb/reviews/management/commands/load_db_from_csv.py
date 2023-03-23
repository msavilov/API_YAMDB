import csv
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from reviews.models import Category, Comment, Genre, Review, Title, User


class Command(BaseCommand):
    help = 'Загрузка тестовых данных из csv'

    def handle(self, *args, **options):
        data_folder = Path('../api_yamdb/static/data/')
        file_path = {
            str(p.name).rstrip('.csv'): p for p in data_folder.iterdir()
        }

        load_same_model = {
            'user': User,
            'category': Category,
            'genre': Genre,
        }

        load_model = {
            'title': self.load_titles,
            'genre_title': self.load_genre_title,
            'review': self.load_review,
            'comment': self.load_comment,
        }

        try:
            for name, model in load_same_model.items():
                self.load_data(file_path[name], model)
            for name, load_func in load_model.items():
                load_func(file_path[name])
            print('Данные успешно импортированы в БД')
        except Exception as r:
            raise CommandError('Ошибка загрузки данных', r)

    def load_data(self, path, model):
        with open(path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            temp_instances = []
            for row in reader:
                temp_instances.append(model(**row))
            model.objects.bulk_create(temp_instances)
        print(f'{model.__name__} загружен')

    def load_titles(self, path):
        with open(path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            temp_instances = []
            for row in reader:
                temp_instances.append(
                    Title(
                        id=row['id'],
                        name=row['name'],
                        year=row['year'],
                        category=Category.objects.get_or_create(
                            id=row['category'])[0],
                    )
                )
            Title.objects.bulk_create(temp_instances)
        print('Titles загружен')

    def load_review(self, path):
        with open(path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            temp_instances = []
            for row in reader:
                temp_instances.append(
                    Review(
                        id=row['id'],
                        title=Title.objects.get_or_create(
                            id=row['title_id'])[0],
                        text=row['text'],
                        author=User.objects.get_or_create(
                            id=row['author'])[0],
                        score=row['score'],
                        pub_date=row['pub_date'],
                    )
                )
            Review.objects.bulk_create(temp_instances)
        print('Review загружен')

    def load_genre_title(self, path):
        with open(path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                title, _ = Title.objects.get_or_create(
                    id=row['title_id']
                )
                genre, _ = Genre.objects.get_or_create(
                    id=row['genre_id']
                )
                title.genre.add(genre)
                title.save()
            print('genre_title загружен')

    def load_comment(self, path):
        with open(path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            temp_instances = []
            for row in reader:
                temp_instances.append(
                    Comment(
                        review=Review.objects.get_or_create(
                            id=row['review_id']
                        )[0],
                        text=row['text'],
                        author=User.objects.get_or_create(
                            id=row['author']
                        )[0],
                        pub_date=row['pub_date'],
                    )
                )
            Comment.objects.bulk_create(temp_instances)
        print('Comment загружен')
