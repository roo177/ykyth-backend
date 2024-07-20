# subapp_logging/logging_utils.py

# from ..models import DailyReportCombinedTaskLogs
from django.db import connection

global_log_entries = []


# def log_data(log_type, log_detail):
#     global global_log_entries
#     global_log_entries.append(DailyReportCombinedTaskLogs(log_type=log_type, log_detail=log_detail[:250]))

# def delete_existing_logs():
#     DailyReportCombinedTaskLogs.objects.all().delete()
#     with connection.cursor() as cursor:
#         cursor.execute("ALTER SEQUENCE combined_task_logs_order_no_seq RESTART WITH 1")


# def write_logs_to_db():
#     global global_log_entries
#     DailyReportCombinedTaskLogs.objects.bulk_create(global_log_entries)

#     global_log_entries = []