import os
import csv
from django.core.management.base import BaseCommand
from django.apps import apps
from django.db import models


class Command(BaseCommand):
    """Команда для загрузки данных из CSV с гарантией порядка обработки."""

    help = 'Загружает данные из CSV файлов в строгом порядке'
    PROCESS_ORDER = [
        ('case.csv', 'case'),
        ('skin.csv', 'skin'),
        ('case_skin.csv', 'case_skins')
    ]

    def add_arguments(self, parser):
        """Добавляет аргументы для команды."""
        parser.add_argument(
            'csv_dir',
            type=str,
            help='Путь к папке с CSV файлами'
        )

    def handle(self, *args, **options):
        """Основной метод обработки команды."""
        csv_dir = options['csv_dir']

        if not os.path.isdir(csv_dir):
            self.stdout.write(
                self.style.ERROR(f'Директория {csv_dir} не существует')
            )
            return

        # Словарь для хранения созданных объектов
        created_objects = {}

        for filename, model_name in self.PROCESS_ORDER:
            self.process_single_file(
                csv_dir, filename, model_name, created_objects
            )

    def process_single_file(self, csv_dir, filename,
                            model_name, created_objects):
        """Обрабатывает один CSV файл."""
        file_path = os.path.join(csv_dir, filename)

        if not os.path.exists(file_path):
            self.stdout.write(
                self.style.WARNING(f'Файл {filename} не найден')
            )
            return

        try:
            model = apps.get_model('cases', model_name)
        except LookupError:
            self.stdout.write(
                self.style.WARNING(f'Модель {model_name} не найдена')
            )
            return

        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            success_count = 0
            error_count = 0

            for row in reader:
                success, error = self.process_single_row(
                    row, model, model_name, filename, reader, created_objects
                )
                success_count += success
                error_count += error

            self.stdout.write(
                self.style.SUCCESS(
                    f'{filename}: успешно {success_count}, '
                    f'ошибок {error_count}'
                )
            )

    def process_single_row(self, row, model, model_name,
                           filename, reader, created_objects):
        """Обрабатывает одну строку CSV файла."""
        try:
            # Подготавливаем данные для модели
            data = self.prepare_model_data(row, model)

            # Особый случай для промежуточной таблицы
            if model_name == 'case_skins':
                if not all(k in row for k in ['case_id', 'skin_id']):
                    raise ValueError(
                        "Отсутствуют обязательные поля title_id или genre_id"
                    )
                obj = model.objects.create(
                    title_id=int(row['case_id']),
                    genre_id=int(row['skin_id'])
                )
            else:
                obj = model.objects.create(**data)

            # Сохраняем созданный объект
            if model_name not in created_objects:
                created_objects[model_name] = []
            created_objects[model_name].append(obj.id)

            return 1, 0
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(
                    f'Ошибка в {filename}, строка {reader.line_num}: {str(e)}'
                )
            )
            return 0, 1

    def prepare_model_data(self, row, model):
        """Подготавливает данные строки для создания модели."""
        data = {}

        for field in model._meta.get_fields():
            if field.name not in row:
                continue

            # Обработка ForeignKey полей
            if isinstance(field, models.ForeignKey):
                fk_value = row[field.name]
                if not fk_value:
                    raise ValueError(
                        f'Пустое значение для обязательного поля {field.name}'
                    )

                # Проверяем, что значение можно преобразовать в число
                try:
                    fk_id = int(fk_value)
                except ValueError:
                    raise ValueError(
                        f'Некорректный ID для поля {field.name}: {fk_value}'
                    )

                data[f'{field.name}_id'] = fk_id

            # Обработка обычных полей
            else:
                data[field.name] = row[field.name]

        return data
