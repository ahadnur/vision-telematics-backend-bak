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

customer_list_response_schema = openapi.Schema(
    type=openapi.TYPE_ARRAY,
    items=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
        'id': openapi.Schema(type=openapi.TYPE_INTEGER),
        'customer_ref_number': openapi.Schema(type=openapi.TYPE_STRING),
        'contact_name': openapi.Schema(type=openapi.TYPE_STRING),
        'phone_numbers': openapi.Schema(type=openapi.TYPE_STRING),
        'email_address': openapi.Schema(type=openapi.TYPE_STRING),
        'company': openapi.Schema(type=openapi.TYPE_INTEGER),  # Assuming company is an ID
        'address': openapi.Schema(type=openapi.TYPE_OBJECT, properties={
            'address_line_1': openapi.Schema(type=openapi.TYPE_STRING),
            'address_line_2': openapi.Schema(type=openapi.TYPE_STRING),
            'address_line_3': openapi.Schema(type=openapi.TYPE_STRING),
            'address_line_4': openapi.Schema(type=openapi.TYPE_STRING),
            'postcode': openapi.Schema(type=openapi.TYPE_STRING),
        }),
    })
)