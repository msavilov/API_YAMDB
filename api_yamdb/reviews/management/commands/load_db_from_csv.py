import csv
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from reviews.models import Category, Comment, Genre, Review, Titles, User


class Command(BaseCommand):
    help = 'Загрузка тестовых данных из csv'

    def handle(self, *args, **options):
        data_folder = Path('../api_yamdb/static/data/')
        file_path = {
            str(p.name).rstrip('.csv'): p for p in data_folder.iterdir()
        }
        print(file_path)
        load_model = {
            'user': self.load_user,
            'category': self.load_category,
            'genre': self.load_genre,
            'title': self.load_titles,
            'genre_title': self.load_genre_title,
            'review': self.load_review,
            'comment': self.load_comment,
        }

        try:
            for name, load_func in load_model.items():
                load_func(file_path[name])
            print('Данные успешно импортированы в БД')
        except Exception as r:
            raise CommandError('Ошибка загрузки данных', r)

    def load_user(self, path):
        with open(path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            temp_instances = []
            for row in reader:
                temp_instances.append(User(**row))
            User.objects.bulk_create(temp_instances)
        print('User загружен')

    def load_category(self, path):
        with open(path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            temp_instances = []
            for row in reader:
                temp_instances.append(Category(**row))
            Category.objects.bulk_create(temp_instances)
        print('Category загружен')

    def load_genre(self, path):
        with open(path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            temp_instances = []
            for row in reader:
                temp_instances.append(Genre(**row))
            Genre.objects.bulk_create(temp_instances)
        print('Genre загружен')

    def load_titles(self, path):
        with open(path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            temp_instances = []
            for row in reader:
                temp_instances.append(
                    Titles(
                        id=row['id'],
                        name=row['name'],
                        year=row['year'],
                        category=Category.objects.get_or_create(
                            id=row['category'])[0],
                    )
                )
            Titles.objects.bulk_create(temp_instances)
        print('Titles загружен')

    def load_review(self, path):
        with open(path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            temp_instances = []
            for row in reader:
                temp_instances.append(
                    Review(
                        id=row['id'],
                        title=Titles.objects.get_or_create(
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
                title, _ = Titles.objects.get_or_create(
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
