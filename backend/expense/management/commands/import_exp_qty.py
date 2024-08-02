import pandas as pd
from django.core.management.base import BaseCommand, CommandError
from libraries.models import R4Code, Unit  # Adjust as per your actual models
from django.db import transaction
from datetime import datetime 
from constants.models import RepMonth
from expense.models import ExpenseQuantity
from libraries.models import L4Code

class Command(BaseCommand):
    help = 'Import R4 Code from an Excel file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the Excel file')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']

        try:
            df = pd.read_excel(file_path, sheet_name='t_Aylik_Mkt_Gider')

            file_columns = set(df.columns)

            rep_month_dict = {rep_month.rep_month: rep_month.id for rep_month in RepMonth.objects.all()}
            l4_code_dict = {
                f"{l4_code.code_comb}".strip(): str(l4_code.id)
                for l4_code in L4Code.objects.filter(aygm_code__isnull=True)
                if l4_code.code_comb and l4_code.id is not None
            }

            df_melted = pd.melt(df, id_vars=['Rep Month', 'L4 Code'], 
                                var_name='month', value_name='qty')
            df.columns = df.iloc[0]  # Set headers from the first row
            # df = df[1:]  # Skip the header row

            # Unpivot DataFrame

            # Convert 'month' to datetime and handle 'qty'
            df_melted['month'] = pd.to_datetime(df_melted['month'], format='%Y-%m-%d %H:%M:%S').dt.date
            df_melted['qty'] = pd.to_numeric(df_melted['qty'], errors='coerce')
            df_melted.dropna(subset=['qty'], inplace=True)
            # Prepare data for bulk insertion
            expense_records = []
            df_melted['L4 Code'] = df_melted['L4 Code'].astype(str)

            for _, row in df_melted.iterrows():
                l4_code_value = str(row['L4 Code']).strip() 
                l4_code_id = l4_code_dict.get(l4_code_value)
                rep_month_id = rep_month_dict.get(str(row['Rep Month']))

                # Print for debugging
                # print(f"Rep Month ID: {rep_month_id}, L4 Code ID: {l4_code_id}, Quantity: {row['qty']}")
                if row['qty'] == 'nan' or row['qty'] == 'NaN' or row['qty'] == 0:
                    continue
                if rep_month_id and l4_code_id and row['qty'] != 0 and not pd.isnull(row['qty']):
                    expense_records.append(
                        ExpenseQuantity(
                            rep_month_id=rep_month_id,
                            l4_code_id=l4_code_id,
                            exp_month=row['month'],
                            exp_qty=row['qty']
                        )
                    )


            with transaction.atomic():
                # Delete existing records for the given rep_month_id (if needed)
                if expense_records:
                    ExpenseQuantity.objects.filter(rep_month_id=rep_month_id).delete()
                    ExpenseQuantity.objects.bulk_create(expense_records)
                    
                    self.stdout.write(self.style.SUCCESS('R4 Codes imported successfully'))

        except FileNotFoundError:
            raise CommandError(f'File not found at {file_path}')
        except Exception as e:
            raise CommandError(f'Error: {str(e)}')
