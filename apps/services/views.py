from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.response import Response

from .models import Service
from .serializers import ServiceSerializer


class ServiceCreateView(CreateAPIView):
	queryset = Service.objects.all()
	serializer_class = ServiceSerializer

	@swagger_auto_schema(
		tags=['Services'],
		request_body=ServiceSerializer,
		responses={
			status.HTTP_200_OK: ServiceSerializer(),
		}
	)
	def post(self, request, *args, **kwargs):
		return self.create(request, *args, **kwargs)


class ServiceListView(ListAPIView):
	queryset = Service.objects.filter(is_active=True, is_deleted=False)
	serializer_class = ServiceSerializer

	@swagger_auto_schema(
		tags=['Services'],
		responses={
			status.HTTP_200_OK: openapi.Schema(
				type=openapi.TYPE_ARRAY,
				items=openapi.Schema(
					type=openapi.TYPE_OBJECT,
					properties={
						**ServiceSerializer().data
					}
				)
			),
		}
	)
	def get(self, request, *args, **kwargs):
		return self.list(request, *args, **kwargs)


class ServiceRetrieveView(RetrieveAPIView):
	queryset = Service.objects.filter(is_active=True, is_deleted=False)
	serializer_class = ServiceSerializer
	lookup_field = 'pk'

	@swagger_auto_schema(
		tags=['Services'],
		responses={
			status.HTTP_200_OK: ServiceSerializer(),
		}
	)
	def get(self, request, *args, **kwargs):
		return self.retrieve(request, *args, **kwargs)


class ServiceUpdateView(UpdateAPIView):
	queryset = Service.objects.all()
	serializer_class = ServiceSerializer
	lookup_field = 'pk'

	@swagger_auto_schema(
		tags=['Services'],
		request_body=ServiceSerializer,
		responses={
			status.HTTP_200_OK: ServiceSerializer(),
		}
	)
	def put(self, request, *args, **kwargs):
		return self.update(request, *args, **kwargs)


class ServiceDeleteView(DestroyAPIView):
	queryset = Service.objects.all()
	serializer_class = ServiceSerializer
	lookup_field = 'pk'

	@swagger_auto_schema(
		tags=['Services'],
		responses={
			status.HTTP_204_NO_CONTENT: "Successfully deleted!",
		}
	)
	def delete(self, request, *args, **kwargs):
		return self.destroy(request, *args, **kwargs)

	def destroy(self, request, *args, **kwargs):
		instance = self.get_object()
		instance.is_deleted = True
		instance.is_active = False
		instance.save()
		return Response(status=status.HTTP_204_NO_CONTENT)

