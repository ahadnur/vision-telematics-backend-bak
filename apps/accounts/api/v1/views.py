from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from rest_framework import status, views
from rest_framework import generics
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from apps.accounts.api.v1.serializers import AccountWriteSerializer
from .schemas.accounts_schema import account_write_request_schema, account_response_schema

User = get_user_model()


class CreateAccountAPIView(generics.CreateAPIView):
    serializer_class = AccountWriteSerializer

    @swagger_auto_schema(
        request_body=account_write_request_schema,
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                description='Account created successfully',
                schema=account_response_schema
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
    def put(self, request, *args, **kwargs):
        pass


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
