from django.db import models
from django.utils.timezone import now

class Report(models.Model):
    content = models.ImageField(max_length=1000,null=False, blank=False)
    date = models.DateField(default=now)
    type = models.CharField(max_length=1000)
    user = models.ForeignKey(
        'votarkUser.VotarkUser',
        on_delete=models.SET_NULL,
        null=True,
        blank=False
    )