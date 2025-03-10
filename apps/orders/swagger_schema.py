from drf_yasg import openapi
from apps.common.enums import (
    ReturnStatusType, 
    ShipmentMode, 
    OrderItemStatusChoice, 
    OperationChoice, 
    OrderStatusChoice
)

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



order_list_schema = openapi.Schema(
    type=openapi.TYPE_ARRAY,
    items=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "id": openapi.Schema(type=openapi.TYPE_INTEGER, description="Order ID"),
            "customer": openapi.Schema(type=openapi.TYPE_INTEGER, description="Customer ID", nullable=True),
            "purchasing_notes": openapi.Schema(type=openapi.TYPE_STRING, description="Purchasing notes", nullable=True),
            "engineer_notes": openapi.Schema(type=openapi.TYPE_STRING, description="Engineer notes", nullable=True),
            "created_at": openapi.Schema(type=openapi.TYPE_STRING, format="date-time", description="Order creation date"),
            "order_product_skus": openapi.Schema(
                type=openapi.TYPE_ARRAY,
                description="List of ordered products",
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "sku_code": openapi.Schema(type=openapi.TYPE_STRING, description="Product SKU code"),
                        "qty": openapi.Schema(type=openapi.TYPE_INTEGER, description="Quantity ordered"),
                        "price": openapi.Schema(type=openapi.TYPE_STRING, format="decimal", description="Product price"),
                    }
                )
            ),
            "order_options": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                description="Order options",
                properties={
                    "existing_kit": openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Is existing kit used"),
                    "service": openapi.Schema(type=openapi.TYPE_INTEGER, description="Service ID"),
                    "available_date": openapi.Schema(type=openapi.TYPE_STRING, format="date", description="Service available date", nullable=True),
                    "is_wrapped_job": openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Is wrapped job"),
                    "wrapper": openapi.Schema(type=openapi.TYPE_STRING, description="Wrapper", maxLength=255, nullable=True),
                }
            ),
            "customer_vehicle_info": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                description="Customer vehicle information",
                properties={
                    "vehicle_make": openapi.Schema(type=openapi.TYPE_INTEGER, description="Vehicle make"),
                    "vehicle_model": openapi.Schema(type=openapi.TYPE_INTEGER, description="Vehicle model"),
                    "vehicle_type": openapi.Schema(type=openapi.TYPE_INTEGER, description="Vehicle type"),
                    "registration_number": openapi.Schema(type=openapi.TYPE_STRING, description="Registration number", maxLength=20, minLength=1),
                }
            ),
            "payment_data": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                description="Payment details",
                properties={
                    "invoice_account_id": openapi.Schema(type=openapi.TYPE_INTEGER, description="Invoice account ID"),
                    "invoice_address": openapi.Schema(type=openapi.TYPE_STRING, description="Invoice address", minLength=1),
                    "requested_by": openapi.Schema(type=openapi.TYPE_STRING, description="Requested by", minLength=1),
                    "po_number": openapi.Schema(type=openapi.TYPE_STRING, description="Purchase Order number", minLength=1),
                }
            ),
            "shipping_charge": openapi.Schema(type=openapi.TYPE_STRING, format="decimal", description="Shipping charge", nullable=True),
            "shipping_address": openapi.Schema(type=openapi.TYPE_OBJECT, description="Shipping address", nullable=True),
            "billing_address": openapi.Schema(type=openapi.TYPE_OBJECT, description="Billing address", nullable=True),
            "order_ref_number": openapi.Schema(type=openapi.TYPE_STRING, description="Order reference number", maxLength=100, minLength=1),
        }
    )
)

order_return_schema = openapi.Schema(
    type=openapi.TYPE_ARRAY,
    items=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'id': openapi.Schema(type=openapi.TYPE_INTEGER),
            'order_refund': openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'order': openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                            'order_ref_number': openapi.Schema(type=openapi.TYPE_STRING),
                            'order_status': openapi.Schema(
                                type=openapi.TYPE_STRING,
                                enum=[choice[0] for choice in OrderStatusChoice.choices]
                            ),
                            'created_at': openapi.Schema(type=openapi.TYPE_STRING, format='date-time'),
                            'customer': openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                    'name': openapi.Schema(type=openapi.TYPE_STRING),
                                    'email': openapi.Schema(type=openapi.TYPE_STRING)
                                }
                            )
                        }
                    ),
                    'refund_reason': openapi.Schema(type=openapi.TYPE_STRING),
                    'refund_initiated': openapi.Schema(type=openapi.TYPE_STRING, format='date-time'),
                    'refund_completed': openapi.Schema(type=openapi.TYPE_STRING, format='date-time'),
                    'admin_approved': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                    'approved_at': openapi.Schema(type=openapi.TYPE_STRING, format='date-time')
                }
            ),
            'order_item': openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'product_sku': openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                            'sku_code': openapi.Schema(type=openapi.TYPE_STRING),
                            'unit_price': openapi.Schema(type=openapi.TYPE_NUMBER, format='float'),
                            'qty': openapi.Schema(type=openapi.TYPE_INTEGER)
                        }
                    ),
                    'quantity': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'price': openapi.Schema(type=openapi.TYPE_NUMBER, format='float'),
                    'discount': openapi.Schema(type=openapi.TYPE_NUMBER, format='float'),
                    'status': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        enum=[choice[0] for choice in OrderItemStatusChoice.choices]
                    )
                }
            ),
            'quantity': openapi.Schema(type=openapi.TYPE_INTEGER),
            'return_status': openapi.Schema(
                type=openapi.TYPE_STRING,
                enum=[choice.value for choice in ReturnStatusType]
            ),
            'refund_amount': openapi.Schema(type=openapi.TYPE_NUMBER, format='float'),
            'shipment_mode': openapi.Schema(
                type=openapi.TYPE_STRING,
                enum=[choice.value for choice in ShipmentMode]
            ),
            'pickup_address': openapi.Schema(
                type=openapi.TYPE_OBJECT,
                additional_properties=True,
                description='JSON address structure'
            ),
            'drop_off_address': openapi.Schema(
                type=openapi.TYPE_OBJECT,
                additional_properties=True,
                description='JSON address structure'
            ),
            'reason': openapi.Schema(type=openapi.TYPE_STRING),
            'cancellation_charges': openapi.Schema(type=openapi.TYPE_NUMBER, format='float'),
            'return_rejected_reason': openapi.Schema(type=openapi.TYPE_STRING),
            'return_rejected_by': openapi.Schema(type=openapi.TYPE_STRING),
            'notes': openapi.Schema(type=openapi.TYPE_STRING),
            'is_restocked': openapi.Schema(type=openapi.TYPE_BOOLEAN),
            'restocked_at': openapi.Schema(type=openapi.TYPE_STRING, format='date-time'),
            'created_at': openapi.Schema(type=openapi.TYPE_STRING, format='date-time'),
            'updated_at': openapi.Schema(type=openapi.TYPE_STRING, format='date-time'),
            'is_active': openapi.Schema(type=openapi.TYPE_BOOLEAN),
            'is_deleted': openapi.Schema(type=openapi.TYPE_BOOLEAN)
        }
    )
)