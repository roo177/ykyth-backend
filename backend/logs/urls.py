from django.urls import include, path
from rest_framework import routers
# from .views import CombinedTaskLogsViewset

router = routers.DefaultRouter()
# router.register(r'combined-task-logs', CombinedTaskLogsViewset, basename='combined_task_logs')


urlpatterns = [
    path('', include(router.urls))
]
