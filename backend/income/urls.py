from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import IncomeQtyImportViewset

router = DefaultRouter()
router.register(r'import', IncomeQtyImportViewset, basename='income-qty-import')

urlpatterns = [
    path('', include(router.urls)),
]   