from django.urls import path
from apps.accounts.views import (activate, CreateAccountAPIView, UpdateAccountAPIView, UserCreateAPIView, ResetUserPasswordAPIView,
                                 GetUserAPIView, AccountListAPIView, LoginAPIView)

app_name = 'accounts'

urlpatterns = [
    path('activate/<uid64>/<token>/', activate, name='activate'),
]+[
    path('user/<_id>/', GetUserAPIView.as_view(), name='user'),
    path('user-create/', UserCreateAPIView.as_view(), name='user_create'),
    path('login/', LoginAPIView.as_view(), name='user_login'),
    path('reset-password/<_id>/', ResetUserPasswordAPIView.as_view(), name='reset-password'),
]+[
    path('create-new-account/', CreateAccountAPIView.as_view(), name='create-account'),
    path('update-new-account/<int:_id>/', UpdateAccountAPIView.as_view(), name='update-account'),
    path('account-list/', AccountListAPIView.as_view(), name='account-list'),
]