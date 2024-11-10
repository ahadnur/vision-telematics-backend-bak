import logging

from django.contrib.auth import get_user_model
from rest_framework import status, views
from rest_framework.response import Response
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

from apps.accounts.serializers import UserWriteSerializer, ResetPasswordSerializer, GetUserSerializer, \
	AuthenticationSerializer
from apps.accounts.schemas.accounts_schema import account_response_schema, reset_user_password_request_schema, \
	get_user_response_schema

from apps.accounts.services import get_user, get_general_user_list
from config.authentication import JWTAuthentication

logger = logging.getLogger(__name__)

User = get_user_model()


class UserCreateAPIView(views.APIView):
	permission_classes = (IsAdminUser,)
	serializer_class = UserWriteSerializer

	@swagger_auto_schema(
		tags=['Users'],
		request_body=UserWriteSerializer,
		responses={
			status.HTTP_201_CREATED: openapi.Response(
				description='User created successfully',
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
				'message': 'Account created successfully',
				'user_id': user.id,
			}, status=status.HTTP_201_CREATED)
		except Exception as e:
			logger.error(str(e))
			return Response({
				'message': str(e),
			}, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(views.APIView):
	permission_classes = (AllowAny,)
	serializer_class = AuthenticationSerializer

	@swagger_auto_schema(
		tags=['Users'],
		request_body=AuthenticationSerializer,
		responses={
			status.HTTP_201_CREATED: openapi.Response(
				description='Account created successfully',
			),
		}
	)
	def post(self, request):
		serializer = self.serializer_class(data=request.data)
		serializer.is_valid(raise_exception=True)
		return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserListAPIView(views.APIView):
	permission_classes = (IsAdminUser,)

	@swagger_auto_schema(
		tags=['Users'],
		responses={
			status.HTTP_200_OK: openapi.Response(
				description='Account created successfully',
				schema=openapi.Schema(
					type=openapi.TYPE_OBJECT,
					properties={
						'users': GetUserSerializer(many=True).data
					},
				),
			),
		}
	)
	def get(self, request):
		user_list = get_general_user_list()
		serializer = GetUserSerializer(user_list, many=True)
		return Response({
			'users': serializer.data,
		}, status=status.HTTP_200_OK)


class GetUserAPIView(views.APIView):
	serializer_class = GetUserSerializer

	@swagger_auto_schema(
		tags=['Users'],
		responses={
			status.HTTP_200_OK: openapi.Response(
				description='Account created successfully',
				schema=get_user_response_schema
			),
		}
	)
	def get(self, request, _id):
		user = get_user(_id)
		serializer = self.serializer_class(user)
		return Response({
			'user': serializer.data,
		}, status=status.HTTP_200_OK)


class UserUpdateAPIView(views.APIView):

	@swagger_auto_schema(
		tags=['Users'],
		request_body=UserWriteSerializer,
		responses={
			status.HTTP_201_CREATED: openapi.Response(
				description='User updated successfully',
				schema=UserWriteSerializer
			),
		}
	)
	def put(self, request, pk):
		try:
			data = request.data
			instance = User.objects.get(id=pk)
			serializer = UserWriteSerializer(instance=instance, data=data)
			serializer.is_valid(raise_exception=True)
			serializer.save()
			return Response(data=serializer.data, status=status.HTTP_200_OK)
		except Exception as e:
			logger.error(f"update user error on: {e} ")
			return Response(status=status.HTTP_400_BAD_REQUEST)


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
