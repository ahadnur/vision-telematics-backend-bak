import logging
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.generics import (
    ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
)
from rest_framework.response import Response
from django.db import transaction
from django.utils.timezone import now
from django.contrib.contenttypes.models import ContentType

from apps.products.models import (
    SubscriptionPlan, SubscribeAPlan, UsageMetrics, SubscriptionTransaction
)
from apps.products.serializers import (
    SubscriptionPlanSerializer, SubscriptionTransactionSerializer,
    UsageMetricsSerializer, SubscribeAPlanSerializer
)
from apps.accounts.models import Company, Customer
from apps.common.enums import (
    SubscriptionStatusChoices, SubscriptionTierChoices, BillingCycleChoices
)

logger = logging.getLogger(__name__)


class SubscriptionPlanListAPIView(ListAPIView):
    serializer_class = SubscriptionPlanSerializer
    queryset = SubscriptionPlan.active_objects.all()

    @swagger_auto_schema(
        tags=['Subscription Plans'],
        manual_parameters=[
            openapi.Parameter('tier', openapi.IN_QUERY, type=openapi.TYPE_STRING, enum=SubscriptionTierChoices.values, required=False),
            openapi.Parameter('billing_cycle', openapi.IN_QUERY, type=openapi.TYPE_STRING, enum=BillingCycleChoices.values, required=False)
        ]
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        params = self.request.query_params

        if tier := params.get('tier'):
            queryset = queryset.filter(tier__iexact=tier)
        if cycle := params.get('billing_cycle'):
            queryset = queryset.filter(billing_cycle__iexact=cycle)

        return queryset


class SubscriptionPlanRetrieveAPIView(RetrieveAPIView):
    serializer_class = SubscriptionPlanSerializer
    queryset = SubscriptionPlan.active_objects.all()
    lookup_field = 'pk'

    @swagger_auto_schema(tags=['Subscription Plans'])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class SubscriptionPlanCreateAPIView(CreateAPIView):
    serializer_class = SubscriptionPlanSerializer
    queryset = SubscriptionPlan.active_objects.all()

    def get_permissions(self):
        if not self.request.user.is_superuser:
            raise PermissionDenied("Only admins can create subscription plans")
        return super().get_permissions()

    @swagger_auto_schema(tags=['Subscription Plans'], request_body=SubscriptionPlanSerializer)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class SubscriptionPlanUpdateAPIView(UpdateAPIView):
    serializer_class = SubscriptionPlanSerializer
    queryset = SubscriptionPlan.active_objects.all()
    lookup_field = 'pk'
    http_method_names = ['put']

    def get_permissions(self):
        if not self.request.user.is_superuser:
            raise PermissionDenied("Only admins can update subscription plans")
        return super().get_permissions()

    @swagger_auto_schema(tags=['Subscription Plans'], request_body=SubscriptionPlanSerializer)
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)


