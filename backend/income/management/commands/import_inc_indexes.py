import pandas as pd
from django.core.management.base import BaseCommand, CommandError
from libraries.models import R4Code, Unit  # Adjust as per your actual models
from django.db import transaction
from datetime import datetime 
from constants.models import RepMonth
from income.models import IncomeIndexes
from libraries.models import L4Code
from libraries.models import ActivityTypeDetailIncome

class Command(BaseCommand):
    help = 'Import ındexes from an Excel file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the Excel file')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']

        try:
            df = pd.read_excel(file_path, sheet_name='inc_indexes', header=0)

            # Prepare data for bulk insertion
            income_records = []

            for _, row in df.iterrows():

                income_records.append(
                        IncomeIndexes(
                            inc_month=row['Month'],
                            inc_index=row['Index'],
                            ppr_no=row['PPR No.']
                        )
                    )

            print(len(income_records), 'records to be saved')
        # Save records to the database
            with transaction.atomic():
                # Delete existing records for the given rep_month_id (if needed)
                if income_records:
                    IncomeIndexes.objects.all().delete()
                    IncomeIndexes.objects.bulk_create(income_records)
                    
            self.stdout.write(self.style.SUCCESS('Indexes imported successfully'))

        except FileNotFoundError:
            raise CommandError(f'File not found at {file_path}')
        except Exception as e:
            raise CommandError(f'Error: {str(e)}')
