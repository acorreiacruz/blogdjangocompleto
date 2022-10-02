from email.policy import default
from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    bio = models.TextField(default='', blank=True)
    author = models.OneToOneField(User, on_delete=models.CASCADE)
