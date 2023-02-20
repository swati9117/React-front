from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
from pyexpat import model
from turtle import mode, update
from django.db import models
#from django.contrib.auth.models import BaseUserManager,AbstractBaseUser
# Create your models here.

#https://docs.djangoproject.com/en/4.1/topics/auth/customizing/#a-full-example

class User(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    specialization = models.CharField(max_length=200,null= True)
    password = models.CharField(max_length=255)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
