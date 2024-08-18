import pandas as pd
from django.core.management.base import BaseCommand, CommandError
from libraries.models import R4Code,R3Code, Unit  # Adjust as per your actual models
from django.db import transaction
from datetime import datetime 
from constants.models import RepMonth
from expense.models import Expense
from libraries.models import L4Code, M2Code, T1Code

class Command(BaseCommand):
    help = 'Import R4 Code from an Excel file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the Excel file')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']

        try:
            df = pd.read_excel(file_path, sheet_name='Expense', usecols=lambda col: col not in ['L4 Desc', 'R4 Desc', 'R4 Subc Code'])

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

            r4_code_dict = {
                f"{r4_code.code_comb}".strip(): str(r4_code.id)
                for r4_code in R4Code.objects.all()
                if r4_code.code_comb and r4_code.id is not None
            }
            unit_dict = {
                f"{unit.unit}".strip(): str(unit.id)
                for unit in Unit.objects.all()
                if unit.unit and unit.id is not None
            }
            r3_code_dict = {
                f"{r3_code.code_comb}".strip(): str(r3_code.id)
                for r3_code in R3Code.objects.all()
                if r3_code.code_comb and r3_code.id is not None
            }
            # df_melted = pd.melt(df, id_vars=['Rep Month', 'L4 Code', 'M2 Code', 'T1 Code','FFAK','Taşeron Kod'], 
            #                     var_name='month', value_name='qty')
            #df.columns = df.iloc[0]  # Set headers from the first row
            #print(df.columns)
            # df = df[1:]  # Skip the header row

            # Unpivot DataFrame

            # Convert 'month' to datetime and handle 'qty'
            df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d %H:%M:%S').dt.date
            df['Qty'] = pd.to_numeric(df['Qty'], errors='coerce')
            df['Expense'] = pd.to_numeric(df['Expense'], errors='coerce')

            df.dropna(subset=['Qty'], inplace=True)
            df.dropna(subset=['Expense'], inplace=True)
            # Prepare data for bulk insertion
            expense_records = []

            df['L4 Code'] = df['L4 Code'].astype(str)
            df['Rep Month'] = df['Rep Month'].astype(str)
            df['M2 Code'] = df['M2 Code'].astype(str)
            df['T1 Code'] = df['T1 Code'].astype(str)
            df['FFAK'] = df['FFAK'].astype(str)
            

            for _, row in df.iterrows():
                l4_code_value = str(row['L4 Code']).strip() 
                l4_code_id = l4_code_dict.get(l4_code_value)
                rep_month_id = rep_month_dict.get(str(row['Rep Month']))
                m2_code_id = m2_code_dict.get(str(row['M2 Code']))
                t1_code_id = t1_code_dict.get(str(row['T1 Code']) + "-"+str(row['FFAK']))
                r4_code_id = r4_code_dict.get(str(row['R4 Code']))
                r3_code_id = r3_code_dict.get(str(row['R3 Code']))
                unit_id = unit_dict.get(str(row['Unit']))

                # Print for debugging
                # print(f"Rep Month ID: {rep_month_id}, L4 Code ID: {l4_code_id}, Quantity: {row['qty']}")
                if row['Qty'] == 'nan' or row['Qty'] == 'NaN' or row['Qty'] == 0 or row['Expense'] == 'nan' or row['Expense'] == 'NaN' or row['Expense'] == 0:
                    continue
                if rep_month_id and l4_code_id:
                    expense_records.append(
                        Expense(
                            rep_month_id=rep_month_id if rep_month_id else None,
                            l4_code_id=l4_code_id if l4_code_id else None,
                            exp_month=row['Date'] if row['Date'] else None, 
                            exp_qty=row['Qty'] if row['Qty'] else 0,
                            exp=row['Expense'] if row['Expense'] else 0,
                            m2_code_id=m2_code_id if m2_code_id else None,
                            t1_code_id=t1_code_id if t1_code_id else None,
                            r4_code_id=r4_code_id if r4_code_id else None,
                            r3_code_id=r3_code_id if r3_code_id else None,
                            exp_unit_id=unit_id if unit_id else None,
                            currency=row['Currency'] if row['Currency'] else None,
                            bool_depriciation=row['Depriciation'] 

                        )
                    )

            with transaction.atomic():
                # Delete existing records for the given rep_month_id (if needed)
                if expense_records:
                    Expense.objects.filter(rep_month_id=rep_month_id).delete()
                    Expense.objects.bulk_create(expense_records)
                    
                    self.stdout.write(self.style.SUCCESS('Expense Data imported successfully'))

        except FileNotFoundError:
            raise CommandError(f'File not found at {file_path}')
        except Exception as e:
            raise CommandError(f'Error: {str(e)}')
