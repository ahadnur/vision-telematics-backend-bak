from drf_yasg import openapi

inventory_list_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "count": openapi.Schema(type=openapi.TYPE_INTEGER),
        "next": openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
        "previous": openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
        "results": openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                    "product_sku": openapi.Schema(type=openapi.TYPE_INTEGER),
                    "product_name": openapi.Schema(type=openapi.TYPE_STRING),
                    "sku_code": openapi.Schema(type=openapi.TYPE_STRING),
                    "unit_price": openapi.Schema(type=openapi.TYPE_STRING, format="decimal"),
                    "stock_quantity": openapi.Schema(type=openapi.TYPE_INTEGER),
                    "is_low_stock": openapi.Schema(type=openapi.TYPE_BOOLEAN),
                },
            ),
        ),
    },
)

stock_movement_list_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "count": openapi.Schema(type=openapi.TYPE_INTEGER),
        "next": openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
        "previous": openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
        "results": openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                    "product_sku": openapi.Schema(type=openapi.TYPE_INTEGER),
                    "sku_code": openapi.Schema(type=openapi.TYPE_STRING),
                    "inventory": openapi.Schema(type=openapi.TYPE_INTEGER),
                    "operation_type": openapi.Schema(type=openapi.TYPE_STRING, enum=["add", "remove", "adjust"]),
                    "quantity": openapi.Schema(type=openapi.TYPE_INTEGER),
                    "previous_quantity": openapi.Schema(type=openapi.TYPE_INTEGER),
                    "new_quantity": openapi.Schema(type=openapi.TYPE_INTEGER),
                    "reason": openapi.Schema(type=openapi.TYPE_STRING),
                    "reference": openapi.Schema(type=openapi.TYPE_STRING),
                    "created_at": openapi.Schema(type=openapi.TYPE_STRING, format="date-time"),
                },
            ),
        ),
    },
)
