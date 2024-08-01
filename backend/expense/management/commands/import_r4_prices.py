import pandas as pd
from django.core.management.base import BaseCommand, CommandError
from libraries.models import R4Code, Unit  # Adjust as per your actual models
from django.db import transaction
from datetime import datetime 
from constants.models import RepMonth
from expense.models import R4Price




class Command(BaseCommand):
    help = 'Import R4 Code from an Excel file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the Excel file')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']

        try:
            # Create a dictionary of R3 Codes for lookup
            r4_code_dict = {str(r4_code.code_comb).upper(): r4_code for r4_code in R4Code.objects.all()}  # Adjust 'name' to your R4Code model's unique field
            r4_name_dict = {str(r4_code.description).upper(): r4_code.id for r4_code in R4Code.objects.all()}  # Adjust 'name' to your R4Code model's unique field
            unit_dict = {str(unit.unit).upper(): unit for unit in Unit.objects.all()}  # Adjust 'name' to your Unit model's unique field
            rep_month_dict = {str(rep_month.rep_month).upper(): rep_month for rep_month in RepMonth.objects.all()}  # Adjust 'name' to your RepMonth model's unique field   
            # Read the Excel file using pandas
            df = pd.read_excel(file_path, sheet_name='R4Prices', dtype={'Rep_Month': str, 'R1 Code': str, 'R2 Code': str, 'R3 Code': str, 'R4 Code': str, 'Description': str, 'Unit': str, 'Currency': str, 'Origin': str, 'Price': float, 'Price Date': str,  'Price Adjustment Type': str, ' Depreciation Price': float, 'Depreciation': bool, 'Depreciation Type': str, 'Energy Type':str,'Finance Type':str, 'Operator R4 Code': str, 'Customs': bool, 'Content Constant': float, 'Machine ID': str})
            required_columns = {'R1 Code', 'R2 Code', 'R3 Code', 'R4 Code', 'Description', 'Unit', 'Currency', 'Origin', 'Finance Type', 'Customs', 'Price Date', 'Price', 'Price Adjustment Type', 'Depreciation', 'Depreciation Type', 'Energy Type', 'Operator R4 Code', 'Content Constant', 'Machine ID'}
            file_columns = set(df.columns)
            df['Price Date'] = pd.to_datetime(df['Price Date'], errors='coerce')
            if not required_columns.issubset(file_columns):
                raise CommandError(f'Excel file must contain columns: {required_columns}. Found columns: {file_columns}')

            with transaction.atomic():  # Ensure atomic transaction
                rep_month_delete= rep_month_dict.get(str(df['Rep Month'][0]).upper())
                R4Price.objects.filter(rep_month__rep_month=rep_month_delete).delete()  # Clear existing data
                
                for index, row in df.iterrows():
                    rep_month = rep_month_dict.get(str(row['Rep Month']).upper()) if pd.notna(row['Rep Month']) else None
                    
                    r1_code = str(row['R1 Code']).upper() if pd.notna(row['R1 Code']) else None
                    r2_code_code = str(row['R2 Code']).upper() if pd.notna(row['R2 Code']) else None
                    r3_code_code = str(row['R3 Code']).upper() if pd.notna(row['R3 Code']) else None
                    r4_code_code = str(row['R4 Code']).upper() if pd.notna(row['R4 Code']) else None

                    r4_code = r4_code_dict.get(f"{r1_code}-{r2_code_code}-{r3_code_code}-{r4_code_code}") if r1_code and r2_code_code and r3_code_code and r4_code_code else None
                    currency = str(row['Currency']).upper() if pd.notna(row['Currency']) else None
                    unit_name = str(row['Unit']).upper() if pd.notna(row['Unit']) else None
                    unit = unit_dict.get(unit_name) if unit_name else None
                    origin = str(row['Origin']).upper() if pd.notna(row['Origin']) else None

                    price = row['Price'] if pd.notna(row['Price']) else None
                    price_date = row['Price Date'] if pd.notna(row['Price Date']) else None
                    price_adjustment_type = str(row['Price Adjustment Type']).upper() if pd.notna(row['Price Adjustment Type']) else None
                    bool_depreciation = bool(row['Depreciation']) if pd.notna(row['Depreciation']) else None
                    depreciation_type = str(row['Depreciation Type']).upper() if pd.notna(row['Depreciation Type']) else None
                    depreciation_price = row['Depreciation Price'] if pd.notna(row['Depreciation Price']) else None
                    energy_type = str(row['Energy Type']).upper() if pd.notna(row['Energy Type']) else None
                    operator_r4_code = r4_name_dict.get(str(row['Operator R4 Code']).upper()) if pd.notna(row['Operator R4 Code']) else None
                    content_constant = row['Content Constant'] if pd.notna(row['Content Constant']) else None
                    machine_id = str(row['Machine ID']) if pd.notna(row['Machine ID']) else None

                    fin_type = str(row['Finance Type']).upper() if pd.notna(row['Finance Type']) else None
                    customs = bool(row['Customs']) if pd.notna(row['Customs']) else None
                    created_by_id = '12f4aa11-b6fc-482f-894d-0962ad5f4313'

                    if r4_code:
                        # Create the R4Price instance
                        R4Price.objects.create(
                            rep_month_id=rep_month.id if rep_month else None,
                            r4_code_id=r4_code.id if r4_code else None,
                            unit_id=unit.id if unit else None,
                            currency=currency,
                            origin=origin,
                            price=price,
                            price_date=price_date,
                            price_adjustment_type=price_adjustment_type,
                            bool_depreciation=bool_depreciation,
                            depreciation_type=depreciation_type,
                            depreciation_price=depreciation_price,
                            energy_type=energy_type,
                            operator_r4_code_id=operator_r4_code if operator_r4_code else None,
                            fin_type=fin_type,
                            customs=customs,
                            content_constant=content_constant,
                            machine_id=machine_id,

                            created_by_id=created_by_id,
                            updated_by_id=created_by_id
                        )
                    else:
                        missing_code = r4_code is None and f'R Code {r1_code + "-" + r2_code_code + "-" + r3_code_code + "-" + r4_code_code}' or f'Unit {unit_name}'
                        raise CommandError(f'{missing_code} not found.')

                self.stdout.write(self.style.SUCCESS('R4 Codes imported successfully'))
        except FileNotFoundError:
            raise CommandError(f'File not found at {file_path}')
        except Exception as e:
            raise CommandError(f'Error: {str(e)}')
