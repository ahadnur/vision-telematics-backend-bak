from django.urls import path

from apps.products.views import (ProductCreateAPIView, ProductListAPIView, ProductDetailAPIVIew, ProductUpdateAPIView,
								 CategoryRetrieveAPIView, CategoryUpdateAPIView, GenerateProductSkuCodeAPIView,
								 ProductDestroyAPIView,CategoryCreateAPIView, CategoryListAPIView,
								 CategoryDestroyAPIView, SupplierCreateAPIView, SupplierListAPIView,
								 SupplierDetailAPIView, SupplierUpdateAPIView, SupplierDeleteAPIView,
								 ProductSKUDestroyAPIView)

urlpatterns = [
	path('create/', ProductCreateAPIView.as_view(), name='product_create'),
	path('list/', ProductListAPIView.as_view(), name='product_list'),
	path('details/<int:pk>/', ProductDetailAPIVIew.as_view(), name='product_detail'),
	path('update/<int:pk>/', ProductUpdateAPIView.as_view(), name='product_update'),
	path('delete/<int:pk>/', ProductDestroyAPIView.as_view(), name='product_delete'),
	path('sku-delete/<int:pk>/', ProductSKUDestroyAPIView.as_view(), name='product_sku_delete'),

	path('category-create/', CategoryCreateAPIView.as_view(), name='category_create'),
	path('category-list/', CategoryListAPIView.as_view(), name='category_list'),
	path('category-details/<pk>/', CategoryRetrieveAPIView.as_view(), name='get_category'),
	path('category-update/<int:pk>/', CategoryUpdateAPIView.as_view(), name='category_update'),
	path('category-delete/<int:pk>/', CategoryDestroyAPIView.as_view(), name='category_delete'),
	path('generate-sku/', GenerateProductSkuCodeAPIView.as_view(), name='generate_sku'),

	path('supplier-create/', SupplierCreateAPIView.as_view(), name='supplier_create'),
	path('supplier-list/', SupplierListAPIView.as_view(), name='supplier_list'),
	path('supplier-detail/<int:pk>/', SupplierDetailAPIView.as_view(), name='supplier_detail'),
	path('supplier-update/<int:pk>/', SupplierUpdateAPIView.as_view(), name='supplier_update'),
	path('supplier-delete/<int:pk>/', SupplierDeleteAPIView.as_view(), name='supplier_delete'),

	# path('po/', POListView.as_view(), name='po-list'),
	# path('po/create/', POCreateView.as_view(), name='po-create'),
	# path('po/<int:id>/', PORetrieveView.as_view(), name='po-retrieve'),
	# path('po/<int:id>/update/', POUpdateView.as_view(), name='po-update'),
	# path('po/<int:id>/delete/', PODeleteView.as_view(), name='po-delete'),
]
