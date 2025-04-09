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

    # subscription plan
    SubscriptionPlanListAPIView,
    SubscriptionPlanRetrieveAPIView,
    SubscriptionPlanCreateAPIView,
    SubscriptionPlanUpdateAPIView,
    SubscriptionPlanDestroyAPIView,

    # subscribe
    SubscriptionListAPIView,
    SubscriptionRetrieveAPIView,
    SubscriptionCreateAPIView,
    SubscriptionUpdateAPIView,
    
    # transsactions
    TransactionHistoryAPIView,

    # usage
    UsageMetricsAPIView,
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

	# subscription plans
    path("subscription/plans/", SubscriptionPlanListAPIView.as_view(), name="subscription-plan-list"),
    path("subscription/plans/create/", SubscriptionPlanCreateAPIView.as_view(), name="subscription-plan-create"),
    path("subscription/plans/<int:pk>/", SubscriptionPlanRetrieveAPIView.as_view(), name="subscription-plan-detail"),
    path("subscription/plans/<int:pk>/update/", SubscriptionPlanUpdateAPIView.as_view(), name="subscription-plan-update"),
    path("subscription/plans/<int:pk>/delete/", SubscriptionPlanDestroyAPIView.as_view(), name="subscription-plan-delete"),

    # Subscriptions 
    path("subscriptions/", SubscriptionListAPIView.as_view(), name="subscription-list"),
    path("subscriptions/create/", SubscriptionCreateAPIView.as_view(), name="subscription-create"),
    path("subscriptions/<int:pk>/", SubscriptionRetrieveAPIView.as_view(), name="subscription-detail"),
    path("subscriptions/<int:pk>/update/", SubscriptionUpdateAPIView.as_view(), name="subscription-update"),

    # Transactions
    path("subscriptions/transactions/", TransactionHistoryAPIView.as_view(), name="transaction-history"),

    # Usage Metrics
    path("subscriptions/usage-metrics/<str:subscriber_type>/<int:subscriber_id>/", UsageMetricsAPIView.as_view(), name="usage-metrics"),
]
