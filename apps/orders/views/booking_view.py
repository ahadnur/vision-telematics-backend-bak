import logging

from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, DestroyAPIView, CreateAPIView
from rest_framework.response import Response
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView

from apps.accounts.models import Account
from apps.customers.models import CustomerVehicle
from apps.orders.models import (
    Order, 
    OrderItem, 
    OrderOptionsData, 
    OrderPaymentOptions, 
    Booking, 
    OrderRefund, 
    ReturnItem
)
from apps.orders.serializers import (
    OrderSerializer, 
    OptionDataSerializer, 
    PaymentDataSerializer, 

    OrderReturnDetailSerializer,
    OrderReturnCreateSerializer,
    OrderReturnUpdateSerializer,
    
    OrderRefundSerializer,
    OrderRefundCreateSerializer,
    OrderRefundUpdateSerializer,

    BookingSerializer, 
    BookingDetailsSerializer,
)
from apps.orders.swagger_schema import booking_list_schema, booking_details_schema
from apps.products.models import ProductSKU
from apps.common.enums import ReturnStatusType, ShipmentMode, OperationChoice, CustomerPaymentStatusType
from apps.inventory.models import Inventory

logger = logging.getLogger(__name__)


class BookingListAPIView(ListAPIView):
    queryset = Booking.active_objects.all().order_by('-created_at')
    serializer_class = BookingSerializer

    @swagger_auto_schema(
        tags=['Booking'],
        responses={
            status.HTTP_200_OK: booking_list_schema
        }
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class BookingDetailsAPIView(RetrieveAPIView):
    queryset = Booking.active_objects.all().select_related(
        'order', 'engineer'
    )
    serializer_class = BookingDetailsSerializer

    @swagger_auto_schema(
        tags=['Booking'],
        responses={
            status.HTTP_200_OK: booking_details_schema
        }
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
