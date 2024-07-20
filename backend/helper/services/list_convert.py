import pandas as pd
import re
# import phonenumbers

# from helper.enums import CheckValueMessageEnum


class ListConvert:

    @staticmethod
    def list_to_generator(lst):
        gen = (gn for gn in lst)
        return gen

    @staticmethod
    def convert_to_uppercase(data):
        try:
            return data.upper()
        except Exception:
            return data

    @staticmethod
    def convert_to_titlecase(data):
        try:
            replacements = {
                'I': 'ı',
                'İ': 'i',
                'Ş': 'ş',
                'Ö': 'ö',
                'Ü': 'ü',
                'Ğ': 'ğ',
                'Ç': 'ç'
            }

            def titlecase_match(match):
                word = match.group(0)
                first_char = word[0]
                rest = word[1:].lower().translate(str.maketrans(replacements))
                return first_char + rest

            return re.sub(r'\b\w+\b', titlecase_match, data)
        except Exception:
            return data

    @staticmethod
    def convert_to_date(data):
        data = pd.to_datetime(data, errors='coerce')

        if pd.isnull(data):
            date_of_status = None
            return date_of_status

        if pd.notnull(data):
            date_of_status = data
            return date_of_status

    # @staticmethod
    # def convert_to_phone_number(phone_number):
    #     country_code = CheckValueMessageEnum.country_code.value
    #     if phone_number:
    #         return country_code + phonenumbers.format_number(phonenumbers.parse(str(phone_number), 'TR'),
    #                                                          phonenumbers.PhoneNumberFormat.NATIONAL)
    #     return phone_number
