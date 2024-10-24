import pandas as pd
from django.core.management.base import BaseCommand, CommandError
from libraries.models import R4Code, L4Code , M2Code, T1Code  # Adjust as per your actual models
from django.db import transaction
from datetime import datetime 
from constants.models import RepMonth
from expense.models import ExpenseMachineryOperatorDistribution


class Command(BaseCommand):
    help = 'Import R4 Code from an Excel file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the Excel file')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']

        try:
            df = pd.read_excel(file_path, sheet_name='MAK-OPER-2410', usecols=lambda col: col not in ['Machine ID'])

            file_columns = set(df.columns)

            rep_month_dict = {rep_month.rep_month: rep_month.id for rep_month in RepMonth.objects.all()}
            l4_code_dict = {
                f"{l4_code.code_comb}".strip(): str(l4_code.id)
                for l4_code in L4Code.objects.filter(aygm_code__isnull=True)
                if l4_code.code_comb and l4_code.id is not None
            }
            r4_code_dict = {
                f"{r4_code.code_comb}".strip(): str(r4_code.id)
                for r4_code in R4Code.objects.all()
                if r4_code.code_comb and r4_code.id is not None
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

            df_melted = pd.melt(df, id_vars=['Rep Month', 'L4 Code','R4 Code','Machine R4 Code','M2 Code','T1 Code','FFAK','R4 Desc','R4 Desc2','OPERATÖR R4 Code'], 
                                var_name='month', value_name='qty')
            df.columns = df.iloc[0]  # Set headers from the first row
            #print(df.columns)
            #print(len(df_melted))
            # df = df[1:]  # Skip the header row

            # Unpivot DataFrame

            # Convert 'month' to datetime and handle 'qty'
            df_melted['month'] = pd.to_datetime(df_melted['month'], format='%Y-%m-%d %H:%M:%S').dt.date
            df_melted['qty'] = pd.to_numeric(df_melted['qty'], errors='coerce')
            df_melted.dropna(subset=['qty'], inplace=True)
            # Prepare data for bulk insertion
            expense_records = []
            df_melted['L4 Code'] = df_melted['L4 Code'].astype(str)
            df_melted['R4 Code'] = df_melted['R4 Code'].astype(str)
            df_melted['Machine R4 Code'] = df_melted['Machine R4 Code'].astype(str)
            df_melted['Rep Month'] = df_melted['Rep Month'].astype(str)
            df_melted['M2 Code'] = df_melted['M2 Code'].astype(str)
            df_melted['T1 Code'] = df_melted['T1 Code'].astype(str)
            df_melted['FFAK'] = df_melted['FFAK'].astype(str)
            df_melted['R4 Desc'] = df_melted['R4 Desc'].astype(str)
            df_melted['R4 Desc2'] = df_melted['R4 Desc2'].astype(str)



            for _, row in df_melted.iterrows():
                 
                l4_code_value = str(row['L4 Code']).strip() 
                l4_code_id = l4_code_dict.get(l4_code_value)
                r4_code_value = str(row['R4 Code']).strip()
                r4_code_id = r4_code_dict.get(r4_code_value)
                #print(r4_code_id, r4_code_value, l4_code_id, l4_code_value)
                machine_r4_code_id = None
                m2_code_id = m2_code_dict.get(str(row['M2 Code']).strip())
                t1_code_id = t1_code_dict.get(str(row['T1 Code']+"-"+row['FFAK']).strip())
                r4_usage_desc = str(row['R4 Desc2']).strip()

                if not r4_code_id:
                    raise CommandError(f'R4 Code not found: {r4_code_value} for L4 Code: {l4_code_value} at row: {row.name}')
                if not l4_code_id:
                    raise CommandError(f'L4 Code not found: {l4_code_value} for L4 Code: {l4_code_value} at row: {row.name}')
                
                if str(row['Machine R4 Code']).strip():
                    machine_r4_code_value = str(row['Machine R4 Code']).strip()
                    machine_r4_code_id = r4_code_dict.get(machine_r4_code_value)

                rep_month_id = rep_month_dict.get(str(row['Rep Month']))
                if rep_month_id and l4_code_id and row['qty'] != 0 and not pd.isnull(row['qty']):
                    #print(row)

                    #print("Adding record")
                    r4_usage_desc = row['R4 Desc2']
                    if r4_usage_desc == 'nan' or r4_usage_desc == 'NaN' or r4_usage_desc == 'Nan':
                        r4_usage_desc = None

                    expense_records.append(
                        ExpenseMachineryOperatorDistribution(
                            rep_month_id=rep_month_id,
                            l4_code_id=l4_code_id,
                            r4_code_id=r4_code_id,
                            m2_code_id=m2_code_id,
                            t1_code_id=t1_code_id,
                            machine_r4_code_id=machine_r4_code_id if machine_r4_code_id else None,
                            exp_month=row['month'],
                            machine_qty=row['qty'],
                            r4_usage_desc=r4_usage_desc if r4_usage_desc else None
                        )
                    )

            print(f'Number of records to be inserted: {len(expense_records)}')
            with transaction.atomic():
                # Delete existing records for the given rep_month_id (if needed)
                if expense_records:
                    ExpenseMachineryOperatorDistribution.objects.filter(rep_month_id=rep_month_id).delete()
                    ExpenseMachineryOperatorDistribution.objects.bulk_create(expense_records)
                    
                self.stdout.write(self.style.SUCCESS('Machinery Dist - Operator Data has been imported successfully'))

        except FileNotFoundError:
            raise CommandError(f'File not found at {file_path}')
        except Exception as e:
            raise CommandError(f'Error: {str(e)}')
