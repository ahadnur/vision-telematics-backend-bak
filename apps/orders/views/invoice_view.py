from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, UpdateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView
import logging
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from apps.orders.models import CustomerInvoice, EngineerInvoice
from apps.orders.serializers import (
    CustomerInvoiceListSerializer,
    CustomerInvoiceSerializer, 
    EngineerInvoiceSerializer
)
from apps.common.enums import CustomerPaymentStatusType


logger = logging.getLogger(__name__)

################################ Customer Invoice ################################
class CustomerInvoiceListAPIView(ListAPIView):
    serializer_class = CustomerInvoiceListSerializer

    @swagger_auto_schema(
        tags=['Customer Invoice'],
        manual_parameters=[
            openapi.Parameter(
                'invoice_date_from', openapi.IN_QUERY,
                description="Filter invoices with invoice_date ≥ this date (YYYY-MM-DD)",
                type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE
            ),
            openapi.Parameter(
                'invoice_date_to', openapi.IN_QUERY,
                description="Filter invoices with invoice_date ≤ this date (YYYY-MM-DD)",
                type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE
            ),
            openapi.Parameter(
                'payment_status', openapi.IN_QUERY,
                description="Filter by payment status",
                type=openapi.TYPE_STRING,
                enum=[status for status, _ in CustomerPaymentStatusType.choices]
            ),
    ])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = CustomerInvoice.active_objects.all()
        params = self.request.query_params

        # filter by invoice_date range
        date_from = params.get('invoice_date_from')
        if date_from:
            d = parse_date(date_from)
            if d:
                queryset = queryset.filter(invoice_date__date__gte=d)

        date_to = params.get('invoice_date_to')
        if date_to:
            d = parse_date(date_to)
            if d:
                queryset = queryset.filter(invoice_date__date__lte=d)

        # filter by payment_status
        status = params.get('payment_status')
        if status in dict(CustomerPaymentStatusType.choices):
            queryset = queryset.filter(payment_status=status)

        return queryset.order_by('-invoice_date')


