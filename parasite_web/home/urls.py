from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('logout', views.logout, name="logout"),
    path('account_settings', views.account_settings, name="account_settings"),
    path('update_user_name', views.update_user_name, name="update_user_name"),
    path('update_password', views.update_password, name="update_password"),
    path('delete_user', views.delete_user, name="delete_user")
]