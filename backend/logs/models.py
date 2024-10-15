from django.db import models

# Create your models here.

from django.db import models


# Create your models here.

class CriticalLogs(models.Model):
    error_type = models.CharField(max_length=60, null=True, blank=True)
    log_detail = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_created=True, auto_now=True)

    class Meta:
        verbose_name_plural = "CriticalLogs"
        db_table = "critical_logs"




# class DailyReportCombinedTaskLogs(models.Model):

#     order_no = models.AutoField(primary_key=True)  # Separate auto-increment field
#     log_type = models.CharField(max_length=60, null=True, blank=True)
#     log_detail = models.CharField(null=True, max_length=255, blank=True)
#     created_at = models.DateTimeField(auto_created=True, auto_now=True)

#     class Meta:
#         verbose_name_plural = "Combined Task Logs"
#         db_table = "combined_task_logs"
