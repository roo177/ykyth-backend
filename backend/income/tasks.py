import logging
# from celery import shared_task

# from helper.services.excel_export_service import ExcelExportService
from .util.import_income_qty import IncomeQtyImportService
# from .util.create_manpower_comparison_static import ManpowerComparisonStaticImportService
logger = logging.getLogger(__name__)


# @shared_task()
def import_income_qty_task(**kwargs):
    logger.info("*****Start Income Qty Import Task**********")
    IncomeQtyImportService.import_income_qty(**kwargs)
    logger.info("*****End Income Qtyt Task*************")




