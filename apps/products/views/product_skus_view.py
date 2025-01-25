from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import RetrieveAPIView

from apps.products.models import ProductSKU
from apps.products.serializers import GetProductSKUByProductIDSerializer


class ProductSkusListByProductID(RetrieveAPIView):
    serializer_class = GetProductSKUByProductIDSerializer
    lookup_field = 'product_id'

    def get_queryset(self):
        product_id = self.kwargs.get(self.lookup_field)
        return ProductSKU.objects.filter(product__id=product_id, is_active=True)


    @swagger_auto_schema(
        tags=['Product SKUs'],
        description='Get product SKUs by product id',
        responses={
            status.HTTP_200_OK: openapi.Response('Product SKU', GetProductSKUByProductIDSerializer),
        }
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)