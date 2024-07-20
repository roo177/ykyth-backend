def account_filter(queryset, fields):
    if fields['username']:
        queryset = queryset.filter(username__exact=fields['username'])
    if fields['email']:
        queryset = queryset.filter(email__exact=fields['email'])

    return queryset

def import_export_status_filter(queryset, fields):
    if fields['file_name']:
        queryset = queryset.filter(file_name__icontains=fields['file_name'])
    if fields['file_type']:
        queryset = queryset.filter(file_type__exact=fields['file_type'])
    if fields['file_process_type']:
        queryset = queryset.filter(file_process_type__exact=fields['file_process_type'])
    if fields['started_at']:
        queryset = queryset.filter(started_at__exact=fields['started_at'])
    if fields['finished_at']:
        queryset = queryset.filter(finished_at__exact=fields['finished_at'])
    if fields['created_by']:
        queryset = queryset.filter(created_by__email__icontains=fields['building_code'])

    if fields['file_status']:
        queryset = queryset.filter(file_status__icontains=fields['excel_import_status'])
    return queryset
