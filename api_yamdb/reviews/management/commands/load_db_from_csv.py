from django.core.management.base import BaseCommand, CommandError
# from polls.models import Question as Poll


class Command(BaseCommand):
    help = 'Загрузка тестовых данных из csv'

    def add_arguments(self, parser):
        parser.add_argument('path_to_csv', nargs='+', type=str)

    def handle(self, *args, **options):

        try:
            print(options)
        except Exception:
            raise CommandError('Ошибка загрузки данных')
