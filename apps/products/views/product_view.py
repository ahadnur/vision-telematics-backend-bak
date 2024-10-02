import logging

from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny

from apps.products.models import Product
from apps.products.schemas.product_shema import product_list_response_schema, product_detail_response_schema
from apps.products.serializers import ProductSerializer


class ProductListAPIView(ListAPIView):
	serializer_class = ProductSerializer
	permission_classes = [AllowAny]
	queryset = Product.objects.filter(is_active=True)

	@swagger_auto_schema(
		tags=['Product'],
		responses=product_list_response_schema
	)
	def get(self, request, *args, **kwargs):
		return self.list(request, *args, **kwargs)


class ProductDetailAPIVIew(RetrieveAPIView):
	permission_classes = [AllowAny, ]
	serializer_class = ProductSerializer
	queryset = Product.objects.filter(is_active=True)
	lookup_field = 'pk'

	@swagger_auto_schema(
		tags=['Product'],
		responses=product_detail_response_schema
	)
	def get(self, request, *args, **kwargs):
		return self.retrieve(request, *args, **kwargs)

