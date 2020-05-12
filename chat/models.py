from django.db import models

class Chat(models.Model):
    picture = models.ImageField(null=False, blank=False)
    name = models.CharField(max_length=200)
