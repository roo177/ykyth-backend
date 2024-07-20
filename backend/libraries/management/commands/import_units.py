import csv
from django.core.management.base import BaseCommand, CommandError
from constants.models import Unit
from django.db import transaction

class Command(BaseCommand):
    help = 'Import Units from a text file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the data file')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                data_to_import = []

                with transaction.atomic():  # Ensure atomic transaction
                    for line in reader:
                        
                        fields = line
                        
                        unit = fields[0] if fields[0] else None
                        description = fields[1].upper()
                        created_by_id = 'ee26630b-fd60-42ee-ad4a-190ef566e493'
                        print(unit, description, created_by_id)
                        if description:
                            data_to_import.append([unit, description, created_by_id])

                    if data_to_import:
                        created_data = [
                            Unit(
                                unit=row[0],
                                description=row[1],
                                created_by_id=row[2],
                                updated_by_id=row[2]
                            )
                            for row in data_to_import
                        ]
                        Unit.objects.bulk_create(created_data)
                    else:
                        raise CommandError('No data to import.')

                self.stdout.write(self.style.SUCCESS('Data imported successfully'))
        except FileNotFoundError:
            raise CommandError(f'File not found at {file_path}')
        except Exception as e:
            raise CommandError(f'Error: {str(e)}')
