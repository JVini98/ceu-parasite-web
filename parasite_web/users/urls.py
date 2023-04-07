from django.urls import path
from . import views

urlpatterns = [
    path('', views.loginUser, name="login"),
    path('register', views.registerUser, name="register"),
    path('forgot_password', views.forgotPassword, name="change_password"),
    path('activate/<uidb64>/<token>', views.activate, name="activate")
]