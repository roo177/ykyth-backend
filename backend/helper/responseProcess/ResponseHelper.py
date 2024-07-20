from __future__ import unicode_literals
from rest_framework.response import Response
from rest_framework.status import (HTTP_201_CREATED, HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT,
                                   HTTP_401_UNAUTHORIZED,
                                   HTTP_404_NOT_FOUND, HTTP_501_NOT_IMPLEMENTED, HTTP_409_CONFLICT, HTTP_403_FORBIDDEN)

from users.models import User
from .ResponseInfo import *
from rest_framework.exceptions import APIException

class SuccessMessages:
    DELETED_SUCCESSFULLY = "Record successfully deleted!"
    SAFE_DELETED_SUCCESSFULLY = "Record successfully safe deleted!"
    UPDATED_SUCCESSFULLY = "Record successfully updated!"
    CREATED_SUCCESSFULLY = "Record successfully created!"
    CHECK_SUCCESSFULLY = "Kayıt başarılı bir şekilde kontrol edildi!"
    CREATED_USER_SUCCESSFULLY = "User successfully created!"
    NOT_FOUND_RECORD = "No records found!"
    LIST_SUCCESSFULLY = "Records successfully listed!"
    DETAIL_SUCCESSFULLY = "Record successfully detailed!"
    CHANGE_PASSWORD_SUCCESSFULLY = "Your password has been successfully updated!"
    SUCCESS_CHECK_DATA = ""


class ErrorMessages:
    ERROR_UNKNOWN = "Unknown error occurred!"
    ERROR_NOT_FOUND = "No records found!"
    ERROR_NOT_OWNER = "You do not have permission to perform this action!"
    ERROR_NOT_LOGIN = "You must be logged in to do this!"
    ERROR_MISSING_INFO = "Missing field!"
    ERROR_ALREADY_DONE = "This action is already done!"
    ERROR_OLD_PASSWORD = "The current password is incorrect!"
    NEW_PASSWORD_NOT_MATCH = "The entered password is not the same!"
    PROVIDE_PASSWORD = "Please provide your password!"
    ERROR_ALREADY_EMAIL = "Email address already exists!"
    ERROR_ALREADY_NAME = "Record already exists!"
    ERROR_NOT_ALREADY_WD_CODE = "WD code is not exists!"
    ERROR_ALREADY_RECORD = " already exists!"
    ERROR_NOT_ALREADY_RECORD = " not already exists!"
    ERROR_RECORD_NOT_DELETE = "Cannot be deleted!"
    ERROR_NOT_CORRECT_EXCEL_FORMAT = "File format must be xls or xlsx!"
    ERROR_NOT_CORRECT_COLUMN_NAME = "Excel sütun başlıkları doğru değildir."
    ERROR_NOT_CORRECT_COLUMN_ORDER = "Excel sütun sıralaması yanlıştır."
    ERROR_NOT_UNIQUE_VALUES = "Excel dosyasında aynı TC Kimlik No, Pasaport No ya da Email değeri içeren kayıtlar mevcut"
    ERROR_ALREADY_VERSION = "Version already exists!"
    ERROR_FIELD_REQUIRED = "Empty fields must be entered!"
    ERROR_ALREADY_USER = "User already exist!"
    ERROR_CHECK_DATA = ""
    ERROR_NOT_CORRECT_DATE_FORMAT = "kolonunda saat değeri olmamalıdır! (ÖR:DD.MM.YYYY)"
    ERROR_ALREADY_TCKN = "Tc kimlik no zaten kayıtlı!"
    ERROR_CHECK_COLUMN_NUMERIC = "Aşağıdaki sütunlar da sayı olmayan değerler bulunmaktadır.Listelenen sütunlar değerler sayı olmalıdır!"
    ERROR_NOT_CORRECT_VALUE = "Aşağıda excel dosyasından girilmiş olan "
    ERROR_WRONG_DATA = "Wrong parameter or input.."