class CustomerInvoiceDetailsAPIView(RetrieveAPIView):
    queryset = CustomerInvoice.active_objects.all()
    lookup_field = 'pk'
    serializer_class = CustomerInvoiceSerializer

    @swagger_auto_schema(
        tags=['Customer Invoice'],
        responses={
            status.HTTP_200_OK : openapi.Response(
                description='Customer Invoice Details', 
                schema=CustomerInvoiceSerializer
            ),
            status.HTTP_404_NOT_FOUND: openapi.Response(
                description='Customer Invoice Not Found',
            )
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class CustomerInvoiceCreateAPIView(CreateAPIView):
    queryset = CustomerInvoice.active_objects.all()
    serializer_class = CustomerInvoiceSerializer

    @swagger_auto_schema(
        tags=['Customer Invoice'],
        request_body=CustomerInvoiceSerializer,
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                description='Customer invoice created',
                schema=CustomerInvoiceSerializer
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response('An error occurred'),
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class CustomerInvoiceUpdateAPIView(UpdateAPIView):
    http_method_names = ['put']
    queryset = CustomerInvoice.active_objects.all()

    @swagger_auto_schema(
        tags=['Customer Invoice'],
        request_body=CustomerInvoiceSerializer,
        responses={
            status.HTTP_200_OK: openapi.Response(
                description='Customer invoice update success',
                schema=CustomerInvoiceSerializer(),
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response('An error occurred')
        }
    )
    def put(self, request, pk, *args, **kwargs):
        try:
            invoice = get_object_or_404(
                CustomerInvoice, 
                pk=pk, is_active=True, 
                is_deleted=False
            )

            serializer = CustomerInvoiceSerializer(invoice, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            validated_data = serializer.validated_data
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except CustomerInvoice.DoesNotExist:
            return Response({'error':'An error occurred'})


class CustomerInvoiceDestroyAPIView(DestroyAPIView):
    queryset = CustomerInvoice.active_objects.all()
    serializer_class = CustomerInvoiceSerializer
    lookup_field = 'pk'

    @swagger_auto_schema(
        tags=['Customer Invoice'],
        responses={
            status.HTTP_204_NO_CONTENT: 'Successfully deleted',
        }
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        with transaction.atomic():
            invoice_instance = self.get_object()
            invoice_instance.is_active = False
            invoice_instance.is_deleted = True
            invoice_instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


################################ Engineer Invoice ################################

class EngineerInvoiceListAPIView(ListAPIView):
    serializer_class = EngineerInvoiceSerializer

    @swagger_auto_schema(
        tags=['Engineer Invoice'],
        manual_parameters=[
            openapi.Parameter(
                'invoice_date_from', openapi.IN_QUERY,
                description="Filter invoices with invoice_date ≥ this date (YYYY-MM-DD)",
                type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE
            ),
            openapi.Parameter(
                'invoice_date_to', openapi.IN_QUERY,
                description="Filter invoices with invoice_date ≤ this date (YYYY-MM-DD)",
                type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE
            )
    ])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = EngineerInvoice.active_objects.all()
        params = self.request.query_params

        # filter by invoice_date range
        date_from = params.get('invoice_date_from')
        if date_from:
            d = parse_date(date_from)
            if d:
                queryset = queryset.filter(invoice_date__date__gte=d)

        date_to = params.get('invoice_date_to')
        if date_to:
            d = parse_date(date_to)
            if d:
                queryset = queryset.filter(invoice_date__date__lte=d)

        return queryset.order_by('-invoice_date')


class EngineerInvoiceDetailsAPIView(RetrieveAPIView):
    queryset = EngineerInvoice.active_objects.all()
    lookup_field = 'pk'
    serializer_class = EngineerInvoiceSerializer

    @swagger_auto_schema(
        tags=['Engineer Invoice'],
        responses={
            status.HTTP_200_OK : openapi.Response(
                description='Engineer Invoice Details', 
                schema=EngineerInvoiceSerializer
            ),
            status.HTTP_404_NOT_FOUND: openapi.Response(
                description='Engineer Invoice Not Found',
            )
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class EngineerInvoiceCreateAPIView(CreateAPIView):
    queryset = EngineerInvoice.active_objects.all()
    serializer_class = EngineerInvoiceSerializer

    @swagger_auto_schema(
        tags=['Engineer Invoice'],
        request_body=EngineerInvoiceSerializer,
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                description='Engineer invoice created',
                schema=EngineerInvoiceSerializer
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response('An error occurred'),
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class EngineerInvoiceUpdateAPIView(UpdateAPIView):
    http_method_names = ['put']
    queryset = EngineerInvoice.active_objects.all()

    @swagger_auto_schema(
        tags=['Engineer Invoice'],
        request_body=EngineerInvoiceSerializer,
        responses={
            status.HTTP_200_OK: openapi.Response(
                description='Engineer invoice update success',
                schema=EngineerInvoiceSerializer(),
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response('An error occurred')
        }
    )
    def put(self, request, pk, *args, **kwargs):
        try:
            invoice = get_object_or_404(
                EngineerInvoice, 
                pk=pk, is_active=True, 
                is_deleted=False
            )

            serializer = EngineerInvoiceSerializer(invoice, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            validated_data = serializer.validated_data
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except EngineerInvoice.DoesNotExist:
            return Response({'error':'An error occurred'})


class EngineerInvoiceDestroyAPIView(DestroyAPIView):
    queryset = EngineerInvoice.active_objects.all()
    serializer_class = EngineerInvoiceSerializer
    lookup_field = 'pk'

    @swagger_auto_schema(
        tags=['Engineer Invoice'],
        responses={
            status.HTTP_204_NO_CONTENT: 'Successfully deleted',
        }
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        with transaction.atomic():
            invoice_instance = self.get_object()
            invoice_instance.is_active = False
            invoice_instance.is_deleted = True
            invoice_instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)