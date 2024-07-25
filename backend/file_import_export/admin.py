from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import FileImportExportStatus


@admin.register(FileImportExportStatus)
class FileImportExportStatusAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('File Name'), {'fields': ('file_name',)}),
    )

    list_display = (
        'file_name', 'file_type', 'file_process_type', 'started_at', 'finished_at', 'created_by', 'file_status', 'path')
    search_fields = (
        'file_name', 'file_type', 'file_process_type', 'file_status'
    )
    ordering = (
        'file_name', 'file_type', 'file_status', 'started_at', 'finished_at')
