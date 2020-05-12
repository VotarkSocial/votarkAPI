from django.db import models

class Versus(models.Model):
    date = models.DateField()
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