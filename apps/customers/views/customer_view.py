from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView, DestroyAPIView
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from django.utils.dateparse import parse_date
from django.db.models import Q

from apps.customers.models import Customer, CustomerFeedback
from apps.customers.serializers import CustomerWriteSerializer, GetCustomerSerializer, CustomerFeedbackSerializer
from apps.customers.schemas import customer_list_response_schema, customer_create_response_schema
import logging

logger = logging.getLogger(__name__)


class CustomerListAPIView(ListAPIView):
    queryset = Customer.active_objects.all().order_by('-created_at')
    serializer_class = GetCustomerSerializer

    @swagger_auto_schema(
        tags=['Customer'],
        manual_parameters=[
            openapi.Parameter(
                'paginated',
                openapi.IN_QUERY,
                description="Enable or disable pagination (true or false)",
                type=openapi.TYPE_BOOLEAN,
                required=False,
                default=True
            )
        ],
        responses={
            status.HTTP_200_OK: openapi.Response(
                description='List of customers',
                schema=customer_list_response_schema,
            ),
            status.HTTP_400_BAD_REQUEST: "Bad request"
        }
    )
    def get(self, request, *args, **kwargs):
        paginated = request.query_params.get('paginated', 'true').lower() == 'true'
        if not paginated:
            self.pagination_class = None
        return self.list(request, *args, **kwargs)


class CustomerCreateAPIView(APIView):
    @swagger_auto_schema(
        tags=['Customer'],
        request_body=CustomerWriteSerializer,
        responses={
            status.HTTP_201_CREATED: customer_create_response_schema
        }
    )
    def post(self, request, *args, **kwargs):
        try:
            serializer = CustomerWriteSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'message': 'Customer created successfully.'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"create customer error on {e}")
            return Response(status=status.HTTP_400_BAD_REQUEST)


class CustomerRetrieveAPIView(RetrieveAPIView):
    serializer_class = GetCustomerSerializer
    queryset = Customer.active_objects.all()
    lookup_field = 'pk'

    @swagger_auto_schema(
        tags=['Customer'],
        responses={
            status.HTTP_200_OK: openapi.Response(
                description='Get customer',
                schema=GetCustomerSerializer
            )
        }
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class CustomerUpdateAPIView(APIView):
    @swagger_auto_schema(
        tags=['Customer'],
        request_body=CustomerWriteSerializer,
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                description='Created customer',
                schema=CustomerWriteSerializer
            )
        }
    )
    def post(self, request, pk):
        try:
            customer = Customer.objects.get(id=pk)
            serializer = CustomerWriteSerializer(instance=customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'message': 'Customer updated successfully.'}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"create customer error on {e}")
            return Response(status=status.HTTP_400_BAD_REQUEST)


class CustomerDestroyAPIView(DestroyAPIView):
    queryset = Customer.objects.filter(is_active=True)

    @swagger_auto_schema(
        tags=['Customer'],
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
            instance.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logger.error(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)