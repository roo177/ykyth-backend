import pandas as pd
from django.core.management.base import BaseCommand, CommandError
from libraries.models import R4Code, Unit,M2Code,T1Code
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
            m2_code_dict = {str(m2_code.code_comb).upper(): m2_code for m2_code in M2Code.objects.all()}  # Adjust 'name' to your M2Code model's unique field
            t1_code_dict = {str(t1_code.code_comb).upper() + "-" + t1_code.price_adjustment: t1_code for t1_code in T1Code.objects.all()}  # Adjust 'name' to your T1Code model's unique field
            # with open('output.txt', 'w', encoding='utf-8') as file:
            #     file.write(str(r4_name_dict))
            # print(r4_name_dict, 'r4_name_dict')
            unit_dict = {str(unit.unit).upper(): unit for unit in Unit.objects.all()}  # Adjust 'name' to your Unit model's unique field
            rep_month_dict = {str(rep_month.rep_month).upper(): rep_month for rep_month in RepMonth.objects.all()}  # Adjust 'name' to your RepMonth model's unique field   
            # Read the Excel file using pandas
            df = pd.read_excel(file_path, sheet_name='R4Prices', dtype={'Rep_Month': str, 'R1 Code': str, 'R2 Code': str, 'R3 Code': str, 'M2 Code': str, 'T1 Code': str, 'R4 Code': str, 'Description': str, 'Unit': str, 'Currency': str, 'Origin': str, 'Price': float, 'Price Date': str,  'Price Adjustment Type': str, ' Depreciation Price': float, 'Depreciation': bool, 'Depreciation Type': str, 'Energy Type':str,'Finance Type':str, 'Operator R4 Code': str, 'Customs': bool, 'Content Constant': float, 'Machine ID': str, 'Depreciation_Qty': float,'Consumption': float, 'Consumption_Unit': str, 'Capacity': float, 'Capacity_Unit': str,'Operator M2 Code': str,'Operator T1 Code': str, 'Rep Month': str, 'Finance Model': str, 'Finance Ratio': float})

            required_columns = {'R1 Code', 'R2 Code', 'R3 Code', 'R4 Code', 'Description', 'Unit', 'Currency', 'Origin', 'Finance Type', 'Customs', 'Price Date', 'Price', 'Price Adjustment Type', 'Depreciation', 'Depreciation Type', 'Energy Type', 'Operator R4 Code', 'Content Constant', 'Machine ID','Depreciation_Qty','Consumption','Consumption_Unit','Capacity','Capacity_Unit','M2 Code','T1 Code','Rep Month', 'Operator M2 Code', 'Operator T1 Code', 'Finance Model', 'Finance Ratio'}

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
                    if pd.notna(row['M2 Code']):
                        m2_code = m2_code_dict.get(str(row['M2 Code']).upper())
                        if m2_code is None:
                            raise CommandError(f'M2 Code {row["M2 Code"]} not found.')
                    else:
                        raise CommandError(f'M2 Code {row["M2 Code"]} is missing.')

                    if pd.notna(row['T1 Code']):
                        t1_code_key = str(row['T1 Code']).upper() + "-" + str(row['Price Adjustment Type'])
                        t1_code = t1_code_dict.get(t1_code_key)
                        if t1_code is None:
                            raise CommandError(f'T1 Code {row["T1 Code"]} with Price Adjustment Type {row["Price Adjustment Type"]} not found.')
                    else:
                        raise CommandError(f'T1 Code {row["T1 Code"]} is missing.')

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
                    operator_m2_code = m2_code_dict.get(str(row['Operator M2 Code']).upper()) if pd.notna(row['Operator M2 Code']) else None
                    operator_t1_code = t1_code_dict.get(str(row['Operator T1 Code']).upper()) if pd.notna(row['Operator T1 Code']) else None
                    # print(operator_r4_code, 'operator_r4_code', row['Operator R4 Code'], 'Operator R4 Code',r4_code)
                    content_constant = row['Content Constant'] if pd.notna(row['Content Constant']) else None
                    machine_id = str(row['Machine ID']) if pd.notna(row['Machine ID']) else None
                    depreciation_quantity = row['Depreciation_Qty'] if pd.notna(row['Depreciation_Qty']) else None
                    energy_consumption = row['Consumption'] if pd.notna(row['Consumption']) else None
                    fin_type = str(row['Finance Type']).upper() if pd.notna(row['Finance Type']) else None
                    customs = bool(row['Customs']) if pd.notna(row['Customs']) else None
                    capacity = row['Capacity'] if pd.notna(row['Capacity']) else None
                    capacity_unit = unit_dict.get(str(row['Capacity_Unit']).upper()) if pd.notna(row['Capacity_Unit']) else None
                    energy_unit = unit_dict.get(str(row['Consumption_Unit']).upper()) if pd.notna(row['Consumption_Unit']) else None
                    finance_model = str(row['Finance Model']).upper() if pd.notna(row['Finance Model']) else None
                    finance_ratio = row['Finance Ratio'] if pd.notna(row['Finance Ratio']) else None
                    created_by_id = '12f4aa11-b6fc-482f-894d-0962ad5f4313'

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
                            depreciation_quantity=depreciation_quantity,
                            energy_consumption=energy_consumption,
                            energy_unit_id=energy_unit.id if energy_unit else None,
                            capacity=capacity,
                            capacity_unit_id=capacity_unit.id if capacity_unit else None,
                            m2_code_id=m2_code.id if m2_code else None,
                            t1_code_id=t1_code.id if t1_code else None,
                            operator_m2_code_id=operator_m2_code.id if operator_m2_code else None,
                            operator_t1_code_id=operator_t1_code.id if operator_t1_code else None,
                            fin_model=finance_model,
                            fin_model_ratio=finance_ratio,

                            created_by_id=created_by_id,
                            updated_by_id=created_by_id
                        )
                        #print(f'R4 Code {r1_code + "-" + r2_code_code + "-" + r3_code_code + "-" + r4_code_code+" / "+m2_code.code_comb + "/" + t1_code.code_comb + "-" +t1_code.price_adjustment} imported successfully')


                self.stdout.write(self.style.SUCCESS('R4 Prices imported successfully'))
        except FileNotFoundError:
            raise CommandError(f'File not found at {file_path}')
        except Exception as e:
            raise CommandError(f'Error: {str(e) + " " + str(index)+ " " + f"{r1_code}-{r2_code_code}-{r3_code_code}-{r4_code_code}"}')
