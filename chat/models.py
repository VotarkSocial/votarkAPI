from django.db import models
from django.utils.timezone import now

class Chat(models.Model):
    picture = models.ImageField(null=False, blank=False)
    name = models.CharField(max_length=200)
    date = models.DateField(default=now)
