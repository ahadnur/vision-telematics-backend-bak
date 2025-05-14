from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView, DestroyAPIView, CreateAPIView, UpdateAPIView
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from django.utils.dateparse import parse_date
from django.db.models import Q

from apps.customers.models import Customer, CustomerFeedback
from apps.customers.serializers import CustomerFeedbackSerializer, CustomerFeedbackCreateSerializer
import logging

logger = logging.getLogger(__name__)


class CustomerFeedbackListAPIView(ListAPIView):
    queryset = CustomerFeedback.active_objects.all()
    serializer_class = CustomerFeedbackSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        params = self.request.query_params

        customer = params.get('customer')
        product = params.get('product')
        rating = params.get('rating')
        status_ = params.get('status')
        order = params.get('order')
        created_from = params.get('created_from')
        created_to = params.get('created_to')

        if customer:
            queryset = queryset.filter(customer_id=customer)
        if product:
            queryset = queryset.filter(product_id=product)
        if rating:
            queryset = queryset.filter(rating=rating)
        if status_:
            queryset = queryset.filter(status=status_)
        if order:
            queryset = queryset.filter(order=order)
        if created_from:
            queryset = queryset.filter(created_at__gte=parse_date(created_from))
        if created_to:
            queryset = queryset.filter(created_at__lte=parse_date(created_to))

        return queryset

    @swagger_auto_schema(
        tags=['Customer Feedback'],
        manual_parameters=[
            openapi.Parameter('paginated', openapi.IN_QUERY, description="Enable or disable pagination", type=openapi.TYPE_BOOLEAN),
            openapi.Parameter('customer', openapi.IN_QUERY, description="Filter by customer ID", type=openapi.TYPE_INTEGER),
            openapi.Parameter('product', openapi.IN_QUERY, description="Filter by product ID", type=openapi.TYPE_INTEGER),
            openapi.Parameter('rating', openapi.IN_QUERY, description="Filter by rating (1-10 or 1-5)", type=openapi.TYPE_INTEGER),
            openapi.Parameter('status', openapi.IN_QUERY, description="Filter by status", type=openapi.TYPE_STRING),
            openapi.Parameter('order', openapi.IN_QUERY, description="Filter by order ID", type=openapi.TYPE_INTEGER),
            openapi.Parameter('created_from', openapi.IN_QUERY, description="Filter feedbacks created from date (YYYY-MM-DD)", type=openapi.TYPE_STRING, format='date'),
            openapi.Parameter('created_to', openapi.IN_QUERY, description="Filter feedbacks created up to date (YYYY-MM-DD)", type=openapi.TYPE_STRING, format='date'),
        ],
        responses={
            status.HTTP_200_OK: openapi.Response(
                description='List of filtered customer feedbacks',
                schema=CustomerFeedbackSerializer,
            ),
            status.HTTP_400_BAD_REQUEST: "Bad request"
        }
    )
    def get(self, request, *args, **kwargs):
        paginated = request.query_params.get('paginated', 'true').lower() == 'true'
        if not paginated:
            self.pagination_class = None
        return self.list(request, *args, **kwargs)


class CustomerFeedbackRetrieveAPIView(RetrieveAPIView):
    queryset = CustomerFeedback.active_objects.all()
    serializer_class = CustomerFeedbackSerializer
    lookup_field = 'pk'

    @swagger_auto_schema(
        tags=['Customer Feedback'],
        responses={
            status.HTTP_200_OK: openapi.Response(
                description='A single customer feedback',
                schema=CustomerFeedbackSerializer()
            ),
            status.HTTP_404_NOT_FOUND: 'Feedback not found'
        }
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class CustomerFeedbackCreateAPIView(CreateAPIView):
    serializer_class = CustomerFeedbackCreateSerializer
    queryset = CustomerFeedback.active_objects.all()

    @swagger_auto_schema(
        tags=['Customer Feedback'],
        request_body=CustomerFeedbackCreateSerializer,
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                description='Customer Feedback created',
                schema=CustomerFeedbackSerializer(),
            ),
            status.HTTP_400_BAD_REQUEST: 'An error occurred'
        }
    )
    def post(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class CustomerFeedbackUpdateAPIView(UpdateAPIView):
    serializer_class = CustomerFeedbackSerializer
    queryset = CustomerFeedback.active_objects.all()
    lookup_field = 'pk'
    http_method_names = ['put']

    @swagger_auto_schema(
        tags=['Customer Feedback'],
        request_body=CustomerFeedbackSerializer,
        responses={
            status.HTTP_200_OK: openapi.Response(
                description='Feedback updated',
                schema=CustomerFeedbackSerializer(),
            ),
            status.HTTP_404_NOT_FOUND: 'Feedback not found',
            status.HTTP_400_BAD_REQUEST: 'An error occurred',
        }
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)


class CustomerFeedbackDestroyAPIView(DestroyAPIView):
    queryset = CustomerFeedback.active_objects.all()
    
    @swagger_auto_schema(
        tags=['Customer Feedback'],
        responses={
            status.HTTP_204_NO_CONTENT: 'Successfully deleted',
        }
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.is_deleted = True
            instance.is_active = False
            instance.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logger.error(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)