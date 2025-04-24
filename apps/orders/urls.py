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
	BookingCreateAPIView,
	BookingDestroyAPIView,
	BookingUpdateAPIView,

	CustomerInvoiceListAPIView,
	CustomerInvoiceDetailsAPIView,
	CustomerInvoiceCreateAPIView,
	CustomerInvoiceDestroyAPIView,
	CustomerInvoiceUpdateAPIView,

	# EngineerInvoiceListAPIView,
	# EngineerInvoiceDetailsAPIView,
	# EngineerInvoiceCreateAPIView,
	# EngineerInvoiceDestroyAPIView,
	# EngineerInvoiceUpdateAPIView,
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
	path('booking/create/', BookingCreateAPIView.as_view(), name='booking-create'),
	path('booking/update/<int:pk>/', BookingUpdateAPIView.as_view(), name='booking-update'),
	path('booking/delete/<int:pk>/', BookingDestroyAPIView.as_view(), name='booking-delete'),

	# customer invoice
	path('customer-invoice/list/', CustomerInvoiceListAPIView.as_view(), name='customer-invoice-list'),
	path('customer-invoice/<int:pk>/', CustomerInvoiceDetailsAPIView.as_view(), name='customer-invoice-retrieve'),
	path('customer-invoice/create/', CustomerInvoiceCreateAPIView.as_view(), name='customer-invoice-create'),
	path('customer-invoice/update/<int:pk>/', CustomerInvoiceUpdateAPIView.as_view(), name='customer-invoice-update'),
	path('customer-invoice/delete/<int:pk>/', CustomerInvoiceDestroyAPIView.as_view(), name='customer-invoice-delete'),

	# engineer invoice
	# path('engineer-invoice/list/', EngineerInvoiceListAPIView.as_view(), name='engineer-invoice-list'),
	# path('engineer-invoice/<int:pk>/', EngineerInvoiceDetailsAPIView.as_view(), name='engineer-invoice-retrieve'),
	# path('engineer-invoice/create/', EngineerInvoiceCreateAPIView.as_view(), name='engineer-invoice-create'),
	# path('engineer-invoice/update/<int:pk>/', EngineerInvoiceUpdateAPIView.as_view(), name='engineer-invoice-update'),
	# path('engineer-invoice/delete/<int:pk>/', EngineerInvoiceDestroyAPIView.as_view(), name='engineer-invoice-delete'),
]
