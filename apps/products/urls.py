from django.urls import path

from apps.products.views.category_view import *
from apps.products.views.product_view import ProductListAPIView, ProductDetailAPIVIew, ProductCreateAPIView, \
	ProductUpdateAPIView, ProductDestroyAPIView

urlpatterns = [
	path('create/', ProductCreateAPIView.as_view(), name='product_create'),
	path('list/', ProductListAPIView.as_view(), name='product_list'),
	path('details/<int:pk>/', ProductDetailAPIVIew.as_view(), name='product_detail'),
	path('update/<int:pk>/', ProductUpdateAPIView.as_view(), name='product_update'),
	path('delete/<int:pk>/', ProductDestroyAPIView.as_view(), name='product_delete'),


	path('category-create/', CategoryCreateAPIView.as_view(), name='category_create'),
	path('category-list/', CategoryListAPIView.as_view(), name='category_list'),
	path('category-details/<pk>/', CategoryRetrieveAPIView.as_view(), name='get_category'),
	path('category-update/<int:pk>/', CategoryUpdateAPIView.as_view(), name='category_update'),
	path('category-delete/<int:pk>/', CategoryDestroyAPIView.as_view(), name='category_delete'),
]
