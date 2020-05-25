from django.db import models
from django.utils.timezone import now

class SearchedHashtag(models.Model):
    user = models.ForeignKey(
        'votarkUser.VotarkUser',
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )
    hashtag = models.ForeignKey(
        'hashtag.Hashtag',
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    date = models.DateTimeField(default=now)