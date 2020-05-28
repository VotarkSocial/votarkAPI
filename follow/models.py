from django.db import models
from django.utils.timezone import now

class Follow(models.Model):
    unique_together = (('user', 'follower'))
    date = models.DateTimeField(default=now)
    onVersus = models.ForeignKey(
        'versus.Versus',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    user = models.ForeignKey(
        'votarkUser.VotarkUser',
        related_name='userfollows',
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )
    follower = models.ForeignKey(
        'votarkUser.VotarkUser',
        related_name='follower',
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )

