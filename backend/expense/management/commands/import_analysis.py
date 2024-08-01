import pandas as pd
from django.core.management.base import BaseCommand, CommandError
from libraries.models import R4Code, L4Code  # Adjust as per your actual models
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
            # Read the Excel file using pandas
            df = pd.read_excel(file_path, sheet_name='Analysis', dtype={'Rep Month': str, 'R1 Code': str, 'L4 Code': str, 'R4 Code': str, 'R4 Desc': str, 'Description': str, 'Work Ratio': float, 'Work Ratio Desc': str, 'Output Unit Time': float, 'Output Desc': str, 'Cons Unit Time': float, 'Cons Desc': str})


            required_columns = {'Rep Month', 'L4 Code', 'R4 Code', 'R4 Desc', 'Work Ratio', 'Work Ratio Desc', 'Output Unit Time', 'Output Desc', 'Cons Unit Time', 'Cons Desc'}
            file_columns = set(df.columns)

            if not required_columns.issubset(file_columns):
                raise CommandError(f'Excel file must contain columns: {required_columns}. Found columns: {file_columns}')

            with transaction.atomic():  # Ensure atomic transaction

                rep_month_delete= rep_month_dict.get(str(df['Rep Month'][0]).upper())
                ExpenseAnalysis.objects.filter(rep_month__rep_month=rep_month_delete).delete()  # Clear existing data


                for index, row in df.iterrows():

                    rep_month = rep_month_dict.get(str(row['Rep Month']).upper()) if pd.notna(row['Rep Month']) else None
                    l4_code = l4_code_dict.get(str(row['L4 Code']).upper()) if pd.notna(row['L4 Code']) else None
                    r4_code = r4_code_dict.get(str(row['R4 Code']).upper()) if pd.notna(row['R4 Code']) else None
                    r4_desc = str(row['R4 Desc']).upper() if pd.notna(row['R4 Desc']) else None
                    work_ratio = row['Work Ratio'] if pd.notna(row['Work Ratio']) else None
                    work_ratio_desc = str(row['Work Ratio Desc']).lower() if pd.notna(row['Work Ratio Desc']) else None
                    output_per_unit_time = row['Output Unit Time'] if pd.notna(row['Output Unit Time']) else None
                    output_desc = str(row['Output Desc']).lower() if pd.notna(row['Output Desc']) else None
                    consumption_per_unit_time = row['Cons Unit Time'] if pd.notna(row['Cons Unit Time']) else None
                    consumption_desc = str(row['Cons Desc']).lower() if pd.notna(row['Cons Desc']) else None

                    created_by_id = '12f4aa11-b6fc-482f-894d-0962ad5f4313'

                    if r4_code:
                        # Create the ExpenseAnalysis instance
                        ExpenseAnalysis.objects.create(
                            rep_month_id=rep_month.id,
                            l4_code_id=l4_code.id,
                            r4_code_id=r4_code.id,
                            r4_desc=r4_desc,
                            work_ratio=work_ratio,
                            work_ratio_desc=work_ratio_desc,
                            output_per_unit_time=output_per_unit_time,
                            output_desc=output_desc,
                            consumption_per_unit_time=consumption_per_unit_time,
                            consumption_desc=consumption_desc,
                            created_by_id=created_by_id,
                            updated_by_id=created_by_id
                        )
                    else:
                        missing_code = r4_code is None and f'Code {str(row['L4 Code']).upper() + "-" + str(row['R4 Code']).upper() }'
                        raise CommandError(f'{missing_code} not found.')

                self.stdout.write(self.style.SUCCESS('Codes imported successfully'))
        except FileNotFoundError:
            raise CommandError(f'File not found at {file_path}')
        except Exception as e:
            raise CommandError(f'Error: {str(e)}')
