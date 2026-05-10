from django.db import models
from django.contrib.auth.models import AbstractUser

class Users(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    bio = models.TextField(max_length=500, blank=True)
    
    def __str__(self):
        return self.username


