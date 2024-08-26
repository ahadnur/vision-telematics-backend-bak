from drf_yasg import openapi

vehicle_info_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'vehicle_makes': openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'id': openapi.Schema(type=openapi.TYPE_INTEGER,),
                    'name': openapi.Schema(type=openapi.TYPE_STRING,),
                }
            )
        ),
        'vehicle_models': openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'id': openapi.Schema(type=openapi.TYPE_INTEGER,),
                    'name': openapi.Schema(type=openapi.TYPE_STRING,),
                }
            )
        ),
        'vehicle_types': openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'id': openapi.Schema(type=openapi.TYPE_INTEGER,),
                    'name': openapi.Schema(type=openapi.TYPE_STRING,),
                }
            )
        ),
    }
)
