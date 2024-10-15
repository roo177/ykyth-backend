from django.shortcuts import render
from rest_framework import viewsets
from .models import IncomeQuantity
from libraries.models import ActivityType, ActivityTypeDetail
# Create your views here.
from .serializers import IncomeQuantitySerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import DjangoModelPermissions
from helper.pagination import *
from file_import_export.models import FileImportExportStatus
from helper.responseProcess.ResponseHelper import *
from helper.enums import *
import pandas as pd
from django.db import transaction
from django.utils import timezone
from django.db.utils import IntegrityError
from rest_framework.exceptions import ValidationError
from income.tasks import import_income_qty_task

class IncomeQtyImportViewset(viewsets.ModelViewSet):
    queryset = IncomeQuantity.objects.all().select_related('rep_month', 'l4_code')
    serializer_class = IncomeQuantitySerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    pagination_class = LargeResultsSetPagination

    def __init__(self, *args, **kwargs):
        self.file_type = FileTypeEnum.income_qty.value
        self.file_process_type = FileProcessTypeEnum.income_qty.value
        super().__init__(*args, **kwargs)

    def create(self, request, *args, **kwargs):
        file_status = FileImportExportStatus()
        try:
            if 'income_qty' in request.FILES:
                excel_file = request.FILES['income_qty']
                file_ext = excel_file.name.split('.')[-1].lower()

                if file_ext not in ('xls', 'xlsx'):
                    return get_file_format_check()

                # Read the Excel file into a DataFrame
                df = pd.read_excel(excel_file, header=None)
                # print(df.head())

                # Prepare the data for the import task
                file_status.file_name = excel_file.name
                file_status.file_type = self.file_type
                file_status.file_process_type = self.file_process_type
                file_status.started_at = timezone.now()
                file_status.finished_at = None
                file_status.created_by_id = request.user.id
                file_status.file_status = FileImportExportStatusEnum.loading.value
                file_status.save()

                file = {
                    'file_status_id': file_status.id,
                    'file_name': excel_file.name,
                    'df_data': df,  # Pass the DataFrame directly
                    'user_id': request.user.id,
                }

                # Call the import task
                import_income_qty_task(**file)

                return get_created_record_successfully_response()

        except (ValidationError, IntegrityError) as exp:
            if file_status.id:  # Only update status if file_status was created
                file_status.excel_export_status = FileImportExportStatusEnum.failed.value
                file_status.finished_at = timezone.now()
                file_status.save()
            return get_bad_request_message_response(exp)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.is_active = False
            instance.save()

            instance_info = {}
            user_fields = ['id', 'username', 'email'] 
            model_fields = ['id', 'is_active', 'created_at', 'updated_at']
            created_by = instance.created_by  

            if created_by:
                for field_name in user_fields:
                    field_value = getattr(created_by, field_name, None)
                    instance_info[f'created_by_{field_name}'] = field_value

            for field_name in model_fields:
                field_value = getattr(instance, field_name, None)
                instance_info[f'{field_name}'] = field_value

            # self.perform_destroy(instance)
            return get_deleted_successfully_response(instance_info)
        
        except (ValidationError, IntegrityError) as exp:
            return get_bad_request_response(exp)

    def list(self, request, *args, **kwargs):
        try:
            return get_list_successfully_response(request.GET, super().list(request, *args, **kwargs).data)
        except (ValidationError, IntegrityError) as exp:
            return get_bad_request_message_response(exp)

    def retrieve(self, request, *args, **kwargs):
        try:
            return get_detail_successfully_response(super().retrieve(request, *args, **kwargs).data)
        except (ValidationError, IntegrityError) as exp:
            return get_bad_request_message_response(exp)
        