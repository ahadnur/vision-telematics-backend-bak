from django.urls import path

from apps.customers.views import CustomerVehicleForOrderDropdown, CustomerVehicleModelForOrderDropdown
from apps.orders.views import OrderCreateAPIView, OrderListAPIView, OrderRetrieveAPIView, OrderUpdateAPIView, \
	OrderDestroyAPIView

# from apps.customers.views

app_name = 'orders'

urlpatterns = [
	path('list/', OrderListAPIView.as_view(), name='list'),
	path('create/', OrderCreateAPIView.as_view(), name='order-create'),
	path('detail/<int:pk>/', OrderRetrieveAPIView.as_view(), name='order-retrieve'),
	path('update/<int:pk>/', OrderUpdateAPIView.as_view(), name='order-update'),
	path('delete/<int:pk>/', OrderDestroyAPIView.as_view(), name='order-delete'),

	path('customer-vehicles/<customer_id>/', CustomerVehicleForOrderDropdown.as_view(), name='customer-vehicle-list'),
	path('customer-vehicle-model/<vehicle_make_id>', CustomerVehicleModelForOrderDropdown.as_view(),
		 name='customer-vehicle-model-list'),
]
