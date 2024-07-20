class ResponseInfo(object):
    SUCCESS_CODE = "successCode"
    SUCCESS_MESSAGE = "successMessage"
    ERROR_CODE = "errorCode"
    ERROR_MESSAGE = "errorMessage"
    ERROR_DETAIL = "errorDetail"
    DATA = "data"
    PAGE = "page_size"
    ITEM_PER_PAGE = "items_per_page"
    TOTAL_PAGE_COUNT = "total_page_count"

    def __init__(self, user=None, **args):
        from .ResponseHelper import SuccessMessages, ErrorCodes, ErrorMessages
        self.response = {
            "successCode": args.get('data', None),
            "successMessage": args.get('data', None),
            "errorCode": args.get('status', None),
            "errorMessage": args.get('error', None),
            "data": args.get('data', None),
            "total_page_count": args.get('total_page_count', None),
        }
