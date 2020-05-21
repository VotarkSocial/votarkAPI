from django.db import models
from django.utils.timezone import now

class Story(models.Model):
    content = models.FileField(upload_to='videos/', null=True, verbose_name="")
    user = models.ForeignKey(
        'votarkUser.VotarkUser',
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )
    date = models.DateTimeField(default=now)