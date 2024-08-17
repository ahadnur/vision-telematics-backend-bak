from django.urls import path
from .views import (activate, CreateAccountAPIView, UpdateAccountAPIView, UserCreateAPIView, ResetUserPasswordAPIView,
                    GetUserAPIView, AccountListAPIView)

app_name = 'accounts'

urlpatterns = [
    path('activate/<uid64>/<token>/', activate, name='activate'),
]+[
    path('user/<_id>/', GetUserAPIView.as_view(), name='user'),
    path('user-create/', UserCreateAPIView.as_view(), name='user-create'),
    path('reset-password/<_id>/', ResetUserPasswordAPIView.as_view(), name='reset-password'),
]+[
    path('create-new-account/', CreateAccountAPIView.as_view(), name='create-account'),
    path('update-new-account/<int:_id>/', UpdateAccountAPIView.as_view(), name='update-account'),
    path('account-list/', AccountListAPIView.as_view(), name='account-list'),
]