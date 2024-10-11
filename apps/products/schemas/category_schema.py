from drf_yasg import openapi
from rest_framework import status

from apps.products.serializers.category_serializer import CategorySerializer


category_list_reponse = {
	status.HTTP_200_OK: openapi.Schema(
		type=openapi.TYPE_ARRAY,
		items=openapi.Schema(
			type=openapi.TYPE_OBJECT,
			properties={
				**CategorySerializer().data
			}
		)
	),
}