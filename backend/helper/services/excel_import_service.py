import numpy as np
from helper.services.list_convert_generator import *
from pandas.api.types import is_string_dtype
from employee.models import Employee
from helper.services.list_convert import *
import calendar
import re
import datetime
import datacompy

class ExcelImportService:

    @staticmethod
    def check_excel_file(request, **kwargs):
        file_key = kwargs['file_key']
        excel_file = request.FILES[file_key]
        if not str(excel_file).split('.')[-1] in ('xls', 'xlsx'):
            return False
        return True

    @staticmethod
    def read_excel(request, **kwargs):
        file_key = kwargs['file_key']
        excel_file = request.FILES[file_key]

        df_excel_data = pd.read_excel(excel_file)

        empty_rows, empty_column = ExcelImportService.check_excel_rows_empty(df_excel_data, **kwargs)
        if empty_rows is False:
            df_excel_data = df_excel_data.apply(
                lambda x: x.astype(str).str.replace('İ', 'I').replace('I', 'ı').str.title())

        return df_excel_data

    @staticmethod
    def check_excel_rows_empty(data, **kwargs):
        not_empty_column_list_gen = ListConvert.list_to_generator(kwargs['not_empty_column_list'])
        for column in not_empty_column_list_gen:
            if True in pd.isnull(data[column]).values:
                return True, column
        return False, None

    @staticmethod
    def check_excel_column_uniques(data, **kwargs):
        df = pd.DataFrame(data)
        unique_column_list = kwargs.get('unique_column_list', [])
        non_unique_rows = {}
        non_unique_found = False

        for column in unique_column_list:
            if column not in df.columns:
                continue

            df[column].replace('Nan', np.nan, inplace=True)
            non_nan_df = df[df[column].notna()]

            # Sütundaki tekrar eden değerleri bul
            duplicates = non_nan_df[non_nan_df.duplicated(column, keep=False)]
            if not duplicates.empty:
                non_unique_found = True
                non_unique_rows[column] = duplicates

        if non_unique_found:
            return True, non_unique_rows
        else:
            return False, None

    @staticmethod
    def check_excel_column_name(data, **kwargs):
        not_valid_column_names = []
        for column in data.columns.values:
            column_list_gen = ListConvert.list_to_generator(kwargs['column_list'])
            if column not in column_list_gen:
                not_valid_column_names.append(column)

        if len(not_valid_column_names) > 0:
            return not_valid_column_names, True
        return None, False

    @staticmethod
    def check_excel_column_order(data, **kwargs):
        if kwargs['column_list'] != list(data.columns.values):
            return True
        return False

    @staticmethod
    def check_new_field(field_list, excel_gen):
        new_field_list = []

        for exg in excel_gen:
            if exg is not None and exg not in field_list and exg not in new_field_list:
                new_field_list.append(exg)

        if len(new_field_list) > 0:
            return new_field_list, True
        return None, False

    @staticmethod
    def check_new_null_field(field_list, excel_gen):
        new_field_list = []

        for exg in excel_gen:
            if exg is not None and str(int(float(exg))) not in field_list and str(
                    int(float(exg))) not in new_field_list:
                new_field_list.append(str(int(float(exg))))

        if len(new_field_list) > 0:
            return new_field_list, True
        return None, False

    @staticmethod
    def check_field_length(values, length):
        element_list = []
        start_row = 1
        for exg in values:
            # 'nan' değerlerini kontrol et
            if not pd.isna(exg) and exg != 'Nan':
                if len(str(int(float(exg)))) != length:
                    # element_list.append(int(float(exg)),start_row)
                    element_list.append((start_row, int(float(exg))))

            start_row += 1

        if len(element_list) > 0:
            return element_list, True

        return None, False

    @staticmethod
    def check_already_exist_tckn(tckn_list, data):
        already_exist_tckn_list = []
        for item in data:
            # 'nan' değerlerini kontrol et
            if not pd.isna(item):
                if str(int(float(item))) in tckn_list:
                    already_exist_tckn_list.append(int(float(item)))

        if len(already_exist_tckn_list) > 0:
            return already_exist_tckn_list, True
        return None, False

    @staticmethod
    def check_already_exist_email(email_list, data):
        already_exist_email_list = []
        for item in data:
            # 'nan' değerlerini kontrol et
            if not pd.isna(item):
                if item.lower() in email_list:
                    already_exist_email_list.append(item.lower())

        if len(already_exist_email_list) > 0:
            return already_exist_email_list, True
        return None, False

    @staticmethod
    def check_already_exist_passport_no(employee_list, data):
        already_exist_passport_no_list = []
        for item in data:
            if ListConvert.convert_to_uppercase(item) in employee_list:
                already_exist_passport_no_list.append(ListConvert.convert_to_uppercase(item))

        if len(already_exist_passport_no_list) > 0:
            return already_exist_passport_no_list, True
        return None, False

    @staticmethod
    def check_employee_tckn(data):
        employee_tckn_list = []
        not_already_employee_tckn = []
        start_row = 1
        for em in Employee.objects.all():
            employee_tckn_list.append(em.tckn)

        for employee in data:
            if not pd.isna(employee) and employee != 'Nan':
                if str(int(float(employee))) not in employee_tckn_list:
                    not_already_employee_tckn.append((start_row, str(int(float(employee)))))
            start_row += 1
        if len(not_already_employee_tckn) > 0:
            return not_already_employee_tckn, True
        return None, False

    @staticmethod
    def check_employee_passport_no(data):
        employee_passport_number_set = {str(em.passport_number).upper() if em.passport_number else '' for em in
                                        Employee.objects.all()}
        not_already_employee_passport_number = []
        start_row = 1
        for employee in data:
            if employee is not None:
                if str(employee).upper() not in employee_passport_number_set and str(
                        employee).upper() not in not_already_employee_passport_number:
                    not_already_employee_passport_number.append((start_row, employee))
            start_row += 1

        if not_already_employee_passport_number:
            return not_already_employee_passport_number, True
        return None, False

    @staticmethod
    def check_tckn_passport_value(excel_list, row=1):
        empty_list = []
        not_empty_list = []
        start_row = 1

        for ex in excel_list:
            if ex[0] is None and ex[1] is None:
                empty_list.append(((int(start_row)), ex))

            if ex[0] is not None and ex[1] is not None:
                not_empty_list.append(((int(start_row)), ex))

            start_row += 1

        if len(empty_list) > 0:
            return empty_list, True, False

        if len(not_empty_list) > 0:
            return not_empty_list, False, True

        return None, False, False

    @staticmethod
    def check_confirm_reject_value(excel_list, row=1):
        empty_list = []
        not_empty_list = []
        start_row = 1

        for ex in excel_list:
            row = row + 1
            if ex[2] is None and ex[3] is None:
                empty_list.append((start_row, ex))

            if ex[2] is not None and ex[3] is not None:
                not_empty_list.append((start_row, ex))
            start_row += 1

        if len(empty_list) > 0:
            return empty_list, True, False

        if len(not_empty_list) > 0:
            return not_empty_list, False, True

        return None, False, False

    @staticmethod
    def check_confirm_date_values(excel_list, start_row=1):
        action_date_list = []
        start_date_list = []
        date_check_list = []
        start_row = 1
        pattern_a = r'^(?:\d{4})-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\d|3[01])$'
        pattern_b = r'^(?:\d{4})-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\d|3[01]) (?:[01]\d|2[0-3]):(?:[0-5]\d):(?:[0-5]\d)$'

        for ex in excel_list:
            if ex[5] is not None:
                if not re.match(pattern_a, ex[5]) and not re.match(pattern_b, ex[5]):
                    action_date_list.append((start_row, ex))
                else:
                    if re.match(pattern_a, ex[5]):
                        try:
                            year, month, day = map(int, ex[5].split('-'))
                            _, num_days_in_month = calendar.monthrange(year, month)
                            if day < 1 or day > num_days_in_month:
                                action_date_list.append((start_row, ex))
                        except ValueError:
                            action_date_list.append((start_row, ex))
                    elif re.match(pattern_b, ex[5]):
                        try:
                            datetime_obj = datetime.datetime.strptime(ex[5], "%Y-%m-%d %H:%M:%S")
                            # Additional checks can be added if necessary
                        except ValueError:
                            action_date_list.append((start_row, ex))
                    else:
                        action_date_list.append((start_row, ex))

            if ex[6] is not None:
                if not re.match(pattern_a, ex[6]) and not re.match(pattern_b, ex[6]):
                    start_date_list.append((start_row, ex))
                else:
                    if re.match(pattern_a, ex[6]):
                        try:
                            year, month, day = map(int, ex[6].split('-'))
                            _, num_days_in_month = calendar.monthrange(year, month)
                            if day < 1 or day > num_days_in_month:
                                start_date_list.append((start_row, ex))
                        except ValueError:
                            start_date_list.append((start_row, ex))
                    elif re.match(pattern_b, ex[6]):
                        try:
                            datetime_obj = datetime.datetime.strptime(ex[6], "%Y-%m-%d %H:%M:%S")
                            # Additional checks can be added if necessary
                        except ValueError:
                            start_date_list.append((start_row, ex))
                    else:
                        start_date_list.append((start_row, ex))

            if ex[5] is not None and ex[6] is not None:
                if ex[5] < ex[6]:
                    date_check_list.append((start_row, ex))

            start_row += 1

        if len(action_date_list) > 0:
            return action_date_list, True, False, False

        if len(start_date_list) > 0:
            return start_date_list, False, True, False

        if len(date_check_list) > 0:
            return date_check_list, False, False, True

        return None, False, False, False

    @staticmethod
    def check_grade_value(excel_list, row=1):
        empty_list = []

        for ex in excel_list:
            row = row + 1
            if ex[11] is None and ex[12] is not None:
                empty_list.append(row)

            if ex[11] is not None and ex[12] is None:
                empty_list.append(row)

        if len(empty_list) > 0:
            return empty_list, True

        return None, False

    @staticmethod
    def check_empty_tckn_passport_value(excel_list, row=1):
        empty_list = []
        start_row = 1
        for ex in excel_list:
            if ex[0] is None and ex[1] is None:
                empty_list.append(((int(start_row)), ex))
            start_row += 1

        if len(empty_list) > 0:
            return empty_list, True

        return None, False

    @staticmethod
    def check_default_value(default_list, data):
        not_default_list = []
        for item in data:
            if item.strip() not in default_list:
                not_default_list.append(item)

        if len(not_default_list) > 0:
            return not_default_list

        return None

    @staticmethod
    def check_birth_place_type(birth_place_list):
        incorrect_birth_place_list = []
        start_row = 1
        for birth_place in birth_place_list:
            if type(birth_place) is not str:
                incorrect_birth_place_list.append((start_row, birth_place))

                start_row += 1

        if len(incorrect_birth_place_list) > 0:
            return incorrect_birth_place_list, True

        return None, False

    @staticmethod
    def check_employee_start_date(start_date_list):
        today = datetime.datetime.today()
        invalid_date_list = []
        start_row = 1
        for start_date in start_date_list:
            if datetime.datetime.strptime(start_date, "%Y-%m-%d") > today:
                invalid_date_list.append((start_row, start_date))

                start_row += 1

        if len(invalid_date_list) > 0:
            return invalid_date_list, True

        return None, False

    @staticmethod
    def check_row_by_row(data, query, **kwargs):
        
        # df_db = pd.DataFrame.from_records(query, columns=kwargs['column_list'])
        compare = datacompy.Compare(
            data,
            query,
            join_columns=kwargs['join_columns'],
            abs_tol=0.0001,
            rel_tol=0,
            df1_name='original',
            df2_name='new'
        )

        return compare