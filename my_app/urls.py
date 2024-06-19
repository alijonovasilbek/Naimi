from rest_framework.routers import DefaultRouter
from .views import RegisterView, VerifyView, PhoneTokenObtainView, CityView, ProfileViewSet, LoginView

from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()

router.register(r'city', CityView, basename='city')
router.register('profile', ProfileViewSet, basename='profile')

urlpatterns = router.urls

urlpatterns += [
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/code/', LoginView.as_view(), name='code'),
    path('api/verify/', VerifyView.as_view(), name='verify'),
    path('api/token/phone/', PhoneTokenObtainView.as_view(), name='token_obtain_phone'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]