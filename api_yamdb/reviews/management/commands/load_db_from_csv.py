import csv

from django.core.management.base import BaseCommand, CommandError
from reviews.models import (
    Category,
    Comment,
    Genre,
    GenreTitle,
    Review,
    Title,
    User
)


class Command(BaseCommand):
    help = "Загрузка тестовых данных из csv"

    def add_arguments(self, parser):
        parser.add_argument("path_to_csv", nargs="+", type=str)

    def handle(self, *args, **options):
        try:
            
            self.load_categories()
        except Exception:
            raise CommandError("Ошибка загрузки данных")

    def load_categories(self):
        with open('/run/media/greger/Disk_E/GRENOW/Dev/sprints/api_yamdb/api_yamdb/static/data/category.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            categories = []
            for row in reader:
                print(row)
                categories.append(
                    Category(
                        name=row['name'],
                        slug=row['slug']
                    )
                )
            Category.objects.bulk_create(categories)
