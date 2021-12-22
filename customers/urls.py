from django.urls import path
from .views import customer_list
from . import views

urlpatterns = [
    path('', views.customer_list,),
]
