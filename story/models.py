from django.db import models
from django.utils.timezone import now

class Story(models.Model):
    image = models.ImageField(null=True, blank=True)
    video = models.FileField(upload_to='videos/', null=True, verbose_name="")
    user = models.ForeignKey(
        'votarkUser.VotarkUser',
        on_delete=models.SET_NULL,
        null=True,
        blank=False
    )
    date = models.DateField(default=now)