from drf_yasg import openapi

order_request_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'customer_order_options': openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'customer': openapi.Schema(type=openapi.TYPE_INTEGER),
                'job_required': openapi.Schema(type=openapi.TYPE_STRING),
                'kit_installed': openapi.Schema(type=openapi.TYPE_STRING),
                'preferred_install_date': openapi.Schema(type=openapi.TYPE_STRING),
            }
        ),
        'customer_vehicle_info': openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'customer': openapi.Schema(type=openapi.TYPE_INTEGER),
                'vehicle_make': openapi.Schema(type=openapi.TYPE_INTEGER),
                'vehicle_model': openapi.Schema(type=openapi.TYPE_INTEGER),
                'vehicle_type': openapi.Schema(type=openapi.TYPE_INTEGER),
                'registration_number': openapi.Schema(type=openapi.TYPE_STRING),
            }
        ),
        'items': openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'product': openapi.Schema(
                        type=openapi.TYPE_INTEGER,
                        description="The ID of the product SKU"
                    ),
                    'quantity': openapi.Schema(
                        type=openapi.TYPE_INTEGER,
                        description="The quantity of the product SKU"
                    ),
                },
            ),
        ),
        'customer': openapi.Schema(
            type=openapi.TYPE_INTEGER,
            description="The ID of the customer SKU"
        ),
        'created_by': openapi.Schema(
            type=openapi.TYPE_INTEGER,
        )
    },
)



