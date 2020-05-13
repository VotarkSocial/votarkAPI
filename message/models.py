from django.db import models
from django.utils.timezone import now

class Message(models.Model):
    content = models.CharField(max_length=1000,null=False, blank=False)
    date = models.DateField(default=now)
    chat = models.ForeignKey(
        'chat.Chat',
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