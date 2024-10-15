from rest_framework import viewsets
from rest_framework.permissions import (IsAuthenticated,
                                        DjangoModelPermissions)
from rest_framework.exceptions import ValidationError
from .models import FileImportExportStatus
from django.db import IntegrityError
from datetime import datetime
from helper.responseProcess.ResponseHelper import *
from core.pagination import LargeResultsSetPagination
from file_import_export.serializers import FileImportExportStatusSerializer
from helper.services.filter import import_export_status_filter


class ImportExpotStatusViewset(viewsets.ReadOnlyModelViewSet):
    queryset = FileImportExportStatus.objects.select_related('created_by').order_by('-id')
    serializer_class = FileImportExportStatusSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):

        fields = {
            'file_name': self.request.query_params.get('file_name'),
            'file_type': self.request.query_params.get('excel_type'),
            'file_process_type': self.request.query_params.get('file_process_type'),
            'started_at': self.request.query_params.get('started_at'),
            'finished_at': self.request.query_params.get('finished_at'),
            'created_by': self.request.query_params.get('created_by'),
            'file_status': self.request.query_params.get('file_status')
        }

        queryset = self.queryset
        if fields['file_process_type'] and fields['file_process_type'] == 'static':
            queryset = queryset.filter(file_process_type__in=['cmdd_static_import', 'cmdd_static_export', 'daily_report_management_static_import', 'manpowercomparison_static_import', 'manpoweronsite_static_import', 'sd_daily_report_static_import']) 
        else: 
            queryset = import_export_status_filter(queryset, fields)
        
        # for item in queryset:
        #     item.started_at = self.format_datetime(item.started_at)
        #     item.finished_at = self.format_datetime(item.finished_at)
        return queryset

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
        
    def format_datetime(self, datetime_str):
        try:
            # Convert to datetime object
            datetime_obj = datetime.fromisoformat(str(datetime_str))
            # Format the datetime object
            formatted_datetime = datetime_obj.strftime("%Y-%m-%d %H:%M:%S %Z%z")
            return formatted_datetime
        except Exception as e:
            # Handle the error gracefully, such as logging the error and returning None
            print(f"Error formatting datetime: {e}")
            return None