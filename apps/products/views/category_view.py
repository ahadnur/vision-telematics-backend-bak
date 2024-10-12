import logging

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.products.models import Category
from apps.products.schemas.category_schema import category_list_reponse
from apps.products.serializers.category_serializer import CategorySerializer

logger = logging.getLogger(__name__)


class CategoryListAPIView(APIView):
	@swagger_auto_schema(
		tags=['Category'],
		responses=category_list_reponse
	)
	def get(self, request, *args, **kwargs):
		try:
			queryset = Category.objects.filter(is_active=True, is_deleted=False)
			serializer = CategorySerializer(queryset, many=True)
			return Response(serializer.data)
		except Exception as e:
			logger.error(e)
			return Response(status=status.HTTP_400_BAD_REQUEST)


class CategoryCreateAPIView(CreateAPIView):
	serializer_class = CategorySerializer
	queryset = Category.objects.all()

	@swagger_auto_schema(
		tags=['Category'],
		request_body=CategorySerializer,
		responses={
			200: CategorySerializer(),
		}
	)
	def post(self, request, *args, **kwargs):
		return self.create(request, *args, **kwargs)


class CategoryUpdateAPIView(APIView):
	serializer_class = CategorySerializer

	@swagger_auto_schema(
		tags=['Category'],
		request_body=CategorySerializer,
		responses={
			status.HTTP_200_OK: CategorySerializer(),
		}
	)
	def put(self, request, pk):
		queryset = Category.objects.filter(id=pk, is_active=True, is_deleted=False).first()
		serializer = self.serializer_class(instance=queryset, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_200_OK)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryRetrieveAPIView(RetrieveAPIView):
	serializer_class = CategorySerializer
	queryset = Category.objects.filter(is_active=True, is_deleted=False)
	lookup_field = 'pk'

	@swagger_auto_schema(
		tags=['Category'],
		responses={
			status.HTTP_200_OK: CategorySerializer(),
		}
	)
	def get(self, request, *args, **kwargs):
		return self.retrieve(request, *args, **kwargs)


class CategoryDestroyAPIView(DestroyAPIView):
	serializer_class = CategorySerializer
	queryset = Category.objects.filter(is_active=True, is_deleted=False)

	@swagger_auto_schema(
		tags=['Category'],
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
			logger.error(e)
			return Response(status=status.HTTP_400_BAD_REQUEST)

