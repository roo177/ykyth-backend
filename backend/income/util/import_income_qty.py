import pandas as pd
from datetime import datetime
from django.db import transaction
from income.models import IncomeQuantity, L4Code
from constants.models import RepMonth
from file_import_export.models import FileImportExportStatus
from helper.enums import FileImportExportStatusEnum
import logging
from helper.responseProcess.ResponseHelper import *
from django.utils import timezone
from libraries.models import ActivityTypeDetailIncome
logger = logging.getLogger(__name__)

class IncomeQtyImportService:

    @staticmethod
    def import_income_qty(**kwargs):
        file_status = FileImportExportStatus.objects.get(id=kwargs['file_status_id'])
        user_id = kwargs['user_id']
        
        # Create mappings for foreign key fields
        rep_month_dict = {rep_month.rep_month: rep_month.id for rep_month in RepMonth.objects.all()}
        l4_code_dict = {
            f"{l4_code.aygm_code}-{l4_code.activity_type.description}": l4_code.id 
            for l4_code in L4Code.objects.filter(aygm_code__isnull=False)
        }
        activity_detail_dict = {
            f"{activity_detail.description}": activity_detail.id 
            for activity_detail in ActivityTypeDetailIncome.objects.all()
        }
        # Load data into DataFrame
        df = kwargs['df_data']  # Ensure df_data is a DataFrame
        df.columns = df.iloc[0]  # Set headers from the first row
        df = df[1:]  # Skip the header row

        # Unpivot DataFrame
        df_melted = pd.melt(df, id_vars=['rep_month', 'aygm_poz', 'tip', 'detay'], 
                             var_name='month', value_name='qty')
        
        # Convert 'month' to datetime and handle 'qty'
        df_melted['month'] = pd.to_datetime(df_melted['month'], format='%Y-%m-%d %H:%M:%S').dt.date
        df_melted['qty'] = pd.to_numeric(df_melted['qty'], errors='coerce')
        df_melted.dropna(subset=['qty'], inplace=True)
        # Prepare data for bulk insertion
        income_records = []
        for _, row in df_melted.iterrows():
            rep_month_id = rep_month_dict.get(str(row['rep_month']))
            l4_code_id = l4_code_dict.get(f"{str(row['aygm_poz'])}-{str(row['tip'])}")
            activity_detail_id = activity_detail_dict.get(str(row['detay']))
            
            if rep_month_id and l4_code_id and row['qty'] != 0 and not pd.isnull(row['qty']):
                income_records.append(
                    IncomeQuantity(
                        rep_month_id=rep_month_id,
                        l4_code_id=l4_code_id,
                        activity_detail_id=activity_detail_id,
                        inc_month=row['month'],
                        inc_qty=row['qty']
                    )
                )

        # Save records to the database
        try:
            with transaction.atomic():
                # Delete existing records for the given rep_month_id (if needed)
                if income_records:
                    IncomeQuantity.objects.filter(rep_month_id=rep_month_id).delete()
                    IncomeQuantity.objects.bulk_create(income_records)
                
                # Update file status
                file_status.file_status = FileImportExportStatusEnum.completed.value
                file_status.save()

        except Exception as exp:
            logger.error(exp)
            file_status.file_status = FileImportExportStatusEnum.failed.value
            file_status.finished_at = timezone.now()
            file_status.save()
            return get_bad_request_message_response(exp)