class ErrorCodes:
    NOT_LOGIN_CODE = 10001
    NOT_OWNER = 10002
    NOT_FOUND = 10003
    BAD_REQUEST = 10004
    UNKNOWN = 10005
    CONFLICT = 1006
    NOT_CORRECT_PASSWORD = 1007
    NOT_MATCH_PASSWORD = 1008
    ALREADY_EMAIL = 1009
    ALREADY_NAME = 1010
    ALREADY_RECORD = 1011
    NOT_ALREADY_RECORD = 1012
    NOT_DELETE_CODE = 1013
    NOT_CORRECT_EXCEL_FORMAT = 1014
    NOT_CORRECT_COLUMN_NAME = 1015
    EXCEL_ROWS_EMPTY = 1016
    ALREADY_VERSION = 1017
    FIELD_REQUIRED = 1018
    CHECK_DATA = 1019
    NOT_CORRECT_COLUMN_ORDER = 1021
    NOT_ALREADY_WD_CODE = 1022
    ALREADY_USER = 1023
    NOT_CORRECT_DATE_FORMAT = 1024
    NOT_UNIQUE_RECORDS = 1025
    ALREADY_TCKN = 1026
    CHECK_COLUMN_NUMERIC = 1027
    NOT_CORRECT_VALUE = 1028
    PROVIDE_PASSWORD = 1029
    WRONG_DATA = 1030

class SuccessCodes:
    SUCCESS_LIST = 20000
    SUCCESS_CREATED = 20001
    SUCCESS_UPDATE = 20002
    SUCCESS_DETAIL = 20003
    SUCCESS_DELETE = 20004
    SUCCESS_CHANGE_PASSWORD = 20005
    SUCCESS_SAFE_DELETE = 20006
    NOT_FOUND_RECORD = 20007
    CHECK_MULTIPLE_DATA = 1020


def is_authenticated(request):
    return bool(request.user and request.user.is_authenticated)


def check_owner_for_model(request, model):
    model_type = type(model)
    if model_type is User and request.user == model.user:
        return True

    return False


def is_owner(request, model):
    if type(model) is User:
        return model == request.user or model == request.user.parent
    return request.user == model.user or model.user == request.user.parent


def get_not_authenticated_response():
    response = ResponseInfo().response
    response[ResponseInfo.ERROR_MESSAGE] = ErrorMessages.ERROR_NOT_LOGIN
    response[ResponseInfo.ERROR_CODE] = ErrorCodes.NOT_LOGIN_CODE

    return Response(response, status=HTTP_401_UNAUTHORIZED)


def get_not_owner_response():
    response = ResponseInfo().response
    response[ResponseInfo.ERROR_MESSAGE] = ErrorMessages.ERROR_NOT_OWNER
    response[ResponseInfo.ERROR_CODE] = ErrorCodes.NOT_OWNER

    return Response(response, status=HTTP_403_FORBIDDEN)


def get_not_found_response():
    response = ResponseInfo().response
    response[ResponseInfo.ERROR_MESSAGE] = ErrorMessages.ERROR_NOT_FOUND
    response[ResponseInfo.ERROR_CODE] = ErrorCodes.NOT_FOUND

    return Response(response, status=HTTP_204_NO_CONTENT)

def get_bad_parameter_response(data):
    response = ResponseInfo().response
    response[ResponseInfo.DATA] = data
    response[ResponseInfo.ERROR_MESSAGE] = ErrorMessages.ERROR_WRONG_DATA
    response[ResponseInfo.ERROR_CODE] = ErrorCodes.WRONG_DATA
    raise APIException(response)

def get_bad_request_response(exception, data=None):
    
    exp_list = list(exception.detail.keys())
    title = exp_list[0]
    message = exception.detail.get(title)[0]
    response = ResponseInfo().response
    response[ResponseInfo.ERROR_MESSAGE] = "{}: {}".format(title, message)
    response[ResponseInfo.ERROR_CODE] = ErrorCodes.BAD_REQUEST
    response[ResponseInfo.DATA] = data  # Include the data in the response
    return Response(response, status=HTTP_400_BAD_REQUEST)


