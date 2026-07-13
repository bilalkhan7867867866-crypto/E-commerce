from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phone = models.CharField(max_length=12,blank=True,)
    address = models.TextField(blank=True,)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username