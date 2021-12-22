from django.urls import path
from .views import get_overview_data
from . import views

urlpatterns = [
    path('get_overview_data/', views.get_overview_data),
]
