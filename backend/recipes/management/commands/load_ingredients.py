# isort:skip
import json

from django.core.management.base import BaseCommand
from django.db import transaction
from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Загрузка ингредиентов из файла JSON'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Путь к файлу JSON')

    @transaction.atomic
    def handle(self, *args, **options):
        file_path = options['file_path']
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            for item in data:
                ingredient = Ingredient(
                    name=item['name'],
                    measurement_unit=item['measurement_unit']
                )
                ingredient.save()
        self.stdout.write(self.style.SUCCESS('Ингредиенты успешно загружены'))
