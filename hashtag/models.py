from django.db import models

class Hashtag(models.Model):
    content = models.CharField(max_length=100,null=False, blank=False)
    topic = models.ForeignKey(
        'topic.Topic',
        on_delete=models.SET_NULL,
        null=True,
        blank=False
    )
