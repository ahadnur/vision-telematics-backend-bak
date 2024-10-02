from django.urls import path

from apps.products.views.product_view import ProductListAPIView, ProductDetailAPIVIew

urlpatterns = [
	path('list/', ProductListAPIView.as_view(), name='product-list'),
	path('<pk>/', ProductDetailAPIVIew.as_view(), name='product-detail')
]
