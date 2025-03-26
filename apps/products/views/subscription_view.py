import logging
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.response import Response
from datetime import timedelta
from django.utils.timezone import now

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


########## Subscribed ##########

class SubscribedCompanyListAPIView(ListAPIView):
    serializer_class = CompanySubscriptionSerializer
    
    def get_queryset(self):
        queryset = CompanySubscription.active_objects.all()
        plan_id = self.request.query_params.get('plan_id')
        status = self.request.query_params.get('status')
        tier = self.request.query_params.get('tier')

        if plan_id:
            queryset = queryset.filter(plan=plan_id)
        if status:
            queryset = queryset.filter(status=status.lower())
        if tier:
            queryset = queryset.filter(company__tier=tier.lower())

        return queryset

    @swagger_auto_schema(
        tags=['Subscribed Company'],
        manual_parameters=[
            openapi.Parameter(
                'plan_id',
                openapi.IN_QUERY,
                description='Filter by plan id',
                type=openapi.TYPE_INTEGER,
                required=False,
            ),
            openapi.Parameter(
                'status',
                openapi.IN_QUERY,
                description='Filter by status (active, expired, canceled)',
                type=openapi.TYPE_STRING,
                required=False,
            ),
            openapi.Parameter(
                'tier',
                openapi.IN_QUERY,
                description='Filter by tier (basic, pro, enterprise)',
                type=openapi.TYPE_STRING,
                required=False,
            ),
        ]
    )
    def get(self, request, *args, **kwargs):        
        return super().get(request, *args, **kwargs)


class SubscribedCompanyDetailsAPIView(RetrieveAPIView):
    queryset = CompanySubscription.active_objects.all()
    serializer_class = CompanySubscriptionSerializer

    @swagger_auto_schema(
        tags=['Subscribed Company'],
        responses={
            status.HTTP_200_OK: openapi.Response(description='Subscribed company details'),
            status.HTTP_400_BAD_REQUEST: openapi.Response(description='An error occurred'),
            status.HTTP_404_NOT_FOUND: openapi.Response(description='subscribed company not found or company is not subscribed any tier')
        }
    )
    def get(self, request, *args, **kwargs):
        try:
            subscribed_company = self.get_object()
            serializer = self.get_serializer(subscribed_company)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CompanySubscription.DoesNotExist:
            return Response({'error' : 'subscribed company not found or company is not subscribed any tier'}, status=status.HTTP_404_NOT_FOUND)
        
    def get_object(self):
        id = self.kwargs.get('pk')

        try:
            subscribed_company = self.queryset.get(pk=id)
        except CompanySubscription.DoesNotExist:
            raise NotFound("subscribed company not found or company is not subscribed any tier")
        return subscribed_company


class CompanySubscribeCreateAPIView(CreateAPIView):
    serializer_class = CompanySubscriptionSerializer
    
    @swagger_auto_schema(
        tags=['Subscribed Company'],
        request_body=CompanySubscriptionSerializer,
        responses={
            status.HTTP_201_CREATED: openapi.Response(description='Successfully Subscribed to a plan!')
        }
    )
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
        if response.status_code == status.HTTP_201_CREATED:
            subscription = CompanySubscription.objects.get(id=response.data['id'])
            
            # Create SubscriptionTransaction
            SubscriptionTransaction.objects.create(
                company=subscription.company,
                plan=subscription.plan,
                amount_paid=subscription.plan.price,
                start_date=subscription.current_start_date or now().date(),
                end_date=subscription.current_end_date,
                status=SubscriptionStatusChoices.ACTIVE,
                payment_reference="INITIAL_PAYMENT"
            )
        
        return response



class ChangeSubscriptionPlanAndStatusAPIView(UpdateAPIView):
    serializer_class = CompanySubscriptionSerializer
    queryset = CompanySubscription.active_objects.all()
    http_method_names = ['put']

    def get_object(self):
        return self.queryset.get(pk=self.kwargs.get('pk'))
    
    @swagger_auto_schema(
        tags=['Subscribed Company'],
        request_body=CompanySubscriptionSerializer,
        responses={
            status.HTTP_200_OK: openapi.Response(description='subscription tier updated successfully'),
            status.HTTP_400_BAD_REQUEST: openapi.Response(description='An error occurred'),
            status.HTTP_404_NOT_FOUND: openapi.Response(description='subscription tier not found'),
        }
    )
    def put(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            old_plan = instance.plan
            old_status = instance.status

            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            
            updated_instance = self.get_object()  # updated instance
            new_plan = updated_instance.plan
            new_status = updated_instance.status

            # Check if the plan or status has changed
            if old_plan != new_plan or old_status != new_status:
                SubscriptionTransaction.objects.create(
                    company=updated_instance.company,
                    plan=new_plan,
                    amount_paid=new_plan.price,
                    start_date=now().date(),
                    status=new_status,
                    payment_reference="PLAN_UPDATE_PAYMENT"
                )

            return Response(serializer.data, status=status.HTTP_200_OK)

        except CompanySubscription.DoesNotExist:
            return Response({'error': 'subscription tier not found'}, status=status.HTTP_404_NOT_FOUND)