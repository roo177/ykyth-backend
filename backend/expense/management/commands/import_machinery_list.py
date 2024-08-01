import pandas as pd
from django.core.management.base import BaseCommand, CommandError
from libraries.models import R4Code, L4Code  # Adjust as per your actual models
from django.db import transaction
from datetime import datetime 
from constants.models import RepMonth
from expense.models import MachineryList


class Command(BaseCommand):
    help = 'Import R4 Code from an Excel file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the Excel file')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']

        try:
            df = pd.read_excel(file_path, sheet_name='MAK-List')

            file_columns = set(df.columns)

            rep_month_dict = {rep_month.rep_month: rep_month.id for rep_month in RepMonth.objects.all()}
            r4_code_dict = {
                f"{r4_code.code_comb}".strip(): str(r4_code.id)
                for r4_code in R4Code.objects.all()
                if r4_code.code_comb and r4_code.id is not None
            }
            # df.columns = df.iloc[0]  # Set headers from the first row

            machine_list = []

            for _, row in df.iterrows():
                r4_code_value = str(row['R4 Code']).strip()
                r4_code_id = r4_code_dict.get(r4_code_value)

                machine_r4_code_id = None

                rep_month_id = rep_month_dict.get(str(row['Rep Month']))


                if rep_month_id and r4_code_id and row['Quantity'] != 0 and not pd.isnull(row['Quantity']):
                    machine_list.append(
                        MachineryList(
                            rep_month_id=rep_month_id,
                            r4_code_id=r4_code_id,
                            machine_qty=row['Quantity']
                        )
                    )


            with transaction.atomic():
                # Delete existing records for the given rep_month_id (if needed)
                if machine_list:
                    MachineryList.objects.filter(rep_month_id=rep_month_id).delete()
                    MachineryList.objects.bulk_create(machine_list)
                    
                    self.stdout.write(self.style.SUCCESS('R4 Codes imported successfully'))

        except FileNotFoundError:
            raise CommandError(f'File not found at {file_path}')
        except Exception as e:
            raise CommandError(f'Error: {str(e)}')
