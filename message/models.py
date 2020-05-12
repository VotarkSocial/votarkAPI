from django.db import models

class Message(models.Model):
    content = models.CharField(max_length=1000,null=False, blank=False)
    date = models.DateField()
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