import logging

from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from rest_framework import status, views
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView

from apps.accounts.serializers import AccountWriteSerializer, AccountSerializer, AccountListDropdownSerializer
from apps.accounts.schemas.accounts_schema import (account_write_request_schema, account_response_schema,
                                                   get_user_response_schema)

from apps.accounts.models import Account
from apps.accounts.services import AccountService

logger = logging.getLogger(__name__)

User = get_user_model()


class CreateAccountAPIView(CreateAPIView):
    serializer_class = AccountWriteSerializer

    @swagger_auto_schema(
        tags=['Accounts'],
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
        tags=['Accounts'],
        request_body=account_write_request_schema,
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                description='Account updated successfully',
                schema=account_response_schema
            ),
        },
    )
    def put(self, request, _id):
        try:
            account = AccountService.get_account(_id)
            serializer = AccountWriteSerializer(account, data=request.data,
                                                partial=True)  # `partial=True` allows partial updates
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


class AccountListAPIView(ListAPIView):
    queryset = Account.objects.filter(is_active=True, is_deleted=False)
    serializer_class = AccountSerializer

    @swagger_auto_schema(
        tags=['Accounts'],
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
                description='List of companies with id and name',
                schema=AccountSerializer(many=True)
            ),
        }
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class GetAccountAPIView(RetrieveAPIView):
    serializer_class = AccountSerializer
    queryset = Account.objects.filter(is_active=True, is_deleted=False)

    @swagger_auto_schema(
        tags=['Accounts'],
        responses={
            status.HTTP_200_OK: openapi.Response(
                description='Account details',
                schema=AccountSerializer,
            )
        }
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class AccountDropdownListAPIView(ListAPIView):
    serializer_class = AccountListDropdownSerializer
    queryset = Account.objects.filter(is_active=True, is_deleted=False)
    pagination_class = None

    @swagger_auto_schema(
        tags=['Accounts'],
        responses={
            status.HTTP_200_OK: openapi.Response(
                description='List of companies with id and name',
                schema=AccountListDropdownSerializer(many=True)
            )
        }
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


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



# class CustomerDestroyAPIView(DestroyAPIView):
#     queryset = Customer.objects.filter(is_active=True)
#
#     @swagger_auto_schema(
#         tags=['Customer'],
#         responses={
#             status.HTTP_204_NO_CONTENT: "Successfully deleted!",
#         }
#     )
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)
#
#     def destroy(self, request, *args, **kwargs):
#         try:
#             instance = self.get_object()
#             instance.is_deleted = True
#             instance.is_active = False
#             instance.save()
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         except Exception as e:
#             logger.error(e)
#             return Response(status=status.HTTP_400_BAD_REQUEST)

