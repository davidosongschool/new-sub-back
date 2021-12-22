from django.urls import path
from . import views

urlpatterns = [
    path('test', views.test_payment),
    path('create_customer', views.create_customer),
]
