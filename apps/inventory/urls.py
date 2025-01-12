from django.urls import path

from apps.inventory.views import (InventoryListAPIView, StockMovementListAPIView,
								  UpdateStockAPIView)

urlpatterns = [
	path('inventory-list/', InventoryListAPIView.as_view(), name='inventory_list'),
	path('stock-movement-list/', StockMovementListAPIView.as_view(), name='stock_movement_list'),
	path('stock-movement/<pk>/', UpdateStockAPIView.as_view(), name='stock_movement_update'),
]
