from django.db import models
from django.utils.timezone import now

class Versus(models.Model):
    unique_together = (('post1', 'post2'))
    date = models.DateField(default=now)
    post1 = models.ForeignKey(
        'post.Post',
        related_name='post1',
        on_delete=models.SET_NULL,
        null=True,
        blank=False
    )
    post2 = models.ForeignKey(
        'post.Post',
        related_name='post2',
        on_delete=models.SET_NULL,
        null=True,
        blank=False
    )