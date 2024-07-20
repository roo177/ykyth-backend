from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import CriticalLogs


@admin.register(CriticalLogs)
class CriticalLogsAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('Error Type'), {'fields': ('error_type',)}),
        (_('Log Detail'), {'fields': ('log_detail',)}),
    )

    list_display = ('error_type', 'log_detail', 'created_at')
    search_fields = ('error_type', 'log_detail')
    ordering = ('error_type', 'log_detail', 'created_at')