def get_bad_request_key_response(key):
    response = ResponseInfo().response
    response[ResponseInfo.ERROR_MESSAGE] = "{}: {}".format(key, ErrorMessages.ERROR_MISSING_INFO)
    response[ResponseInfo.ERROR_CODE] = ErrorCodes.BAD_REQUEST

    return Response(response, status=HTTP_400_BAD_REQUEST)


def get_bad_request_message_response(exp):
    response = ResponseInfo().response
    response[ResponseInfo.ERROR_MESSAGE] = ErrorMessages.ERROR_UNKNOWN
    response[ResponseInfo.ERROR_CODE] = ErrorCodes.BAD_REQUEST
    response[ResponseInfo.ERROR_DETAIL] = str(exp)

    return Response(response, status=HTTP_400_BAD_REQUEST)


def get_unknown_error_response(exp):
    response = ResponseInfo().response
    response[ResponseInfo.ERROR_MESSAGE] = ErrorMessages.ERROR_UNKNOWN
    response[ResponseInfo.ERROR_CODE] = ErrorCodes.UNKNOWN
    response[ResponseInfo.ERROR_DETAIL] = str(exp)

    return Response(response, status=HTTP_501_NOT_IMPLEMENTED)


def get_already_done_response(model):
    response = ResponseInfo().response
    response[ResponseInfo.ERROR_MESSAGE] = ErrorMessages.ERROR_ALREADY_DONE
    response[ResponseInfo.ERROR_CODE] = ErrorCodes.CONFLICT
    response[ResponseInfo.DATA] = model

    return Response(response, status=HTTP_409_CONFLICT)


def get_deleted_successfully_response(model):
    response = ResponseInfo().response
    response[ResponseInfo.SUCCESS_MESSAGE] = SuccessMessages.DELETED_SUCCESSFULLY
    response[ResponseInfo.SUCCESS_CODE] = SuccessCodes.SUCCESS_DELETE
    response[ResponseInfo.DATA] = model
    response[ResponseInfo.ITEM_PER_PAGE] = "1"

    return Response(response, status=HTTP_200_OK)


def get_safe_deleted_successfully_response():
    response = ResponseInfo().response
    response[ResponseInfo.SUCCESS_MESSAGE] = SuccessMessages.SAFE_DELETED_SUCCESSFULLY
    response[ResponseInfo.SUCCESS_CODE] = SuccessCodes.SUCCESS_SAFE_DELETE
    response[ResponseInfo.ITEM_PER_PAGE] = "1"

    return Response(response, status=HTTP_200_OK)


def get_not_deleted_record_error_response(msg):
    response = ResponseInfo().response
    response[ResponseInfo.SUCCESS_MESSAGE] = msg + ErrorMessages.ERROR_RECORD_NOT_DELETE
    response[ResponseInfo.SUCCESS_CODE] = ErrorCodes.NOT_DELETE_CODE
    response[ResponseInfo.ITEM_PER_PAGE] = "1"

    return Response(response, status=HTTP_200_OK)


def get_created_successfully_response(model):
    response = ResponseInfo().response
    response[ResponseInfo.SUCCESS_MESSAGE] = SuccessMessages.CREATED_SUCCESSFULLY
    response[ResponseInfo.SUCCESS_CODE] = SuccessCodes.SUCCESS_CREATED
    response[ResponseInfo.DATA] = model
    response[ResponseInfo.ITEM_PER_PAGE] = "1"

    return Response(response, status=HTTP_201_CREATED)


def get_check_successfully_response(model):
    response = ResponseInfo().response
    response[ResponseInfo.SUCCESS_MESSAGE] = SuccessMessages.CHECK_SUCCESSFULLY
    response[ResponseInfo.SUCCESS_CODE] = SuccessCodes.SUCCESS_CREATED
    response[ResponseInfo.DATA] = model
    response[ResponseInfo.ITEM_PER_PAGE] = "1"

    return Response(response, status=HTTP_201_CREATED)


