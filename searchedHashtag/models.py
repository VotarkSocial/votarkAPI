from django.db import models
from django.utils.timezone import now

class SearchedHashtag(models.Model):
    user = models.ForeignKey(
        'votarkUser.VotarkUser',
        on_delete=models.SET_NULL,
        null=True,
        blank=False
    )
    hashtag = models.ForeignKey(
        'post.Post',
        on_delete=models.SET_NULL,
        null=True,
        blank=False
    )
    date = models.DateTimeField(default=now)