from django.core.management.base import BaseCommand

from ._csv_tools import import_from_csv


class Command(BaseCommand):
    """Костыль импорта csv файлов.

    Использование:
    manage.py -p|--path <путь> путь относительно settings.BASE_DIR
    Проверок очень мало, кое-что работает.
    На неверное имя файла падает.
    Важна последовательность заполнения БД. Связанные поля после того,
    как есть объекты, куда им ссылаться.
    # TODO очень много всего.
    """
    help = (
        'Импорт .csv файла(ов) в БД.\n'
        'Использование: -p | --path <путь>'
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '-p',
            '--path',
            action='store',
            default=False,
            help='относительный путь к csv'
        )

    def handle(self, *args, **options):
        # берём аргументы
        path = None
        if options['path']:
            path = options['path']
            self.stdout.write(f'Указан путь до csv: {path}')
        else:
            self.stdout.write('Путь до csv не задан')

        # делаем работу
        import_from_csv(path)
