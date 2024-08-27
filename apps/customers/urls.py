from django.urls import path
from apps.customers.views import CompanyListAPIView, CreateCustomerAPIView, CreateCustomerVehicleAPIView, \
    GetVehicleInfoAPIView

app_name = 'customers'

urlpatterns = [
    path('company-list/', CompanyListAPIView.as_view(), name='customer-list'),
    path('create-customer/', CreateCustomerAPIView.as_view(), name='customer-create'),
    path('create-vehicle-info/', CreateCustomerVehicleAPIView.as_view(), name='customer-vehicle-create'),
    path('get-vehicle-info/', GetVehicleInfoAPIView.as_view(), name='customer-get-vehicle-info'),
]
