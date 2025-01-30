from django.urls import path
from apps.customers.views import (CustomerCreateAPIView, CreateCustomerVehicleAPIView,
    GetVehicleInfoAPIView, CustomerUpdateAPIView, CustomerListAPIView, CustomerRetrieveAPIView, CustomerDestroyAPIView)
from apps.customers.views.customer_utils_view import (CustomerDropdownListAPIView, CustomerVehicleListAPIView,
    CustomerSpecificVehicleListAPIView)

app_name = 'customers'

urlpatterns = [
    path('list/', CustomerListAPIView.as_view(), name='customer-list'),
    path('create/', CustomerCreateAPIView.as_view(), name='customer-create'),
    path('detail/<int:pk>/', CustomerRetrieveAPIView.as_view(), name='customer-detail'),
    path('update/<pk>/', CustomerUpdateAPIView.as_view(), name='customer-update'),
    path('delete/<pk>/', CustomerDestroyAPIView.as_view(), name='customer-delete'),
    path('create-vehicle-info/', CreateCustomerVehicleAPIView.as_view(), name='customer-vehicle-create'),
    path('get-vehicle-info/', GetVehicleInfoAPIView.as_view(), name='customer-get-vehicle-info'),
    path('customer-dropdown-list/', CustomerDropdownListAPIView.as_view(), name='customer-dropdown-list'),
    path('customer-vehicle-list/', CustomerVehicleListAPIView.as_view(), name='customer-vehicle-list'),
    path('custmer-specifiv-vehicle-list/<customer_id>/', CustomerSpecificVehicleListAPIView.as_view(),
         name='customer-specific-vehicle-list'),
]
