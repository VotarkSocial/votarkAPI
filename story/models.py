from django.db import models

class Story(models.Model):
    content = models.ImageField(null=False, blank=False)
    user = models.ForeignKey(
        'votarkUser.VotarkUser',
        on_delete=models.SET_NULL,
        null=True,
        blank=False
    )