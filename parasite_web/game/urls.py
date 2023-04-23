from django.urls import path
from . import views

urlpatterns = [
    path('', views.manipulateImage, name="game"),
    path('reported', views.reportedPhotograph,  name='reported'),
]