def get_check_excel_response(model):
    response = ResponseInfo().response
    response[ResponseInfo.SUCCESS_MESSAGE] = SuccessMessages.CREATED_SUCCESSFULLY
    response[ResponseInfo.SUCCESS_CODE] = SuccessCodes.SUCCESS_CREATED
    response[ResponseInfo.DATA] = model
    response[ResponseInfo.ITEM_PER_PAGE] = len(model)

    return Response(response, status=HTTP_201_CREATED)


def get_created_record_successfully_response(data=None):
    response = ResponseInfo().response
    response[ResponseInfo.SUCCESS_MESSAGE] = SuccessMessages.CREATED_SUCCESSFULLY
    response[ResponseInfo.SUCCESS_CODE] = SuccessCodes.SUCCESS_CREATED
    response[ResponseInfo.DATA] = data
    response[ResponseInfo.ITEM_PER_PAGE] = "1"

    return Response(response, status=HTTP_201_CREATED)


def get_not_found_record_response():
    response = ResponseInfo().response
    response[ResponseInfo.SUCCESS_MESSAGE] = SuccessMessages.NOT_FOUND_RECORD
    response[ResponseInfo.SUCCESS_CODE] = SuccessCodes.NOT_FOUND_RECORD

    return Response(response, status=HTTP_200_OK)


def get_updated_successfully_response(model):
    response = ResponseInfo().response
    response[ResponseInfo.SUCCESS_MESSAGE] = SuccessMessages.UPDATED_SUCCESSFULLY
    response[ResponseInfo.SUCCESS_CODE] = SuccessCodes.SUCCESS_UPDATE
    response[ResponseInfo.DATA] = model
    response[ResponseInfo.ITEM_PER_PAGE] = "1"

    return Response(response, status=HTTP_200_OK)


def get_detail_successfully_response(model):
    response = ResponseInfo().response
    response[ResponseInfo.DATA] = model
    response[ResponseInfo.SUCCESS_CODE] = SuccessCodes.SUCCESS_DETAIL
    response[ResponseInfo.SUCCESS_MESSAGE] = SuccessMessages.DETAIL_SUCCESSFULLY
    response[ResponseInfo.ITEM_PER_PAGE] = "1"

    return Response(response, status=HTTP_200_OK)


def get_list_successfully_response(params, data):
    response = ResponseInfo().response
    
    if 'count' in data:
        response[ResponseInfo.TOTAL_PAGE_COUNT] = int(data['count'] / 100) + 1
    
    if params.get("page"):
        response[ResponseInfo.ITEM_PER_PAGE] = len(data['results'])

    if params.get("page_size"):
        response[ResponseInfo.ITEM_PER_PAGE] = len(data['results'])
        response[ResponseInfo.PAGE] = params.get("page_size")
        if 'count' in data:
            response[ResponseInfo.TOTAL_PAGE_COUNT] = int(data['count'] / int(params.get("page_size"))) + 1

    response[ResponseInfo.DATA] = data
    response[ResponseInfo.SUCCESS_MESSAGE] = SuccessMessages.LIST_SUCCESSFULLY
    response[ResponseInfo.SUCCESS_CODE] = SuccessCodes.SUCCESS_LIST

    return Response(response, status=HTTP_200_OK)


def get_not_already_wd_code_error_response():
    response = ResponseInfo().response
    response[ResponseInfo.ERROR_MESSAGE] = ErrorMessages.ERROR_NOT_ALREADY_WD_CODE

    response[ResponseInfo.ERROR_CODE] = ErrorCodes.NOT_ALREADY_WD_CODE

    return Response(response, status=HTTP_409_CONFLICT)


def get_old_error_response():
    response = ResponseInfo().response
    response[ResponseInfo.ERROR_MESSAGE] = ErrorMessages.ERROR_OLD_PASSWORD
    response[ResponseInfo.ERROR_CODE] = ErrorCodes.NOT_CORRECT_PASSWORD

    return Response(response, status=HTTP_400_BAD_REQUEST)


def get_already_user_error_response():
    response = ResponseInfo().response
    response[ResponseInfo.ERROR_MESSAGE] = ErrorMessages.ERROR_ALREADY_USER
    response[ResponseInfo.ERROR_CODE] = ErrorCodes.ALREADY_USER
    return Response(response, status=HTTP_409_CONFLICT)


