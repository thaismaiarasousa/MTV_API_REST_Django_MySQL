from django.urls import path
from .views import CompanyView

urlpatterns = [
    path('companies/', CompanyView.as_view(), name='companies_list'),    # http://127.0.0.1:8000/api/companies/
    path('companies/<int:id>', CompanyView.as_view(), name='companies_process')    # http://127.0.0.1:8000/api/companies/2
]
