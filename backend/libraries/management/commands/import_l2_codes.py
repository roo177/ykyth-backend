import csv
from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from libraries.models import L1Code, L2Code  # Adjust as per your actual models
from django.db import transaction

class Command(BaseCommand):
    help = 'Import L2 Code from a text file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the data file')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']

        try:
            # Create a dictionary of L1 Codes for lookup
            l1_code_dict = {l1_code.l1_code: str(l1_code.id) for l1_code in L1Code.objects.all()}

            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.reader(file, delimiter=',')

                k = 1

                with transaction.atomic():  # Ensure atomic transaction
                    for line in reader:
                        fields = line
                        l1_code_id = l1_code_dict.get(fields[0].upper())
                        l2_code_code = fields[1].upper()
                        l2_code_description = fields[2].upper()
                        created_by_id = 'ee26630b-fd60-42ee-ad4a-190ef566e493'

                        if l1_code_id:
                            # Create the L2Code instance
                            L2Code.objects.create(
                                l1_code_id=l1_code_id,
                                l2_code=l2_code_code,
                                description=l2_code_description,
                                created_by_id=created_by_id,
                                updated_by_id=created_by_id
                            )
                        else:
                            raise CommandError(f'L1 Code {fields[0].upper()} not found.')

                        k += 1

                self.stdout.write(self.style.SUCCESS('Data imported successfully'))
        except FileNotFoundError:
            raise CommandError(f'File not found at {file_path}')
        except Exception as e:
            raise CommandError(f'Error: {str(e)}')
