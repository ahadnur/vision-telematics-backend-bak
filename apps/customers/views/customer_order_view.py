from django.db.models import Prefetch
from rest_framework.generics import RetrieveAPIView
from rest_framework.views import APIView

from apps.customers.models import Customer, CustomerVehicleInfo


class CustomerInfoForOrderAPIView(RetrieveAPIView):

	def get_queryset(self, request, pk):
		customers = Customer.objects.prefetch_related(
			Prefetch(
				'vehicles',
				queryset=CustomerVehicleInfo.objects.select_related('vehicle_make', 'vehicle_model', 'vehicle_type')
			),
			'customeraddress_set'
		).select_related('company').filter(id=pk)
	def get(self, request, *args, **kwargs):
		return self.retrieve(request, *args, **kwargs)

	# def retrieve(self, request, *args, **kwargs):
	# 	instance = self.get_object()
	# 	serializer = self.get_serializer(instance)
	# 	return Response(serializer.data)
