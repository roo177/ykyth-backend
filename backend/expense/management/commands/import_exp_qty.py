import pandas as pd
from django.core.management.base import BaseCommand, CommandError
from libraries.models import R4Code, Unit  # Adjust as per your actual models
from django.db import transaction
from datetime import datetime 
from constants.models import RepMonth
from expense.models import ExpenseQuantity
from libraries.models import L4Code, M2Code, T1Code

class Command(BaseCommand):
    help = 'Import R4 Code from an Excel file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the Excel file')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']

        try:
            df = pd.read_excel(file_path, sheet_name='Gider Miktar', usecols=lambda col: col not in ['Sözleşme Miktar', 'Kalan Miktar', 'Toplam Miktar', 'Kalan Dağılan Fark','L4 Desc','M2 Desc','T1 Desc','KIRMATAŞ','SU TEMİNİ','TAŞ','BAĞLANTI'])

            file_columns = set(df.columns)  

            rep_month_dict = {rep_month.rep_month: rep_month.id for rep_month in RepMonth.objects.all()}

            l4_code_dict = {
                f"{l4_code.code_comb}".strip(): str(l4_code.id)
                for l4_code in L4Code.objects.filter(aygm_code__isnull=True)
                if l4_code.code_comb and l4_code.id is not None
            }
            m2_code_dict = {  
                f"{m2_code.code_comb}".strip(): str(m2_code.id)
                for m2_code in M2Code.objects.all()
                if m2_code.code_comb and m2_code.id is not None
            }

            t1_code_dict = {
                f"{t1_code.code_comb}".strip() + "-" + t1_code.price_adjustment : str(t1_code.id)
                for t1_code in T1Code.objects.all()
                if t1_code.code_comb and t1_code.id is not None
            }
            df_melted = pd.melt(df, id_vars=['Rep Month', 'L4 Code', 'M2 Code', 'T1 Code','FFAK','Taşeron Kod'], 
                                var_name='month', value_name='qty')
            df.columns = df.iloc[0]  # Set headers from the first row
            # df = df[1:]  # Skip the header row

            # Unpivot DataFrame

            # Convert 'month' to datetime and handle 'qty'
            df_melted['month'] = pd.to_datetime(df_melted['month'], format='%d.%m.%Y', dayfirst=True).dt.date

            df_melted['qty'] = pd.to_numeric(df_melted['qty'], errors='coerce')
            df_melted.dropna(subset=['qty'], inplace=True)
            print(df_melted.count())
            # Prepare data for bulk insertion
            expense_records = []
            df_melted['L4 Code'] = df_melted['L4 Code'].astype(str)
            df_melted['Rep Month'] = df_melted['Rep Month'].astype(str)
            df_melted['M2 Code'] = df_melted['M2 Code'].astype(str)
            df_melted['T1 Code'] = df_melted['T1 Code'].astype(str)
            df_melted['FFAK'] = df_melted['FFAK'].astype(str)
            df_melted['Taşeron Kod'] = df_melted['Taşeron Kod'].astype(str)

            for _, row in df_melted.iterrows():
                l4_code_value = str(row['L4 Code']).strip() 
                l4_code_id = l4_code_dict.get(l4_code_value)
                rep_month_id = rep_month_dict.get(str(row['Rep Month']))
                m2_code_id = m2_code_dict.get(str(row['M2 Code']))
                t1_code_id = t1_code_dict.get(str(row['T1 Code']) + "-"+str(row['FFAK']))
                qty_type = True if row['Taşeron Kod'] != 'MALZEME DAĞILIM İÇİN' else False
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
                            exp_qty=row['qty'],
                            m2_code_id=m2_code_id,
                            t1_code_id=t1_code_id,
                            qty_type=qty_type
                        )
                    )

            with transaction.atomic():
                # Delete existing records for the given rep_month_id (if needed)
                print("Expense Quantity to be appended: ", len(expense_records))
                if expense_records:
                    ExpenseQuantity.objects.filter(rep_month_id=rep_month_id).delete()
                    ExpenseQuantity.objects.bulk_create(expense_records)
                    
                self.stdout.write(self.style.SUCCESS('Exp Quantity Data has been imported successfully'))

        except FileNotFoundError:
            raise CommandError(f'File not found at {file_path}')
        except Exception as e:
            raise CommandError(f'Error: {str(e)}')
