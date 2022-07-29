
from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class Create_User(AbstractUser):
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
    )
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=10, unique=True)
    street = models.TextField()
    zip_code = models.CharField(max_length=6)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
