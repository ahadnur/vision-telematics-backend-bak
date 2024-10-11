from django.urls import path

from apps.products.views.category_view import (CategoryCreateAPIView, CategoryUpdateAPIView, CategoryRetrieveAPIView,
											   CategoryDestroyAPIView, CategoryListAPIView)
from apps.products.views.product_view import ProductListAPIView, ProductDetailAPIVIew, ProductCreateAPIView

urlpatterns = [
	path('create/', ProductCreateAPIView.as_view(), name='create'),
	path('list/', ProductListAPIView.as_view(), name='product-list'),
	path('<pk>/', ProductDetailAPIVIew.as_view(), name='product-detail')
] + [
	path('category-list/', CategoryListAPIView.as_view(), name='category-list'),
	path('category/<pk>/', CategoryRetrieveAPIView.as_view(), name='category'),
	path('category-create/', CategoryCreateAPIView.as_view(), name='category-create'),
	path('category-update/<int:pk>/', CategoryUpdateAPIView.as_view(), name='category-update'),
	path('category-delete/<int:pk>/', CategoryDestroyAPIView.as_view(), name='category-update'),
]
