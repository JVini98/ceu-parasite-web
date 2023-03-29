from django.urls import path
from . import views

urlpatterns = [
    path('', views.registerUser, name="users"),
    path('login', views.loginUser, name="login")
]