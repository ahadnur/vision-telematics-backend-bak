import uuid

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.engineers.views import logger
from apps.products.models import Product, ProductSKU
from apps.products.schemas.product_shema import product_list_response_schema, product_detail_response_schema
from apps.products.serializers import ProductSerializer


class ProductCreateAPIView(CreateAPIView):
	serializer_class = ProductSerializer
	queryset = Product.active_objects.all()

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
	queryset = Product.objects.filter(is_active=True).order_by('-created_at')

	@swagger_auto_schema(
		tags=['Products'],
		responses=product_list_response_schema
	)
	def get(self, request, *args, **kwargs):
		return self.list(request, *args, **kwargs)


class ProductDetailAPIVIew(RetrieveAPIView):
	serializer_class = ProductSerializer
	queryset = Product.active_objects.all()
	lookup_field = 'pk'

	@swagger_auto_schema(
		tags=['Products'],
		responses=product_detail_response_schema
	)
	def get(self, request, *args, **kwargs):
		return self.retrieve(request, *args, **kwargs)


class ProductUpdateAPIView(APIView):
	serializer_class = ProductSerializer

	@swagger_auto_schema(
		tags=['Products'],
		request_body=ProductSerializer,
		responses={
			status.HTTP_200_OK: ProductSerializer(),
		}
	)
	def put(self, request, pk, *args, **kwargs):
		instance = Product.active_objects.filter(pk=pk).first()
		serializer = self.serializer_class(instance, data=request.data, partial=True)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		return Response(serializer.data, status=status.HTTP_200_OK)


class ProductDestroyAPIView(DestroyAPIView):
	serializer_class = ProductSerializer
	queryset = Product.active_objects.all()

	@swagger_auto_schema(
		tags=['Products'],
		responses={
			status.HTTP_204_NO_CONTENT: "Successfully deleted!",
		}
	)
	def delete(self, request, *args, **kwargs):
		return self.destroy(request, *args, **kwargs)

	def destroy(self, request, *args, **kwargs):
		try:
			instance = self.get_object()
			instance.is_deleted = True
			instance.is_active = False
			return Response(status=status.HTTP_204_NO_CONTENT)
		except Exception as e:
			logger.error(f'error on {e}')
			return Response(status=status.HTTP_400_BAD_REQUEST)


class GenerateProductSkuCodeAPIView(APIView):
	permission_classes = (AllowAny, )

	@swagger_auto_schema(
		tags=['Products'],
		responses={
			status.HTTP_200_OK: openapi.Schema(
				type=openapi.TYPE_OBJECT,
				properties={
					'sku_code': openapi.Schema(
						type=openapi.TYPE_STRING,
					)
				}
			),
		}
	)
	def get(self, request, *args, **kwargs):
		prefix = "SKU"
		while True:
			unique_code = f"{prefix}-{uuid.uuid4().hex[:8].upper()}"
			if not ProductSKU.objects.filter(sku_code=unique_code).exists():
				break
		return Response({"sku_code": unique_code})
