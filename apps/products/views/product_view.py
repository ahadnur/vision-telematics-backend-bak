from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView

from apps.products.models import Product
from apps.products.schemas.product_shema import product_list_response_schema, product_detail_response_schema
from apps.products.serializers import ProductSerializer


class ProductCreateAPIView(CreateAPIView):
	serializer_class = ProductSerializer
	queryset = Product.objects.filter(is_active=True, is_deleted=False)

	@swagger_auto_schema(
		tags=['Products'],
		request_body=ProductSerializer,
		responses={
			status.HTTP_200_OK: ProductSerializer(),
		}
	)
	def post(self, request, *args, **kwargs):
		return self.create(request, *args, **kwargs)


class ProductListAPIView(ListAPIView):
	serializer_class = ProductSerializer
	queryset = Product.objects.filter(is_active=True)

	@swagger_auto_schema(
		tags=['Products'],
		responses=product_list_response_schema
	)
	def get(self, request, *args, **kwargs):
		return self.list(request, *args, **kwargs)


class ProductDetailAPIVIew(RetrieveAPIView):
	serializer_class = ProductSerializer
	queryset = Product.objects.filter(is_active=True)
	lookup_field = 'pk'

	@swagger_auto_schema(
		tags=['Products'],
		responses=product_detail_response_schema
	)
	def get(self, request, *args, **kwargs):
		return self.retrieve(request, *args, **kwargs)

