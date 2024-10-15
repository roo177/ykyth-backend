from django.core.management.base import BaseCommand
from indexes.models import ActualIndexes
from constants.models import RepMonth
import pandas as pd
from indexes.models import IndexIncRates

class Command(BaseCommand):
    help = 'Import data from a .txt file into ActualIndexes model'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='The path to the .txt file to be imported')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']

        # Read data from Excel file
        df = pd.read_excel(file_path, engine='openpyxl')

        for index, row in df.iterrows():
            # Convert 'ac_month' to a datetime object if needed
            ac_month = pd.to_datetime(row['ac_month'], errors='coerce')

            # Assuming rep_month needs to be unique or specific identifier
            try:
                rep_month = RepMonth.objects.get(rep_month='2409')
            except RepMonth.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'RepMonth with rep_month "2409" does not exist.'))
                continue

            # Create or update the IndexIncRates entry
            IndexIncRates.objects.update_or_create(
                rep_month=rep_month,
                ac_month=ac_month,
                defaults={
                    'art_tufe': row['art_TUFE'] if pd.notna(row['art_TUFE']) else None,
                    'art_ufe': row['art_UFE'] if pd.notna(row['art_UFE']) else None,
                    'art_eur_try': row['art_EUR'] if pd.notna(row['art_EUR']) else None,
                    'art_usd_try': row['art_USD'] if pd.notna(row['art_USD']) else None,
                    'created_by_id': '12f4aa11-b6fc-482f-894d-0962ad5f4313'
                }
            )


        self.stdout.write(self.style.SUCCESS('Successfully imported data from Excel file.'))
