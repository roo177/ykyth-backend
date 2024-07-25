from django.urls import include, path
from rest_framework import routers
from .views import ImportExpotStatusViewset
router = routers.DefaultRouter()
router.register(r'work-design-import-status', ImportExpotStatusViewset, basename='work_design_import_status')
router.register(r'work-design-export-status', ImportExpotStatusViewset, basename='work_design_export_status')
router.register(r'ppr-design-import-status', ImportExpotStatusViewset, basename='ppr_design_import_status')
router.register(r'ppr-design-export-status', ImportExpotStatusViewset, basename='ppr_design_export_status')
router.register(r'material-management-import-status', ImportExpotStatusViewset, basename='material_management_import_status')
router.register(r'material-management-export-status', ImportExpotStatusViewset, basename='material_management_export_status')
router.register(r'thematic-plan-import-status', ImportExpotStatusViewset, basename='thematic_plan_import_status')
router.register(r'thematic-plan-export-status', ImportExpotStatusViewset, basename='thematic_plan_export_status')
router.register(r'site-obstacles-export-status', ImportExpotStatusViewset, basename='site_obstacles_export_status')
router.register(r'static-reports-status', ImportExpotStatusViewset, basename='static_reports_status')

urlpatterns = [
    path('', include(router.urls))
]
