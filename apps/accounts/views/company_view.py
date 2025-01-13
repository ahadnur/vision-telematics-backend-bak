from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView, DestroyAPIView
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView

from apps.accounts.models import Company
from apps.accounts.schemas import company_create_response_schema
from apps.accounts.schemas.company_schema import company_list_response_schema
from apps.accounts.serializers import CompanySerializer
import logging


logger = logging.getLogger(__name__)


class CompanyListAPIView(ListAPIView):
    queryset = Company.active_objects.all().order_by('-created_at')
    serializer_class = CompanySerializer

    @swagger_auto_schema(
        tags=['Company'],
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
                description='List of companies',
                schema=company_list_response_schema,
            ),
            status.HTTP_400_BAD_REQUEST: "Bad request"
        }
    )
    def get(self, request, *args, **kwargs):
        paginated = request.query_params.get('paginated', 'true').lower() == 'true'
        if not paginated:
            self.pagination_class = None
        return self.list(request, *args, **kwargs)


class CompanyCreateAPIView(APIView):
    @swagger_auto_schema(
        tags=['Company'],
        request_body=CompanySerializer,
        responses={
            status.HTTP_201_CREATED: company_create_response_schema
        }
    )
    def post(self, request, *args, **kwargs):
        try:
            serializer = CompanySerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'message': 'Company created successfully.'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"create company error on {e}")
            return Response(status=status.HTTP_400_BAD_REQUEST)


class CompanyRetrieveAPIView(RetrieveAPIView):
    serializer_class = CompanySerializer
    queryset = Company.active_objects.all()
    lookup_field = 'pk'

    @swagger_auto_schema(
        tags=['Company'],
        responses={
            status.HTTP_200_OK: openapi.Response(
                description='Get company',
                schema=CompanySerializer
            )
        }
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class CompanyUpdateAPIView(APIView):
    @swagger_auto_schema(
        tags=['Company'],
        request_body=CompanySerializer,
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                description='Created company',
                schema=CompanySerializer
            )
        }
    )
    def post(self, request, pk):
        try:
            company = Company.objects.get(id=pk)
            serializer = CompanySerializer(instance=company, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'message': 'Company updated successfully.'}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"create company error on {e}")
            return Response(status=status.HTTP_400_BAD_REQUEST)


class CompanyDestroyAPIView(DestroyAPIView):
    queryset = Company.objects.filter(is_active=True)

    @swagger_auto_schema(
        tags=['Company'],
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
