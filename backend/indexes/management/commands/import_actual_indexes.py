import csv
from django.core.management.base import BaseCommand
from indexes.models import ActualIndexes
from constants.models import RepMonth
from datetime import datetime
import pandas as pd

class Command(BaseCommand):
    help = 'Import data from a .txt file into ActualIndexes model'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='The path to the .txt file to be imported')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']
        # py manage.py import_actual_indexes backend\indexes\management\commands\actual_indexes.txt

        df = pd.read_csv(file_path, delimiter=';', encoding='utf-8')


                # Define a function to convert Excel date serial number to datetime
        def excel_date_to_datetime(excel_date, date_system='1900'):
            if date_system == '1900':
                return pd.to_datetime('1899-12-30') + pd.to_timedelta(excel_date, 'D')
            elif date_system == '1904':
                return pd.to_datetime('1904-01-01') + pd.to_timedelta(excel_date, 'D')
            else:
                raise ValueError("Unsupported date system. Use '1900' or '1904'.")
            
        df['ac_month'] = df['ac_month'].apply(lambda x: excel_date_to_datetime(x) if isinstance(x, (int, float)) else x)

        for index, row in df.iterrows():
            
            ActualIndexes.objects.update_or_create(
                ac_month=pd.to_datetime(row['ac_month']).date(),
                defaults = {
                    'b01_tufe': row['b01_tufe'] if pd.notna(row['b01_tufe']) else None,
                    'b02_mineral': row['b02_mineral'] if pd.notna(row['b02_mineral']) else None,
                    'b03_main_metal': row['b03_main_metal'] if pd.notna(row['b03_main_metal']) else None,
                    'b04_other_metal': row['b04_other_metal'] if pd.notna(row['b04_other_metal']) else None,
                    'b05_petrol': row['b05_petrol'] if pd.notna(row['b05_petrol']) else None,
                    'b06_wood': row['b06_wood'] if pd.notna(row['b06_wood']) else None,
                    'b07_electricity': row['b07_electricity'] if pd.notna(row['b07_electricity']) else None,
                    'b08_computer': row['b08_computer'] if pd.notna(row['b08_computer']) else None,
                    'b09_ufe': row['b09_ufe'] if pd.notna(row['b09_ufe']) else None,
                    'b10_machinery': row['b10_machinery'] if pd.notna(row['b10_machinery']) else None,
                    'r_usd_try': row['r_usd_try'] if pd.notna(row['r_usd_try']) else None,
                    'r_eur_try': row['r_eur_try'] if pd.notna(row['r_eur_try']) else None,
                }
            )

        self.stdout.write(self.style.SUCCESS('Successfully imported data from {}'.format(file_path)))
