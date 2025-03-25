import logging
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.response import Response

from apps.products.models import (
    SubscriptionPlan,
    SubscriptionTransaction,
    UsageMetrics,
    CompanySubscription,
)
from apps.products.serializers import (
    SubscriptionPlanSerializer,
    SubscriptionTransactionSerializer,
    UsageMetricsSerializer,
    CompanySubscriptionSerializer,
)
from apps.common.enums import (
    SubscriptionTierChoices, 
    SubscriptionStatusChoices, 
    BillingCycleChoices
)

logger = logging.getLogger(__name__)


class SubscriptionPlanListAPIView(ListAPIView):
    serializer_class = SubscriptionPlanSerializer
    queryset = SubscriptionPlan.active_objects.all()

    @swagger_auto_schema(
        tags=['Subscription Plan'],
        manual_parameters=[
            openapi.Parameter(
                'paginated',
                openapi.IN_QUERY,
                description='Enable or disable pagination',
                type=openapi.TYPE_BOOLEAN,
                default=True,
                required=False
            )
        ],
        responses={
            status.HTTP_200_OK: openapi.Response(
                description='Subscription Plan List',
                schema=SubscriptionPlanSerializer()
            )
        }
    )
    def get(self, request, *args, **kwargs):
        pagination = self.request.query_params.get('paginated', 'true').lower() == 'true'
        if not pagination:
            self.pagination_class = None

        return super().get(request, *args, **kwargs)


class SubscriptionPlanDetailsAPIView(RetrieveAPIView):
    queryset = SubscriptionPlan.active_objects.all()
    serializer_class = SubscriptionPlanSerializer
    lookup_field = 'pk'

    @swagger_auto_schema(
        tags=['Subscription Plan'],
        responses={
            status.HTTP_200_OK: openapi.Response(
                description='Subscription Plan Details',
                schema=SubscriptionPlanSerializer
            )
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class SubscriptionPlanCreateAPIView(CreateAPIView):
    serializer_class = SubscriptionPlanSerializer

    @swagger_auto_schema(
        tags=['Subscription Plan'],
        request_body=SubscriptionPlanSerializer,
        responses={
            status.HTTP_201_CREATED: openapi.Response(description='Subscription plan created successfully'),
            status.HTTP_400_BAD_REQUEST: openapi.Response(description='An error occurred'),
            status.HTTP_401_UNAUTHORIZED: openapi.Response(description='You are not authorized to create a lesson')
        }
    )
    def post(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().post(request, *args, **kwargs)
        return Response({'error':"You are not authorized to create a plan"}, status=status.HTTP_401_UNAUTHORIZED)


class SubscriptionPlanUpdateAPIView(UpdateAPIView):
    http_method_names = ['put']
    serializer_class = SubscriptionPlanSerializer
    queryset = SubscriptionPlan.active_objects.all()

    def get_object(self):
        return self.queryset.get(pk=self.kwargs.get('pk'))
    
    @swagger_auto_schema(
        tags=['Subscription Plan'],
        request_body= SubscriptionPlanSerializer,
        responses={
            status.HTTP_200_OK: openapi.Response(description='Subscription plan updated successfully'),
            status.HTTP_400_BAD_REQUEST: openapi.Response(description='An error occurred'),
            status.HTTP_404_NOT_FOUND: openapi.Response(description='Subscription plan not found'),
            status.HTTP_401_UNAUTHORIZED: openapi.Response(description='you are not authorized to edit Subscription plan')
        }
    )
    def put(self, request, *args, **kwargs):
        if request.user.is_superuser:
            try:
                instance = self.get_object()
                serializer = self.get_serializer(instance, data=request.data, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data)
            except SubscriptionPlan.DoesNotExist:
                return Response({'error' : 'Subscription plan not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error' : "you are not authorized to edit subscription plan"}, status.HTTP_401_UNAUTHORIZED)


class DeleteSubscriptionPlanAPIView(DestroyAPIView):
    serializer_class = SubscriptionPlanSerializer
    queryset = SubscriptionPlan.active_objects.all()

    def get_object(self):
        return self.queryset.get(pk=self.kwargs.get('pk'))
    
    @swagger_auto_schema(
        tags=['Subscription Plan'],
        responses={
            status.HTTP_204_NO_CONTENT: openapi.Response(description='Subscription Plan deleted successfully'),
            status.HTTP_400_BAD_REQUEST: openapi.Response(description='An error occurred'),
            status.HTTP_404_NOT_FOUND: openapi.Response(description='Subscription Plan not found'),
            status.HTTP_401_UNAUTHORIZED: openapi.Response(description='you are not authorized to delete Subscription Plan')
        }
    )
    def delete(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return self.destroy(request, *args, **kwargs)
        return Response({'error':'you are not authorized to delete Subscription Plan'})
    
    def destroy(request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.is_active = False
            instance.is_deleted = True
            instance.save()
            return Response({'success' : 'subscription plan deleted'})
        except SubscriptionPlan.DoesNotExist:
            return Response({'error': 'Subscription plan not found'})

