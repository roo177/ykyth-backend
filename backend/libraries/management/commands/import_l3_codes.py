import csv
from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from libraries.models import L2Code, L3Code  # Adjust as per your actual models
from django.db import transaction

class Command(BaseCommand):
    help = 'Import L2 Code from a text file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the data file')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']

        try:
            # Create a dictionary of L1 Codes for lookup
            l2_code_dict = {l2_code.l2_code + "-" + l2_code.l1_code.l1_code: str(l2_code.id) for l2_code in L2Code.objects.all()}

            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.reader(file, delimiter=';')

                with transaction.atomic():  # Ensure atomic transaction

                    for line in reader:
                        fields = line
                        
                        l2_code_id = l2_code_dict.get(fields[0]+"-"+fields[3].upper())
                        l3_code_code = fields[1].upper()
                        l3_code_description = fields[2].upper()
                        created_by_id = 'ee26630b-fd60-42ee-ad4a-190ef566e493'

                        if l2_code_id:
                            # Create the L2Code instance
                            L3Code.objects.create(
                                l2_code_id=l2_code_id,
                                l3_code=l3_code_code,
                                description=l3_code_description,
                                created_by_id=created_by_id,
                                updated_by_id=created_by_id
                            )
                        else:
                            raise CommandError(f'L2-L1 Code {fields[0]+"-"+fields[3].upper()} not found.')


            self.stdout.write(self.style.SUCCESS('Data imported successfully'))

        except FileNotFoundError:
            raise CommandError(f'File not found at {file_path}')
        except Exception as e:
            raise CommandError(f'Error: {str(e)}')
