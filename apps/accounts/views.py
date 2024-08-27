from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from rest_framework import status, views, generics
from rest_framework.response import Response
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny, IsAuthenticated

from apps.accounts.serializers import (AccountWriteSerializer, UserWriteSerializer, ResetPasswordSerializer,
                                       GetUserSerializer, AccountListSerializer)
from apps.accounts.schemas.accounts_schema import (account_write_request_schema, account_response_schema, user_create_request_schema,
                                                   reset_user_password_request_schema, get_user_response_schema)

import logging

from apps.accounts.models import Account
from apps.accounts.services import UserService, AccountService

logger = logging.getLogger(__name__)

User = get_user_model()


class UserCreateAPIView(views.APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserWriteSerializer

    @swagger_auto_schema(
        request_body=user_create_request_schema,
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                description='Account created successfully',
                schema=account_response_schema
            ),
        }
    )
    def post(self, request):
        try:
            data = request.data
            serializer = self.serializer_class(data=data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            return Response({
                'message': 'Account     created successfully',
                'user_id': user.id,
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(str(e))
            return Response({
                'message': str(e),
            }, status=status.HTTP_400_BAD_REQUEST)


class GetUserAPIView(views.APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = GetUserSerializer

    def __init__(self):
        super().__init__()
        self.user_service = UserService()

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: openapi.Response(
                description='Account created successfully',
                schema=get_user_response_schema
            ),
        }
    )
    def get(self, request, _id):
        get_user = self.user_service.get_user(_id)
        serializer = self.serializer_class(get_user)
        return Response({
            'user': serializer.data,
        }, status=status.HTTP_200_OK)


class ResetUserPasswordAPIView(views.APIView):
    permission_classes = (AllowAny,)
    serializer_class = ResetPasswordSerializer

    @swagger_auto_schema(
        request_body=reset_user_password_request_schema,
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                description='Account created successfully',
                schema=account_response_schema
            ),
        }
    )
    def put(self, request, _id):
        try:
            data = request.data
            data['id'] = _id
            user_instance = User.objects.get(pk=data['id'])
            serializer = self.serializer_class(instance=user_instance, data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({
                'message': 'Reset password successfully',
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(str(e))
            return Response({
                'message': str(e),
            }, status=status.HTTP_400_BAD_REQUEST)


class CreateAccountAPIView(generics.CreateAPIView):
    serializer_class = AccountWriteSerializer

    @swagger_auto_schema(
        request_body=account_write_request_schema,
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                description='Account created successfully',
                schema=get_user_response_schema
            ),
        }
    )
    def post(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class UpdateAccountAPIView(views.APIView):
    @swagger_auto_schema(
        request_body=account_write_request_schema,
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                description='Account created successfully',
                schema=account_response_schema
            ),
        },
    )
    def put(self, request, _id):
        try:
            account = AccountService.get_account(_id)
            serializer = AccountWriteSerializer(account, data=request.data, partial=True)  # `partial=True` allows partial updates
            if serializer.is_valid():
                updated_account = serializer.save()
                response_serializer = AccountWriteSerializer(updated_account)
                return Response(response_serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(str(e))
            return Response({
                'message': str(e),
            }, status=status.HTTP_400_BAD_REQUEST)


def activate(request, uidb64, token):
    try:
        uidb64 = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uidb64)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
        user = None

    if user is not None and user.verification_token == token:
        user.is_active = True
        user.verification_token = None
        user.save()
        return HttpResponse('Thank you for your email confirmation. Your account is now activated.')
    else:
        return HttpResponse('Activation link is invalid!')


class AccountListAPIView(generics.ListAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountListSerializer

    # permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: openapi.Response(
                description='List of companies with id and name',
                schema=AccountListSerializer(many=True)
            ),
        }
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
