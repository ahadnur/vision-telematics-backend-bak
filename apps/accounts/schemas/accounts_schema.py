from drf_yasg import openapi

base_account_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'account_contact': openapi.Schema(type=openapi.TYPE_STRING, description="Contact person for the account"),
        'account_number': openapi.Schema(type=openapi.TYPE_STRING, description="Unique account number"),
        'account_type': openapi.Schema(
            type=openapi.TYPE_STRING,
            description="Type of account (company or individual)",
            enum=["company", "individual"]
        ),
        'owner_company': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID of the associated company"),
        'owner_customer': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID of the associated customer"),
        'discount': openapi.Schema(
            type=openapi.TYPE_NUMBER,
            format="decimal",
            description="Discount percentage (e.g., 10.00 for 10%)"
        ),
        'invoice_terms': openapi.Schema(type=openapi.TYPE_STRING, description="Terms for invoice payments"),
        'freeze_account': openapi.Schema(
            type=openapi.TYPE_BOOLEAN,
            description="Indicates if the account is frozen",
            default=False
        ),
        'hot_account': openapi.Schema(
            type=openapi.TYPE_BOOLEAN,
            description="Indicates if the account is marked as high priority",
            default=False
        ),
        'reseller_account': openapi.Schema(
            type=openapi.TYPE_BOOLEAN,
            description="Indicates if the account belongs to a reseller",
            default=False
        ),
        'confirmation_email': openapi.Schema(
            type=openapi.TYPE_STRING,
            format="email",
            description="Email for account confirmation"
        ),
        'send_confirmation': openapi.Schema(
            type=openapi.TYPE_BOOLEAN,
            description="Indicates if confirmation should be sent",
            default=False
        ),
    },
    required=['account_number', 'account_type']
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
        'password': openapi.Schema(type=openapi.TYPE_STRING,)
    }
)

reset_user_password_request_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'email': openapi.Schema(type=openapi.TYPE_STRING),
        'password': openapi.Schema(type=openapi.TYPE_STRING),
    }
)

get_user_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'id': openapi.Schema(type=openapi.TYPE_INTEGER),
        **user_base_schema
    }
)


