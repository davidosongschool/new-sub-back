from django.urls import path
from . import views

urlpatterns = [
    path('check_email_exists/', views.check_email_exists),
    path('check_email_verified/', views.check_email_verified),
]
