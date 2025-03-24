import logging

from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.db.models import Prefetch, F, Q, ExpressionWrapper, DateTimeField, Value
from django.db.models.functions import Concat, Cast

from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, DestroyAPIView, CreateAPIView
from rest_framework.response import Response
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView

from apps.accounts.models import Account
from apps.orders.models import Order, Booking
from apps.orders.serializers import (
    BookingSerializer, 
    BookingDetailsSerializer,
)
from apps.orders.swagger_schema import booking_list_schema, booking_details_schema
from apps.common.enums import BookingStatusType
from apps.inventory.models import Inventory

logger = logging.getLogger(__name__)


class BookingListAPIView(ListAPIView):
    serializer_class = BookingSerializer

    def get_queryset(self):
        current_time = timezone.now()

        # Define expressions to compute start and end datetimes
        start_expr = Cast(
            Concat(F('booking_date'), Value(' '), F('booking_time')),
            output_field=DateTimeField()
        )
        end_expr = start_expr + F('duration')

        # Update bookings to COMPLETED
        Booking.active_objects.annotate(end=end_expr).filter(
            end__lt=current_time,
            booking_status__in=[BookingStatusType.SCHEDULED, BookingStatusType.IN_PROGRESS]
        ).update(booking_status=BookingStatusType.COMPLETED)

        # Update bookings to IN_PROGRESS
        Booking.active_objects.annotate(
            start=start_expr,
            end=end_expr
        ).filter(
            start__lte=current_time,
            end__gte=current_time,
            booking_status=BookingStatusType.SCHEDULED
        ).update(booking_status=BookingStatusType.IN_PROGRESS)

        # Proceed with the original queryset
        queryset = Booking.active_objects.all().order_by('-created_at')

        engineer_id = self.request.query_params.get('engineer')
        booking_status = self.request.query_params.get('booking_status')

        if engineer_id:
            queryset = queryset.filter(engineer_id=engineer_id)
        if booking_status:
            queryset = queryset.filter(booking_status=booking_status)
        
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
            openapi.Parameter(
                'booking_status', 
                openapi.IN_QUERY, 
                description="Filter bookings by Booking Status", 
                type=openapi.TYPE_STRING
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
            booking = get_object_or_404(
                Booking, pk=pk, is_active=True, is_deleted=False, 
                booking_status=BookingStatusType.SCHEDULED
            )

            new_status = request.data.get('booking_status')
            if new_status != BookingStatusType.SCHEDULED or new_status != BookingStatusType.CANCELLED:
                return Response(f"You can only change status to: {BookingStatusType.CANCELLED}")

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

