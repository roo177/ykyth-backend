import pandas as pd
from django.core.management.base import BaseCommand, CommandError
from libraries.models import R4Code, L4Code , M2Code, T1Code,R3Code  # Adjust as per your actual models
from django.db import transaction
from constants.models import RepMonth
from expense.models import ExpenseAnalysis




class Command(BaseCommand):
    help = 'Import R4 Code from an Excel file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the Excel file')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']

        try:
            # Create a dictionary of R3 Codes for lookup
            r4_code_dict = {str(r4_code.code_comb).upper(): r4_code for r4_code in R4Code.objects.all()}  # Adjust 'name' to your R4Code model's unique field
            l4_code_dict = {str(l4_code.code_comb).upper(): l4_code for l4_code in L4Code.objects.all()}  # Adjust 'name' to your L4Code model's unique field
            rep_month_dict = {str(rep_month.rep_month).upper(): rep_month for rep_month in RepMonth.objects.all()}  # Adjust 'name' to your RepMonth model's unique field   

            m2_code_dict = {    
                f"{m2_code.code_comb}".strip(): str(m2_code.id)
                for m2_code in M2Code.objects.all()
                if m2_code.code_comb and m2_code.id is not None
            }
            t1_code_dict = {
                f"{t1_code.code_comb}".strip()+"-"+str(t1_code.price_adjustment): str(t1_code.id)
                for t1_code in T1Code.objects.all()
                if t1_code.code_comb and t1_code.id is not None
            }
            r3_code_dict = {str(r3_code.code_comb).upper(): r3_code for r3_code in R3Code.objects.all()}  # Adjust 'name' to your R3Code model's unique field
            # Read the Excel file using pandas
            df = pd.read_excel(file_path, sheet_name='Analysis', dtype={'Rep Month': str, 'R1 Code': str, 'L4 Code': str, 'R3 Code': str,'R4 Code': str, 'M2 Code': str, 'T1 Code': str, 'R4 Desc': str, 'Description': str, 'Work Ratio': float, 'Work Ratio Desc': str, 'Output Unit Time': float, 'Output Desc': str, 'Cons Unit Time': float, 'Cons Desc': str, 'FFAK': str, 'R3 Currency': str })


            required_columns = {'Rep Month', 'L4 Code',  'R3 Code','R4 Code','M2 Code', 'T1 Code', 'FFAK', 'R4 Desc', 'Work Ratio', 'Work Ratio Desc', 'Output Unit Time', 'Output Desc', 'Cons Unit Time', 'Cons Desc','R3 Currency'}
            file_columns = set(df.columns)

            if not required_columns.issubset(file_columns):
                raise CommandError(f'Excel file must contain columns: {required_columns}. Found columns: {file_columns}')

            with transaction.atomic():  # Ensure atomic transaction

                rep_month_delete= rep_month_dict.get(str(df['Rep Month'][0]).upper())
                ExpenseAnalysis.objects.filter(rep_month__rep_month=rep_month_delete).delete()  # Clear existing data


                for index, row in df.iterrows():

                    rep_month = rep_month_dict.get(str(row['Rep Month']).upper()) if pd.notna(row['Rep Month']) else None
                    l4_code = l4_code_dict.get(str(row['L4 Code']).upper()) if pd.notna(row['L4 Code']) else None
                    if l4_code is None:
                        raise CommandError(f'L4 Code {str(row["L4 Code"]).upper()} not found.')
                    r4_code = r4_code_dict.get(str(row['R4 Code']).upper()) if pd.notna(row['R4 Code']) else None
                    r4_desc = str(row['R4 Desc']).upper() if pd.notna(row['R4 Desc']) else None
                    work_ratio = row['Work Ratio'] if pd.notna(row['Work Ratio']) else None
                    work_ratio_desc = str(row['Work Ratio Desc']).lower() if pd.notna(row['Work Ratio Desc']) else None
                    output_per_unit_time = row['Output Unit Time'] if pd.notna(row['Output Unit Time']) else None
                    output_desc = str(row['Output Desc']).lower() if pd.notna(row['Output Desc']) else None
                    consumption_per_unit_time = row['Cons Unit Time'] if pd.notna(row['Cons Unit Time']) else None
                    consumption_desc = str(row['Cons Desc']).lower() if pd.notna(row['Cons Desc']) else None
                    m2_code = m2_code_dict.get(str(row['M2 Code']).upper()) if pd.notna(row['M2 Code']) else None
                    t1_code = t1_code_dict.get(str(row['T1 Code']).upper()+"-"+str(row['FFAK']).upper()) if pd.notna(row['T1 Code']) else None
                    r3_code = r3_code_dict.get(str(row['R3 Code']).upper()) if pd.notna(row['R3 Code']) else None
                    r3_currecy = str(row['R3 Currency']).upper() if pd.notna(row['R3 Currency']) else None
                    
                    created_by_id = '12f4aa11-b6fc-482f-894d-0962ad5f4313'

                    if r4_code or r3_code:
                        # Create the ExpenseAnalysis instance
                        ExpenseAnalysis.objects.create(
                            rep_month_id=rep_month.id,
                            l4_code_id=l4_code.id if l4_code else None,
                            r4_code_id=r4_code.id if r4_code else None,
                            r4_desc=r4_desc if r4_desc else None,
                            work_ratio=work_ratio,
                            work_ratio_desc=work_ratio_desc,
                            output_per_unit_time=output_per_unit_time,
                            output_desc=output_desc,
                            consumption_per_unit_time=consumption_per_unit_time,
                            consumption_desc=consumption_desc,
                            m2_code_id=m2_code,
                            t1_code_id=t1_code,
                            r3_code_machine_id=r3_code.id if r3_code else None,
                            r3_currency=r3_currecy if r3_currecy else None,
                            created_by_id=created_by_id,
                            updated_by_id=created_by_id

                        )
                    else:
                        missing_code = r4_code is None and f'Code {str(row['L4 Code']).upper() + "-" + str(row['R4 Code']).upper() }'
                        raise CommandError(f'{missing_code} not found. Row: {index + 2}')

                self.stdout.write(self.style.SUCCESS('Analysis Data has been imported successfully'))
        except FileNotFoundError:
            raise CommandError(f'File not found at {file_path}')
        except Exception as e:
            raise CommandError(f'Error: {str(e)}')
