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


class CustomerInvoiceListAPIView(ListAPIView):
    serializer_class = CustomerInvoiceListSerializer

    @swagger_auto_schema(manual_parameters=[
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
        qs = CustomerInvoice.active_objects.all()
        params = self.request.query_params

        # filter by invoice_date range
        date_from = params.get('invoice_date_from')
        if date_from:
            d = parse_date(date_from)
            if d:
                qs = qs.filter(invoice_date__date__gte=d)

        date_to = params.get('invoice_date_to')
        if date_to:
            d = parse_date(date_to)
            if d:
                qs = qs.filter(invoice_date__date__lte=d)

        # filter by payment_status
        status = params.get('payment_status')
        if status in dict(CustomerPaymentStatusType.choices):
            qs = qs.filter(payment_status=status)

        return qs.order_by('-invoice_date')