from django.urls import path
from .views import *

urlpatterns = [
	path('create/', ServiceCreateView.as_view(), name='create'),
	path('list/', ServiceListView.as_view(), name='list'),
	path('details/<int:pk>/', ServiceRetrieveView.as_view(), name='details'),
	path('update/<int:pk>/', ServiceUpdateView.as_view(), name='update'),
	path('delete/<int:pk>/', ServiceDeleteView.as_view(), name='delete'),
]
