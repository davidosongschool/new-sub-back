from django.db import models
from django.contrib.auth.models import User
from allauth.account.signals import user_signed_up
from django.dispatch import receiver

# Model to store stripe keys
class Accounts(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    account_type=models.IntegerField(default=1)


    def __str__(self):
        return self.account_type


@receiver(user_signed_up)
def set_user_type(request, user, **kwargs):
    """ Listens for user signed up signal from allauth and will then assign user roles etc"""
    print(user)

