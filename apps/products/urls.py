from django.urls import path

from apps.products.views.category_view import *
from apps.products.views.product_view import ProductListAPIView, ProductDetailAPIVIew, ProductCreateAPIView, \
	ProductUpdateAPIView

urlpatterns = [
	path('create/', ProductCreateAPIView.as_view(), name='product_create'),
	path('list/', ProductListAPIView.as_view(), name='product_list'),
	path('detail/<int:pk>/', ProductDetailAPIVIew.as_view(), name='product_detail'),
	path('update/<int:pk>/', ProductUpdateAPIView.as_view(), name='product_update'),


	path('category-create/', CategoryCreateAPIView.as_view(), name='category_create'),
	path('categorylist/', CategoryListAPIView.as_view(), name='category_list'),
	path('category/<pk>/', CategoryRetrieveAPIView.as_view(), name='get_category'),
	path('category-update/<int:pk>/', CategoryUpdateAPIView.as_view(), name='category_update'),
	path('category-delete/<int:pk>/', CategoryDestroyAPIView.as_view(), name='category_delete'),
]
