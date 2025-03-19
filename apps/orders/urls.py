from django.urls import path

from apps.customers.views import CustomerVehicleForOrderDropdown, CustomerVehicleModelForOrderDropdown
from apps.orders.views import (
	OrderCreateAPIView, 
	OrderListAPIView, 
	OrderRetrieveAPIView, 
	OrderUpdateAPIView, 
	OrderDestroyAPIView, 

	OrderStatusChangeAPIView,

	OrderReturnCreateAPIView,
	OrderReturnUpdateAPIView,
	OrderReturnRetrieveAPIView,
	OrderReturnDestroyAPIView,
	OrderReturnListAPIView,

	OrderRefundListAPIView,
	OrderRefundRetrieveAPIView,
	OrderRefundCreateAPIView,
	OrderRefundUpdateAPIView,
	OrderRefundDestroyAPIView,

	BookingListAPIView,
	BookingDetailsAPIView,
)


app_name = 'orders'

urlpatterns = [
	path('list/', OrderListAPIView.as_view(), name='list'),
	path('create/', OrderCreateAPIView.as_view(), name='order-create'),
	path('detail/<int:pk>/', OrderRetrieveAPIView.as_view(), name='order-retrieve'),
	path('update/<int:pk>/', OrderUpdateAPIView.as_view(), name='order-update'),
	path('delete/<int:pk>/', OrderDestroyAPIView.as_view(), name='order-delete'),
	path('change-status/<int:pk>/', OrderStatusChangeAPIView.as_view(), name='order-status-change'),

	path('customer-vehicles/<customer_id>/', CustomerVehicleForOrderDropdown.as_view(), name='customer-vehicle-list'),
	path('customer-vehicle-model/<vehicle_make_name>', CustomerVehicleModelForOrderDropdown.as_view(),
		 name='customer-vehicle-model-list'),
	
	# return 
	path('return/list/', OrderReturnListAPIView.as_view(), name='order-return-list'),
	path('return/<int:pk>/', OrderReturnRetrieveAPIView.as_view(), name='order-return-retrieve'),
	path('return/create/', OrderReturnCreateAPIView.as_view(), name='order-return-create'),
	path('return/update/<int:pk>/', OrderReturnUpdateAPIView.as_view(), name='order-return-update'),
	path('return/delete/<int:pk>/', OrderReturnDestroyAPIView.as_view(), name='order-return-delete'),

	# refunds
	path('refund/list/', OrderRefundListAPIView.as_view(), name='order-refund-list'),
	path('refund/<int:pk>/', OrderRefundRetrieveAPIView.as_view(), name='order-refund-retrieve'),
	path('refund/create/', OrderRefundCreateAPIView.as_view(), name='order-refund-create'),
	path('refund/update/<int:pk>/', OrderRefundUpdateAPIView.as_view(), name='order-refund-update'),
	path('refund/delete/<int:pk>/', OrderRefundDestroyAPIView.as_view(), name='order-refund-delete'),

	# booking
	path('booking/list/', BookingListAPIView.as_view(), name='booking-list'),
	path('booking/<int:pk>/', BookingDetailsAPIView.as_view(), name='booking-retrieve'),
]
