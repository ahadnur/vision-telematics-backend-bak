from django.urls import path
from apps.accounts.views import (activate, CreateAccountAPIView, UpdateAccountAPIView, UserCreateAPIView,
                                 ResetUserPasswordAPIView, GetUserAPIView, AccountListAPIView, LoginAPIView,
                                 UserListAPIView, UserUpdateAPIView)

app_name = 'accounts'

urlpatterns = [
    path('activate/<uid64>/<token>/', activate, name='activate'),
]+[
    path('user_list/', UserListAPIView.as_view(), name='user_list'),
    path('user/<_id>/', GetUserAPIView.as_view(), name='user'),
    path('user-create/', UserCreateAPIView.as_view(), name='user_create'),
    path('user-update/<pk>/', UserUpdateAPIView.as_view(), name='user_update'),
    path('login/', LoginAPIView.as_view(), name='user_login'),
    # path('user/reset-password/<_id>/', ResetUserPasswordAPIView.as_view(), name='reset-password'),
]+[
    path('create-new-account/', CreateAccountAPIView.as_view(), name='create-account'),
    path('update-new-account/<int:_id>/', UpdateAccountAPIView.as_view(), name='update-account'),
    path('account-list/', AccountListAPIView.as_view(), name='account-list'),
]