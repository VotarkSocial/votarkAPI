from django.db import models
from django.utils.timezone import now

class SearchedUser(models.Model):
    user = models.ForeignKey(
        'votarkUser.VotarkUser',
        related_name='userSearches',
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )
    searchedUser = models.ForeignKey(
        'votarkUser.VotarkUser',
        related_name='searched',
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    date = models.DateTimeField(default=now)