def get_new_password_error_response():
    response = ResponseInfo().response
    response[ResponseInfo.ERROR_MESSAGE] = ErrorMessages.NEW_PASSWORD_NOT_MATCH
    response[ResponseInfo.ERROR_CODE] = ErrorCodes.NOT_MATCH_PASSWORD

    return Response(response, status=HTTP_400_BAD_REQUEST)

def get_provide_password_error_response():
    response = ResponseInfo().response
    response[ResponseInfo.ERROR_MESSAGE] = ErrorMessages.PROVIDE_PASSWORD
    response[ResponseInfo.ERROR_CODE] = ErrorCodes.PROVIDE_PASSWORD
    return Response(response, status=HTTP_400_BAD_REQUEST)

def get_already_email_error_response():
    response = ResponseInfo().response
    response[ResponseInfo.ERROR_MESSAGE] = ErrorMessages.ERROR_ALREADY_EMAIL
    response[ResponseInfo.ERROR_CODE] = ErrorCodes.ALREADY_EMAIL

    return Response(response, status=HTTP_409_CONFLICT)


def get_already_name_error_response():
    response = ResponseInfo().response
    response[ResponseInfo.ERROR_MESSAGE] = ErrorMessages.ERROR_ALREADY_NAME

    response[ResponseInfo.ERROR_CODE] = ErrorCodes.ALREADY_NAME

    return Response(response, status=HTTP_409_CONFLICT)


def get_already_version_error_response():
    response = ResponseInfo().response
    response[ResponseInfo.ERROR_MESSAGE] = ErrorMessages.ERROR_ALREADY_VERSION

    response[ResponseInfo.ERROR_CODE] = ErrorCodes.ALREADY_VERSION

    return Response(response, status=HTTP_409_CONFLICT)


def get_already_tckn_error_response():
    response = ResponseInfo().response
    response[ResponseInfo.ERROR_MESSAGE] = ErrorMessages.ERROR_ALREADY_TCKN
    response[ResponseInfo.ERROR_CODE] = ErrorCodes.ALREADY_TCKN

    return Response(response, status=HTTP_409_CONFLICT)


def get_create_user_successfully_response():
    response = ResponseInfo().response
    response[ResponseInfo.SUCCESS_MESSAGE] = SuccessMessages.CREATED_USER_SUCCESSFULLY
    response[ResponseInfo.SUCCESS_CODE] = SuccessCodes.SUCCESS_CREATED
    response[ResponseInfo.ITEM_PER_PAGE] = "1"

    return Response(response, status=HTTP_201_CREATED)


def get_change_password_successfully_response():
    response = ResponseInfo().response
    response[ResponseInfo.SUCCESS_MESSAGE] = SuccessMessages.CHANGE_PASSWORD_SUCCESSFULLY
    response[ResponseInfo.SUCCESS_CODE] = SuccessCodes.SUCCESS_CHANGE_PASSWORD
    response[ResponseInfo.ITEM_PER_PAGE] = "1"

    return Response(response, status=HTTP_200_OK)


def get_file_format_check():
    response = ResponseInfo().response
    response[ResponseInfo.ERROR_MESSAGE] = ErrorMessages.ERROR_NOT_CORRECT_EXCEL_FORMAT

    response[ResponseInfo.ERROR_CODE] = ErrorCodes.NOT_CORRECT_EXCEL_FORMAT

    return Response(response, status=HTTP_404_NOT_FOUND)


def get_date_format_not_correct(msg):
    response = ResponseInfo().response
    response[ResponseInfo.ERROR_MESSAGE] = msg + " " + ErrorMessages.ERROR_NOT_CORRECT_DATE_FORMAT

    response[ResponseInfo.ERROR_CODE] = ErrorCodes.NOT_CORRECT_DATE_FORMAT

    return Response(response, status=HTTP_404_NOT_FOUND)


