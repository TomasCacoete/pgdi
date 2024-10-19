from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    phone_no=models.CharField(max_length=15)
    
    USER_TYPES = [
        ('contestant', 'Contestant'),
        ('creator', 'Creator'),
        ]
    
    user_type = models.CharField(max_length=10, choices=USER_TYPES,blank=False)

    
    
    def __str__(self):
        return self.username

class Contestant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def customMethod(self):
        return f'sou um competidor'

class Creator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def customMethod(self):
        return f'sou um criador de competicoes'