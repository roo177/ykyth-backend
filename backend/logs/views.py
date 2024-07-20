from django.shortcuts import render
from rest_framework import viewsets
# from .models import DailyReportCombinedTaskLogs    
# from .serializers import CombinedTaskLogsSerializer
from helper.pagination import LargeResultsSetPagination
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError
from helper.responseProcess.ResponseHelper import *
# Create your views here.

# class CombinedTaskLogsViewset(viewsets.ReadOnlyModelViewSet):
#     queryset = DailyReportCombinedTaskLogs.objects.all()
#     serializer_class = CombinedTaskLogsSerializer
#     permission_classes = [IsAuthenticated, DjangoModelPermissions]
#     pagination_class = LargeResultsSetPagination

#     def list(self, request, *args, **kwargs):
#         try:
#             return get_list_successfully_response(request.GET, super().list(request, *args, **kwargs).data, page_size=1000)
#         except (ValidationError, IntegrityError, ValueError) as exp:
#             return get_bad_request_message_response(exp)

#     def retrieve(self, request, *args, **kwargs):
#         try:
#             return get_detail_successfully_response(super().retrieve(request, *args, **kwargs).data)
#         except (ValidationError, IntegrityError,ValueError) as exp:
#             return get_bad_request_message_response(exp)
