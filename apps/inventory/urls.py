from django.urls import path

from apps.inventory.views import (InventoryListAPIView, StockMovementListAPIView,
								  UpdateStockAPIView, InventoryCreateAPIView, InventoryUpdateAPIView, InventoryDestroyAPIView)

urlpatterns = [
	path('inventory-list/', InventoryListAPIView.as_view(), name='inventory_list'),
	path('inventory-create/', InventoryCreateAPIView.as_view(), name='inventory_create'),
	path('inventory-update/', InventoryUpdateAPIView.as_view(), name='inventory_update'),
	path('inventory-delete/', InventoryDestroyAPIView.as_view(), name='inventory_delete'),

	path('stock-movement-list/', StockMovementListAPIView.as_view(), name='stock_movement_list'),
	path('stock-movement/<pk>/', UpdateStockAPIView.as_view(), name='stock_movement_update'),
]
