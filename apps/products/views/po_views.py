from django.db import transaction

from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from apps.products.models import PO
from apps.products.serializers import (
    POListSerializer,
    POCreateSerializer,
    POUpdateSerializer,
    PORetrieveSerializer
)
from apps.inventory.models import Inventory, StockMovement
from apps.common.enums import OperationChoice


class POListView(generics.ListAPIView):
    serializer_class = POListSerializer
    queryset = PO.active_objects.select_related('supplier', 'product_sku').all()

    @swagger_auto_schema(
        tags=['Purchase Order'],
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="PO List",
                schema=POListSerializer()
            )
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class POCreateView(generics.CreateAPIView):
    queryset = PO.active_objects.select_related('supplier', 'product_sku').all()
    serializer_class = POCreateSerializer

    @swagger_auto_schema(
        tags=['Purchase Order'],
        request_body=POCreateSerializer,
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                description="Creaded Purchase order",
                schema=POCreateSerializer()
            )
        }
    )
    def post(self, request, *args, **kwargs):
        with transaction.atomic():
            response = super().post(request, *args, **kwargs)
            po_instance = self.get_queryset().filter(po_ref=response.data['po_ref']).first()
            if po_instance and po_instance.received:
                inventory, _ = Inventory.objects.get_or_create(product_sku=po_instance.product_sku)

                inventory.update_stock(
                    quantity=po_instance.qty,
                    operation_type=OperationChoice.ADD.value,
                    reason="Purchase Order Received",
                    reference=po_instance.po_ref
                )
                # Update ProductSKU quantity
                product_sku = po_instance.product_sku
                product_sku.qty += po_instance.qty
                product_sku.save()
        return response


class PORetrieveView(generics.RetrieveAPIView):
    serializer_class = PORetrieveSerializer
    queryset = PO.active_objects.select_related('supplier', 'product_sku').all()
    lookup_field = 'id'

    @swagger_auto_schema(
        tags=['Purchase Order'],
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Retrieve details of a specific po",
                schema=PORetrieveSerializer()
            )
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class POUpdateView(generics.UpdateAPIView):
    http_method_names = ['put']
    serializer_class = POUpdateSerializer
    queryset = PO.active_objects.all()
    lookup_field = 'id'

    @swagger_auto_schema(
        tags=['Purchase Order'],
        request_body=POUpdateSerializer,
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="PO Updated successfully",
                schema=POUpdateSerializer()
            )
        }
    )
    def put(self, request, *args, **kwargs):
        with transaction.atomic():
            response = super().put(request, *args, **kwargs)
            po_instance = self.get_queryset().filter(id=kwargs['id']).first()
            if po_instance and po_instance.received:
                inventory, _ = Inventory.objects.get_or_create(product_sku=po_instance.product_sku)

                inventory.update_stock(
                    quantity=po_instance.qty,
                    operation_type=OperationChoice.ADD.value,
                    reason="Purchase Order Received",
                    reference=po_instance.po_ref
                )
                # Update ProductSKU quantity
                product_sku = po_instance.product_sku
                product_sku.qty += po_instance.qty
                product_sku.save()
                
        return response


class PODeleteView(generics.DestroyAPIView):
    lookup_field = 'id'
    queryset = PO.active_objects.all()
    serializer_class = PORetrieveSerializer

    @swagger_auto_schema(
        tags=['Purchase Order'],
        responses={
            status.HTTP_204_NO_CONTENT:"Successfully deleted!",
        }
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        with transaction.atomic():
            po_instance = self.get_object()
            po_instance.is_active = False
            po_instance.is_deleted = True
            po_instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)