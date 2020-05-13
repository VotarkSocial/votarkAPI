from django.db import models
from django.utils.timezone import now

class Post(models.Model):
    content = models.ImageField(null=False, blank=False)
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