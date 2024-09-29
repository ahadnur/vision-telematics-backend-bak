from django.urls import path
from apps.customers.views import CompanyListAPIView,CustomerCreateAPIView, CreateCustomerVehicleAPIView, \
    GetVehicleInfoAPIView, CustomerUpdateAPIView

app_name = 'customers'

urlpatterns = [
    path('company-list/', CompanyListAPIView.as_view(), name='customer-list'),
    path('customer-create/', CustomerCreateAPIView.as_view(), name='customer-create'),
    path('customer-update/<pk>/', CustomerUpdateAPIView.as_view(), name='customer-update'),
    path('create-vehicle-info/', CreateCustomerVehicleAPIView.as_view(), name='customer-vehicle-create'),
    path('get-vehicle-info/', GetVehicleInfoAPIView.as_view(), name='customer-get-vehicle-info'),
]
