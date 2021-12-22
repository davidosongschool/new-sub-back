from django.db import models
from django.contrib.auth.models import User

# Model to store stripe keys
class StripeKeys(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    publish_key = models.CharField(max_length=256)
    secret_key = models.CharField(max_length=256)


    def __str__(self):
        return self.secret_key

