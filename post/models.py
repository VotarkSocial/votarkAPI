from django.db import models
from django.utils.timezone import now

class Post(models.Model):
    image = models.ImageField(null=True, blank=True)
    video = models.FileField(upload_to='videos/', null=True, verbose_name="")
    description = models.CharField(max_length=500)
    victories = models.IntegerField()
    date = models.DateField(default=now)
    order = models.IntegerField()
    topic = models.ForeignKey(
        'topic.Topic',
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