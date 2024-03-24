from django.db import models
from django.contrib.auth.models import AbstractBaseUser , PermissionsMixin
from django.utils import timezone
from .manager import CustomUserManager

# Create your models here.

class CustomUser(AbstractBaseUser , PermissionsMixin):
    username = models.CharField(unique = True , max_length = 255)
    email = models.EmailField(unique = True)
    is_active = models.BooleanField(default = True)
    is_admin = models.BooleanField(default = False)
    date_added = models.DateTimeField(default=timezone.now)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    
    objects = CustomUserManager()
    
    def __str__(self):
        return self.email