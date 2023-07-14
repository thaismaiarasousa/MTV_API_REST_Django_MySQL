from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import CompanyView

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('companies/', CompanyView.as_view(), name='companies_list'),    # http://127.0.0.1:8000/api/companies/
    path('companies/<int:id>/', CompanyView.as_view(), name='companies_process')    # http://127.0.0.1:8000/api/companies/2/
]
