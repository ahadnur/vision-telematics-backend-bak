import logging
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, DestroyAPIView
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
    pagination_class = None
    queryset = SubscriptionPlan.active_objects.all()

    @swagger_auto_schema(
        tags=['Subscription Plan'],
        responses={
            status.HTTP_200_OK: openapi.Response(
                description='Subscription Plan List',
                schema=SubscriptionPlanSerializer()
            )
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class SubscriptionPlanDetailsAPIView(RetrieveAPIView):
    queryset = SubscriptionPlan.active_objects.all()
    serializer_class = SubscriptionPlanSerializer
    lookup_field = 'id'

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