from django.db import models
from django.utils.timezone import now

class Vote(models.Model):
    user = models.ForeignKey(
        'votarkUser.VotarkUser',
        on_delete=models.SET_NULL,
        null=True,
        blank=False
    )
    versus = models.ForeignKey(
        'versus.Versus',
        on_delete=models.SET_NULL,
        null=True,
        blank=False
    )
    date = models.DateField(default=now)
    winner = models.BooleanField(null=False,blank=False)    #True for Post1 - False for Post2s