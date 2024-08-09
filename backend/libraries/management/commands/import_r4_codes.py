import pandas as pd
from django.core.management.base import BaseCommand, CommandError
from libraries.models import R2Code, R3Code, R4Code, Unit  # Adjust as per your actual models
from django.db import transaction

class Command(BaseCommand):
    help = 'Import R4 Code from an Excel file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the Excel file')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']

        try:
            # Create a dictionary of R3 Codes for lookup
            r3_code_dict = {r3_code.r2_code.r1_code.r1_code + "-" + r3_code.r2_code.r2_code + "-" + r3_code.r3_code: r3_code for r3_code in R3Code.objects.all()}
            #unit_dict = {str(unit.unit).upper(): unit for unit in Unit.objects.all()}  # Adjust 'name' to your Unit model's unique field
            r4_code_dict = {r4_code.r3_code.r2_code.r1_code.r1_code + "-" + r4_code.r3_code.r2_code.r2_code + "-" + r4_code.r3_code.r3_code + "-" + r4_code.r4_code: r4_code for r4_code in R4Code.objects.all()}
            # Read the Excel file using pandas
            df = pd.read_excel(file_path, sheet_name='R4', dtype={'R1 Code': str, 'R2 Code': str, 'R3 Code': str, 'R4 Code': str, 'Description': str, 'Machine ID': str})
            required_columns = {'R1 Code', 'R2 Code', 'R3 Code', 'R4 Code', 'Description','Machine ID'}
            file_columns = set(df.columns)

            if not required_columns.issubset(file_columns):
                raise CommandError(f'Excel file must contain columns: {required_columns}. Found columns: {file_columns}')

            with transaction.atomic():  # Ensure atomic transaction



                for index, row in df.iterrows():
                    r1_code = str(row['R1 Code']).upper()
                    r2_code_code = str(row['R2 Code']).upper()
                    r3_code_code = str(row['R3 Code']).upper()
                    r4_code_code = str(row['R4 Code']).upper()
                    machine_id = str(row['Machine ID']).upper() if pd.notna(row['Machine ID']) else None

                    
                    try:
                        r4code_update = r4_code_dict.get(r1_code + "-" + r2_code_code + "-" + r3_code_code + "-" + r4_code_code)
                        update_obj = R4Code.objects.get(id=r4code_update.id)
                        update_obj.description = str(row['Description']).upper()
                        update_obj.machine_id = str(row['Machine ID']).upper() if pd.notna(row['Machine ID']) else None
                        update_obj.save()
                    except:

                        description = str(row['Description']).upper()
                        machine_id = str(row['Machine ID']).upper() if pd.notna(row['Machine ID']) else None
                        #unit_name = row['Unit'].upper()
                        #currency = row['Currency'].upper() if pd.notna(row['Currency']) else None
                    # origin = row['Origin'].upper() if pd.notna(row['Origin']) else None
                        #fin_type = row['Fin Type'].upper() if pd.notna(row['Fin Type']) else None
                        #customs = bool(row['Customs'])
                        created_by_id = '12f4aa11-b6fc-482f-894d-0962ad5f4313'

                        r3_code_instance = r3_code_dict.get(r1_code + "-" + r2_code_code + "-" + r3_code_code)
                        #unit_instance = unit_dict.get(unit_name)

                        if r3_code_instance:
                            # Create the R4Code instance
                            R4Code.objects.create(
                                r3_code=r3_code_instance,
                                r4_code=r4_code_code,
                                description=description.lstrip().rstrip(),
                                machine_id=machine_id,
                                #unit=unit_instance,
                                #currency=currency,
                                #origin=origin,
                                #fin_type=fin_type,
                                #customs=customs,
                                created_by_id=created_by_id,
                                updated_by_id=created_by_id
                            )
                        else:
                            missing_code = r3_code_instance is None and f'R Code {r1_code + "-" + r2_code_code + "-" + r3_code_code}'
                            raise CommandError(f'{missing_code} not found.')

                self.stdout.write(self.style.SUCCESS('R4 Codes imported successfully'))
        except FileNotFoundError:
            raise CommandError(f'File not found at {file_path}')
        except Exception as e:
            raise CommandError(f'Error: {str(e)}')
