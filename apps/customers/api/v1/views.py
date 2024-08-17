from rest_framework import status, views
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from apps.customers.models import CustomerCompany
from apps.customers.api.v1.serializers import CompanyListSerializer


class CompanyListAPIView(ListAPIView):
    queryset = CustomerCompany.objects.all()
    serializer_class = CompanyListSerializer

    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: openapi.Response(
                description='List of companies with id and name',
                schema=CompanyListSerializer(many=True)
            ),
        }
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class CreateOrderAPIView(views.APIView):

    def post(self, request, *args, **kwargs):
        pass