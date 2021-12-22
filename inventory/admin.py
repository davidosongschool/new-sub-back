from django.contrib import admin
from .models import Inventory, Storefront

# Register your models here.
admin.site.register([Inventory, Storefront])
