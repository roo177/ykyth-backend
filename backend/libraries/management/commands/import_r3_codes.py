import pandas as pd
from django.core.management.base import BaseCommand, CommandError
from libraries.models import R2Code, R3Code  # Adjust as per your actual models
from django.db import transaction

class Command(BaseCommand):
    help = 'Import R3 Code from an Excel file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the Excel file')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']

        try:
            # Create a dictionary of R2 Codes for lookup
            r2_code_dict = {r2_code.r1_code.r1_code + "-" + r2_code.r2_code: r2_code for r2_code in R2Code.objects.all()}
            r3_code_dict = {r3_code.r2_code.r1_code.r1_code + "-" + r3_code.r2_code.r2_code + "-" + r3_code.r3_code: r3_code for r3_code in R3Code.objects.all()}
            # Read the Excel file using pandas
            df = pd.read_excel(file_path, sheet_name='R3', dtype={'R1 Code':str,'R2_Code': str, 'R3_Code': str, 'Description': str})
            required_columns = {'R1 Code','R2 Code', 'R3 Code', 'Description'}
            file_columns = set(df.columns)
            
            if not required_columns.issubset(file_columns):
                raise CommandError(f'Excel file must contain columns: {required_columns}. Found columns: {file_columns}')

            with transaction.atomic():  # Ensure atomic transaction



                

                for index, row in df.iterrows():
                    r1_code = str(row['R1 Code']).upper()
                    r2_code_code = str(row['R2 Code']).upper()
                    r3_code_code = str(row['R3 Code']).upper()

                    try:
                        r3code_update = r3_code_dict.get(r1_code + "-" + r2_code_code + "-" + r3_code_code)
                        update_obj = R3Code.objects.get(id=r3code_update.id)
                        update_obj.description = str(row['Description']).upper()
                        update_obj.save()
                    except:


                        r3_code_description = row['Description'].upper()
                        created_by_id = '12f4aa11-b6fc-482f-894d-0962ad5f4313'

                        r2_code_instance = r2_code_dict.get(r1_code + "-" + r2_code_code)

                        if r2_code_instance:
                            # Create the R3Code instance
                            R3Code.objects.create(
                                r2_code=r2_code_instance,
                                r3_code=r3_code_code,
                                description=r3_code_description,
                                created_by_id=created_by_id,
                                updated_by_id=created_by_id
                            )
                        else:
                            raise CommandError(f'R2 Code {r2_code_code} not found.')

                self.stdout.write(self.style.SUCCESS('R3 Codes imported successfully'))
        except FileNotFoundError:
            raise CommandError(f'File not found at {file_path}')
        except Exception as e:
            raise CommandError(f'Error: {str(e)}')
