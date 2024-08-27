from rest_framework import views, status
from rest_framework.response import Response
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .models import Order
from .serializers import CreateOrderSerializer
from .swagger_schema import order_request_schema


class OrderCreateAPIView(views.APIView):
    queryset = Order.objects.all()
    serializer_class = CreateOrderSerializer

    @swagger_auto_schema(
        request_body=order_request_schema,
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                description='Account created successfully',
                schema=serializer_class
            ),
        },
    )
    def post(self, request):
        data = request.data
        serializer = CreateOrderSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
        return Response("Account created successfully", status.HTTP_201_CREATED)