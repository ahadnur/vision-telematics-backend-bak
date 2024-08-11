from drf_yasg import openapi

base_account_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'account_name': openapi.Schema(type=openapi.TYPE_STRING),
        'contact_number': openapi.Schema(type=openapi.TYPE_STRING),
        'in_add': openapi.Schema(type=openapi.TYPE_STRING),
        'notes': openapi.Schema(type=openapi.TYPE_STRING),
        'discount': openapi.Schema(type=openapi.TYPE_NUMBER),
        'invoice_terms': openapi.Schema(type=openapi.TYPE_STRING),
        'opened': openapi.Schema(type=openapi.TYPE_STRING),
        'opened_by': openapi.Schema(type=openapi.TYPE_INTEGER),
        'confirmation_email': openapi.Schema(type=openapi.TYPE_STRING),
        'send_confirmation': openapi.Schema(type=openapi.TYPE_BOOLEAN),
        'sales_contact': openapi.Schema(type=openapi.TYPE_STRING),
        'sales_contact_number': openapi.Schema(type=openapi.TYPE_STRING),
        'sales_email': openapi.Schema(type=openapi.TYPE_STRING)
    },
)


account_write_request_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties=base_account_schema.properties
)


account_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'id': openapi.Schema(type=openapi.TYPE_INTEGER, format=openapi.FORMAT_INT64),
        **base_account_schema.properties
    }
)

user_base_schema = {
    'email': openapi.Schema(type=openapi.TYPE_STRING),
    'role': openapi.Schema(type=openapi.TYPE_INTEGER)
}

user_create_request_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        **user_base_schema,
        'password1': openapi.Schema(type=openapi.TYPE_STRING,),
        'password2': openapi.Schema(type=openapi.TYPE_STRING),
    }
)

reset_user_password_request_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'email': openapi.Schema(type=openapi.TYPE_STRING),
        'password1': openapi.Schema(type=openapi.TYPE_STRING),
        'password2': openapi.Schema(type=openapi.TYPE_STRING),
    }
)

get_user_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'id': openapi.Schema(type=openapi.TYPE_INTEGER),
        **user_base_schema
    }
)


