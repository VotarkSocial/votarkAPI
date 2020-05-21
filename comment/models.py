from django.db import models
from django.utils.timezone import now

class Comment(models.Model):
    content = models.CharField(max_length=1000)
    date = models.DateTimeField(default=now)
    user = models.ForeignKey(
        'votarkUser.VotarkUser',
        on_delete=models.SET_NULL,
        null=True,
        blank=False
    )
    post = models.ForeignKey(
        'post.Post',
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