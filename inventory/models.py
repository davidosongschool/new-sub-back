from django.db import models
from django.contrib.auth.models import User

class Inventory(models.Model):
    product_name = models.CharField(max_length=200)
    product_description = models.TextField(default="")
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    product_stripe_id = models.CharField(max_length=200, default="")
    image = models.ImageField(null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)    


    def __str__(self):
        return self.product_name

class Storefront(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    store_name = models.CharField(max_length=200)

    def __str__(self):
        return self.store_name
