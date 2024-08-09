import pandas as pd
from django.core.management.base import BaseCommand, CommandError
from libraries.models import R4Code, Unit  # Adjust as per your actual models
from django.db import transaction
from datetime import datetime 
from constants.models import RepMonth
from income.models import IncomeQuantity
from libraries.models import L4Code
from libraries.models import ActivityTypeDetailIncome

class Command(BaseCommand):
    help = 'Import R4 Code from an Excel file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the Excel file')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']

        try:
            df = pd.read_excel(file_path, sheet_name='t_Aylik_Mkt_Gelir')

            # Create mappings for foreign key fields
            rep_month_dict = {rep_month.rep_month: rep_month.id for rep_month in RepMonth.objects.all()}
            l4_code_dict = {
                f"{l4_code.aygm_code}-{l4_code.activity_type.description}": l4_code.id 
                for l4_code in L4Code.objects.filter(aygm_code__isnull=False)
            }
            activity_detail_dict = {
                f"{activity_detail.description}": activity_detail.id 
                for activity_detail in ActivityTypeDetailIncome.objects.all()
            }
            # Load data into DataFrame
        # Ensure df_data is a DataFrame
            # df.columns = df.iloc[0]  # Set headers from the first row
            # df = df[1:]  # Skip the header row

            # Unpivot DataFrame
            df_melted = pd.melt(df, id_vars=['rep_month', 'aygm_poz', 'tip', 'detay'], 
                                var_name='month', value_name='qty')
            
            # Convert 'month' to datetime and handle 'qty'
            df_melted['month'] = pd.to_datetime(df_melted['month'], format='%Y-%m-%d %H:%M:%S').dt.date
            df_melted['qty'] = pd.to_numeric(df_melted['qty'], errors='coerce')
            df_melted.dropna(subset=['qty'], inplace=True)
            # Prepare data for bulk insertion
            income_records = []
            for _, row in df_melted.iterrows():
                rep_month_id = rep_month_dict.get(str(row['rep_month']))
                l4_code_id = l4_code_dict.get(f"{str(row['aygm_poz'])}-{str(row['tip'])}")
                activity_detail_id = activity_detail_dict.get(str(row['detay']))
                if row['qty'] == 'nan' or row['qty'] == 'NaN' or row['qty'] == 0:
                    continue
                
                
                if rep_month_id and l4_code_id and row['qty'] != 0 and not pd.isnull(row['qty']):
                    # print("Appending new record", row['qty'])

                    income_records.append(
                        IncomeQuantity(
                            rep_month_id=rep_month_id,
                            l4_code_id=l4_code_id,
                            activity_detail_id=activity_detail_id,
                            inc_month=row['month'],
                            inc_qty=row['qty']
                        )
                    )

        # Save records to the database
            with transaction.atomic():
                # Delete existing records for the given rep_month_id (if needed)
                if income_records:
                    IncomeQuantity.objects.filter(rep_month_id=rep_month_id).delete()
                    IncomeQuantity.objects.bulk_create(income_records)
                    
            self.stdout.write(self.style.SUCCESS('R4 Codes imported successfully'))

        except FileNotFoundError:
            raise CommandError(f'File not found at {file_path}')
        except Exception as e:
            raise CommandError(f'Error: {str(e)}')
