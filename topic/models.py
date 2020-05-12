from django.db import models

class Topic(models.Model):
    name = models.CharField(max_length=100,null=False, blank=False)
    privacity = models.BooleanField(default=False)
    creator = models.ForeignKey(
        'votarkUser.VotarkUser',
        on_delete=models.SET_NULL,
        null=True,
        blank=False
    )