

from rest_framework.routers import DefaultRouter
from .views import CityView

router=DefaultRouter()

router.register(r'city',CityView,basename='city')


urlpatterns=router.urls

from django.urls import path
from .views import RegisterView, VerifyView, PhoneTokenObtainView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns += [
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/verify/', VerifyView.as_view(), name='verify'),
    path('api/token/phone/', PhoneTokenObtainView.as_view(), name='token_obtain_phone'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]