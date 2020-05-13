from django.db import models
from django.utils.timezone import now

class Like(models.Model):
    reaction = models.IntegerField()
    date = models.DateField(default=now)
    versus = models.ForeignKey(
        'versus.Versus',
        on_delete=models.SET_NULL,
        null=True,
        blank=False
    )
    user = models.ForeignKey(
        'votarkUser.VotarkUser',
        on_delete=models.SET_NULL,
        null=True,
        blank=False
    )
