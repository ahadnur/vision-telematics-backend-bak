from drf_yasg import openapi

vehicle_model_schema = openapi.Schema(
    type=openapi.TYPE_ARRAY,
    items=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "id": openapi.Schema(type=openapi.TYPE_INTEGER),
            "name": openapi.Schema(type=openapi.TYPE_STRING),
            "vehicle_make": openapi.Schema(type=openapi.TYPE_INTEGER),
        }
    )
)
