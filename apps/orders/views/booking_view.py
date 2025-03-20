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
    serializer_class = BookingSerializer

    def get_queryset(self):
        queryset = Booking.active_objects.all().order_by('-created_at')
        engineer_id = self.request.query_params.get('engineer')
        if engineer_id:
            queryset = queryset.filter(engineer_id=engineer_id)
        return queryset

    @swagger_auto_schema(
        tags=['Booking'],
        manual_parameters=[
            openapi.Parameter(
                'engineer', 
                openapi.IN_QUERY, 
                description="Filter bookings by engineer ID", 
                type=openapi.TYPE_INTEGER
            ),
        ],
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


class BookingCreateAPIView(CreateAPIView):
    serializer_class = BookingSerializer
    queryset = Booking.active_objects.all()

    @swagger_auto_schema(
        tags=['Booking'],
        request_body=BookingSerializer,
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                description='Booking created',
                schema=BookingSerializer,
            )
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class BookingUpdateAPIView(APIView):
    @swagger_auto_schema(
        tags=['Booking'],
        request_body=BookingSerializer,
        responses={
            status.HTTP_200_OK: openapi.Response(
                description='Booking update success',
                schema=BookingSerializer(),
            )
        }
    )
    def put(self, request, pk, *args, **kwargs):
        try:
            booking = get_object_or_404(Booking, pk=pk, is_active=True, is_deleted=False)
            serializer = BookingSerializer(booking, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            validated_data = serializer.validated_data
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Booking.DoesNotExist:
            return Response({'error':'An error occurred'})


class BookingDestroyAPIView(DestroyAPIView):
    queryset = Booking.active_objects.all()
    serializer_class = BookingSerializer
    lookup_field = 'pk'

    @swagger_auto_schema(
        tags=['Booking'],
        responses={
            status.HTTP_204_NO_CONTENT: 'successfully deleted!',
        }
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        with transaction.atomic():
            booking_instance = self.get_object()
            booking_instance.is_active = False
            booking_instance.is_deleted = True
            booking_instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

