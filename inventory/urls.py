from django.urls import path
from .views import product_list, set_price, store_front, storefront_product_list, storefront_single_product
from . import views

urlpatterns = [
    path('', views.product_list,),
    path('create_product/', views.create_product),
    path('set_price/', views.set_price),
    path('store_front/', views.store_front),
    path('storefront_product_list/', views.storefront_product_list),
    path('storefront_single_product/', views.storefront_single_product)

]
