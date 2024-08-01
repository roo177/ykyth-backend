import pandas as pd
from django.core.management.base import BaseCommand, CommandError
from libraries.models import R1Code, R2Code  # Adjust as per your actual models
from django.db import transaction

class Command(BaseCommand):
    help = 'Import L2 Code from an Excel file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the Excel file')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']

        try:
            # Create a dictionary of L1 Codes for lookup
            r1_code_dict = {r1_code.r1_code: str(r1_code.id) for r1_code in R1Code.objects.all()}
            # print(r1_code_dict)
            # Read the Excel file using pandas
            df = pd.read_excel(file_path, sheet_name='R2', dtype={'R1_Code': str, 'R2_Code': str, 'Description': str})
            required_columns = {'R1 Code', 'R2 Code', 'Description'}
            file_columns = set(df.columns)
            
            if not required_columns.issubset(file_columns):
                raise CommandError(f'Excel file must contain columns: {required_columns}. Found columns: {file_columns}')

            with transaction.atomic():  # Ensure atomic transaction
                R2Code.objects.all().delete()  # Clear existing data

                for index, row in df.iterrows():
                    # print(row)
                    r1_code = str(row['R1 Code']).upper()
                    r2_code_code = str(row['R2 Code']).upper()
                    r2_code_description = row['Description'].upper()
                    created_by_id = '12f4aa11-b6fc-482f-894d-0962ad5f4313'

                    r1_code_id = r1_code_dict.get(r1_code)

                    if r1_code_id:
                        # Create the R2Code instance
                        R2Code.objects.create(
                            r1_code_id=r1_code_id,
                            r2_code=r2_code_code,
                            description=r2_code_description,
                            created_by_id=created_by_id,
                            updated_by_id=created_by_id
                        )
                    else:
                        raise CommandError(f'R1 Code {r1_code} not found.')

                self.stdout.write(self.style.SUCCESS('Data imported successfully'))
        except FileNotFoundError:
            raise CommandError(f'File not found at {file_path}')
        except Exception as e:
            raise CommandError(f'Error: {str(e)}')
