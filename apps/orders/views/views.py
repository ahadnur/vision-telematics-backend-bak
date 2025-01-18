import logging


from django.db.models import Prefetch
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.response import Response
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView

from apps.orders.models import Order, OrderItem
from apps.orders.serializers import OrderWriteSerializer, OrderReadSerializer

logger = logging.getLogger(__name__)


class OrderCreateAPIView(APIView):
    queryset = Order.objects.all()
    serializer_class = OrderWriteSerializer

    @swagger_auto_schema(
        tags=['Orders'],
        request_body=OrderWriteSerializer,
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                description='Account created successfully',
                schema=serializer_class
            ),
        },
    )
    def post(self, request):
        data = request.data
        serializer = OrderWriteSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data={
            'message': "Order created successfully!",
        }, status=status.HTTP_201_CREATED)


class OrderUpdateAPIView(APIView):
    queryset = Order.objects.prefetch_related(
        Prefetch('item_orders', queryset=OrderItem.objects.all())
    ).all()
    serializer_class = OrderWriteSerializer

    @swagger_auto_schema(
        tags=['Orders'],
        request_body=OrderWriteSerializer,
        responses={
            status.HTTP_200_OK: openapi.Response(
                description='order updated successfully',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        **OrderReadSerializer().data
                    }
                ),
            )
        }
    )
    def put(self, request, pk, *args, **kwargs):
        instance = Order.objects.filter(is_active=True, is_deleted=False).get(pk=pk)
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderRetrieveAPIView(RetrieveAPIView):
    queryset = Order.objects.prefetch_related(
        Prefetch('item_orders', queryset=OrderItem.objects.all())
    ).all()
    serializer_class = OrderReadSerializer

    @swagger_auto_schema(
        tags=['Orders'],
        responses={
            status.HTTP_200_OK: openapi.Response(
                description='Order retrieved successfully',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        **OrderReadSerializer().data,
                    }
                )
            )
        }
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class OrderListAPIView(ListAPIView):
    queryset = Order.objects.prefetch_related(
        Prefetch("item_orders", queryset=OrderItem.objects.filter(is_active=True)),
    ).order_by('-created_at')
    serializer_class = OrderReadSerializer

    @swagger_auto_schema(
        tags=['Orders'],
        responses={
            status.HTTP_200_OK: openapi.Response(
                description='Order list',
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            **OrderReadSerializer().data,
                        }
                    )
                )
            )
        }
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class OrderDestroyAPIView(DestroyAPIView):
    queryset = Order.objects.filter(is_active=True, is_deleted=False)
    lookup_field = 'pk'

    @swagger_auto_schema(
        tags=['Orders'],
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
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logger.error(f'error on {e}')
            return Response(status=status.HTTP_400_BAD_REQUEST)
