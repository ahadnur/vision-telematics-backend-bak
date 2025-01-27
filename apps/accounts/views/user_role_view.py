from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView, DestroyAPIView
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView

from apps.accounts.models import UserRole
from apps.accounts.serializers import  UserRoleSerializer
import logging


logger = logging.getLogger(__name__)


class UserRoleListAPIView(ListAPIView):
    serializer_class = UserRoleSerializer
    queryset = UserRole.active_objects.all()

    @swagger_auto_schema(
        tags=['UserRole'],
        manual_parameters=[
            openapi.Parameter(
                'paginated',
                openapi.IN_QUERY,
                description="Enable or disable pagination (true or false)",
                type=openapi.TYPE_BOOLEAN,
                required=False,
                default=True
            ),
        ],
    )
    def get(self, request, *args, **kwargs):
        paginated = request.query_params.get('paginated', 'true').lower() == 'true'
        if not paginated:
            self.pagination_class = None
        return self.list(request, *args, **kwargs)


class UserRoleCreateAPIView(APIView):
    @swagger_auto_schema(
        tags=['UserRole'],
        request_body=UserRoleSerializer,
        responses={
            status.HTTP_201_CREATED: UserRoleSerializer(),
        }
    )
    def post(self, request, *args, **kwargs):
        try:
            serializer = UserRoleSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'message': 'UserRole created successfully.'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"create user role error on {e}")
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserRoleRetrieveAPIView(RetrieveAPIView):
    serializer_class = UserRoleSerializer
    queryset = UserRole.active_objects.all()
    lookup_field = 'pk'

    @swagger_auto_schema(
        tags=['UserRole'],
        responses={
            status.HTTP_200_OK: openapi.Response(
                description='Get UserRole',
                schema=UserRoleSerializer
            )
        }
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class UserRoleUpdateAPIView(APIView):
    @swagger_auto_schema(
        tags=['UserRole'],
        request_body=UserRoleSerializer,
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                description='Created user role',
                schema=UserRoleSerializer
            )
        }
    )
    def post(self, request, pk):
        try:
            user_role = UserRole.objects.get(id=pk)
            serializer = UserRoleSerializer(instance=user_role, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'message': 'UserRole updated successfully.'}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"create user role error on {e}")
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserRoleDestroyAPIView(DestroyAPIView):
    queryset = UserRole.active_objects.all()

    @swagger_auto_schema(
        tags=['UserRole'],
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
