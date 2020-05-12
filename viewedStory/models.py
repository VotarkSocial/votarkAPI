from django.db import models

class ViewedStory(models.Model):
    user = models.ForeignKey(
        'votarkUser.VotarkUser',
        on_delete=models.SET_NULL,
        null=True,
        blank=False
    )
    story = models.ForeignKey(
        'story.Story',
        on_delete=models.SET_NULL,
        null=True,
        blank=False
    )