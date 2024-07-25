from django.urls import include, path
from rest_framework import routers
from .views import UserViewSet, GroupsViewSet, MyObtainTokenPairView, ChangePasswordView, UserDeleteView

router = routers.DefaultRouter()
router.register(r'user', UserViewSet, basename="user")
router.register(r'group', GroupsViewSet)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('', include(router.urls)),
    path('login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('change-password/<str:pk>/', ChangePasswordView.as_view(), name='change_password'),
    path('user/<str:pk>/delete/', UserDeleteView.as_view(), name='user_delete'),  # Add this line for user deletion
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