def get_excel_not_correct_column(msg, data):
    response = ResponseInfo().response
    response[ResponseInfo.ERROR_MESSAGE] = ErrorMessages.ERROR_NOT_CORRECT_COLUMN_NAME + " " + msg
    response[ResponseInfo.ERROR_CODE] = ErrorCodes.NOT_CORRECT_COLUMN_NAME
    response[ResponseInfo.DATA] = data
    response[ResponseInfo.ITEM_PER_PAGE] = len(data)
    
    return Response(response, status=HTTP_404_NOT_FOUND)


def get_excel_not_correct_column_order(data, msg=None):
    response = ResponseInfo().response
    response[ResponseInfo.ERROR_MESSAGE] = ErrorMessages.ERROR_NOT_CORRECT_COLUMN_ORDER + (msg or "") + " "
    response[ResponseInfo.ERROR_CODE] = ErrorCodes.NOT_CORRECT_COLUMN_ORDER
    response[ResponseInfo.ITEM_PER_PAGE] = 1
    response[ResponseInfo.DATA] = data

    return Response(response, status=HTTP_404_NOT_FOUND)


def get_excel_check_column_numeric(data):
    response = ResponseInfo().response
    response[ResponseInfo.ERROR_MESSAGE] = ErrorMessages.ERROR_CHECK_COLUMN_NUMERIC
    response[ResponseInfo.ERROR_CODE] = ErrorCodes.CHECK_COLUMN_NUMERIC
    response[ResponseInfo.ITEM_PER_PAGE] = 1
    response[ResponseInfo.DATA] = data

    return Response(response, status=HTTP_404_NOT_FOUND)


def get_excel_rows_empty_check(name):
    response = ResponseInfo().response
    response[ResponseInfo.ERROR_MESSAGE] = "{} sütunun da boş değer bulunmaktadır!".format(name)

    response[ResponseInfo.ERROR_CODE] = ErrorCodes.EXCEL_ROWS_EMPTY

    return Response(response, status=HTTP_404_NOT_FOUND)


def get_data_check(msg):
    response = ResponseInfo().response
    response[ResponseInfo.ERROR_MESSAGE] = msg
    response[ResponseInfo.ERROR_CODE] = ErrorCodes.CHECK_DATA

    return Response(response, status=HTTP_404_NOT_FOUND)


def get_multiple_data_check_error(msg, code, data):
    response = ResponseInfo().response
    ErrorMessages.ERROR_CHECK_DATA = msg
    response[ResponseInfo.ERROR_MESSAGE] = ErrorMessages.ERROR_CHECK_DATA
    response[ResponseInfo.ERROR_CODE] = code
    response[ResponseInfo.DATA] = data
    response[ResponseInfo.ITEM_PER_PAGE] = len(data)

    return Response(response, status=HTTP_404_NOT_FOUND)


def get_multiple_data_check(msg, code, data):
    response = ResponseInfo().response
    SuccessMessages.SUCCESS_CHECK_DATA = msg
    response[ResponseInfo.SUCCESS_MESSAGE] = SuccessMessages.SUCCESS_CHECK_DATA
    response[ResponseInfo.SUCCESS_CODE] = code
    response[ResponseInfo.DATA] = data
    response[ResponseInfo.ITEM_PER_PAGE] = len(data)

    return Response(response, status=HTTP_200_OK)


def get_field_required_check():
    response = ResponseInfo().response
    response[ResponseInfo.ERROR_MESSAGE] = ErrorMessages.ERROR_FIELD_REQUIRED

    response[ResponseInfo.ERROR_CODE] = ErrorCodes.FIELD_REQUIRED

    return Response(response, status=HTTP_404_NOT_FOUND)


def get_not_correct_value(msg, data):
    response = ResponseInfo().response
    response[ResponseInfo.ERROR_MESSAGE] = ErrorMessages.ERROR_NOT_CORRECT_VALUE + " " + msg
    response[ResponseInfo.ERROR_CODE] = ErrorCodes.NOT_CORRECT_VALUE
    response[ResponseInfo.DATA] = data
    response[ResponseInfo.ITEM_PER_PAGE] = len(data)

    return Response(response, status=HTTP_404_NOT_FOUND)
