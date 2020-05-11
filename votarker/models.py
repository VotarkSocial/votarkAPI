from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Votarker(models.Model):
    username = models.TextField(max_length=50, blank=False,null=False)
    email = models.EmailField(max_length=50, blank=False,null=False)
    password = models.TextField(max_length=100, blank=False,null=False)
    first_name = models.TextField(max_length=100, blank=True)
    last_name = models.TextField(max_length=100, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=30, blank=True)
    picture = models.DateField(null=True, blank=True)