from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password

class VotarkUser(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=30, blank=True)
    picture = models.DateField(null=True, blank=True)   

    def perform_create(self, serializer):
        serializer.data['password'] = make_password(serializer.data['password'])
        user.save()
        return Response({})