from django.db import models
from django.utils.timezone import now

class Follow(models.Model):
    date = models.DateField(default=now)
    onVersus = models.ForeignKey(
        'versus.Versus',
        on_delete=models.SET_NULL,
        null=True,
        blank=False
    )
    user = models.ForeignKey(
        'votarkUser.VotarkUser',
        related_name='userfollows',
        on_delete=models.SET_NULL,
        null=True,
        blank=False
    )
    follower = models.ForeignKey(
        'votarkUser.VotarkUser',
        related_name='follower',
        on_delete=models.SET_NULL,
        null=True,
        blank=False
    )