class SubscriptionPlanDestroyAPIView(DestroyAPIView):
    serializer_class = SubscriptionPlanSerializer
    queryset = SubscriptionPlan.active_objects.all()
    lookup_field = 'pk'

    def get_permissions(self):
        if not self.request.user.is_superuser:
            raise PermissionDenied("Only admins can delete subscription plans")
        return super().get_permissions()

    @swagger_auto_schema(tags=['Subscription Plans'])
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        with transaction.atomic():
            plan = self.get_object()
            plan.is_active = False
            plan.is_deleted = True
            plan.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SubscriptionListAPIView(ListAPIView):
    serializer_class = SubscribeAPlanSerializer
    queryset = SubscribeAPlan.active_objects.all()

    @swagger_auto_schema(
        tags=['Subscriptions'],
        manual_parameters=[
            openapi.Parameter('subscriber_type', openapi.IN_QUERY, type=openapi.TYPE_STRING, enum=['company', 'customer'], required=False),
            openapi.Parameter('subscriber_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, required=False),
            openapi.Parameter('status', openapi.IN_QUERY, type=openapi.TYPE_STRING, enum=SubscriptionStatusChoices.values, required=False)
        ]
    )
    def get(self):
        return self.get_queryset()

    def get_queryset(self):
        queryset = super().get_queryset()
        params = self.request.query_params

        if sub_type := params.get('subscriber_type'):
            try:
                content_type = ContentType.objects.get(model=sub_type.lower())
                queryset = queryset.filter(subscriber_type=content_type)
            except ContentType.DoesNotExist:
                raise NotFound("Invalid subscriber type")

        if sub_id := params.get('subscriber_id'):
            queryset = queryset.filter(subscriber_id=sub_id)

        if status := params.get('status'):
            queryset = queryset.filter(status__iexact=status)

        return queryset


class SubscriptionRetrieveAPIView(RetrieveAPIView):
    serializer_class = SubscribeAPlanSerializer
    queryset = SubscribeAPlan.objects.all()
    lookup_field = 'pk'

    @swagger_auto_schema(tags=['Subscriptions'])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class SubscriptionCreateAPIView(CreateAPIView):
    serializer_class = SubscribeAPlanSerializer
    queryset = SubscribeAPlan.objects.all()

    @swagger_auto_schema(tags=['Subscriptions'], request_body=SubscribeAPlanSerializer)
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_201_CREATED:
            subscription = SubscribeAPlan.objects.get(id=response.data['id'])
            SubscriptionTransaction.objects.create(
                subscriber_type=subscription.subscriber_type,
                subscriber_id=subscription.subscriber_id,
                plan=subscription.plan,
                amount_paid=subscription.plan.price,
                start_date=subscription.current_start_date,
                end_date=subscription.current_end_date,
                payment_reference="INITIAL_PAYMENT",
                note="New Subscription Added."
            )
        return response


class SubscriptionUpdateAPIView(UpdateAPIView):
    serializer_class = SubscribeAPlanSerializer
    queryset = SubscribeAPlan.objects.all()
    lookup_field = 'pk'
    http_method_names = ['put']

    @swagger_auto_schema(tags=['Subscriptions'], request_body=SubscribeAPlanSerializer)
    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        old_plan = instance.plan
        response = super().put(request, *args, **kwargs)

        if response.status_code == status.HTTP_200_OK:
            new_plan = instance.plan
            if old_plan != new_plan:
                SubscriptionTransaction.objects.create(
                    subscriber_type=instance.subscriber_type,
                    subscriber_id=instance.subscriber_id,
                    plan=new_plan,
                    amount_paid=new_plan.price,
                    start_date=now().date(),
                    payment_reference="PLAN_UPDATE",
                    note="Subscription Plan Updated"
                )
        return response


# ==================== Transactions & Usage Metrics Views ====================
class TransactionHistoryAPIView(ListAPIView):
    serializer_class = SubscriptionTransactionSerializer
    queryset = SubscriptionTransaction.objects.all()

    @swagger_auto_schema(
        tags=['Transactions'],
        manual_parameters=[
            openapi.Parameter('subscriber_type', openapi.IN_QUERY, type=openapi.TYPE_STRING, enum=['company', 'customer'], required=False),
            openapi.Parameter('subscriber_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, required=False)
        ]
    )
    def get(self):
        return self.get_queryset()
        
    def get_queryset(self):
        queryset = super().get_queryset()
        params = self.request.query_params

        if sub_type := params.get('subscriber_type'):
            try:
                content_type = ContentType.objects.get(model=sub_type.lower())
                queryset = queryset.filter(subscriber_type=content_type)
            except ContentType.DoesNotExist:
                raise NotFound("Invalid subscriber type")

        if sub_id := params.get('subscriber_id'):
            queryset = queryset.filter(subscriber_id=sub_id)

        return queryset


class UsageMetricsAPIView(RetrieveAPIView):
    serializer_class = UsageMetricsSerializer

    @swagger_auto_schema(
        tags=['Usage Metrics'],
        manual_parameters=[
            openapi.Parameter('subscriber_type', openapi.IN_PATH, type=openapi.TYPE_STRING, enum=['company', 'customer']),
            openapi.Parameter('subscriber_id', openapi.IN_PATH, type=openapi.TYPE_INTEGER)
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_object(self):
        try:
            content_type = ContentType.objects.get(model=self.kwargs['subscriber_type'].lower())
            return UsageMetrics.objects.get(
                subscriber_type=content_type,
                subscriber_id=self.kwargs['subscriber_id']
            )
        except ContentType.DoesNotExist:
            raise NotFound("Invalid subscriber type")
        except UsageMetrics.DoesNotExist:
            raise NotFound("Usage metrics not found for given subscriber")
