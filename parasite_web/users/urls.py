from django.urls import path
from . import views

urlpatterns = [
    path('', views.loginUser, name="login"),
    path('register', views.registerUser, name="register"),
    path('forgot_password', views.forgotPassword, name="forgot_password"),
    path('reset_password', views.resetPassword, name="reset_password"),
    path('verifyLink/<uidb64>/<token>/<action>', views.verifyLink, name="verifyLink"),
    path('error', views.error, name="Error")
]