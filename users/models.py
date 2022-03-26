from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    code = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True, blank=False)
