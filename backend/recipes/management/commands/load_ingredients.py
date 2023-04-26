import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import IntegrityError

from recipes.models import Ingredient

path = os.path.join(settings.BASE_DIR, 'data')
print(path)


class Command(BaseCommand):
    help = 'Импорт ингридиентов из csv файла в базу данных'

    def handle(self, *args, **options):
        add_count = 0
        error_count = 0
        for row in csv.DictReader(open(f'{path}/ingredients.csv')):
            try:
                obj, created = Ingredient.objects.get_or_create(
                    name=row['name'],
                    measurement_unit=row['measurement_unit']
                )
                if created:
                    add_count += 1

            except IntegrityError as e:
                self.stderr.write(
                    f'Ошибка при импорте строки "{row}": {e}')
                error_count += 1

        self.stdout.write(self.style.SUCCESS(
            f'Загружено в базу {add_count} объектов\n'
            f'Обнаружено {error_count} ошибок'
        ))
