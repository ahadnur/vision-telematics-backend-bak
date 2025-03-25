from django.urls import path

from apps.products.views import (
	ProductCreateAPIView, 
	ProductListAPIView, 
	ProductDetailAPIVIew, 
	ProductUpdateAPIView,
	ProductDestroyAPIView,

	CategoryCreateAPIView, 
	CategoryListAPIView,
	CategoryRetrieveAPIView, 
	CategoryUpdateAPIView, 
	CategoryDestroyAPIView, 
	
	SupplierCreateAPIView, 
	SupplierListAPIView,
	SupplierDetailAPIView, 
	SupplierUpdateAPIView, 
	SupplierDeleteAPIView,

	GenerateProductSkuCodeAPIView,
	ProductSKUDestroyAPIView, 
	ProductSkusListByProductID,

	POListView,
	POCreateView,
	PORetrieveView,
	POUpdateView,
	PODeleteView,

	SubscriptionPlanListAPIView,
	SubscriptionPlanDetailsAPIView,
	SubscriptionPlanCreateAPIView,
	SubscriptionPlanUpdateAPIView,
	DeleteSubscriptionPlanAPIView,
)

urlpatterns = [
	#product
	path('create/', ProductCreateAPIView.as_view(), name='product_create'),
	path('list/', ProductListAPIView.as_view(), name='product_list'),
	path('details/<int:pk>/', ProductDetailAPIVIew.as_view(), name='product_detail'),
	path('update/<int:pk>/', ProductUpdateAPIView.as_view(), name='product_update'),
	path('delete/<int:pk>/', ProductDestroyAPIView.as_view(), name='product_delete'),
	path('sku-delete/<int:pk>/', ProductSKUDestroyAPIView.as_view(), name='product_sku_delete'),

	# Category
	path('category-create/', CategoryCreateAPIView.as_view(), name='category_create'),
	path('category-list/', CategoryListAPIView.as_view(), name='category_list'),
	path('category-details/<pk>/', CategoryRetrieveAPIView.as_view(), name='get_category'),
	path('category-update/<int:pk>/', CategoryUpdateAPIView.as_view(), name='category_update'),
	path('category-delete/<int:pk>/', CategoryDestroyAPIView.as_view(), name='category_delete'),
	path('generate-sku/', GenerateProductSkuCodeAPIView.as_view(), name='generate_sku'),

	# supplier
	path('supplier-create/', SupplierCreateAPIView.as_view(), name='supplier_create'),
	path('supplier-list/', SupplierListAPIView.as_view(), name='supplier_list'),
	path('supplier-detail/<int:pk>/', SupplierDetailAPIView.as_view(), name='supplier_detail'),
	path('supplier-update/<int:pk>/', SupplierUpdateAPIView.as_view(), name='supplier_update'),
	path('supplier-delete/<int:pk>/', SupplierDeleteAPIView.as_view(), name='supplier_delete'),
	path('product-skus/<product_id>/', ProductSkusListByProductID.as_view(), name='product_skus_by_product_id'),

	# purchase order (PO)
	path('po/list/', POListView.as_view(), name='po-list'),
	path('po/create/', POCreateView.as_view(), name='po-create'),
	path('po/details/<int:id>/', PORetrieveView.as_view(), name='po-retrieve'),
	path('po/<int:id>/update/', POUpdateView.as_view(), name='po-update'),
	path('po/<int:id>/delete/', PODeleteView.as_view(), name='po-delete'),

	# Subscription plan
	path('subscription-plan/list/', SubscriptionPlanListAPIView.as_view(), name='subscription-plan-list'),
	path('subscription-plan/details/<int:pk>/', SubscriptionPlanDetailsAPIView.as_view(), name='subscription-plan-details'),
	path('subscription-plan/create/', SubscriptionPlanCreateAPIView.as_view(), name='subscription-plan-create'),
	path('subscription-plan/update/<int:pk>/', SubscriptionPlanUpdateAPIView.as_view(), name='subscription-plan-update'),
	path('subscription-plan/delete/<int:pk>/', DeleteSubscriptionPlanAPIView.as_view(), name='subscription-plan-delete')
]
