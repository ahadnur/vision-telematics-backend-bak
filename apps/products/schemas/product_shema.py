from rest_framework import status
from drf_yasg import openapi

product_response_schema = openapi.Schema(
	type=openapi.TYPE_OBJECT,
	properties={
		"id": openapi.Schema(type=openapi.TYPE_INTEGER, description="Unique identifier for the product"),
		"product_name": openapi.Schema(type=openapi.TYPE_STRING, description="Name of the product"),
		"description": openapi.Schema(type=openapi.TYPE_STRING, description="Description of the product"),
		"cost": openapi.Schema(type=openapi.TYPE_STRING, description="Cost of the product"),
		"note": openapi.Schema(type=openapi.TYPE_STRING, description="Additional notes about the product"),
		"category": openapi.Schema(type=openapi.TYPE_INTEGER, description="ID of the associated category"),
		"product_skus": openapi.Schema(
			type=openapi.TYPE_ARRAY,
			items=openapi.Schema(
				type=openapi.TYPE_OBJECT,
				properties={
					"id": openapi.Schema(type=openapi.TYPE_INTEGER, description="Unique identifier for the SKU"),
					"sku_code": openapi.Schema(type=openapi.TYPE_STRING, description="Stock Keeping Unit code"),
					"description": openapi.Schema(type=openapi.TYPE_STRING, description="Description of the SKU"),
					"unit_price": openapi.Schema(type=openapi.TYPE_STRING, description="Unit price of the SKU"),
					"qty": openapi.Schema(type=openapi.TYPE_INTEGER, description="Quantity available for the SKU"),
					"discount": openapi.Schema(type=openapi.TYPE_STRING, description="Discount applicable to the SKU"),
					"total": openapi.Schema(type=openapi.TYPE_STRING, description="Total price after discount"),
					"product": openapi.Schema(type=openapi.TYPE_INTEGER, description="ID of the associated product")
				}
			)
		)
	}
)

product_list_response_schema = {
	status.HTTP_200_OK: openapi.Response(
		description='List of products',
		schema=openapi.Schema(
			type=openapi.TYPE_ARRAY,
			items=product_response_schema  # Correctly reference the product_response_schema here
		)
	)
}


product_detail_response_schema = {
	status.HTTP_201_CREATED: openapi.Response(
		description='Product detail',
		schema=openapi.Schema(
			type=openapi.TYPE_OBJECT,  # This should be 'object' since it has properties
			properties={
				"id": openapi.Schema(type=openapi.TYPE_INTEGER, description="Unique identifier for the SKU"),
				"sku_code": openapi.Schema(type=openapi.TYPE_STRING, description="Stock Keeping Unit code"),
				"description": openapi.Schema(type=openapi.TYPE_STRING, description="Description of the SKU"),
				"unit_price": openapi.Schema(type=openapi.TYPE_STRING, description="Unit price of the SKU"),
				"qty": openapi.Schema(type=openapi.TYPE_INTEGER, description="Quantity available for the SKU"),
				"discount": openapi.Schema(type=openapi.TYPE_STRING, description="Discount applicable to the SKU"),
				"total": openapi.Schema(type=openapi.TYPE_STRING, description="Total price after discount"),
				"product": openapi.Schema(type=openapi.TYPE_INTEGER, description="ID of the associated product")
			}
		)
	)
}
