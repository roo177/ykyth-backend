from rest_framework import serializers
from .models import FileImportExportStatus


class FileImportExportStatusSerializer(serializers.ModelSerializer):
    created_by_email = serializers.CharField(source='created_by.email', read_only=True)

    class Meta:
        model = FileImportExportStatus
        fields = (
            'id', 'file_name', 'file_type', 'file_process_type', 'started_at', 'finished_at', 'created_by',
            'created_by_email', 'file_status')
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}
        read_only_fields = (
            'id', 'started_at', 'finished_at')
