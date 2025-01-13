from drf_yasg import openapi

from apps.accounts.serializers import CompanySerializer
from apps.customers.serializers import CustomerWriteSerializer


company_list_response_schema = openapi.Schema(
    type=openapi.TYPE_ARRAY,
    items=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID of the company"),
            'company_name': openapi.Schema(type=openapi.TYPE_STRING, description="Name of the company"),
            'registration_number': openapi.Schema(type=openapi.TYPE_STRING, description="Registration number of the company (optional)", nullable=True),
            'primary_contact_name': openapi.Schema(type=openapi.TYPE_STRING, description="Primary contact name (optional)", nullable=True),
            'primary_contact_email': openapi.Schema(type=openapi.TYPE_STRING, description="Primary contact email (optional)", nullable=True),
            'primary_contact_phone': openapi.Schema(type=openapi.TYPE_STRING, description="Primary contact phone number (optional)", nullable=True),
            'address': openapi.Schema(type=openapi.TYPE_STRING, description="Company address (optional)", nullable=True),
            'postal_code': openapi.Schema(type=openapi.TYPE_STRING, description="Postal code (optional)", nullable=True),
            'notes': openapi.Schema(type=openapi.TYPE_STRING, description="Additional notes (optional)", nullable=True),
        }
    )
)


company_create_response_schema = openapi.Response(
    description='Created Company object',
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            **CompanySerializer().data
        }
    )
)
