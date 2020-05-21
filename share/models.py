from django.db import models
from django.utils.timezone import now

class Share(models.Model):
    date = models.DateTimeField(default=now)
    versus = models.ForeignKey(
        'versus.Versus',
        on_delete=models.SET_NULL,
        null=True,
        blank=False
    )
    post = models.ForeignKey(
        'votarkUser.VotarkUser',
        on_delete=models.SET_NULL,
        null=True,
        blank=False
    )