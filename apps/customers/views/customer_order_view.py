from django.db.models import Prefetch
from rest_framework.views import APIView

from apps.customers.models import Customer, CustomerVehicleInfo


class CustomerInfoForOrderAPIView(APIView):
	def get(self, request, pk):
		customers = Customer.objects.prefetch_related(
			Prefetch(
				'vehicles',
				queryset=CustomerVehicleInfo.objects.select_related('vehicle_make', 'vehicle_model', 'vehicle_type')
			),
			'customeraddress_set'
		).filter(id=pk)
