from django.urls import path
from apps.customers.views import CustomerCompanyListAPIView, CustomerCreateAPIView, CreateCustomerVehicleAPIView, \
    GetVehicleInfoAPIView, CustomerUpdateAPIView, CustomerListAPIView, CustomerRetrieveAPIView

app_name = 'customers'

urlpatterns = [
    path('company-list/', CustomerCompanyListAPIView.as_view(), name='company-list'),
    path('list/', CustomerListAPIView.as_view(), name='customer-list'),
    path('create/', CustomerCreateAPIView.as_view(), name='customer-create'),
    path('detail/<int:pk>/', CustomerRetrieveAPIView.as_view(), name='customer-detail'),
    path('update/<pk>/', CustomerUpdateAPIView.as_view(), name='customer-update'),
    path('create-vehicle-info/', CreateCustomerVehicleAPIView.as_view(), name='customer-vehicle-create'),
    path('get-vehicle-info/', GetVehicleInfoAPIView.as_view(), name='customer-get-vehicle-info'),
]
