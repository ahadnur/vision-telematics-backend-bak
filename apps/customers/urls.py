from django.urls import path
from apps.customers.views import CompanyListAPIView

app_name = 'customers'

urlpatterns = [
    path('company-list/', CompanyListAPIView.as_view(), name='customer-list'),
    # path('get-company-to-cutomer-ref/')
]
